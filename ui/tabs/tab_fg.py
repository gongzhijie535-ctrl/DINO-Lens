from tkinter import ttk

from core.config import COLORMAPS


def build(app, parent):
    ov_frame = ttk.LabelFrame(parent, text="叠加原图")
    ov_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(ov_frame, text='概率图叠加原图',
                    variable=app.fg_show_overlay,
                    command=app._refresh_right).pack(anchor='w', padx=6, pady=2)
    ttk.Label(ov_frame, text="透明度:").pack(anchor='w', padx=6)
    ttk.Scale(ov_frame, from_=0.0, to=1.0, variable=app.fg_overlay_alpha,
              orient='horizontal',
              command=lambda _: app._refresh_right()).pack(fill='x', padx=6, pady=(0, 4))

    cmap_frame = ttk.LabelFrame(parent, text="色彩映射")
    cmap_frame.pack(fill='x', padx=4, pady=4)
    fg_cmap_combo = ttk.Combobox(cmap_frame, textvariable=app.fg_cmap_var,
                                 values=list(COLORMAPS.keys()),
                                 state='readonly', width=12)
    fg_cmap_combo.pack(padx=6, pady=6, anchor='w')
    fg_cmap_combo.bind('<<ComboboxSelected>>', lambda _: app._refresh_right())

    thresh_frame = ttk.LabelFrame(parent, text="🎚 二值化阈值")
    thresh_frame.pack(fill='x', padx=4, pady=4)
    app.fg_thresh_label = ttk.Label(thresh_frame, text="阈值: 0.50")
    app.fg_thresh_label.pack(anchor='w', padx=6)
    ttk.Scale(thresh_frame, from_=0.0, to=1.0, variable=app.fg_threshold,
              orient='horizontal',
              command=app._on_fg_threshold_change).pack(fill='x', padx=6, pady=(0, 2))

    left_frame = ttk.LabelFrame(parent, text="左图叠加")
    left_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(left_frame, text='左图叠加前景遮罩（绿色）',
                    variable=app.fg_show_on_left,
                    command=app._refresh_left).pack(anchor='w', padx=6, pady=4)

    stat_frame = ttk.LabelFrame(parent, text="📊 前景统计")
    stat_frame.pack(fill='x', padx=4, pady=4)
    app.lbl_fg_ratio = ttk.Label(stat_frame, text="前景占比: —", anchor='w')
    app.lbl_fg_count = ttk.Label(stat_frame, text="前景patch数: —", anchor='w')
    app.lbl_fg_ratio.pack(fill='x', padx=6, pady=1)
    app.lbl_fg_count.pack(fill='x', padx=6, pady=1)
