# 贡献指南

感谢你考虑为 Literature Agent System 做出贡献！

## 如何贡献

### 报告Bug

如果发现Bug，请创建一个Issue并包含：

1. **清晰的标题**：简短描述问题
2. **复现步骤**：详细说明如何触发Bug
3. **预期行为**：应该发生什么
4. **实际行为**：实际发生了什么
5. **环境信息**：
   - 操作系统
   - Python版本
   - 依赖包版本
6. **日志和截图**：如果可能

### 提出新功能

创建Feature Request Issue，包含：

1. **功能描述**：清晰说明想要的功能
2. **使用场景**：为什么需要这个功能
3. **建议实现**：如果有想法，说明如何实现
4. **替代方案**：考虑过的其他方案

### 提交代码

1. **Fork仓库**
   ```bash
   # Fork后克隆你的仓库
   git clone https://github.com/YOUR_USERNAME/literature_agent.git
   cd literature_agent
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-description
   ```

3. **开发**
   - 遵循代码风格指南（见下文）
   - 添加必要的测试
   - 更新相关文档

4. **提交**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```
   
   提交信息格式：
   - `feat:` 新功能
   - `fix:` Bug修复
   - `docs:` 文档更新
   - `style:` 代码格式（不影响功能）
   - `refactor:` 重构
   - `test:` 添加测试
   - `chore:` 构建/工具变更

5. **推送并创建PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   然后在GitHub上创建Pull Request

## 代码风格

### Python代码

遵循 PEP 8 规范：

```python
# ✅ 好的例子
def process_literature(title: str, abstract: str) -> dict:
    """
    处理文献数据
    
    Parameters:
    -----------
    title : str
        文献标题
    abstract : str
        文献摘要
        
    Returns:
    --------
    dict : 处理结果
    """
    result = {
        'title': title.strip(),
        'abstract': abstract.strip(),
        'processed': True
    }
    return result


# ❌ 不好的例子
def ProcessLit(t,a):
    r={'title':t.strip(),'abstract':a.strip(),'processed':True}
    return r
```

### 文档字符串

使用Google风格或NumPy风格：

```python
def download_paper(doi: str, output_path: str) -> bool:
    """
    下载论文PDF
    
    Args:
        doi (str): 论文DOI
        output_path (str): 输出路径
        
    Returns:
        bool: 是否成功下载
        
    Raises:
        ValueError: DOI格式不正确
        IOError: 文件写入失败
        
    Example:
        >>> download_paper('10.1000/xyz123', 'paper.pdf')
        True
    """
    pass
```

### 命名约定

- **类名**: PascalCase - `class ScreeningAgent`
- **函数/方法**: snake_case - `def process_literature()`
- **常量**: UPPER_SNAKE_CASE - `API_BASE_URL`
- **私有方法**: 前缀下划线 - `def _internal_method()`

### 注释

- 代码应该自解释，只在必要时添加注释
- 注释解释"为什么"而不是"做什么"
- 中文或英文注释都可以，保持一致

```python
# ✅ 好的注释
# 使用重试机制避免网络抖动导致的失败
for attempt in range(max_retries):
    try:
        return self._download(url)
    except NetworkError:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)

# ❌ 不必要的注释
# 创建一个空列表
results = []
# 遍历DOI列表
for doi in doi_list:
    # 下载PDF
    pdf = download_pdf(doi)
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_screening.py

# 运行特定测试函数
pytest tests/test_screening.py::test_screen_literature
```

### 编写测试

为新功能添加测试：

```python
# tests/test_screening.py

import pytest
from agents.screening_agent import ScreeningAgent

def test_screening_agent_init():
    """测试ScreeningAgent初始化"""
    agent = ScreeningAgent(llm=mock_llm)
    assert agent.name == "文献筛选Agent"

def test_screen_relevant_paper():
    """测试筛选相关文献"""
    agent = ScreeningAgent(llm=mock_llm)
    result = agent.screen({
        'title': 'Study on soil carbon',
        'abstract': 'This study measures soil carbon...'
    })
    assert result['decision'] == 'accept'

def test_screen_irrelevant_paper():
    """测试筛选不相关文献"""
    agent = ScreeningAgent(llm=mock_llm)
    result = agent.screen({
        'title': 'Machine learning',
        'abstract': 'This is about AI...'
    })
    assert result['decision'] == 'reject'
```

## 文档

### 更新文档

如果你的改动影响使用方式，请更新：

1. **README.md** - 如果改变了基本功能或API
2. **docs/** - 添加详细的使用说明
3. **代码注释** - 保持文档字符串最新
4. **CHANGELOG.md** - 添加变更记录（如果有）

### 文档风格

- 使用清晰简洁的语言
- 提供代码示例
- 包含截图（如果有助于理解）
- 中英文均可，保持一致

## 提交Pull Request

### PR描述

好的PR描述应包含：

```markdown
## 变更类型
- [ ] Bug修复
- [x] 新功能
- [ ] 文档更新
- [ ] 性能优化
- [ ] 代码重构

## 描述
添加了增强版PDF下载工具，集成了4个合法数据源。

## 变更内容
- 创建 `EnhancedPDFDownloadTool` 类
- 集成 Unpaywall、Semantic Scholar、Crossref、Europe PMC
- 添加自动回退机制
- 更新文档

## 测试
- [x] 本地测试通过
- [x] 添加了单元测试
- [x] 更新了相关文档

## 相关Issue
Closes #123
```

### PR检查清单

在提交PR前确认：

- [ ] 代码遵循项目风格
- [ ] 添加了必要的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确
- [ ] 分支基于最新的main
- [ ] 没有合并冲突

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺：

- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表现出同理心

### 不可接受的行为

- 使用性别化语言或图像
- 人身攻击或政治攻击
- 公开或私下骚扰
- 未经许可发布他人隐私信息
- 其他不道德或不专业的行为

### 执行

不可接受的行为可向项目维护者报告。所有投诉都将被审查和调查。

## 许可证

贡献代码即表示同意以MIT许可证发布你的贡献。

## 问题？

如有任何问题，请：

1. 查看 [FAQ](README.md#-常见问题)
2. 搜索现有的Issues
3. 创建新的Issue询问

---

再次感谢你的贡献！ 🎉
