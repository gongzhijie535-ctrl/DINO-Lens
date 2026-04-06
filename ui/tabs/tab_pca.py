from tkinter import ttk


def build(app, parent):
    ov_frame = ttk.LabelFrame(parent, text="叠加原图")
    ov_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(ov_frame, text='PCA图叠加原图',
                    variable=app.pca_show_overlay,
                    command=app._refresh_right).pack(anchor='w', padx=6, pady=2)
    ttk.Label(ov_frame, text="透明度:").pack(anchor='w', padx=6)
    ttk.Scale(ov_frame, from_=0.0, to=1.0, variable=app.pca_overlay_alpha,
              orient='horizontal',
              command=lambda _: app._refresh_right()).pack(fill='x', padx=6, pady=(0, 4))

    fg_frame = ttk.LabelFrame(parent, text="🎭 前景选项")
    fg_frame.pack(fill='x', padx=4, pady=4)
    ttk.Checkbutton(fg_frame, text='仅对前景 patch 做 PCA\n（背景显示为黑色）',
                    variable=app.pca_fg_only,
                    command=app._on_pca_fg_toggle).pack(anchor='w', padx=6, pady=4)
    app.pca_fg_thresh_label = ttk.Label(fg_frame, text="前景阈值: 0.50")
    app.pca_fg_thresh_label.pack(anchor='w', padx=6)
    ttk.Scale(fg_frame, from_=0.0, to=1.0, variable=app.pca_fg_threshold,
              orient='horizontal',
              command=app._on_pca_fg_threshold_change).pack(fill='x', padx=6, pady=(0, 4))
    app.lbl_pca_fg_status = ttk.Label(
        fg_frame, text="", foreground='#888888', wraplength=200)
    app.lbl_pca_fg_status.pack(anchor='w', padx=6, pady=(0, 4))
