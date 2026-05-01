$ErrorActionPreference = "Stop"

python projects/data-report-agent/src/report_agent.py `
  --input projects/data-report-agent/sample_data/agent_workflows.csv `
  --out proof/data-report-demo

python projects/eval-harness/src/eval_harness.py `
  --prompts projects/eval-harness/prompts/workflow_prompts.json `
  --responses projects/eval-harness/runs/sample_responses.json `
  --out proof/eval-demo

python tools/capture_dashboard.py
python tools/render_proof_images.py

python -m unittest discover -s projects/data-report-agent/tests
python -m unittest discover -s projects/eval-harness/tests

Write-Host "Demo outputs regenerated under proof/."
