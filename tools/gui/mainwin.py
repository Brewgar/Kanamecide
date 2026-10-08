#!/usr/bin/env python3
"""Compose the single MainWindow from the mixin parts."""
from __future__ import annotations

from .actions import ActionsMixin
from .engmix import EngineMixin
from .refresh import RefreshMixin
from .window import BaseWindow as _Base


class MainWindow(ActionsMixin, EngineMixin, RefreshMixin, _Base):
    def __init__(self):
        _Base.__init__(self)
        self._build2()
        self._refresh_all()
        self.after(1000, self._tick)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        if self.proc.is_alive():
            from tkinter import messagebox
            if not messagebox.askyesno(
                    "Training running",
                    "Training is still running in the background.\n"
                    "Close the GUI and leave it running?"):
                return
        try:
            self._save_local()
        except Exception:
            pass
        self.destroy()


def main() -> int:
    win = MainWindow()
    win.mainloop()
    return 0
