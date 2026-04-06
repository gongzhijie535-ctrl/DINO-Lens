import numpy as np
import cv2
from PIL import Image, ImageTk

from core.config import PATCH_SIZE, COLORMAPS
from core.model  import sim_to_heatmap
from ui.logic.compute import get_pca_rgb


def fit_to_canvas(app, canvas, img_rgb):
    cw = canvas.winfo_width()
    ch = canvas.winfo_height()
    if cw < 10 or ch < 10:
        cw = ch = app.CANVAS_MAX
    ih, iw = img_rgb.shape[:2]
    ratio   = min(cw / iw, ch / ih)
    disp_w  = int(iw * ratio)
    disp_h  = int(ih * ratio)
    resized = cv2.resize(img_rgb, (disp_w, disp_h), interpolation=cv2.INTER_AREA)
    return ImageTk.PhotoImage(Image.fromarray(resized)), disp_w, disp_h, ratio


def refresh_left(app, *_):
    if app.img_resized is None:
        return
    img = app.img_resized.copy()

    if app.fg_show_on_left.get() and app.fg_mask is not None:
        ih, iw = img.shape[:2]
        mask_up = cv2.resize(
            app.fg_mask.astype(np.uint8) * 255,
            (iw, ih), interpolation=cv2.INTER_NEAREST)
        green          = np.zeros_like(img)
        green[:, :, 1] = mask_up
        img = cv2.addWeighted(img, 1.0, green, 0.35, 0)

    if app.show_grid.get():
        h, w = img.shape[:2]
        for i in range(1, app.w_patches):
            cv2.line(img, (i*PATCH_SIZE, 0), (i*PATCH_SIZE, h), (80, 80, 220), 1)
        for j in range(1, app.h_patches):
            cv2.line(img, (0, j*PATCH_SIZE), (w, j*PATCH_SIZE), (80, 80, 220), 1)

    for ch, cw in app.multi_patches:
        x0, y0 = cw*PATCH_SIZE, ch*PATCH_SIZE
        cv2.rectangle(img, (x0, y0), (x0+PATCH_SIZE, y0+PATCH_SIZE), (0, 120, 255), 2)

    if app.selected_patch:
        ch, cw = app.selected_patch
        x0, y0 = cw*PATCH_SIZE, ch*PATCH_SIZE
        cv2.rectangle(img, (x0, y0), (x0+PATCH_SIZE, y0+PATCH_SIZE), (255, 60, 60), 2)

    photo, dw, dh, _ = fit_to_canvas(app, app.canvas_left, img)
    cw_c  = app.canvas_left.winfo_width()
    ch_c  = app.canvas_left.winfo_height()
    x_off = (cw_c - dw) // 2
    y_off = (ch_c - dh) // 2
    app.canvas_left.delete('all')
    app.canvas_left.create_image(x_off, y_off, anchor='nw', image=photo)
    app.canvas_left.image = photo
    app._left_offset = (x_off, y_off)
    app._left_ratio  = dw / app.img_resized.shape[1]


def refresh_right(app, *_):
    if app.img_resized is None:
        return
    mode   = app.right_mode.get()
    ih, iw = app.img_resized.shape[:2]

    if mode == 'pca':
        label = "PCA 语义图（仅前景）" if app.pca_fg_only.get() else "PCA 语义图（全图）"
        app.right_panel_label.config(text=label)
        pca_map = get_pca_rgb(app)
        display = cv2.resize(pca_map, (iw, ih), interpolation=cv2.INTER_NEAREST)
        if app.pca_show_overlay.get():
            alpha   = app.pca_overlay_alpha.get()
            display = cv2.addWeighted(app.img_resized, 1 - alpha, display, alpha, 0)

    elif mode == 'fg':
        app.right_panel_label.config(text="前景概率图")
        if app.fg_prob_map is None:
            return
        thresh   = app.fg_threshold.get()
        prob_u8  = (app.fg_prob_map * 255).astype(np.uint8)
        heat_bgr = cv2.applyColorMap(prob_u8, COLORMAPS[app.fg_cmap_var.get()])
        heat_up  = cv2.resize(heat_bgr, (iw, ih), interpolation=cv2.INTER_NEAREST)
        display  = cv2.cvtColor(heat_up, cv2.COLOR_BGR2RGB)

        mask_up  = cv2.resize(
            (app.fg_prob_map < thresh).astype(np.uint8),
            (iw, ih), interpolation=cv2.INTER_NEAREST).astype(bool)
        alpha_ch = np.where(mask_up, 0.35, 1.0).astype(np.float32)
        for c in range(3):
            display[:, :, c] = (display[:, :, c] * alpha_ch).astype(np.uint8)

        if app.fg_show_overlay.get():
            alpha   = app.fg_overlay_alpha.get()
            display = cv2.addWeighted(app.img_resized, 1 - alpha, display, alpha, 0)

    else:
        if app.sim_map is None:
            return
        app.right_panel_label.config(text="余弦相似度热力图")
        sim  = app.sim_map.copy()
        mask = sim < app.threshold_val.get() if app.use_threshold.get() else None

        heatmap_bgr = sim_to_heatmap(sim, app.cmap_var.get())
        heatmap_up  = cv2.resize(heatmap_bgr, (iw, ih), interpolation=cv2.INTER_NEAREST)
        display     = cv2.cvtColor(heatmap_up, cv2.COLOR_BGR2RGB)

        if mask is not None:
            mask_up = cv2.resize(
                mask.astype(np.uint8), (iw, ih),
                interpolation=cv2.INTER_NEAREST).astype(bool)
            display[mask_up] = 0

        if app.sim_show_overlay.get():
            alpha   = app.sim_overlay_alpha.get()
            display = cv2.addWeighted(app.img_resized, 1 - alpha, display, alpha, 0)

        if app.use_topk.get():
            k    = app.topk_val.get()
            flat = app.sim_map.flatten().copy()
            if app.selected_patch:
                sch, scw = app.selected_patch
                flat[sch * app.w_patches + scw] = -999
            for idx in np.argsort(flat)[-k:]:
                tj, ti = idx % app.w_patches, idx // app.w_patches
                cv2.rectangle(display,
                              (tj*PATCH_SIZE, ti*PATCH_SIZE),
                              (tj*PATCH_SIZE+PATCH_SIZE, ti*PATCH_SIZE+PATCH_SIZE),
                              (0, 255, 80), 1)

        if app.selected_patch:
            ch, cw = app.selected_patch
            cv2.drawMarker(display,
                           (cw*PATCH_SIZE + PATCH_SIZE//2,
                            ch*PATCH_SIZE + PATCH_SIZE//2),
                           (255, 255, 255), cv2.MARKER_CROSS, 16, 2)

    photo, dw, dh, _ = fit_to_canvas(app, app.canvas_right, display)
    cw_c  = app.canvas_right.winfo_width()
    ch_c  = app.canvas_right.winfo_height()
    x_off = (cw_c - dw) // 2
    y_off = (ch_c - dh) // 2
    app.canvas_right.delete('all')
    app.canvas_right.create_image(x_off, y_off, anchor='nw', image=photo)
    app.canvas_right.image = photo
