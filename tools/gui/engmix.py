#!/usr/bin/env python3
"""Main window part 3b: engine-testing actions."""
from __future__ import annotations

import subprocess
import threading
from tkinter import filedialog, messagebox

from . import engines as E


class EngineMixin:
    def _browse_exe(self, var):
        p = filedialog.askopenfilename(title="Select executable")
        if p:
            var.set(p)
            self._save_local()

    def _uci_check(self):
        exe = self.kana_engine.get().strip()
        self.eng_var.set("UCI check running...")
        self._save_local()

        def run():
            ok, detail = E.uci_smoke(exe)
            self.after(0, lambda: self.eng_var.set(
                f"KANAMECIDE UCI: {'OK' if ok else 'FAIL'} — {detail}"))

        threading.Thread(target=run, daemon=True).start()

    def _test_game(self):
        from . import match as M
        if M is None:
            messagebox.showerror("Test game", "match module missing")
            return
        a = self.kana_engine.get().strip()
        b = self.stockfish.get().strip() or a
        if not a:
            messagebox.showerror("Test game",
                                 "set the KANAMECIDE engine path")
            return
        self.eng_var.set("test game running (depth 2, casual)...")

        def run():
            try:
                res = M.play_game(a, b, depth=2)
                txt = (f"test game: {res['result']} "
                       f"({len(res['moves'])} plies) — {res['reason']}; "
                       "casual only, not a strength claim")
            except Exception as exc:
                txt = f"test game failed: {exc}"
            self.after(0, lambda: self.eng_var.set(txt))

        threading.Thread(target=run, daemon=True).start()

    def _open_cute(self):
        exe = self.cutechess.get().strip()
        self._save_local()
        if not exe:
            messagebox.showinfo(
                "Engine Testing",
                "Cute Chess path is not set.\n\n"
                "Install Cute Chess 1.5.0 (GPLv3+) from "
                "https://github.com/cutechess/cutechess, then Browse "
                "to cutechess-gui (or cutechess-cli).\n\n"
                "KANAMECIDE engine path for registration:\n"
                f"{self.kana_engine.get() or '(not set)'}")
            return
        try:
            subprocess.Popen([exe])
            self.eng_var.set(f"Cute Chess launched: {exe}")
        except Exception as exc:
            messagebox.showerror("Engine Testing", f"cannot launch: {exc}")
