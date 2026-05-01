# MiMo Orbit Agent Workflow Lab

这是为 Xiaomi MiMo Orbit 百万亿 Token 创造者激励计划准备的真实项目包，也可以作为后续 GitHub 项目 README 的起点。

## 项目定位

本项目面向个人和小团队的高频 AI 工作流：数据分析、资料整理、代码生成、报告/表格自动化、学习复盘和轻量前端工具。目标是把这些零散任务整理成可复用的 Agent 流水线，并用 MiMo API 做长上下文、多 Agent 协作、中文报告生成和代码修改评测。

## 真实子项目

- `projects/agent-dashboard`：静态网页仪表盘，用于登记 Agent 工作流、估算 token 和生成项目摘要。
- `projects/data-report-agent`：Python CSV 报告生成器，输出 Markdown 报告和 SVG 图表。
- `projects/eval-harness`：Python 模型评测记录工具，输出评分报告和 CSV 汇总。

## 资源规划

- 阶段目标：完成一轮 30 天连续 Agent 工作流评测。
- 估算消耗：2.4 亿到 3.6 亿 token。
- 使用周期：30 天。
- 主要用途：真实项目构建、MiMo 接入评测、跨模型对照、自动化日志和公开案例整理。

## 当前材料

- `MiMo_Orbit_申请填写稿.md`：表单第 01-05 项的填写建议和可复制文案。
- `proof/token_plan.csv`：token 消耗估算表。
- `proof/screenshots/agent-dashboard.png`：真实网页渲染截图。
- `proof/screenshots/data-report-output.png`：数据报告输出证明图。
- `proof/screenshots/eval-report-output.png`：模型评测输出证明图。
- `proof/data-report-demo/report.md`：CSV 工作流报告生成结果。
- `proof/eval-demo/evaluation_report.md`：模型评测样例报告。
- `proof/upload_note.md`：上传材料说明和优先级。
- `proof/workflow_log_template.md`：终端/Agent 工作流日志模板。
- `proof/mimo_orbit_proof_card.png`：可上传的项目说明图。
- `tools/make_proof_card.py`：重新生成上传图的脚本。

## 证明材料建议

如果有真实的账单截图、终端运行日志、Agent 工作流截图、GitHub 仓库或在线演示，优先使用真实材料。本目录生成的截图和报告可以证明项目已经可运行，不应该冒充账单或历史用量证明。

## 复现命令

```powershell
python projects/data-report-agent/src/report_agent.py --input projects/data-report-agent/sample_data/agent_workflows.csv --out proof/data-report-demo
python projects/eval-harness/src/eval_harness.py --prompts projects/eval-harness/prompts/workflow_prompts.json --responses projects/eval-harness/runs/sample_responses.json --out proof/eval-demo
python tools/capture_dashboard.py
```
