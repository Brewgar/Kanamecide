#!/usr/bin/env python3
"""Main window part 2: training actions + state machine."""
from __future__ import annotations

import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from . import backend as B
from . import ckpts as C
from . import engines as E
from .app import open_path, read_config_summary


class ActionsMixin:
    proc = None  # set by MainWindow
    config_path: Path
    _quick_procs: set = set()

    # -- config ------------------------------------------------------
    def _browse_config(self):
        from tkinter import filedialog
        p = filedialog.askopenfilename(
            title="Select training config",
            filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if p:
            self.config_path = Path(p)
            self.cfg_var.set(p)
            self._refresh_all()

    def _save_local(self):
        self.settings["config"] = str(self.config_path)
        self.settings["kana_engine"] = self.kana_engine.get()
        self.settings["cutechess"] = self.cutechess.get()
        self.settings["stockfish"] = self.stockfish.get()
        B.save_settings(self.settings)

    # -- log callbacks (called from reader thread) --------------------
    def _on_line(self, line: str):
        self.after(0, lambda: self._append_log(line))

    def _on_exit(self, status):
        self.after(0, self._refresh_all)

    def _append_log(self, line: str):
        try:
            self.log.configure(state="normal")
            self.log.insert("end", line + "\n")
            lines = int(self.log.index("end-1c").split(".")[0])
            if lines > 5000:
                self.log.delete("1.0", f"{lines - 5000}.0")
            self.log.see("end")
            self.log.configure(state="disabled")
        except Exception:
            pass
        try:
            self._refresh_live()
            self._apply_buttons()
        except Exception:
            pass

    # -- training ------------------------------------------------------
    def _start(self):
        if self.proc.is_alive():
            messagebox.showinfo("Training", "a run is already active")
            return
        if not B.TRAINER.is_file():
            messagebox.showerror(
                "Training",
                f"canonical trainer missing:\n{B.TRAINER}")
            return
        if not Path(self.config_path).is_file():
            messagebox.showerror("Training", "config file not found")
            return
        # Preflight gate runs in a worker thread so the GUI never freezes;
        # train starts only after PREFLIGHT PASS.
        self._append_log("$ " + " ".join(
            B.trainer_command("preflight", self.config_path)))
        self._append_log("[preflight running... Start gated on PASS]")

        def gate():
            ok = self._run_preflight_capture()
            if not ok:
                self.after(0, lambda: messagebox.showerror(
                    "Preflight FAILED",
                    "exit != 0; Start blocked.\n"
                    "See log view for the canonical trainer output."))
                self.after(0, self._refresh_all)
                return

            def launch():
                cmd = B.trainer_command("train", self.config_path)
                try:
                    self.proc.start(cmd)
                except Exception as exc:
                    messagebox.showerror("Start", str(exc))
                    return
                self._append_log("$ " + " ".join(cmd))
                self._save_local()
                self._refresh_all()
            self.after(0, launch)

        threading.Thread(target=gate, daemon=True).start()

    def _run_preflight_capture(self) -> bool:
        """Run canonical preflight, stream to log view. Returns pass/fail."""
        cmd = B.trainer_command("preflight", self.config_path)
        try:
            r = subprocess.run(cmd, cwd=str(B.ROOT), capture_output=True,
                               text=True, timeout=600, encoding="utf-8",
                               errors="replace")
        except Exception as exc:
            self._on_line(f"[preflight could not run: {exc}]")
            return False
        out = (r.stdout or "") + "\n" + (r.stderr or "")
        for line in out.splitlines()[-60:]:
            self._on_line(line)
        self.after(0, self._refresh_all)
        return r.returncode == 0

    def _stop(self):
        msg = self.proc.stop(timeout=10.0)
        self._append_log(f"[stop] {msg}")
        self._refresh_all()

    def _resume(self):
        if self.proc.is_alive():
            messagebox.showinfo("Resume", "a run is already active")
            return
        ck = C.latest_checkpoint(self.config_path)
        if ck is None:
            messagebox.showerror(
                "Resume", "no valid checkpoint for this config; "
                "Start a fresh run first")
            return
        cmd = B.trainer_command("resume", self.config_path,
                                checkpoint=ck["path"])
        try:
            self.proc.start(cmd, resuming=True)
        except Exception as exc:
            messagebox.showerror("Resume", str(exc))
            return
        self._append_log(f"[resume from {ck['phase']}] " + " ".join(cmd))
        self._save_local()
        self._refresh_all()

    def _quick(self, sub: str):
        if self.proc.is_alive():
            messagebox.showinfo(sub, "a run is already active")
            return
        if sub in ("preflight", "dry-run", "train", "resume", "manifest") \
                and not B.TRAINER.is_file():
            messagebox.showerror(
                sub, f"canonical trainer missing:\n{B.TRAINER}")
            return
        cmd = B.trainer_command(sub, self.config_path)
        self._append_log("$ " + " ".join(cmd))

        def run():
            try:
                r = subprocess.run(cmd, cwd=str(B.ROOT),
                                   capture_output=True, text=True,
                                   timeout=900, encoding="utf-8",
                                   errors="replace")
                out = (r.stdout or "") + "\n" + (r.stderr or "")
                for line in out.splitlines():
                    self._on_line(line)
                self._on_line(f"[{sub} exit {r.returncode}]")
            except Exception as exc:
                self._on_line(f"[{sub} failed: {exc}]")
            self.after(0, self._refresh_all)

        threading.Thread(target=run, daemon=True).start()
