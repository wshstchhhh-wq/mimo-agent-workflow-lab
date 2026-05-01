# Data Report Agent

一个标准库 Python 工具：读取 CSV 工作流数据，生成 Markdown 报告和 SVG 图表。它是 MiMo Agent Workflow Lab 里的真实数据分析子项目。

## 运行

```powershell
python projects/data-report-agent/src/report_agent.py `
  --input projects/data-report-agent/sample_data/agent_workflows.csv `
  --out proof/data-report-demo
```

生成：

- `proof/data-report-demo/report.md`
- `proof/data-report-demo/token_chart.svg`

## 测试

```powershell
python -m unittest discover -s projects/data-report-agent/tests
```

## 输入字段

- `workflow`
- `domain`
- `cases`
- `avg_input_tokens`
- `avg_output_tokens`
- `retry_rate`
- `verification_runs`
- `public_output`
