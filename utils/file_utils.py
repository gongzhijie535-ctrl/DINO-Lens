import os
from core.config import IMG_EXTS, HISTORY_MAX


def scan_folder(folder):
    """扫描文件夹，返回排序后的图片路径列表"""
    return sorted([
        os.path.join(folder, f) for f in os.listdir(folder)
        if os.path.splitext(f)[1].lower() in IMG_EXTS
    ])


def add_to_history(history, path):
    """添加路径到历史记录，去重，限制最大条数，返回新列表"""
    history = [(p, n) for p, n in history if p != path]
    history.insert(0, (path, os.path.basename(path)))
    return history[:HISTORY_MAX]
