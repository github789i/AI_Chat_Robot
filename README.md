<div align="center">

# 🤖 SmartChat Desktop / 基于百度 API 的桌面智能助手

**基于 PyQt5 打造的现代化桌面 AI 对话客户端，支持多线程后台处理与本地历史记录管理**

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-PyQt5-green.svg?style=flat-square&logo=qt)](https://pypi.org/project/PyQt5/)
[![API Provider](https://img.shields.io/badge/API-Baidu%20Qianfan-red.svg?style=flat-square)](https://cloud.baidu.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

[✨ 核心特性](#-核心特性) • [🖼️ 界面效果](#️-界面效果演示) • [📦 快速上手](#-快速上手) • [🔑 API 配置](#-百度-api-密钥配置说明) • [🗺️ 路线图](#️-未来规划-roadmap)

</div>

---

## 📌 项目简介

**SmartChat Desktop** 是一款轻量级、开箱即用的桌面端 AI 对话软件。项目采用 **PyQt5** 构建原生 GUI 界面，对接**百度文心一言/千帆大模型 API**，并结合 Python 多线程机制实现了流畅无卡顿的交互体验。

无论你是想拥有一个桌面随身 AI 助手，还是想学习 PyQt5 与 AI API 结合的完整项目开发，本项目都能为你提供清晰、规范的代码实现。

---

## ✨ 核心特性

- 💬 **智能 AI 对话**：无缝对接百度大模型 API，响应迅速，支持连续多轮对话。
- 🎨 **优雅图形界面**：基于 PyQt5 设计，界面布局清晰，符合常规桌面聊天软件的使用习惯。
- ⚡ **流畅后台处理**：引入 `QThread` 多线程异步处理网络请求，彻底告别界面卡死与未响应。
- 💾 **历史记录持久化**：自动保存对话上下文与本地历史记录，支持随时翻阅历史聊天的精彩内容。

---

## 🖼️ 界面效果演示

以下为软件实际运行与交互效果图：

<p align="center">
  <img width="600" alt="SmartChat Desktop Preview" src="https://github.com/user-attachments/assets/04a2b790-b7a7-4e52-a40b-1f9eb4879124" />
</p>

---

## 🔑 百度 API 密钥配置说明

> ⚠️ **使用前必读**：本项目依赖百度千帆大模型 / 文心一言开放平台的 API。运行前请务必配置你自己的 API Key。

1. 登录 [百度智能云千帆大模型平台](https://cloud.baidu.com/product/wenxinworkshop) 获取账号。
2. 进入控制台，创建应用并获取 `API Key` 与 `Secret Key`。
3. 在项目代码中找到 API 配置文件或变量处（例如 `config.py` 或主程序顶部），填入你申请到的密钥：

```python
# 示例配置项
BAIDU_API_KEY = "Your_Baidu_API_Key"
BAIDU_SECRET_KEY = "Your_Baidu_Secret_Key"
```

---

## 📦 快速上手

### 1. 环境要求 (Prerequisites)

- **Python** 3.8 及以上版本
- 操作系统：Windows / macOS / Linux

### 2. 克隆仓库与安装依赖

```bash
# 克隆本项目
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# (可选) 创建并激活虚拟环境
python -m venv venv
# Windows 激活命令:
venv\Scripts\activate
# macOS/Linux 激活命令:
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt
```

*(若无 `requirements.txt`，可使用以下指令手动安装依赖)*

```bash
pip install PyQt5 requests
```

### 3. 运行项目

```bash
python main.py
```

---

## 🛠️ 技术栈与架构设计

| 模块 | 使用技术 | 说明 |
| :--- | :--- | :--- |
| **GUI 渲染** | PyQt5 | 构建应用主窗口、聊天列表与输入框 |
| **网络与 API** | Requests / Baidu SDK | 负责与百度大模型服务端进行 HTTP/REST 交互 |
| **并发处理** | QThread | 将耗时的 API 调用放入后台子线程，保证 UI 界面流畅 |
| **数据存储** | JSON / SQLite | 实现本地聊天历史记录的读取与持久化存储 |

---

## 🗺️ 未来规划 (Roadmap)

- [x] 基于 PyQt5 实现基础聊天 UI 界面
- [x] 集成百度 API 基础对话功能
- [x] 优化多线程异步响应机制，消除卡顿
- [x] 支持本地历史记录保存
- [ ] 增加流式传输（Streaming Response）打字机效果
- [ ] 支持多种系统主题（深色模式 / 浅色模式）切换
- [ ] 增加快捷键发送消息 (如 `Enter` 发送, `Ctrl+Enter` 换行)
- [ ] 导出对话记录为 Markdown / PDF 格式

---

## 🤝 贡献指南

非常欢迎你提交 Issue 或 Pull Request 来改进这个项目！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 License & 致谢

本项目采用 [MIT License](LICENSE) 开源协议。

感谢以下项目及平台提供的支持：
- [PyQt5](https://pypi.org/project/PyQt5/) - 强大的 Python 桌面 GUI 框架
- [百度智能云千帆大模型平台](https://cloud.baidu.com/) - 提供稳定的大模型 API 支持
```
