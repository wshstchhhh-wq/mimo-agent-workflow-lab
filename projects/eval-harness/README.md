# Eval Harness

一个标准库 Python 工具：读取 prompt suite 和模型回答，生成简洁的模型回答评测报告。它用于证明 MiMo Agent Workflow Lab 有真实的跨模型评测方法，而不是只写计划。

## 运行

```powershell
python projects/eval-harness/src/eval_harness.py `
  --prompts projects/eval-harness/prompts/workflow_prompts.json `
  --responses projects/eval-harness/runs/sample_responses.json `
  --out proof/eval-demo
```

生成：

- `proof/eval-demo/evaluation_report.md`
- `proof/eval-demo/score_summary.csv`

## 测试

```powershell
python -m unittest discover -s projects/eval-harness/tests
```

## 评分说明

这个工具不声称替代人工评审。它只做可解释的辅助评分：

- 必要术语覆盖率。
- 回答结构化程度。
- 是否包含数字、路径、命令、步骤等具体信息。
