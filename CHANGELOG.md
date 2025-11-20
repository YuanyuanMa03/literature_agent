# 更新日志

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- 📥 增强版PDF下载工具，集成多个合法数据源
- 🔍 Unpaywall、Semantic Scholar、Crossref、Europe PMC支持
- 📖 完整的文档体系（docs/目录）
- 🎯 手动下载模式（第二阶段）
- 🧪 测试脚本和示例代码

### 变更
- 📁 重新组织项目结构，更符合开源规范
- 📝 大幅改进README，添加详细说明
- 🔧 优化gitignore规则
- 📊 改进输出文件组织

### 修复
- 🐛 修复Elsevier文献下载403错误
- 🐛 修复linkinghub重定向问题
- 🐛 改进错误处理和日志输出

### 文档
- 📚 新增《文献下载方案汇总》
- 📚 新增《手动下载指南》
- 📚 新增《机构代理下载说明》
- 📚 新增《快速开始_增强版下载》
- 📚 添加CONTRIBUTING.md贡献指南

## [1.0.0] - 2025-01-20

### 新增
- 🎉 初始版本发布
- 📊 第一阶段：智能文献筛选与分析
- 🔍 第二阶段：PDF深度分析（OCR+多模态LLM）
- 🤖 基于LLM的Agent系统
- 📝 自动生成研究报告
- 💾 支持多种数据格式（CSV、Excel）
- 🔄 断点续传功能
- 📈 实时进度显示

### 功能
- **Screening Agent**: 智能判断文献相关性
- **Analysis Agent**: 提取关键信息
- **Report Agent**: 生成结构化报告
- **PDF Download Agent**: 批量下载PDF
- **Deep Analysis Agent**: PDF深度分析
- **Planning Agent**: 研究规划
  
### 支持的API
- 硅基流动 (SiliconFlow)
- DeepSeek
- OpenAI
- 其他OpenAI兼容接口

---

## 贡献者

感谢所有为这个项目做出贡献的人！

## 反馈

如有建议或问题，请：
- 提交 [GitHub Issue](https://github.com/YuanyuanMa03/literature_agent/issues)
- 发送邮件到 yym290552@gmail.com,2025101184@stu.njau.edu.cn
