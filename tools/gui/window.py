#!/usr/bin/env python3
"""KANAMECIDE Training Control GUI part 2: main window frame.

tkinter imports live in this module (standard for a Tk app); headless
`python tools/gui_test.py` never imports this module — it tests
backend/proc/ckpts/engines only.
"""
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from . import backend as B
from . import engines as E
from .app import APP_TITLE
from .proc import TrainerProc


class BaseWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("860x640")
        self.settings = B.load_settings()
        cfg = self.settings.get("config", "")
        self.config_path = Path(cfg) if cfg else B.DEFAULT_CONFIG
        det = E.detect_engines(self.settings)
        self.kana_engine = tk.StringVar(value=det["kana_engine"])
        self.cutechess = tk.StringVar(value=det["cutechess"])
        self.stockfish = tk.StringVar(value=det["stockfish"])
        self.proc = TrainerProc(self._on_line, self._on_exit)
        self._build()
        # NOTE: _build2/_refresh_all/_tick are wired by mainwin.MainWindow
        # after the mixin methods exist.

    # -- layout ------------------------------------------------------
    def _build(self):
        import tkinter as tk
        from tkinter import ttk
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="KANAMECIDE",
                  font=("TkDefaultFont", 14, "bold")).pack(side="left")
        self.status_var = tk.StringVar(value="Status: IDLE")
        ttk.Label(top, textvariable=self.status_var,
                  font=("TkDefaultFont", 11, "bold")).pack(side="right")

        cfgf = ttk.LabelFrame(self, text="Training configuration", padding=8)
        cfgf.pack(fill="x", padx=8, pady=4)
        row = ttk.Frame(cfgf)
        row.pack(fill="x")
        ttk.Label(row, text="Config:").pack(side="left")
        self.cfg_var = tk.StringVar(value=str(self.config_path))
        ttk.Entry(row, textvariable=self.cfg_var, width=60).pack(
            side="left", padx=4, expand=True, fill="x")
        ttk.Button(row, text="Browse...",
                   command=self._browse_config).pack(side="left")
        self.summary_var = tk.StringVar(value="")
        ttk.Label(cfgf, textvariable=self.summary_var,
                  wraplength=800, justify="left").pack(fill="x", pady=4)

        btn = ttk.Frame(self, padding=(8, 0))
        btn.pack(fill="x")
        self.b_start = ttk.Button(btn, text="Start Training",
                                  command=self._start)
        self.b_start.pack(side="left", padx=2)
        self.b_stop = ttk.Button(btn, text="Stop Training",
                                 command=self._stop)
        self.b_stop.pack(side="left", padx=2)
        self.b_resume = ttk.Button(btn, text="Resume Training",
                                   command=self._resume)
        self.b_resume.pack(side="left", padx=2)
        self.b_pre = ttk.Button(btn, text="Preflight",
                                command=lambda: self._quick("preflight"))
        self.b_pre.pack(side="left", padx=2)
        self.b_dry = ttk.Button(btn, text="Dry Run",
                                command=lambda: self._quick("dry-run"))
        self.b_dry.pack(side="left", padx=2)

        btn2 = ttk.Frame(self, padding=(8, 4))
        btn2.pack(fill="x")
        ttk.Button(btn2, text="Copy Training Command",
                   command=self._copy_cmd).pack(side="left", padx=2)
        ttk.Button(btn2, text="Open Output Folder",
                   command=self._open_output).pack(side="left", padx=2)
        ttk.Button(btn2, text="Open Log",
                   command=self._open_log).pack(side="left", padx=2)
        ttk.Button(btn2, text="Open Manifest",
                   command=self._open_manifest).pack(side="left", padx=2)
        ttk.Button(btn2, text="Clear View",
                   command=self._clear_view).pack(side="left", padx=2)

    def _build2(self):
        import tkinter as tk
        from tkinter import ttk
        live = ttk.LabelFrame(self, text="Live status", padding=8)
        live.pack(fill="x", padx=8, pady=4)
        self.live_var = tk.StringVar(value="")
        ttk.Label(live, textvariable=self.live_var, justify="left",
                  font=("TkFixedFont", 10)).pack(fill="x")
        self.err_var = tk.StringVar(value="")
        ttk.Label(live, textvariable=self.err_var, justify="left",
                  foreground="red", wraplength=800).pack(fill="x")

        logf = ttk.LabelFrame(self, text="Log (display only; full log on disk)",
                              padding=8)
        logf.pack(fill="both", padx=8, pady=4, expand=True)
        self.log = tk.Text(logf, font=("TkFixedFont", 9), wrap="none",
                           state="disabled")
        ys = ttk.Scrollbar(logf, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=ys.set)
        self.log.pack(side="left", fill="both", expand=True)
        ys.pack(side="right", fill="y")

        eng = ttk.LabelFrame(self, text="Engine testing (casual; not a strength claim)",
                             padding=8)
        eng.pack(fill="x", padx=8, pady=4)
        for label, var in (("KANAMECIDE engine:", self.kana_engine),
                           ("Cute Chess:", self.cutechess),
                           ("Stockfish (optional):", self.stockfish)):
            r = ttk.Frame(eng)
            r.pack(fill="x", pady=1)
            ttk.Label(r, text=label, width=20).pack(side="left")
            ttk.Entry(r, textvariable=var).pack(side="left", expand=True,
                                                fill="x", padx=4)
            ttk.Button(r, text="Browse...",
                       command=lambda v=var: self._browse_exe(v)).pack(
                           side="left")
        er = ttk.Frame(eng)
        er.pack(fill="x", pady=4)
        ttk.Button(er, text="Engine UCI Check",
                   command=self._uci_check).pack(side="left", padx=2)
        ttk.Button(er, text="Play Test Game (depth 2)",
                   command=self._test_game).pack(side="left", padx=2)
        ttk.Button(er, text="Open Engine Testing GUI",
                   command=self._open_cute).pack(side="left", padx=2)
        self.eng_var = tk.StringVar(value="")
        ttk.Label(eng, textvariable=self.eng_var, wraplength=800,
                  justify="left").pack(fill="x")

