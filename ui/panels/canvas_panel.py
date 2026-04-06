import tkinter as tk
from tkinter import ttk


def build(app, body):
    canvas_area = ttk.LabelFrame(body, text="图像查看器")
    canvas_area.pack(side=tk.LEFT, fill='both', expand=True, padx=(0, 4))

    left_panel = ttk.LabelFrame(canvas_area,
                                text="原图  [左键=选主点  右键=添加多点]")
    left_panel.pack(side=tk.LEFT, fill='both', expand=True, padx=4, pady=4)
    app.canvas_left = tk.Canvas(left_panel, bg='#2b2b2b', cursor='crosshair',
                                width=app.CANVAS_MAX, height=app.CANVAS_MAX,
                                highlightthickness=0)
    app.canvas_left.pack(fill='both', expand=True, padx=2, pady=2)
    app.canvas_left.bind('<Button-1>', app._on_left_click)
    app.canvas_left.bind('<Button-3>', app._on_right_click)
    app.canvas_left.bind('<Configure>', app._on_canvas_resize)

    app.right_panel_label = ttk.LabelFrame(canvas_area, text="余弦相似度热力图")
    app.right_panel_label.pack(side=tk.LEFT, fill='both', expand=True, padx=4, pady=4)
    app.canvas_right = tk.Canvas(app.right_panel_label, bg='#2b2b2b',
                                 width=app.CANVAS_MAX, height=app.CANVAS_MAX,
                                 highlightthickness=0)
    app.canvas_right.pack(fill='both', expand=True, padx=2, pady=2)
