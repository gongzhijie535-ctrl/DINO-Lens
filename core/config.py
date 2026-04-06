import cv2
from pathlib import Path

# 项目根目录（config.py 在 core/ 里，所以往上一级）
BASE_DIR = Path(__file__).parent.parent

# 模型路径（别人 clone 后把文件放这里就行）
REPO_DIR    = BASE_DIR / "dinov3"
WEIGHTS     = BASE_DIR / "dinov3" / "weights" / "dinov3_vitb16_pretrain_lvd1689m-73cec8be.pth"
CLF_PATH    = BASE_DIR / "checkpoints" / "clf.pkl"
SCALER_PATH = BASE_DIR / "checkpoints" / "scaler.pkl"


PATCH_SIZE    = 16
IMAGE_SIZE    = 672
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]
IMG_EXTS      = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
HISTORY_MAX   = 12

COLORMAPS = {
    'viridis': cv2.COLORMAP_VIRIDIS,
    'jet'    : cv2.COLORMAP_JET,
    'hot'    : cv2.COLORMAP_HOT,
    'cool'   : cv2.COLORMAP_COOL,
    'magma'  : cv2.COLORMAP_MAGMA,
}

# 确保所有路径都是字符串
REPO_DIR    = str(REPO_DIR)
WEIGHTS     = str(WEIGHTS)
CLF_PATH    = str(CLF_PATH)
SCALER_PATH = str(SCALER_PATH)
