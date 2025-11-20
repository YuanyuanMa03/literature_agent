#!/bin/bash
# 文献分析Agent系统 - 快速安装脚本

echo "=================================="
echo "文献分析Agent系统 - 快速安装"
echo "=================================="
echo ""

# 检查Python版本
echo "检查Python环境..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.10"

if [ -z "$python_version" ]; then
    echo "❌ 未找到Python3，请先安装Python 3.10或更高版本"
    exit 1
fi

echo "✅ Python版本: $python_version"

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境? (y/n, 默认y): " create_venv
create_venv=${create_venv:-y}

if [ "$create_venv" = "y" ]; then
    echo ""
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境已创建"
    
    echo ""
    echo "激活虚拟环境..."
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 安装依赖
echo ""
echo "安装依赖包..."
pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 配置.env
echo ""
if [ -f ".env" ]; then
    echo "⚠️  .env文件已存在，跳过配置"
else
    echo "创建.env配置文件..."
    cp .env.example .env
    echo "✅ .env文件已创建"
    echo ""
    echo "⚠️  请编辑.env文件，填入您的API信息："
    echo "   OPENAI_API_BASE=https://your-api-endpoint.com/v1"
    echo "   OPENAI_API_KEY=your-api-key-here"
fi

# 完成
echo ""
echo "=================================="
echo "✅ 安装完成！"
echo "=================================="
echo ""
echo "下一步："
echo "1. 编辑.env文件，配置API信息"
echo "   vim .env  # 或使用您喜欢的编辑器"
echo ""
echo "2. 准备文献数据文件（支持 .xls, .xlsx, .csv）"
echo "   将文献文件放在项目根目录"
echo ""
echo "3. 运行程序："
echo "   python main.py"
echo ""
echo "4. 查看生成的结果："
echo "   - literature_screening_results.xlsx  (筛选结果)"
echo "   - literature_analysis_results.xlsx   (分析数据)"
echo "   - literature_research_report.md      (研究报告)"
echo ""
echo "更多信息请查看 README.md 或访问项目文档"
echo ""
