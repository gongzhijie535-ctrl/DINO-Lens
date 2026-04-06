\# 🦖 DINO-Lens: Visual Feature Explorer \& Segmenter



<div align="center">



\[English](README.md) | \[简体中文](README\_zh.md)



<br/>



\[!\[PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge\&logo=PyTorch\&logoColor=white)](https://pytorch.org/)

\[!\[DINOv3](https://img.shields.io/badge/Model-DINOv3-blue?style=for-the-badge)](https://github.com/facebookresearch/dinov3)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

\[!\[Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=for-the-badge)]()



<br/>



\*\*A lightweight, interactive visual feature analysis and few-shot segmentation tool based on DINOv3.\*\*



<br/>



\*A tool that lets you truly "see" what Vision Foundation Models are thinking.\*



> 🚧 \*\*Work in Progress\*\* — More features are under active development. Star to stay tuned!



</div>



\---



\## 🎬 Demo



<div align="center">



!\[Demo](demo.gif)



\*Left Click → Real-time Cosine Similarity Heatmap | PCA Semantic Visualization | Foreground Segmentation trained on 10 images\*



</div>



\---



\## 💡 Highlights



> This is not just a visualization tool—it's an experiment exploring \*\*"what powerful features can actually do."\*\*

>

> The foreground segmentation head in this project is an \*\*ultra-lightweight single-layer logistic regression model\*\*, trained on \*\*only 10 images\*\*. 

> No fine-tuning, no complex architectures, yet it achieves high-quality foreground extraction.

>

> \*\*This is not the classifier doing the heavy lifting—this is the raw power of DINOv3 features.\*\*



\---



\## ✨ Features



Unlike tedious command-line scripts, this project provides an out-of-the-box desktop GUI, allowing you to intuitively explore the underlying features of Vision Foundation Models:



\- \*\*🖱️ Interactive Similarity Analysis:\*\* Click anywhere on the original image to render the cosine similarity heatmap extracted by DINOv3 in real-time. Right-click is supported for "multi-point average" feature extraction.

\- \*\*🧠 Real-time PCA Semantic Visualization:\*\* Reduce high-dimensional Patch Tokens to RGB space, intuitively demonstrating the model's unsupervised clustering ability for image semantics (supports PCA on foreground only).

\- \*\*🎭 Minimalist \& Powerful Foreground Segmentation:\*\* Single-layer logistic regression + 10 training images. Achieve high-quality few-shot foreground extraction with zero fine-tuning, directly validating the semantic representation limit of DINOv3 features.

\- \*\*⚡ Efficient Inference Architecture:\*\* Multi-threaded asynchronous loading and feature caching mechanisms ensure a silky-smooth GUI interaction without freezing.



\---



\## 🛠️ Installation



\### 1. Clone the repository and install dependencies



Python 3.9+ is recommended. Ensure you have PyTorch with CUDA support installed (CPU works, but GPU is highly recommended for real-time experience).



```bash

git clone https://github.com/gongzhijie535-ctrl/DINO-Lens.git

cd DINO-Lens

pip install -r requirements.txt

```



Clone the official DINOv3 repository into the project directory:



```bash

git clone https://github.com/facebookresearch/dinov3.git

```



\### 2. Download Model Weights



DINOv3 official weights require access permission from Meta AI. Please submit a request at their official repository:



👉 https://github.com/facebookresearch/dinov3



Upon approval, you will receive an email with download links. This project uses the \*\*ViT-B/16 distilled (LVD-1689M)\*\* version.



After downloading, rename the file and place it in the specified path:



```

dinov3/weights/dinov3\_vitb16\_pretrain\_lvd1689m-73cec8be.pth

```



\### 3. Download Segmentation Classifier (Optional)



To enable the foreground segmentation feature, download our pre-trained minimalist classifier (trained on only 10 images):



👉 \[GitHub Releases v1.0](https://github.com/gongzhijie535-ctrl/DINO-Lens/releases/tag/v1.0)



Place the downloaded files in the following paths:



```

checkpoints/clf.pkl

checkpoints/scaler.pkl

```



\---



\## 🚀 Quick Start



Once the environment is configured, launch the interactive interface with a single command:



```bash

python main.py

```



\*\*Operation Guide:\*\*

1\. Click \*\*"Open Image"\*\* in the top left corner to load a local image.

2\. In the original image area on the left, \*\*Left-click\*\* to select the main feature point, and \*\*Right-click\*\* to add multiple feature points (for multi-point averaging).

3\. Switch between \*\*Similarity / PCA / Foreground\*\* modes in the right control panel to observe feature changes in real-time.



\---



\## 📅 Roadmap



This project will be continuously maintained and updated, aiming to build the best visual foundation model feature exploration tool.



\- \[ ] Introduce lightweight validation modules for more downstream tasks (e.g., depth estimation, edge detection).

\- \[ ] Support importing custom lightweight classifier weights.

\- \[ ] Further optimize GUI interaction and support batch image feature analysis.

\- \[ ] Explore integration with other vision foundation models (e.g., SAM).



\*(Issues and Pull Requests are welcome!)\*



\---



\## 📂 Project Structure



```text

DINO-Lens/

├── core/

│   ├── config.py       # Global paths, colormaps, and parameter configs

│   └── model.py        # DINOv3 loading, feature extraction, and PCA logic

├── utils/

│   └── file\_utils.py   # File scanning and history management

├── dinov3/             # Official DINOv3 source code (needs to be cloned)

│   └── weights/        # Official .pth weights (added to .gitignore)

├── checkpoints/        # clf.pkl and scaler.pkl (added to .gitignore)

├── main.py             # GUI main entry point

└── requirements.txt    # Dependencies list

```



\---



\## 🤝 Acknowledgements



\- Core visual feature extraction is based on the excellent work by Meta AI: \[facebookresearch/dinov3](https://github.com/facebookresearch/dinov3)

\- Thanks to the open-source community for excellent vision processing libraries: OpenCV, PIL, Tkinter.



If this project helps your research or work, please consider giving it a \*\*Star ⭐\*\*!



