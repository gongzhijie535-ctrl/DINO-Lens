import numpy as np
from core.model import compute_pca_rgb


def compute_sim(app):
    if app.multi_mode.get() and app.multi_patches:
        all_patches = [app.selected_patch] + app.multi_patches
        vecs = [app.tokens_normed[ch * app.w_patches + cw]
                for ch, cw in all_patches]
        avg_vec = np.mean(vecs, axis=0)
        avg_vec = avg_vec / (np.linalg.norm(avg_vec) + 1e-8)
        app.sim_map = (app.tokens_normed @ avg_vec
                       ).reshape(app.h_patches, app.w_patches)
    else:
        ch, cw = app.selected_patch
        idx = ch * app.w_patches + cw
        app.sim_map = (app.tokens_normed @ app.tokens_normed[idx]
                       ).reshape(app.h_patches, app.w_patches)


def get_pca_rgb(app):
    if app.pca_fg_only.get() and app.fg_prob_map is not None:
        thresh = round(app.pca_fg_threshold.get(), 2)
        if thresh not in app.pca_cache['fg']:
            app.status_var.set("正在计算 PCA 降维（前景）...")
            app.master.update_idletasks()
            fg = app.fg_prob_map > thresh
            app.pca_cache['fg'][thresh] = compute_pca_rgb(
                app.patch_tokens_raw, app.h_patches, app.w_patches,
                fg_mask=fg)
            app.status_var.set("PCA 计算完成")
        return app.pca_cache['fg'][thresh]
    else:
        if app.pca_cache['full'] is None:
            app.status_var.set("正在计算 PCA 降维（全图）...")
            app.master.update_idletasks()
            app.pca_cache['full'] = compute_pca_rgb(
                app.patch_tokens_raw, app.h_patches, app.w_patches,
                fg_mask=None)
            app.status_var.set("PCA 计算完成")
        return app.pca_cache['full']
