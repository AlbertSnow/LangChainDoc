# LangChainDoc

投资AI项目骨架：支持网页采集、结构化信号、摘要与报告生成。

## 目录结构
- `src/` 核心代码
- `src/config/` 配置文件
- `scripts/` 运行脚本
- `data/` 输出数据（忽略提交）

## 快速开始
1. 安装依赖
   - `pip install -r requirements.txt`
2. 配置数据源
   - 编辑 `src/config/sources.yaml`
   - 编辑 `src/config/keywords.yaml`
3. 运行采集与报告
   - `python scripts/run_pipeline.py`

## 说明
`scripts/run_pipeline.py` 会在 `data/` 生成原始/清洗数据与报告。
