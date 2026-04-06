import tkinter as tk
from tkinter import ttk

from core.config import COLORMAPS
from ui.tabs.tab_similarity import build as build_tab_similarity
from ui.tabs.tab_pca        import build as build_tab_pca
from ui.tabs.tab_fg         import build as build_tab_fg


def build(app, body):
    ctrl_container = ttk.Frame(body, width=260)
    ctrl_container.pack(side=tk.RIGHT, fill='y')
    ctrl_container.pack_propagate(False)

    ctrl_canvas = tk.Canvas(ctrl_container, width=258, highlightthickness=0)
    ctrl_scrollbar = ttk.Scrollbar(ctrl_container, orient='vertical',
                                   command=ctrl_canvas.yview)
    ctrl_canvas.configure(yscrollcommand=ctrl_scrollbar.set)
    ctrl_scrollbar.pack(side=tk.RIGHT, fill='y')
    ctrl_canvas.pack(side=tk.LEFT, fill='both', expand=True)

    ctrl = ttk.Frame(ctrl_canvas)
    ctrl_canvas.create_window((0, 0), window=ctrl, anchor='nw')

    def _on_ctrl_configure(event):
        ctrl_canvas.configure(scrollregion=ctrl_canvas.bbox('all'))

    def _on_ctrl_mousewheel(event):
        ctrl_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    ctrl.bind('<Configure>', _on_ctrl_configure)
    ctrl_canvas.bind('<MouseWheel>', _on_ctrl_mousewheel)
    ctrl.bind('<MouseWheel>', _on_ctrl_mousewheel)

    _build_info(app, ctrl)
    _build_params(app, ctrl)
    _build_common(app, ctrl)
    _build_tabs(app, ctrl)
    _build_history(app, ctrl)


def _build_info(app, parent):
    info_frame = ttk.LabelFrame(parent, text="图像信息")
    info_frame.pack(fill='x', padx=6, pady=4)
    app.lbl_filename  = ttk.Label(info_frame, text="文件名: —",    wraplength=220, anchor='w')
    app.lbl_orig_size = ttk.Label(info_frame, text="原始尺寸: —",  anchor='w')
    app.lbl_proc_size = ttk.Label(info_frame, text="处理尺寸: —",  anchor='w')
    app.lbl_patches   = ttk.Label(info_frame, text="Patch网格: —", anchor='w')
    app.lbl_selected  = ttk.Label(info_frame, text="选中patch: —", anchor='w',
                                   foreground='#cc3300')
    app.lbl_multi     = ttk.Label(info_frame, text="多点数量: 0",  anchor='w',
                                   foreground='#0066cc')
    for w in (app.lbl_filename, app.lbl_orig_size, app.lbl_proc_size,
              app.lbl_patches, app.lbl_selected, app.lbl_multi):
        w.pack(fill='x', padx=6, pady=1)


def _build_params(app, parent):
    param_frame = ttk.LabelFrame(parent, text="提取参数")
    param_frame.pack(fill='x', padx=6, pady=4)
    ttk.Label(param_frame, text="SCALE:").pack(anchor='w', padx=6, pady=(4, 0))
    scale_row = ttk.Frame(param_frame)
    scale_row.pack(fill='x', padx=6)
    for val, label in [(1, '1x'), (2, '2x'), (3, '3x'), (4, '4x')]:
        ttk.Radiobutton(scale_row, text=label, variable=app.scale_var,
                        value=val).pack(side=tk.LEFT)
    ttk.Button(param_frame, text='🔄 重新提取特征',
               command=app._reextract).pack(fill='x', padx=6, pady=6)


def _build_common(app, parent):
    common_frame = ttk.LabelFrame(parent, text="通用显示")
    common_frame.pack(fill='x', padx=6, pady=4)
    ttk.Checkbutton(common_frame, text='显示 patch 网格线',
                    variable=app.show_grid,
                    command=app._refresh_left).pack(anchor='w', padx=6, pady=2)
    ttk.Label(common_frame, text="色彩映射（相似度图）:").pack(anchor='w', padx=6)
    cmap_combo = ttk.Combobox(common_frame, textvariable=app.cmap_var,
                              values=list(COLORMAPS.keys()),
                              state='readonly', width=12)
    cmap_combo.pack(padx=6, pady=(0, 4), anchor='w')
    cmap_combo.bind('<<ComboboxSelected>>', lambda _: app._refresh_right())


def _build_tabs(app, parent):
    app.mode_nb = ttk.Notebook(parent)
    app.mode_nb.pack(fill='x', padx=6, pady=4)

    app._tab_sim = ttk.Frame(app.mode_nb)
    app._tab_pca = ttk.Frame(app.mode_nb)
    app._tab_fg  = ttk.Frame(app.mode_nb)
    app.mode_nb.add(app._tab_sim, text='🔥 相似度')
    app.mode_nb.add(app._tab_pca, text='🧠 PCA')
    app.mode_nb.add(app._tab_fg,  text='🎭 前景')
    app.mode_nb.bind('<<NotebookTabChanged>>', app._on_tab_changed)

    build_tab_similarity(app, app._tab_sim)
    build_tab_pca(app, app._tab_pca)
    build_tab_fg(app, app._tab_fg)


def _build_history(app, parent):
    hist_nb = ttk.Notebook(parent)
    hist_nb.pack(fill='both', expand=True, padx=6, pady=4)

    hist_tab = ttk.Frame(hist_nb)
    hist_nb.add(hist_tab, text='🕐 最近')
    hist_scroll = ttk.Scrollbar(hist_tab, orient='vertical')
    app.history_listbox = tk.Listbox(
        hist_tab, yscrollcommand=hist_scroll.set,
        selectmode='single', activestyle='dotbox',
        font=('Consolas', 8), bg='#f5f5f5')
    hist_scroll.config(command=app.history_listbox.yview)
    hist_scroll.pack(side=tk.RIGHT, fill='y')
    app.history_listbox.pack(fill='both', expand=True)
    app.history_listbox.bind('<<ListboxSelect>>', app._on_history_select)

    fav_tab = ttk.Frame(hist_nb)
    hist_nb.add(fav_tab, text='⭐ 收藏')
    fav_btn_row = ttk.Frame(fav_tab)
    fav_btn_row.pack(fill='x')
    ttk.Button(fav_btn_row, text='删除选中',
               command=app._remove_favorite).pack(side=tk.LEFT, padx=4, pady=2)
    fav_scroll = ttk.Scrollbar(fav_tab, orient='vertical')
    app.fav_listbox = tk.Listbox(
        fav_tab, yscrollcommand=fav_scroll.set,
        selectmode='single', activestyle='dotbox',
        font=('Consolas', 8), bg='#fffbe6')
    fav_scroll.config(command=app.fav_listbox.yview)
    fav_scroll.pack(side=tk.RIGHT, fill='y')
    app.fav_listbox.pack(fill='both', expand=True)
    app.fav_listbox.bind('<<ListboxSelect>>', app._on_fav_select)
