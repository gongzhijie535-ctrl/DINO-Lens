import os
import threading
import tkinter as tk
from tkinter import messagebox

from core.model      import load_and_extract, predict_fg_mask, is_seg_ready
from utils.file_utils import add_to_history
from ui.logic.compute import compute_sim
from ui.logic.render  import refresh_left, refresh_right


def load_image(app, path):
    app.status_var.set(f"⏳ 正在提取特征：{os.path.basename(path)} ...")
    app._set_buttons_state('disabled')
    app.master.update_idletasks()

    def worker():
        try:
            result = load_and_extract(path, app.scale_var.get())
            app.master.after(0, lambda: on_extract_done(app, path, result))
        except Exception as e:
            app.master.after(0, lambda: on_extract_error(app, e))

    threading.Thread(target=worker, daemon=True).start()


def on_extract_error(app, e):
    app._set_buttons_state('normal')
    messagebox.showerror("加载失败", f"错误信息：\n{e}")
    app.status_var.set("❌ 加载失败，请检查图片文件")


def on_extract_done(app, path, result):
    (app.img_resized, app.tokens_normed, app.patch_tokens_raw,
     app.h_patches, app.w_patches,
     app.orig_w, app.orig_h) = result

    app.image_path     = path
    app.selected_patch = (app.h_patches // 2, app.w_patches // 2)
    app.multi_patches  = []
    app.pca_cache      = {'full': None, 'fg': {}}

    scale = app.scale_var.get()

    if is_seg_ready():
        app.fg_prob_map, app.fg_mask = predict_fg_mask(
            app.patch_tokens_raw, app.h_patches, app.w_patches)
        fg_count = int(app.fg_mask.sum())
        fg_total = app.h_patches * app.w_patches
        app.lbl_fg_ratio.config(
            text=f"前景占比: {fg_count / fg_total * 100:.1f}%")
        app.lbl_fg_count.config(
            text=f"前景patch数: {fg_count} / {fg_total}")
        app.lbl_pca_fg_status.config(
            text=f"分割头就绪，前景 {fg_count} 个 patch")
    else:
        app.fg_prob_map = None
        app.fg_mask     = None
        app.lbl_fg_ratio.config(text="前景占比: 分割头未加载")
        app.lbl_fg_count.config(text="前景patch数: —")
        app.lbl_pca_fg_status.config(text="⚠ 分割头未加载，将使用全图PCA")

    compute_sim(app)

    new_h, new_w = app.img_resized.shape[:2]
    app.lbl_filename.config( text=f"文件名: {os.path.basename(path)}")
    app.lbl_orig_size.config(text=f"原始尺寸: {app.orig_w}×{app.orig_h}")
    app.lbl_proc_size.config(text=f"处理尺寸: {new_w}×{new_h}  (SCALE={scale})")
    app.lbl_patches.config(  text=f"Patch网格: {app.w_patches}×{app.h_patches}")
    ch, cw = app.selected_patch
    app.lbl_selected.config( text=f"选中patch: ({ch}, {cw})")
    app.lbl_multi.config(    text="多点数量: 0")

    app.history = add_to_history(app.history, path)
    app.history_listbox.delete(0, tk.END)
    for _, name in app.history:
        app.history_listbox.insert(tk.END, name)
    app.history_listbox.selection_clear(0, tk.END)
    app.history_listbox.selection_set(0)

    refresh_left(app)
    refresh_right(app)
    app._set_buttons_state('normal')

    app.status_var.set(
        f"已加载: {os.path.basename(path)}  |  "
        f"SCALE={scale}  |  {app.w_patches}×{app.h_patches} patches  |  "
        f"原始: {app.orig_w}×{app.orig_h}"
    )
