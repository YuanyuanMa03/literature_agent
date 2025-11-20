#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Literature Agent System - 安装配置
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="literature-agent-system",
    version="1.0.0",
    author="Yuanyuan Ma",
    author_email="yym290552@gmail.com",
    description="智能文献分析系统 - 自动筛选、深度分析和总结学术文献",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/YuanyuanMa03/literature_agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "pdf": [
            "poppler-utils",
        ],
    },
    entry_points={
        "console_scripts": [
            "literature-agent=main:main",
            "literature-preprocess=demo_data_preprocessing:demo_data_preprocessing",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", ".env.example"],
    },
    zip_safe=False,
    keywords="literature analysis, academic research, data preprocessing, machine learning, nlp",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/literature_agent/issues",
        "Source": "https://github.com/yourusername/literature_agent",
        "Documentation": "https://github.com/yourusername/literature_agent/blob/main/README.md",
    },
)