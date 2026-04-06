\# DINOv3 Test



基于 DINOv3 的前景分割与特征提取项目。



\## 环境要求



\- Python 3.9+

\- CUDA（推荐，CPU 也可运行）



\## 安装步骤



1\. 克隆仓库



git clone https://github.com/gongzhijie535-ctrl/dinov3\_test.git

cd dinov3\_test



2\. 安装依赖



pip install -r requirements.txt



3\. 下载权重文件，放入以下路径



dinov3/weights/dinov3\_vitb16\_pretrain\_lvd1689m-73cec8be.pth



4\. 将训练好的分类器放入以下路径



checkpoints/clf.pkl

checkpoints/scaler.pkl



\## 运行



python main.py



\## 目录结构



dinov3\_test/

├── core/

│   ├── config.py       # 路径与参数配置

│   ├── model.py        # 模型加载

│   └── ...

├── dinov3/             # DINOv3 源码（需自行 clone）

│   └── weights/        # 权重文件（需自行下载）

├── checkpoints/        # clf.pkl 和 scaler.pkl（需自行提供）

├── main.py

├── requirements.txt

└── .gitignore



\## 注意事项



\- `dinov3/weights/` 和 `checkpoints/` 已加入 .gitignore，不会上传到 GitHub

\- 权重文件请从 Meta AI 官方渠道下载

## 权重下载

DINOv3 官方权重请从 Meta AI 下载：
https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_pretrain.pth

下载后命名为 `dinov3_vitb16_pretrain_lvd1689m-73cec8be.pth`，放入 `dinov3/weights/`

## 分类器下载

clf.pkl 和 scaler.pkl 请从 Releases 下载：
https://github.com/gongzhijie535-ctrl/dinov3_test/releases/tag/v1.0

下载后放入 `checkpoints/`


