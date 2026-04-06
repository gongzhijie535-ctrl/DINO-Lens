# 🦖 DINO-Lens: Visual Feature Explorer & Segmenter

<div align="center">

**[English](README.md) | [简体中文](README_zh.md)**

<br/>

[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![DINOv3](https://img.shields.io/badge/Model-DINOv3-blue?style=for-the-badge)](https://github.com/facebookresearch/dinov3)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=for-the-badge)]()

<br/>

**基于 DINOv3 的轻量级、交互式视觉特征分析与少样本分割工具**

<br/>

*一个让你真正"看见" Vision Foundation Model 在想什么的工具。*

> 🚧 **本项目持续迭代中** — 更多功能正在开发，欢迎 Star 关注进度！

</div>

---

## 🎬 效果演示 (Demo)

<div align="center">

![Demo](demo.gif)

*左键点击 → 实时余弦相似度热力图 ｜ PCA 语义可视化 ｜ 10张图训练的前景分割*

</div>

---

## 💡 项目亮点 (Highlights)

> 这不只是一个可视化工具——它是一个关于 **"强大特征究竟能做什么"** 的实验。
>
> 本项目的前景分割头是一个**仅有一层的超轻量逻辑回归模型**，训练数据**仅仅 10 张图片**。
> 没有微调，没有复杂架构，却能实现高质量的前景提取。
>
> **这不是分类器的功劳，这是 DINOv3 特征本身的力量。**

---

## ✨ 核心特性 (Features)

与枯燥的命令行脚本不同，本项目提供了一个开箱即用的桌面级 GUI，让你能够直观地探索大视觉模型（Vision Foundation Models）的底层特征：

- **🖱️ 交互式相似度分析：** 鼠标点击原图任意位置，实时渲染 DINOv3 提取的余弦相似度热力图，支持右键"多点平均"特征提取。
- **🧠 实时 PCA 语义可视化：** 将高维 Patch Token 降维至 RGB 空间，直观展示模型对图像语义的无监督聚类能力（支持仅对前景进行 PCA）。
- **🎭 极简且强大的前景分割：** 单层逻辑回归 + 10 张训练图，零微调实现高质量少样本前景提取，直接验证 DINOv3 特征的语义表征上限。
- **⚡ 高效推理架构：** 多线程异步加载与特征缓存机制，确保 GUI 交互丝滑不卡顿。

---

## 🛠️ 安装指南 (Installation)

### 1. 克隆仓库并安装依赖

建议使用 Python 3.9+，并确保已安装支持 CUDA 的 PyTorch（CPU 亦可运行，但推荐 GPU 以获得实时体验）。

```bash
git clone https://github.com/gongzhijie535-ctrl/DINO-Lens.git
cd DINO-Lens
pip install -r requirements.txt
```

同时克隆 DINOv3 官方源码至项目目录：

```bash
git clone https://github.com/facebookresearch/dinov3.git
```

### 2. 下载模型权重

DINOv3 官方权重需向 Meta AI 申请访问权限，请前往官方仓库提交申请：

👉 https://github.com/facebookresearch/dinov3

申请通过后会收到邮件，包含所有权重的下载链接。本项目使用 **ViT-B/16 distilled（LVD-1689M）** 版本。

下载后将文件重命名并放入指定路径：

```
dinov3/weights/dinov3_vitb16_pretrain_lvd1689m-73cec8be.pth
```

### 3. 下载分割分类器（可选）

为启用前景分割功能，需下载预训练的极简分类器（单层逻辑回归，仅用 10 张图训练）：

👉 [GitHub Releases v1.0](https://github.com/gongzhijie535-ctrl/DINO-Lens/releases/tag/v1.0)

下载后放入以下路径：

```
checkpoints/clf.pkl
checkpoints/scaler.pkl
```

---

## 🚀 快速开始 (Quick Start)

环境配置完成后，一行命令启动交互式界面：

```bash
python main.py
```

**操作指南：**

1. 点击左上角 **"打开图片"** 加载本地图像。
2. 在左侧原图区域，**左键单击** 选择主特征点，**右键单击** 添加多个特征点（用于多点平均）。
3. 在右侧控制面板切换 **相似度 / PCA / 前景** 模式，实时观察特征变化。

---

## 📅 未来规划 (Roadmap)

本项目将持续维护并更新，致力于打造最好用的视觉大模型特征探索工具。

- [ ] 引入更多下游任务的轻量级验证模块（如深度估计、边缘检测等）
- [ ] 支持导入自定义的轻量级分类器权重
- [ ] 进一步优化 GUI 交互体验，支持批量图像特征分析
- [ ] 探索与其他视觉基础模型（如 SAM 等）的联动

*(欢迎提交 Issue 或 Pull Request 参与共建！)*

---

## 📂 目录结构 (Project Structure)

```text
DINO-Lens/
├── core/
│   ├── config.py       # 全局路径、颜色映射与参数配置
│   └── model.py        # DINOv3 模型加载、特征提取与 PCA 核心逻辑
├── utils/
│   └── file_utils.py   # 文件扫描与历史记录管理
├── dinov3/             # DINOv3 官方源码（需自行 clone）
│   └── weights/        # 存放官方 .pth 权重（已加入 .gitignore）
├── checkpoints/        # 存放 clf.pkl 和 scaler.pkl（已加入 .gitignore）
├── main.py             # GUI 主程序入口
└── requirements.txt    # 依赖清单
```

---

## 🤝 致谢 (Acknowledgements)

- 核心视觉特征提取基于 Meta AI 的出色工作：[facebookresearch/dinov3](https://github.com/facebookresearch/dinov3)
- 感谢开源社区提供的优秀视觉处理库：OpenCV、PIL、Tkinter

如果这个项目对你的研究或工作有帮助，欢迎点亮右上角的 **Star ⭐**！
