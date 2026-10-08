#!/usr/bin/env python3
"""Trainer subprocess manager (never runs on the Tk main thread)."""
from __future__ import annotations

import os
import subprocess
import threading
import time
from pathlib import Path

from .backend import ERROR_HINTS, ROOT, RunStatus, output_dir_for

B_TMP_LOGDIR = ROOT / "build" / "e0017"


class TrainerProc:
    def __init__(self, on_line, on_exit):
        self._on_line = on_line
        self._on_exit = on_exit
        self.proc: subprocess.Popen | None = None
        self.status = RunStatus()
        self._lines: list[str] = []
        self._lock = threading.Lock()
        self._stop_requested = False
        self._log_fh = None
        self.log_path: Path | None = None

    def log_snapshot(self, n: int = 2000) -> list[str]:
        with self._lock:
            return list(self._lines[-n:])

    def _emit(self, line: str) -> None:
        with self._lock:
            self._lines.append(line)
            if len(self._lines) > 5000:
                del self._lines[:len(self._lines) - 5000]
        from .backend import parse_line
        parse_line(self.status, line)
        try:
            self._on_line(line)
        except Exception:
            pass
        if self._log_fh is not None:
            try:
                self._log_fh.write(line + "\n")
                self._log_fh.flush()
            except Exception:
                pass

    def is_alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def start(self, cmd: list[str], resuming: bool = False) -> None:
        if self.is_alive():
            raise RuntimeError("training already running")
        cfg = None
        if "--config" in cmd:
            cfg = Path(cmd[cmd.index("--config") + 1])
        logdir = output_dir_for(cfg) if cfg else B_TMP_LOGDIR
        try:
            logdir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        stamp = time.strftime("%Y%m%d-%H%M%S")
        self.log_path = logdir / f"gui-run-{stamp}.log"
        try:
            self._log_fh = self.log_path.open("w", encoding="utf-8")
            self._log_fh.write("$ " + " ".join(cmd) + "\n")
        except Exception:
            self._log_fh = None
        self._stop_requested = False
        self.status = RunStatus(
            state="RESUMING" if resuming else "STARTING",
            command=list(cmd), started_at=time.time())
        flags = 0
        if os.name == "nt":
            flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        root = Path(__file__).resolve().parent.parent.parent
        self.proc = subprocess.Popen(
            cmd, cwd=str(root), stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, bufsize=1,
            encoding="utf-8", errors="replace", creationflags=flags)
        self.status.pid = self.proc.pid
        self.status.state = "RESUMING" if resuming else "RUNNING"
        th = threading.Thread(target=self._pump, daemon=True)
        th.start()

    def _pump(self) -> None:
        assert self.proc is not None and self.proc.stdout is not None
        try:
            for line in self.proc.stdout:
                self._emit(line.rstrip("\n"))
        except Exception as exc:
            self._emit(f"[gui-reader-error] {exc}")
        finally:
            try:
                self.proc.stdout.close()
            except Exception:
                pass
        try:
            rc = self.proc.wait(timeout=30)
        except Exception:
            rc = self.proc.poll()
        self._finish(rc)

    def _finish(self, rc) -> None:
        try:
            if self._log_fh is not None:
                self._log_fh.close()
        except Exception:
            pass
        self._log_fh = None
        self.status.exit_code = rc
        self.status.ended_at = time.time()
        tail = " ".join(self.log_snapshot(40))
        bad = any(h in tail for h in ERROR_HINTS)
        if self._stop_requested:
            if rc == 0:
                self.status.state = "COMPLETED"
            else:
                self.status.state = "STOPPED"
                self.status.error_text = (
                    f"stopped by user (exit {rc}); "
                    "phase checkpoints are atomic so the last "
                    "complete checkpoint stays resumable")
        elif rc == 0 and not bad:
            self.status.state = "COMPLETED"
        else:
            self.status.state = "FAILED"
            last = self.log_snapshot(8)
            self.status.error_text = (
                f"exit code {rc}\n" + "\n".join(last[-8:]))
        try:
            self._on_exit(self.status)
        except Exception:
            pass

    def stop(self, timeout: float = 10.0) -> str:
        """Terminate first; kill only after grace period.

        Checkpoint files are atomic (temp + rename), so termination
        cannot tear one; the in-flight phase is simply re-run on resume.
        """
        p = self.proc
        if p is None or p.poll() is not None:
            return "not running"
        self._stop_requested = True
        self.status.state = "STOPPING"
        try:
            p.terminate()
        except Exception as exc:
            return f"terminate failed: {exc}"
        try:
            p.wait(timeout=timeout)
            return "terminated gracefully"
        except subprocess.TimeoutExpired:
            try:
                p.kill()
            except Exception as exc:
                return f"kill failed: {exc}"
            return "killed after grace period (emergency)"
