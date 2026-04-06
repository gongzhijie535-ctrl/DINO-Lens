import tkinter as tk
from tkinter import ttk


def build(app, parent):
    ov_frame = ttk.LabelFrame(parent, text="叠加原图")
    ov_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(ov_frame, text='热力图叠加原图',
                    variable=app.sim_show_overlay,
                    command=app._refresh_right).pack(anchor='w', padx=6, pady=2)
    ttk.Label(ov_frame, text="透明度:").pack(anchor='w', padx=6)
    ttk.Scale(ov_frame, from_=0.0, to=1.0, variable=app.sim_overlay_alpha,
              orient='horizontal',
              command=lambda _: app._refresh_right()).pack(fill='x', padx=6, pady=(0, 4))

    thresh_frame = ttk.LabelFrame(parent, text="🎚 阈值遮罩")
    thresh_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(thresh_frame, text='启用阈值遮罩',
                    variable=app.use_threshold,
                    command=app._refresh_right).pack(anchor='w', padx=6, pady=2)
    app.thresh_label = ttk.Label(thresh_frame, text="阈值: 0.50")
    app.thresh_label.pack(anchor='w', padx=6)
    ttk.Scale(thresh_frame, from_=0.0, to=1.0, variable=app.threshold_val,
              orient='horizontal',
              command=app._on_threshold_change).pack(fill='x', padx=6, pady=(0, 4))

    topk_frame = ttk.LabelFrame(parent, text="🏆 Top-K 高亮")
    topk_frame.pack(fill='x', padx=4, pady=4)
    topk_row = ttk.Frame(topk_frame)
    topk_row.pack(fill='x', padx=6, pady=4)
    ttk.Checkbutton(topk_row, text='启用 Top-K',
                    variable=app.use_topk,
                    command=app._refresh_right).pack(side=tk.LEFT)
    ttk.Label(topk_row, text="  K=").pack(side=tk.LEFT)
    ttk.Spinbox(topk_row, from_=1, to=100, textvariable=app.topk_val,
                width=5, command=app._refresh_right).pack(side=tk.LEFT)

    multi_frame = ttk.LabelFrame(parent, text="📍 多点平均模式")
    multi_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(multi_frame, text='启用多点模式（右键添加点）',
                    variable=app.multi_mode,
                    command=app._on_multi_mode_change).pack(anchor='w', padx=6, pady=2)
    ttk.Button(multi_frame, text='🗑 清除所有多点',
               command=app._clear_multi_patches).pack(fill='x', padx=6, pady=(0, 4))
