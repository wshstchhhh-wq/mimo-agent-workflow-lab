# MiMo Agent Workflow Lab 评测报告

## 模型平均分

| 模型 | 平均分 |
| --- | ---: |
| MiMo V2.5 planned | 87.07 |
| Claude baseline | 73.00 |
| GPT series baseline | 67.00 |
| DeepSeek baseline | 56.20 |

## 明细

| Prompt | 模型 | 术语覆盖 | 结构化 | 具体性 | 总分 |
| --- | --- | ---: | ---: | ---: | ---: |
| Agent 代码修改与验证 | MiMo V2.5 planned | 100.00 | 74.00 | 60.00 | 86.80 |
| Agent 代码修改与验证 | DeepSeek baseline | 60.00 | 61.00 | 40.00 | 56.20 |
| CSV 数据报告生成 | MiMo V2.5 planned | 100.00 | 74.00 | 100.00 | 94.80 |
| CSV 数据报告生成 | GPT series baseline | 80.00 | 35.00 | 60.00 | 67.00 |
| MiMo 跨模型评测 | MiMo V2.5 planned | 100.00 | 48.00 | 50.00 | 79.60 |
| MiMo 跨模型评测 | Claude baseline | 100.00 | 35.00 | 30.00 | 73.00 |

## 说明

该报告用于记录同题 prompt 下不同模型输出的可解释评分，后续可接入 MiMo API，把真实响应写入 `runs/` 后重新生成报告。
