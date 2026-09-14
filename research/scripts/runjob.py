#!/usr/bin/env python3
"""runjob.py — detached, resumable, heartbeat-monitored job launcher (stdlib only).

WHY THIS EXISTS (DEC-0009 / R-0003 F1,F2,F3):
  * this environment kills foreground sleeps at ~30 s and "detached" processes did not
    survive agent shell turnover, so a multi-hour campaign must be launched truly detached
    and must prove it is alive from disk;
  * two sessions reported work as "still running" while ZERO processes existed and no
    result files were being written. A heartbeat file with a timestamp is the cheapest
    evidence that separates "running" from "narrated as running";
  * a freshly built unsigned exe is intermittently BLOCKED by Device Guard / Smart App
    Control; a launch needs a retry loop.

CONTRACT (SYSTEM.md §6): the JOB itself must (a) append incremental evidence to disk with
per-item flush, (b) be resumable by skipping items already present in its checkpoint, and
(c) take no interactive input. runjob.py adds the heartbeat, the retry and the liveness
report. It never waits in the foreground.

USAGE
  python research/scripts/runjob.py launch --id RUN-0001 --name "e0011 campaign" --log
      m0_audit/e0011/run.log --heartbeat m0_audit/e0011/heartbeat.txt --checkpoint
      m0_audit/e0011/games.jsonl [--retry 5] [--probe 4] -- <cmd> [args...]

  python research/scripts/runjob.py status --heartbeat <path> [--log ...] [--checkpoint ...]
  python research/scripts/runjob.py resume <same args as launch>
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CREATE_NEW_PROCESS_GROUP = 0x00000200
DETACHED_PROCESS = 0x00000008
DETACHED = (CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS) if os.name == "nt" else 0


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def alive(pid: int) -> bool:
    """True if the PID names a live process. NEVER use os.kill(pid, 0) on Windows:
    CPython TERMINATES the target for any non CTRL_* signal."""
    if pid <= 0:
        return False
    if os.name != "nt":
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    import ctypes
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    k32 = ctypes.windll.kernel32
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return False
    k32.CloseHandle(h)
    return True


def counts(checkpoint) -> tuple:
    if not checkpoint or not Path(checkpoint).exists():
        return (0, 0)
    try:
        data = Path(checkpoint).read_bytes()
    except OSError:
        return (0, 0)
    return (len(data.splitlines()), len(data))


def heartbeat_line(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"{now()} {text}\n")
        fh.flush()
        os.fsync(fh.fileno())


def supervise(pid: int, heartbeat: Path, log: Path, checkpoint, interval: int) -> int:
    """Runs DETACHED. Writes a heartbeat while the job lives, then the exit record."""
    lines, size = counts(checkpoint)
    while True:
        lines, size = counts(checkpoint)
        log_bytes = log.stat().st_size if log.exists() else 0
        heartbeat_line(heartbeat, f"ALIVE pid={pid} log_bytes={log_bytes} "
                                  f"checkpoint_lines={lines}")
        if not alive(pid):
            time.sleep(interval)
            if not alive(pid):
                heartbeat_line(heartbeat, f"EXIT pid={pid} checkpoint_lines={lines} "
                                          f"checkpoint_bytes={size} (process gone)")
                return 0
        time.sleep(interval)


def spawn(cmd: list, cwd: Path, log: Path) -> subprocess.Popen:
    log.parent.mkdir(parents=True, exist_ok=True)
    out = open(log, "ab")
    return subprocess.Popen(cmd, cwd=str(cwd), stdout=out, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL, close_fds=True, creationflags=DETACHED)
def _resolve(p, cwd: Path):
    if p is None:
        return None
    q = Path(p)
    return q if q.is_absolute() else (cwd / q)


def cmd_launch(a) -> int:
    if not a.command:
        print("no command given (use: ... -- <cmd> [args...])")
        return 2
    cwd = Path(a.cwd).resolve()
    log = _resolve(a.log, cwd)
    heartbeat = _resolve(a.heartbeat, cwd)
    checkpoint = _resolve(a.checkpoint, cwd)

    for p in (log, heartbeat):
        p.parent.mkdir(parents=True, exist_ok=True)
    if log.exists():
        log.unlink()

    lines, size = counts(checkpoint)
    print(f"{a.id or 'run'}: checkpoint before launch: {lines} item(s), {size} bytes")
    print(f"  command: {' '.join(a.command)}")

    attempt, proc = 0, None
    while attempt <= max(0, a.retry):
        attempt += 1
        proc = spawn(a.command, cwd, log)
        deadline = time.time() + max(1, a.probe)   # short probe, never a foreground wait
        while time.time() < deadline and proc.poll() is None:
            time.sleep(0.25)
        if proc.poll() is None:
            break
        empty = (not log.exists()) or log.stat().st_size == 0
        if not empty or attempt > a.retry:
            break
        print(f"  attempt {attempt}: exited (code {proc.returncode}) with no output — likely the "
              f"Device Guard / Smart App Control block; retrying in {a.retry_delay}s")
        time.sleep(max(0, a.retry_delay))

    if proc is None:
        print("launch failed")
        return 1

    heartbeat_line(heartbeat, f"LAUNCHED id={a.id or '-'} pid={proc.pid} cmd={' '.join(a.command)}")
    if proc.poll() is not None:
        heartbeat_line(heartbeat, f"EXIT pid={proc.pid} exit_code={proc.returncode} (immediate)")
        print(f"  job exited immediately with code {proc.returncode}; see {log}")
        return proc.returncode or 1

    sup_cmd = [sys.executable, str(Path(__file__).resolve()), "_supervise",
               "--pid", str(proc.pid), "--heartbeat", str(heartbeat), "--log", str(log),
               "--interval", str(a.interval)]
    if checkpoint:
        sup_cmd += ["--checkpoint", str(checkpoint)]
    sup = spawn(sup_cmd, cwd, Path(str(log) + ".supervisor"))
    heartbeat_line(heartbeat, f"SUPERVISOR pid={sup.pid} (interval {a.interval}s)")
    print(f"  detached pid={proc.pid}; supervisor pid={sup.pid}")
    print(f"  log        : {log}")
    print(f"  heartbeat  : {heartbeat}")
    if checkpoint:
        print(f"  checkpoint : {checkpoint}")
    print()
    print("  The job is NOT monitored by this shell. Verify liveness with:")
    print(f"    python research/scripts/runjob.py status --heartbeat {heartbeat}"
          + (f" --checkpoint {checkpoint}" if checkpoint else ""))
    print("  A stale heartbeat means the job is DEAD (or never really started).")
    return 0
def cmd_status(a) -> int:
    hb = Path(a.heartbeat)
    if not hb.exists():
        print(f"heartbeat MISSING: {hb}  -> the job is NOT running (do not claim it is)")
        return 1
    age = time.time() - hb.stat().st_mtime
    lines = hb.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    last = lines[-1] if lines else "(empty)"
    state = "ALIVE" if age <= 120 else "STALE"
    if " EXIT " in f" {last} " or last.startswith("EXIT"):
        state = "FINISHED (process gone)"
    print(f"heartbeat : {hb}")
    print(f"state     : {state}   (last heartbeat {age:.0f}s ago; STALE if >120s)")
    print(f"last line : {last}")
    pid = None
    for tok in last.split():
        if tok.startswith("pid="):
            try:
                pid = int(tok[4:])
            except ValueError:
                pass
    if pid:
        print(f"process   : pid {pid} is {'RUNNING' if alive(pid) else 'GONE'}")
    if a.checkpoint:
        n, sz = counts(Path(a.checkpoint))
        print(f"checkpoint: {n} item(s), {sz} bytes ({a.checkpoint})")
    if a.log and Path(a.log).exists():
        print(f"log       : {Path(a.log).stat().st_size} bytes ({a.log})")
        try:
            tail = Path(a.log).read_text(encoding="utf-8", errors="replace").strip().splitlines()[-3:]
            for ln in tail:
                print(f"    | {ln[:160]}")
        except OSError:
            pass
    return 0


def cmd_resume(a) -> int:
    print("resume = launch with the same job; the JOB must skip items already present in its")
    print("checkpoint (SYSTEM.md §6). Current checkpoint state:")
    if a.checkpoint:
        n, sz = counts(_resolve(a.checkpoint, Path(a.cwd).resolve()))
        print(f"  {a.checkpoint}: {n} item(s), {sz} bytes")
    else:
        print("  (no checkpoint declared — resume is NOT guaranteed!)")
    return cmd_launch(a)


def cmd_supervise(a) -> int:
    return supervise(a.pid, Path(a.heartbeat), Path(a.log), a.checkpoint, a.interval)


def _add_job_args(p):
    p.add_argument("--id")
    p.add_argument("--name")
    p.add_argument("--log", required=True)
    p.add_argument("--heartbeat", required=True)
    p.add_argument("--checkpoint")
    p.add_argument("--cwd", default=".")
    p.add_argument("--retry", type=int, default=5, help="retries after an immediate silent exit")
    p.add_argument("--retry-delay", type=int, default=3)
    p.add_argument("--probe", type=int, default=4, help="seconds to detect an immediate exit")
    p.add_argument("--interval", type=int, default=15, help="heartbeat interval (seconds)")
    p.add_argument("command", nargs=argparse.REMAINDER)


def build_parser():
    p = argparse.ArgumentParser(prog="runjob", description="detached resumable job launcher")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("launch", cmd_launch), ("resume", cmd_resume)):
        sp = sub.add_parser(name)
        _add_job_args(sp)
        sp.set_defaults(func=fn)
    sp = sub.add_parser("status")
    sp.add_argument("--heartbeat", required=True)
    sp.add_argument("--log")
    sp.add_argument("--checkpoint")
    sp.set_defaults(func=cmd_status)
    sp = sub.add_parser("_supervise")
    sp.add_argument("--pid", type=int, required=True)
    sp.add_argument("--heartbeat", required=True)
    sp.add_argument("--log", required=True)
    sp.add_argument("--checkpoint")
    sp.add_argument("--interval", type=int, default=15)
    sp.set_defaults(func=cmd_supervise)
    return p


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    if getattr(args, "command", None) and args.command[:1] == ["--"]:
        args.command = args.command[1:]
    if args.cmd in ("launch", "resume") and not args.command:
        print("no command given (use: ... -- <cmd> [args...])")
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())