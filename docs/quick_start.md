# 🚀 快速入门指南

## 📋 目录
- [安装指南](#安装指南)
- [快速开始](#快速开始)
- [使用示例](#使用示例)
- [常见问题](#常见问题)

---

## 🔧 安装指南

### 方式一：自动安装（推荐）
```bash
# 克隆项目
git clone https://github.com/yourusername/literature_agent.git
cd literature_agent

# 运行安装脚本
chmod +x setup.sh
./setup.sh
```

### 方式二：手动安装
```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入API信息
```

### 方式三：pip安装
```bash
# 从源码安装
pip install -e .

# 或从PyPI安装（如果已发布）
pip install literature-agent-system
```

---

## 🚀 快速开始

### 1. 配置API
编辑`.env`文件：
```env
# API配置
OPENAI_API_BASE=https://api.siliconflow.cn/v1
OPENAI_API_KEY=your-api-key-here
LLM_MODEL=Qwen/Qwen3-Omni-30B-A3B-Instruct
```

### 2. 准备数据
支持的文件格式：
- Web of Science导出文件（分段文件）
- Excel文件（.xlsx, .xls）
- CSV文件

### 3. 运行程序
```bash
# 完整流程（推荐）
python main.py

# 仅数据预处理
python demo_data_preprocessing.py

# PDF深度分析
python main_stage2.py
```

---

## 💡 使用示例

### 示例1：处理WOS数据
```python
from agents.data_preprocessing_agent import preprocess_wos_data

# 自动检测并处理WOS分段文件
result = preprocess_wos_data(
    input_source="auto",
    output_dir="data",
    output_filename="processed_literature.csv"
)

if result["success"]:
    print(f"处理成功: {result['total_records']} 篇文献")
    print(f"输出文件: {result['output_file']}")
```

### 示例2：完整分析流程
```python
from main import LiteratureResearchSystem

# 创建系统实例
system = LiteratureResearchSystem()

# 运行完整流程
df, report = system.run_research(
    research_topic="土壤有机碳饱和机制",
    test_mode=True,  # 测试模式，只处理10篇
    test_size=10,
    analyze_top=5
)

print(f"分析完成，处理了 {len(df)} 篇文献")
```

### 示例3：自定义筛选标准
```python
from agents.screening_agent import LiteratureScreeningAgent
from core.llm import LiteratureLLM

# 创建LLM和Agent
llm = LiteratureLLM()
agent = LiteratureScreeningAgent(llm)

# 自定义筛选提示
custom_prompt = """
请判断以下文献是否包含关于【气候变化对农业影响】的数据。

评判标准：
1. 必须包含实验数据或调查数据
2. 研究对象为农业系统
3. 研究方法包括定量分析
"""

# 运行筛选
df_filtered = agent.run(df, custom_prompt=custom_prompt)
```

### 示例4：批量处理PDF
```python
from agents.deep_analysis_agent import DeepAnalysisAgent

# 创建深度分析Agent
agent = DeepAnalysisAgent(llm)

# 批量分析PDF
result = agent.run(
    pdf_directory="pdfs/",
    output_dir="data/results/",
    extract_tables=True,
    extract_figures=True
)
```

---

## 📊 输出文件说明

### 数据预处理阶段
- `literature_data_processed.csv` - 标准化的文献数据
- `literature_data_processed.xlsx` - Excel格式的文献数据

### 筛选分析阶段
- `literature_screening_results.xlsx` - 筛选结果
- `literature_analysis_results.xlsx` - 分析数据
- `literature_research_report.md` - 研究报告

### PDF深度分析阶段
- `deep_analysis_results.xlsx` - 深度分析结果
- `deep_analysis_results.json` - 详细JSON数据
- `extracted_tables/` - 提取的表格
- `extracted_figures/` - 提取的图表

---

## ❓ 常见问题

### Q1: API配置问题
**问题**: 提示"需要提供API密钥"
**解决**: 
1. 检查`.env`文件是否存在
2. 确保`OPENAI_API_KEY`已正确填写
3. 验证API密钥是否有效

### Q2: PDF处理失败
**问题**: PDF转换报错
**解决**:
1. 安装poppler-utils：
   - macOS: `brew install poppler`
   - Ubuntu: `sudo apt-get install poppler-utils`
2. 检查PDF文件是否损坏

### Q3: 内存不足
**问题**: 处理大量文献时内存不足
**解决**:
1. 使用测试模式：`test_mode=True`
2. 分批处理：设置`test_size`
3. 增加系统内存或使用更强大的机器

### Q4: 网络连接问题
**问题**: API调用超时
**解决**:
1. 检查网络连接
2. 使用代理或VPN
3. 调整API超时设置

### Q5: 数据格式问题
**问题**: 文献数据读取失败
**解决**:
1. 确保文件包含必需的列（标题、摘要）
2. 检查文件编码（建议UTF-8）
3. 使用数据预处理Agent进行格式转换

---

## 🔧 高级配置

### 自定义LLM模型
```python
# 在.env文件中配置
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
```

### 批量处理配置
```python
# 在main.py中调整参数
system.run_research(
    test_mode=False,  # 关闭测试模式
    test_size=0,      # 处理所有文献
    analyze_top=100,  # 分析前100篇
    enable_planning=False  # 跳过规划阶段
)
```

### 进度追踪
```python
# 启用详细进度追踪
system = LiteratureResearchSystem(
    enable_progress_tracking=True
)
```

---

## 📚 更多文档

- [完整API文档](docs/api.md)
- [Agent开发指南](docs/agent_development.md)
- [部署指南](docs/deployment.md)
- [故障排除](docs/troubleshooting.md)

---

## 🆘 获取帮助

- 📖 查看[README.md](README.md)
- 🐛 提交[Issue](https://github.com/yourusername/literature_agent/issues)
- 💬 加入讨论群
- 📧 联系开发团队