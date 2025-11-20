#!/bin/bash
# 文献分析Agent系统 - 增强版安装脚本

echo "=========================================="
echo "🔬 文献分析Agent系统 - 增强版安装脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查Python版本
print_info "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    print_error "未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.8"

if [ -z "$python_version" ]; then
    print_error "无法获取Python版本信息"
    exit 1
fi

print_success "Python版本: $python_version"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    print_error "未找到pip3，请先安装pip"
    exit 1
fi

# 创建虚拟环境（可选）
echo ""
read -p "是否创建虚拟环境? (y/n, 默认y): " create_venv
create_venv=${create_venv:-y}

if [ "$create_venv" = "y" ]; then
    print_info "创建虚拟环境..."
    python3 -m venv venv
    print_success "虚拟环境已创建"
    
    print_info "激活虚拟环境..."
    source venv/bin/activate
    print_success "虚拟环境已激活"
    
    # 升级pip
    print_info "升级pip..."
    pip install --upgrade pip
fi

# 安装依赖
print_info "安装Python依赖包..."
if pip install -r requirements.txt; then
    print_success "依赖安装完成"
else
    print_error "依赖安装失败"
    exit 1
fi

# 检查系统依赖
print_info "检查系统依赖..."

# 检查poppler（用于PDF处理）
if command -v pdftoppm &> /dev/null; then
    print_success "poppler已安装"
else
    print_warning "未检测到poppler，PDF处理功能可能受限"
    echo "    macOS: brew install poppler"
    echo "    Ubuntu: sudo apt-get install poppler-utils"
    echo "    Windows: 下载poppler并添加到PATH"
fi

# 配置.env
echo ""
if [ -f ".env" ]; then
    print_warning ".env文件已存在，跳过创建"
else
    print_info "创建.env配置文件..."
    cp .env.example .env
    print_success ".env文件已创建"
    
    echo ""
    print_warning "请编辑.env文件，填入您的API信息："
    echo "    OPENAI_API_BASE=https://api.siliconflow.cn/v1"
    echo "    OPENAI_API_KEY=your-api-key-here"
    echo "    LLM_MODEL=Qwen/Qwen3-Omni-30B-A3B-Instruct"
fi

# 创建必要的目录
print_info "创建项目目录..."
mkdir -p data/{pdfs,pdf_images,results,cache}
print_success "项目目录结构已创建"

# 测试安装
print_info "测试安装..."
if python3 -c "from agents.data_preprocessing_agent import DataPreprocessingAgent; print('✅ DataPreprocessingAgent导入成功')" 2>/dev/null; then
    print_success "核心模块测试通过"
else
    print_warning "核心模块测试失败，请检查安装"
fi

# 完成
echo ""
echo "=========================================="
echo "🎉 安装完成！"
echo "=========================================="
echo ""
print_info "快速开始："
echo ""
echo "1. 配置API信息："
echo "   vim .env  # 或使用您喜欢的编辑器"
echo ""
echo "2. 运行数据预处理（新功能）："
echo "   python demo_data_preprocessing.py"
echo ""
echo "3. 运行完整流程："
echo "   python main.py"
echo ""
echo "4. 仅PDF深度分析："
echo "   python main_stage2.py"
echo ""
print_info "生成的文件："
echo "   📊 预处理数据: data/literature_data_processed.csv"
echo "   📋 筛选结果: literature_screening_results.xlsx"
echo "   📈 分析数据: literature_analysis_results.xlsx"
echo "   📄 研究报告: literature_research_report.md"
echo ""
print_info "更多信息："
echo "   📖 README.md - 详细文档"
echo "   🌐 GitHub仓库 - 项目主页"
echo "   📧 联系支持 - 技术帮助"
echo ""
print_success "感谢使用文献分析Agent系统！"
echo ""
