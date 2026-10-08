#!/usr/bin/env python3
"""Main window part 3a: refresh + file actions."""
from __future__ import annotations

from pathlib import Path

from . import backend as B
from . import ckpts as C
from .app import open_path, read_config_summary


class RefreshMixin:
    def _refresh_all(self):
        s = read_config_summary(self.config_path)
        if "error" in s:
            self.summary_var.set(f"config error: {s['error']}")
        else:
            self.summary_var.set(
                f"record {s['record']} | {s['model']} "
                f"(free {s['free']}, stage {s['stage']}) | "
                f"maxiter {s['maxiter']} seed {s['seed']} | "
                f"device {s['device']} / {s['precision']} | out {s['output']}")
        self._refresh_live()
        self._apply_buttons()

    def _refresh_live(self):
        st = self.proc.status
        self.status_var.set(f"Status: {st.state}")
        ec = st.exit_code if st.exit_code is not None else "--"
        lines = [
            f"elapsed {st.elapsed}  pid {st.pid or '--'}  exit {ec}",
            f"fit games/rows: {st.fit_games or '?'} / "
            f"{st.fit_rows or '?'}  design: {st.jac_shape or '?'}",
            f"floor {st.floor_loss or '?'}  fitted {st.fitted_loss or '?'}"
            f"  d_fit {st.delta_fit or '?'}  "
            f"d_inner {st.delta_inner_val or '?'}",
            f"checkpoint: {st.last_checkpoint or '?'} "
            f"{st.last_checkpoint_sha or ''}",
            "device: cpu (frozen config pins CPU; no silent GPU claim)",
        ]
        if st.error_text and st.state in ("FAILED", "STOPPED"):
            lines.append("NOTE: " + st.error_text.splitlines()[0][:200])
        self.live_var.set("\n".join(lines))
        if st.error_text and st.state == "FAILED":
            self.err_var.set("TRAINING FAILED:\n" + st.error_text[:1500])
        else:
            self.err_var.set("")

    def _apply_buttons(self):
        running = self.proc.is_alive() or \
            self.proc.status.state in ("STARTING", "RESUMING", "STOPPING")
        ck = C.latest_checkpoint(self.config_path)
        for b in (self.b_start, self.b_pre, self.b_dry):
            b.configure(state="disabled" if running else "normal")
        self.b_stop.configure(state="normal" if running else "disabled")
        self.b_resume.configure(
            state="normal"
            if (not running and ck is not None) else "disabled")

    def _tick(self):
        try:
            self._refresh_live()
        except Exception:
            pass
        self.after(1000, self._tick)

    def _copy_cmd(self):
        cmd = B.trainer_command("train", self.config_path)
        self.clipboard_clear()
        self.clipboard_append(" ".join(str(c) for c in cmd))
        self._append_log("[copied training command to clipboard]")

    def _open_output(self):
        self._append_log("[open] " +
                         open_path(B.output_dir_for(self.config_path)))

    def _open_log(self):
        p = self.proc.log_path
        if p is None or not Path(p).is_file():
            d = B.output_dir_for(self.config_path)
            cands = sorted(d.glob("gui-run-*.log")) if d.is_dir() else []
            p = cands[-1] if cands else None
        self._append_log("[open] " + open_path(p) if p else "[no log yet]")

    def _open_manifest(self):
        self._append_log("[open] " + open_path(
            B.output_dir_for(self.config_path) / "manifest.json"))

    def _clear_view(self):
        try:
            self.log.configure(state="normal")
            self.log.delete("1.0", "end")
            self.log.configure(state="disabled")
        except Exception:
            pass
