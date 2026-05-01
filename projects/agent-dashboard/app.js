const STORAGE_KEY = "mimo-agent-workflow-lab";

const seedWorkflows = [
  {
    id: "data-report",
    name: "CSV 数据报告生成器",
    domain: "数据分析",
    runs: 24,
    tokens: 1200000,
    retry: 0.35,
    publicOutput: true,
  },
  {
    id: "eval-harness",
    name: "跨模型回答评测",
    domain: "模型评测",
    runs: 35,
    tokens: 2500000,
    retry: 0.45,
    publicOutput: true,
  },
  {
    id: "coding-agent",
    name: "多 Agent 代码修改与验证",
    domain: "代码生成",
    runs: 30,
    tokens: 1800000,
    retry: 0.55,
    publicOutput: true,
  },
  {
    id: "doc-automation",
    name: "中文报告与图表自动化",
    domain: "文档自动化",
    runs: 30,
    tokens: 900000,
    retry: 0.25,
    publicOutput: true,
  },
];

let workflows = loadWorkflows();

const form = document.querySelector("#workflowForm");
const list = document.querySelector("#workflowList");
const chart = document.querySelector("#chart");
const submission = document.querySelector("#submissionText");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(form);
  workflows.push({
    id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()),
    name: data.get("name").trim(),
    domain: data.get("domain"),
    runs: Number(data.get("runs")),
    tokens: Number(data.get("tokens")),
    retry: Number(data.get("retry")),
    publicOutput: data.get("publicOutput") === "on",
  });
  form.reset();
  form.elements.runs.value = 20;
  form.elements.tokens.value = 1200000;
  form.elements.retry.value = 0.4;
  form.elements.publicOutput.checked = true;
  saveAndRender();
});

document.querySelector("#resetBtn").addEventListener("click", () => {
  workflows = structuredClone(seedWorkflows);
  saveAndRender();
});

document.querySelector("#copyBtn").addEventListener("click", async () => {
  const text = buildSubmissionText();
  submission.value = text;
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    submission.focus();
    submission.select();
  }
});

function loadWorkflows() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : structuredClone(seedWorkflows);
  } catch {
    return structuredClone(seedWorkflows);
  }
}

function saveAndRender() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(workflows));
  render();
}

function estimate(workflow) {
  return Math.round(workflow.runs * workflow.tokens * (1 + workflow.retry));
}

function formatTokens(value) {
  if (value >= 100000000) return `${(value / 100000000).toFixed(2)} 亿`;
  if (value >= 10000) return `${Math.round(value / 10000).toLocaleString("zh-CN")} 万`;
  return value.toLocaleString("zh-CN");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderSummary(total) {
  const retryAverage = workflows.length
    ? workflows.reduce((sum, item) => sum + item.retry, 0) / workflows.length
    : 0;
  document.querySelector("#totalTokens").textContent = formatTokens(total);
  document.querySelector("#workflowCount").textContent = workflows.length;
  document.querySelector("#retryAverage").textContent = retryAverage.toFixed(2);
  document.querySelector("#publicCount").textContent = workflows.filter((item) => item.publicOutput).length;
}

function renderChart() {
  const max = Math.max(...workflows.map(estimate), 1);
  chart.innerHTML = workflows
    .map((workflow) => {
      const value = estimate(workflow);
      const width = Math.max(4, Math.round((value / max) * 100));
      return `
        <div class="bar-row">
          <span class="bar-label">${escapeHtml(workflow.domain)}</span>
          <div class="bar-track">
            <div class="bar-fill" style="width:${width}%"></div>
          </div>
          <span class="bar-value">${formatTokens(value)}</span>
        </div>
      `;
    })
    .join("");
}

function renderList() {
  list.innerHTML = workflows
    .map(
      (workflow) => `
        <article class="workflow-card">
          <header>
            <h3>${escapeHtml(workflow.name)}</h3>
            <span class="badge">${escapeHtml(workflow.domain)}</span>
          </header>
          <div class="card-grid">
            <div><span>30 天任务</span><strong>${workflow.runs}</strong></div>
            <div><span>单任务 token</span><strong>${formatTokens(workflow.tokens)}</strong></div>
            <div><span>重试系数</span><strong>${workflow.retry.toFixed(2)}</strong></div>
            <div><span>估算总量</span><strong>${formatTokens(estimate(workflow))}</strong></div>
          </div>
          <button class="delete-btn" type="button" data-delete="${workflow.id}">删除</button>
        </article>
      `
    )
    .join("");

  list.querySelectorAll("[data-delete]").forEach((button) => {
    button.addEventListener("click", () => {
      workflows = workflows.filter((workflow) => workflow.id !== button.dataset.delete);
      saveAndRender();
    });
  });
}

function buildSubmissionText() {
  const total = workflows.reduce((sum, workflow) => sum + estimate(workflow), 0);
  const domains = [...new Set(workflows.map((workflow) => workflow.domain))].join("、");
  const publicOutputs = workflows.filter((workflow) => workflow.publicOutput).length;
  return `我正在构建 MiMo Agent Workflow Lab，一个面向个人和小团队的 AI Agent 工作流项目。它包含静态工作流仪表盘、CSV 数据报告生成器和模型回答评测工具，覆盖${domains}等场景。核心痛点是日常任务跨数据、脚本、图表、报告和代码修改，人工切换成本高，而 Agent 工作流需要长上下文、多轮重试、执行验证和跨模型对照，普通赠额很快耗尽。

目前计划在 30 天内运行 ${workflows.length} 类工作流，合计约 ${formatTokens(total)} token，其中 ${publicOutputs} 类会沉淀为 README、报告、截图或评测记录。Token 将用于 MiMo API 接入、Codex/Claude Code/OpenClaw 工作流测试、MiMo 与 GPT/Claude/DeepSeek 同题对照、中文报告生成、代码修改验证和失败重试复盘。我希望申请 3 亿 Token Plan 或等值赠金，用于完成 20-30 个端到端案例并公开整理结果。`;
}

function render() {
  const total = workflows.reduce((sum, workflow) => sum + estimate(workflow), 0);
  renderSummary(total);
  renderChart();
  renderList();
  submission.value = buildSubmissionText();
}

render();
