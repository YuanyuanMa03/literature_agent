# 🔬 Literature Agent System

<div align="center">

**智能文献分析系统 - 自动筛选、深度分析和总结学术文献**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[功能特性](#-功能特性) •
[快速开始](#-快速开始) •
[使用指南](#-使用指南) •
[文档](#-文档) •
[贡献](#-贡献)

</div>

---

## 📋 目录

- [功能特性](#-功能特性)
- [系统架构](#-系统架构)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [项目结构](#-项目结构)
- [配置说明](#-配置说明)
- [示例](#-示例)
- [文档](#-文档)
- [常见问题](#-常见问题)
- [贡献](#-贡献)
- [许可证](#-许可证)

---

## ✨ 功能特性

### 数据预处理阶段（新增）

- 🔄 **智能数据预处理**：自动处理Web of Science导出的原始文献数据
- 📊 **关键信息提取**：提取作者、年份、标题、摘要、DOI等核心字段
- 🧹 **数据清理标准化**：去重、格式标准化、缺失值处理
- 📈 **统计分析**：生成详细的数据质量报告和统计信息
- 💾 **多格式输出**：同时生成CSV和Excel格式，保持中英文对照
- 🔍 **自动检测**：智能识别WOS分段文件并自动合并

### 第一阶段：智能筛选与分析

- 📊 **智能筛选**：基于LLM自动判断文献相关性
- 🔍 **关键信息提取**：自动提取研究方法、数据、结论
- 📝 **结构化报告**：生成专业的Markdown研究报告
- 💾 **多格式支持**：支持CSV、Excel、RIS等格式
- 🔄 **断点续传**：支持中断后继续处理
- 📈 **实时进度**：显示处理进度和统计信息

### 第二阶段：PDF深度分析（可选）

- 📥 **智能下载**：集成多个合法数据源（Unpaywall、Semantic Scholar等）
- 🖼️ **OCR识别**：使用多模态LLM识别PDF内容
- 📊 **表格提取**：自动提取论文中的数据表格
- 🎨 **图表分析**：识别和分析论文图表
- 🔗 **数据集追踪**：提取Data Availability和数据集链接
- 📁 **批量处理**：支持批量PDF分析

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────┐
│                  Raw Input Data                      │
│  (WOS导出文件/Excel/CSV/分段文件)                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│        Stage 0: 数据预处理 (新增)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Data       │  │  Column      │  │  Data      │ │
│  │  Loading    │→ │  Mapping     │→ │  Cleaning  │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└─────────────────┬───────────────────────────────────┘
                  │ 标准化数据
                  ▼
┌─────────────────────────────────────────────────────┐
│            Stage 1: 智能筛选与分析                    │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Planning    │  │  Screening   │  │  Analysis  │ │
│  │   Agent     │→ │    Agent     │→ │   Agent    │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│                  │              │              │
│                  ▼              ▼              ▼
│              筛选结果        关键提取        深度分析
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│            Stage 2: 报告生成                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Report    │  │  Statistics  │  │  Summary   │ │
│  │   Agent     │→ │  Generation  │→ │  Export    │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                   Outputs                           │
│  • 预处理数据 (CSV/Excel)                            │
│  • 筛选结果 (Excel)                                  │
│  • 分析报告 (Markdown)                              │
│  • 深度分析结果 (Excel/JSON)                        │
│  • 统计报告和可视化                                  │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- pip包管理器
- （可选）poppler-utils（用于PDF处理）

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/literature_agent.git
cd literature_agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**macOS用户**（如果需要PDF处理）：
```bash
brew install poppler
```

**Ubuntu/Debian用户**：
```bash
sudo apt-get install poppler-utils
```

### 3. 配置API

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API信息：

```ini
# API配置
OPENAI_API_BASE=https://api.siliconflow.cn/v1
OPENAI_API_KEY=sk-your-api-key-here
LLM_MODEL=Qwen/Qwen3-Omni-30B-A3B-Instruct

# 可选：Unpaywall邮箱（用于下载开放获取文献）
UNPAYWALL_EMAIL=your@email.com
```

### 4. 准备数据

支持多种数据格式：
- **Web of Science导出文件**：支持分段文件（0-1000.xls, 1001-2000.xls等）
- **Excel/CSV文件**：包含标准文献元数据
- **必需字段**：标题、摘要（其他字段可选）

### 5. 运行

**方式一：完整流程（推荐）**
```bash
# 自动进行数据预处理 → 筛选 → 分析 → 报告生成
python main.py
```

**方式二：仅数据预处理**
```bash
# 独立运行数据预处理
python demo_data_preprocessing.py
```

**方式三：分步执行**
```bash
# 第一阶段：数据预处理 + 筛选与分析
python main.py

# 第二阶段：PDF深度分析（可选）
python main_stage2.py
```

**方式四：使用便捷函数**
```python
from agents.data_preprocessing_agent import preprocess_wos_data

# 快速预处理WOS数据
result = preprocess_wos_data(
    input_source="auto",  # 自动检测文件
    output_dir="data",
    output_filename="processed_literature.csv"
)
```

---

## 📖 使用指南

### 第一阶段：智能筛选与分析

1. **启动程序**
   ```bash
   python main.py
   ```

2. **选择运行模式**
   - 测试模式（10篇）- 快速验证系统
   - 小批量（50篇）- 中等规模处理
   - 完整模式 - 处理全部文献

3. **查看结果**
   - `data/results/literature_screening_results.xlsx` - 筛选结果
   - `data/results/literature_analysis_results.xlsx` - 分析结果
   - `data/results/literature_research_report.md` - 研究报告

### 第二阶段：PDF深度分析

1. **手动下载PDF**（推荐）
   - 通过校园网/VPN访问文献数据库
   - 下载通过筛选的文献PDF
   - 放入 `./pdfs/` 目录
   - 详见：[`docs/手动下载指南.md`](docs/手动下载指南.md)

2. **运行深度分析**
   ```bash
   python main_stage2.py
   ```

3. **查看结果**
   - `data/results/deep_analysis_results.xlsx` - 深度分析结果
   - `data/results/deep_analysis_results.json` - 详细JSON数据
   - `./pdf_images/` - PDF转换的图片

---

## 📁 项目结构

```
literature_agent/
├── README.md                    # 项目说明
├── LICENSE                      # 许可证
├── requirements.txt             # Python依赖
├── setup.sh                     # 快速安装脚本
├── .env.example                # 环境变量示例
├── .gitignore                  # Git忽略规则
│
├── agents/                     # Agent模块
│   ├── __init__.py
│   ├── data_preprocessing_agent.py  # 数据预处理Agent (新增)
│   ├── planning_agent.py       # 规划Agent
│   ├── screening_agent.py      # 文献筛选Agent
│   ├── analysis_agent.py       # 文献分析Agent
│   ├── report_agent.py         # 报告生成Agent
│   ├── deep_analysis_agent.py  # PDF深度分析Agent
│   └── pdf_download_agent.py   # PDF下载Agent
│
├── core/                       # 核心框架
│   ├── __init__.py
│   ├── agent.py                # Agent基类
│   ├── llm.py                  # LLM接口封装
│   ├── message.py              # 消息类
│   └── ...
│
├── tools/                      # 工具模块
│   ├── __init__.py
│   ├── screening_tool.py       # 筛选工具
│   ├── extraction_tool.py      # 信息提取工具
│   ├── pdf_download_tool.py    # PDF下载工具
│   ├── enhanced_pdf_download_tool.py  # 增强版下载工具
│   ├── pdf_process_tool.py     # PDF处理工具
│   ├── ocr_tool.py             # OCR识别工具
│   └── deep_analysis_tool.py   # 深度分析工具
│
├── docs/                       # 文档
│   ├── 快速开始_增强版下载.md
│   ├── 手动下载指南.md
│   ├── 文献下载方案汇总.md
│   └── 机构代理下载说明.md
│
├── examples/                   # 示例和测试
│   ├── check_proxy.py          # 代理检测脚本
│   ├── test_enhanced_download.py
│   └── test_institution_download.py
│
├── main.py                     # 主程序（完整流程）
├── main_stage2.py             # 第二阶段主程序
├── demo_data_preprocessing.py  # 数据预处理演示脚本
├── test_data_preprocessing.py  # 数据预处理测试脚本
│
└── data/                       # 数据目录（不提交到git）
    ├── pdfs/                   # PDF文件
    ├── pdf_images/             # PDF转图片
    ├── results/                # 分析结果
    └── cache/                  # 缓存文件
```

---

## ⚙️ 配置说明

### 支持的LLM API

系统支持所有OpenAI兼容的API，已测试：

| 平台 | API Base | 推荐模型 | 说明 |
|------|----------|---------|------|
| **硅基流动** | `https://api.siliconflow.cn/v1` | Qwen3-Omni-30B | ✅ 推荐（性价比高） |
| **DeepSeek** | `https://api.deepseek.com/v1` | deepseek-chat | 高质量分析 |
| **OpenAI** | `https://api.openai.com/v1` | gpt-4o-mini | 稳定可靠 |
| **Gemini** | 通过代理 | gemini-pro | 需配置代理 |

### 环境变量

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `OPENAI_API_BASE` | ✅ | API基础URL | `https://api.siliconflow.cn/v1` |
| `OPENAI_API_KEY` | ✅ | API密钥 | `sk-xxxxx` |
| `LLM_MODEL` | ✅ | 模型名称 | `Qwen/Qwen3-Omni-30B-A3B-Instruct` |
| `LLM_TEMPERATURE` | ❌ | 温度参数 | `0.1` (默认) |
| `LLM_MAX_TOKENS` | ❌ | 最大token数 | `2000` (默认) |
| `UNPAYWALL_EMAIL` | ❌ | Unpaywall邮箱 | `your@email.com` |

---

## 💡 示例

### 示例1：处理Web of Science导出的文献

```bash
# 1. 从WOS导出CSV文件
# 2. 放入项目目录
# 3. 运行程序
python main.py

# 选择模式 -> 等待处理完成 -> 查看结果
```

### 示例2：深度分析特定文献

```bash
# 1. 运行第一阶段筛选
python main.py

# 2. 查看筛选结果，手动下载PDF
# 3. 将PDF放入 ./pdfs/ 目录
# 4. 运行深度分析
python main_stage2.py
```

### 示例3：自定义筛选标准

编辑 `tools/screening_tool.py`：

```python
screening_prompt = """
请判断以下文献是否包含关于【你的研究主题】的数据。

评判标准：
1. 必须包含实验数据或调查数据
2. 研究对象为【特定对象】
3. 研究方法包括【特定方法】
...
"""
```

---

## 📚 文档

详细文档请查看 `docs/` 目录：

- [**快速开始 - 增强版下载**](docs/快速开始_增强版下载.md) - 多源PDF下载方案
- [**手动下载指南**](docs/手动下载指南.md) - 通过校园网手动下载PDF的步骤
- [**文献下载方案汇总**](docs/文献下载方案汇总.md) - 所有可用的文献下载方法
- [**机构代理下载说明**](docs/机构代理下载说明.md) - 配置校园网代理下载

---

## ❓ 常见问题

<details>
<summary><b>Q: API限流怎么办？</b></summary>

A: 系统已内置延迟控制。如仍超限：
1. 减少批量大小（选择测试模式）
2. 增加延迟时间（修改代码中的delay参数）
3. 升级API套餐或切换到其他API
</details>

<details>
<summary><b>Q: 支持哪些语言的文献？</b></summary>

A: 主要支持英文文献。中文文献的识别效果取决于所用LLM模型，使用Qwen等中文模型效果更好。
</details>

<details>
<summary><b>Q: 如何提高筛选准确率？</b></summary>

A: 
1. 使用更强大的模型（如GPT-4）
2. 在prompt中提供更详细的筛选标准
3. 提供示例文献作为参考
4. 增加温度参数以获得更多样的判断
</details>

<details>
<summary><b>Q: PDF下载失败怎么办？</b></summary>

A: 
1. 优先使用手动下载（通过校园网最稳定）
2. 参考 `docs/文献下载方案汇总.md` 了解多种下载方法
3. 申请出版商TDM API（Elsevier、Wiley等）
4. 联系作者获取PDF副本
</details>

<details>
<summary><b>Q: 如何处理大量文献？</b></summary>

A:
1. 使用断点续传功能（系统会自动保存进度）
2. 分批处理（先50篇，再50篇...）
3. 优化筛选标准，减少需要深度分析的文献数量
4. 使用多个API Key轮换使用
</details>

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 开发指南

- 遵循PEP 8代码风格
- 添加适当的注释和文档字符串
- 更新相关文档
- 添加测试用例

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- OpenAI、DeepSeek、硅基流动等提供优秀的LLM API
- 所有贡献者和使用者

---

## 📮 联系方式

- 提交Issue：[GitHub Issues](https://github.com/YuanyuanMa/literature_agent/issues)
- 邮件：mayuanyuan813@qq.com、yym290552@gmail.com

---

<div align="center">
**如果这个项目对你有帮助，请给个⭐️Star支持一下！**

Made with ❤️ by Literature Agent Team

</div>
