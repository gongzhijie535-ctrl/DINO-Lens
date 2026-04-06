import os
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from ui.panels       import canvas_panel, control_panel
from ui.logic.image_loader import load_image, on_extract_done, on_extract_error
from ui.logic.compute      import compute_sim, get_pca_rgb
from ui.logic.render       import refresh_left, refresh_right


class DinoSimilarityApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("DINOv3 特征探索器")
        self.pack(fill='both', expand=True)

        # ── 数据状态 ──────────────────────────────
        self.image_path       = None
        self.image_list       = []
        self.img_idx          = 0
        self.img_resized      = None
        self.tokens_normed    = None
        self.patch_tokens_raw = None
        self.h_patches        = 0
        self.w_patches        = 0
        self.orig_w           = 0
        self.orig_h           = 0
        self.sim_map          = None
        self.selected_patch   = None
        self.multi_patches    = []
        self.pca_cache        = {'full': None, 'fg': {}}
        self.fg_prob_map      = None
        self.fg_mask          = None
        self.history          = []
        self.favorites        = []
        self._left_offset     = (0, 0)
        self._left_ratio      = 1.0
        self.CANVAS_MAX       = 520

        # ── tkinter 变量 ──────────────────────────
        self.show_grid      = tk.BooleanVar(value=True)
        self.scale_var      = tk.IntVar(value=2)
        self.cmap_var       = tk.StringVar(value='viridis')
        self.status_var     = tk.StringVar(value="📂 请点击「打开图片」开始")
        self.right_mode     = tk.StringVar(value='similarity')
        self.multi_mode     = tk.BooleanVar(value=False)

        self.sim_show_overlay  = tk.BooleanVar(value=False)
        self.sim_overlay_alpha = tk.DoubleVar(value=0.5)
        self.use_threshold     = tk.BooleanVar(value=False)
        self.threshold_val     = tk.DoubleVar(value=0.5)
        self.use_topk          = tk.BooleanVar(value=False)
        self.topk_val          = tk.IntVar(value=10)

        self.pca_show_overlay  = tk.BooleanVar(value=False)
        self.pca_overlay_alpha = tk.DoubleVar(value=0.5)
        self.pca_fg_only       = tk.BooleanVar(value=False)
        self.pca_fg_threshold  = tk.DoubleVar(value=0.5)
        self.pca_n_components  = tk.IntVar(value=3)

        self.fg_show_overlay   = tk.BooleanVar(value=False)
        self.fg_overlay_alpha  = tk.DoubleVar(value=0.5)
        self.fg_threshold      = tk.DoubleVar(value=0.5)
        self.fg_show_on_left   = tk.BooleanVar(value=False)
        self.fg_cmap_var       = tk.StringVar(value='viridis')

        self._build_ui()

    # ── 模型状态 ──────────────────────────────────
    def set_model_loading(self):
        self.status_var.set("⏳ 正在加载模型，请稍候...")
        self._set_buttons_state('disabled')

    def set_model_ready(self):
        self.status_var.set("✅ 模型加载完成，请点击「打开图片」开始")
        self._set_buttons_state('normal')

    # ── 按钮状态 ──────────────────────────────────
    def _set_buttons_state(self, state):
        for widget in self.winfo_children():
            self._toggle_widget(widget, state)

    def _toggle_widget(self, widget, state):
        try:
            if isinstance(widget, (ttk.Button, ttk.Radiobutton,
                                    ttk.Checkbutton, ttk.Scale, ttk.Combobox)):
                widget.config(state=state)
        except Exception:
            pass
        for child in widget.winfo_children():
            self._toggle_widget(child, state)

    # ── UI 组装 ───────────────────────────────────
    def _build_ui(self):
        self._build_menubar()

        body = ttk.Frame(self)
        body.pack(fill='both', expand=True, padx=4, pady=2)
        canvas_panel.build(self, body)
        control_panel.build(self, body)

        status_bar = ttk.Frame(self, relief='sunken')
        status_bar.pack(side=tk.BOTTOM, fill='x')
        ttk.Label(status_bar, textvariable=self.status_var, anchor='w').pack(
            side=tk.LEFT, padx=6, pady=2)

    def _build_menubar(self):
        menubar = ttk.Frame(self, relief='groove')
        menubar.pack(side=tk.TOP, fill='x', padx=2, pady=2)
        ttk.Button(menubar, text='📂 打开图片',
                   command=self._open_image).pack(side=tk.LEFT, padx=4, pady=3)
        ttk.Button(menubar, text='🎲 随机图片',
                   command=self._random_image).pack(side=tk.LEFT, padx=4, pady=3)
        ttk.Button(menubar, text='⭐ 收藏当前',
                   command=self._add_favorite).pack(side=tk.LEFT, padx=4, pady=3)
        ttk.Button(menubar, text='💾 保存结果',
                   command=self._save_result).pack(side=tk.LEFT, padx=4, pady=3)
        ttk.Separator(menubar, orient='vertical').pack(side=tk.LEFT, fill='y', padx=6)
        ttk.Label(menubar, text="右图模式:").pack(side=tk.LEFT)
        for text, val in [('🔥 相似度热力图', 'similarity'),
                          ('🧠 PCA语义图',    'pca'),
                          ('🎭 前景概率图',    'fg')]:
            ttk.Radiobutton(menubar, text=text, variable=self.right_mode,
                            value=val,
                            command=self._on_mode_change).pack(side=tk.LEFT, padx=2)

    # ── 代理方法（供子模块和回调使用）────────────
    def _refresh_left(self,  *_): refresh_left(self)
    def _refresh_right(self, *_): refresh_right(self)
    def _compute_sim(self):       compute_sim(self)
    def _get_pca_rgb(self):       return get_pca_rgb(self)
    def _load_image(self, path):  load_image(self, path)

    def _on_extract_done(self, path, result):
        on_extract_done(self, path, result)

    def _on_extract_error(self, e):
        on_extract_error(self, e)

    # ── 事件 ──────────────────────────────────────
    def _canvas_click_to_patch(self, event):
        from core.config import PATCH_SIZE
        x_off, y_off = self._left_offset
        px = (event.x - x_off) / self._left_ratio
        py = (event.y - y_off) / self._left_ratio
        ih, iw = self.img_resized.shape[:2]
        if not (0 <= px < iw and 0 <= py < ih):
            return None
        cw = max(0, min(int(px) // PATCH_SIZE, self.w_patches - 1))
        ch = max(0, min(int(py) // PATCH_SIZE, self.h_patches - 1))
        return ch, cw

    def _on_left_click(self, event):
        if self.tokens_normed is None:
            return
        result = self._canvas_click_to_patch(event)
        if result is None:
            return
        self.selected_patch = result
        self.lbl_selected.config(text=f"选中patch: {result}")
        self._compute_sim()
        self._refresh_left()
        self._refresh_right()

    def _on_right_click(self, event):
        if self.tokens_normed is None or not self.multi_mode.get():
            return
        result = self._canvas_click_to_patch(event)
        if result is None or result == self.selected_patch:
            return
        if result in self.multi_patches:
            self.multi_patches.remove(result)
        else:
            self.multi_patches.append(result)
        self.lbl_multi.config(text=f"多点数量: {len(self.multi_patches)}")
        self._compute_sim()
        self._refresh_left()
        self._refresh_right()

    def _on_canvas_resize(self, event):
        self._refresh_left()
        self._refresh_right()

    def _on_mode_change(self):
        tab_map = {'similarity': 0, 'pca': 1, 'fg': 2}
        self.mode_nb.select(tab_map[self.right_mode.get()])
        self._refresh_right()

    def _on_tab_changed(self, event):
        idx_map = {0: 'similarity', 1: 'pca', 2: 'fg'}
        idx = self.mode_nb.index('current')
        self.right_mode.set(idx_map[idx])
        self._refresh_right()

    def _on_threshold_change(self, val):
        self.thresh_label.config(text=f"阈值: {float(val):.2f}")
        self._refresh_right()

    def _on_fg_threshold_change(self, val):
        self.fg_thresh_label.config(text=f"阈值: {float(val):.2f}")
        self._refresh_right()

    def _on_pca_fg_threshold_change(self, val):
        self.pca_fg_thresh_label.config(text=f"前景阈值: {float(val):.2f}")
        if self.pca_fg_only.get():
            self._refresh_right()

    def _on_multi_mode_change(self):
        if not self.multi_mode.get():
            self.multi_patches = []
            self.lbl_multi.config(text="多点数量: 0")
            self._compute_sim()
            self._refresh_left()
            self._refresh_right()

    def _clear_multi_patches(self):
        self.multi_patches = []
        self.lbl_multi.config(text="多点数量: 0")
        if self.tokens_normed is not None:
            self._compute_sim()
            self._refresh_left()
            self._refresh_right()

    def _on_pca_fg_toggle(self):
        self.pca_cache = {'full': None, 'fg': {}}
        self._refresh_right()

    def _on_history_select(self, event):
        sel = self.history_listbox.curselection()
        if not sel:
            return
        path = self.history[sel[0]][0]
        if path != self.image_path and os.path.isfile(path):
            self._load_image(path)

    def _on_fav_select(self, event):
        sel = self.fav_listbox.curselection()
        if not sel:
            return
        path = self.favorites[sel[0]][0]
        if path != self.image_path and os.path.isfile(path):
            self._load_image(path)

    # ── 按钮功能 ──────────────────────────────────
    def _open_image(self):
        from utils.file_utils import scan_folder
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.webp"),
                       ("所有文件", "*.*")]
        )
        if not path:
            return
        self.image_list = scan_folder(os.path.dirname(path))
        if path in self.image_list:
            self.img_idx = self.image_list.index(path)
        self._load_image(path)

    def _random_image(self):
        pool = [p for p in self.image_list if p != self.image_path]
        if not pool:
            messagebox.showinfo("提示", "当前文件夹只有一张图片或尚未打开文件夹")
            return
        path = random.choice(pool)
        self.img_idx = self.image_list.index(path)
        self._load_image(path)

    def _reextract(self):
        if self.image_path:
            self.pca_cache = {'full': None, 'fg': {}}
            self._load_image(self.image_path)

    def _add_favorite(self):
        if not self.image_path:
            return
        if any(p == self.image_path for p, _ in self.favorites):
            messagebox.showinfo("提示", "已经在收藏列表中了")
            return
        name = os.path.basename(self.image_path)
        self.favorites.append((self.image_path, name))
        self.fav_listbox.insert(tk.END, name)
        self.status_var.set(f"⭐ 已收藏: {name}")

    def _remove_favorite(self):
        sel = self.fav_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.favorites.pop(idx)
        self.fav_listbox.delete(idx)

    def _save_result(self):
        import cv2
        import numpy as np
        from core.config import COLORMAPS
        from core.model  import sim_to_heatmap
        if self.img_resized is None:
            messagebox.showwarning("提示", "请先加载图片")
            return
        ih, iw   = self.img_resized.shape[:2]
        orig_bgr = cv2.cvtColor(self.img_resized, cv2.COLOR_RGB2BGR)
        mode     = self.right_mode.get()

        if mode == 'pca':
            right_img = cv2.cvtColor(
                cv2.resize(self._get_pca_rgb(), (iw, ih),
                           interpolation=cv2.INTER_NEAREST),
                cv2.COLOR_RGB2BGR)
        elif mode == 'fg':
            if self.fg_prob_map is None:
                messagebox.showwarning("提示", "前景分割头未就绪")
                return
            prob_u8   = (self.fg_prob_map * 255).astype(np.uint8)
            right_img = cv2.applyColorMap(
                cv2.resize(prob_u8, (iw, ih), interpolation=cv2.INTER_NEAREST),
                COLORMAPS[self.fg_cmap_var.get()])
        else:
            if self.sim_map is None:
                messagebox.showwarning("提示", "请先选择 patch")
                return
            right_img = cv2.resize(
                sim_to_heatmap(self.sim_map, self.cmap_var.get()),
                (iw, ih), interpolation=cv2.INTER_NEAREST)

        combined     = np.hstack([orig_bgr, right_img])
        default_name = os.path.splitext(
            os.path.basename(self.image_path))[0] + f'_{mode}.png'
        save_path = filedialog.asksaveasfilename(
            title="保存结果", initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG图片", "*.png"), ("所有文件", "*.*")]
        )
        if save_path:
            cv2.imwrite(save_path, combined)
            self.status_var.set(f"已保存: {save_path}")
