# MiMo Orbit 真实项目提交摘要

## 推荐提交项目名

MiMo Agent Workflow Lab

## 项目一句话

一个面向个人和小团队的 AI Agent 工作流实验室，用真实工具把数据分析、报告生成、模型评测和 token 预算管理串成可复现流程。

## 当前包含的真实子项目

1. `projects/agent-dashboard`
   - 静态网页仪表盘。
   - 用于登记 Agent 工作流、估算 30 天 token 消耗、生成申请文案。
   - 可直接打开 `index.html` 使用。

2. `projects/data-report-agent`
   - Python CSV 报告生成器。
   - 输入工作流数据，输出 Markdown 报告和 SVG 图表。
   - 适合证明“数据分析 + 文档自动化”的真实落地。

3. `projects/eval-harness`
   - Python 模型回答评测记录工具。
   - 读取 prompt suite 和模型回答，计算覆盖率、结构化程度和具体性分。
   - 适合证明“MiMo 与 GPT/Claude/DeepSeek 同题评测”的计划和方法。

## 资源规划口径

建议把重点放在 30 天连续评测和真实项目产出上，让资源需求自然来自工作量本身：

- 20-30 个端到端数据/工作流案例。
- 35 组跨模型评测。
- 18 组长上下文、多 Agent、失败重试与验证场景。
- 每个案例沉淀为脚本、日志、报告、截图和 README。

按当前样例数据，完整跑完一轮预计会消耗约 3.52 亿 token。这个数字用于解释工作量规模，不建议写成硬性目标。

## 上传材料优先级

1. 真实账单、终端日志、GitHub 仓库链接。
2. `proof/screenshots/agent-dashboard.png`。
3. `proof/screenshots/data-report-output.png`。
4. `proof/screenshots/eval-report-output.png`。
5. `proof/mimo_orbit_proof_card.png`。
