from __future__ import annotations

import argparse
import csv
import html
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkflowRecord:
    workflow: str
    domain: str
    cases: int
    avg_input_tokens: int
    avg_output_tokens: int
    retry_rate: float
    verification_runs: int
    public_output: bool

    @property
    def base_tokens(self) -> int:
        return self.cases * (self.avg_input_tokens + self.avg_output_tokens)

    @property
    def retry_tokens(self) -> int:
        return round(self.base_tokens * self.retry_rate)

    @property
    def verification_tokens(self) -> int:
        average_tokens = self.avg_input_tokens + self.avg_output_tokens
        return round(self.verification_runs * average_tokens * 0.35)

    @property
    def total_tokens(self) -> int:
        return self.base_tokens + self.retry_tokens + self.verification_tokens


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "是"}


def load_records(path: Path) -> list[WorkflowRecord]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        records = []
        for row in rows:
            records.append(
                WorkflowRecord(
                    workflow=row["workflow"].strip(),
                    domain=row["domain"].strip(),
                    cases=int(row["cases"]),
                    avg_input_tokens=int(row["avg_input_tokens"]),
                    avg_output_tokens=int(row["avg_output_tokens"]),
                    retry_rate=float(row["retry_rate"]),
                    verification_runs=int(row["verification_runs"]),
                    public_output=parse_bool(row["public_output"]),
                )
            )
    return records


def token_label(value: int) -> str:
    if value >= 100_000_000:
        return f"{value / 100_000_000:.2f} 亿"
    if value >= 10_000:
        return f"{value / 10_000:.0f} 万"
    return str(value)


def summarize(records: list[WorkflowRecord]) -> dict[str, int | float]:
    total = sum(record.total_tokens for record in records)
    cases = sum(record.cases for record in records)
    public_outputs = sum(1 for record in records if record.public_output)
    average_retry = sum(record.retry_rate for record in records) / len(records) if records else 0.0
    return {
        "total_tokens": total,
        "cases": cases,
        "public_outputs": public_outputs,
        "average_retry": average_retry,
    }


def render_markdown(records: list[WorkflowRecord]) -> str:
    summary = summarize(records)
    lines = [
        "# MiMo Agent Workflow Lab 数据报告",
        "",
        "## 总览",
        "",
        f"- 工作流数量：{len(records)}",
        f"- 30 天案例数：{summary['cases']}",
        f"- 预计 token：{token_label(int(summary['total_tokens']))}",
        f"- 平均重试系数：{summary['average_retry']:.2f}",
        f"- 可公开产出：{summary['public_outputs']}",
        "",
        "## 工作流明细",
        "",
        "| 工作流 | 类型 | 案例数 | 重试系数 | 验证轮次 | 预计 token | 公开产出 |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]

    for record in sorted(records, key=lambda item: item.total_tokens, reverse=True):
        public_output = "yes" if record.public_output else "planned"
        lines.append(
            "| "
            + " | ".join(
                [
                    record.workflow,
                    record.domain,
                    str(record.cases),
                    f"{record.retry_rate:.2f}",
                    str(record.verification_runs),
                    token_label(record.total_tokens),
                    public_output,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 申请说明",
            "",
            "这些数据用于说明 3 亿 token 申请目标的消耗来源：长上下文输入、模型输出、失败重试、验证轮次和公开案例整理都会产生实际 token 成本。",
        ]
    )
    return "\n".join(lines) + "\n"


def render_svg_chart(records: list[WorkflowRecord]) -> str:
    width = 1100
    row_height = 62
    top = 70
    left = 280
    chart_width = 700
    height = top + row_height * len(records) + 55
    max_tokens = max((record.total_tokens for record in records), default=1)
    colors = ["#087f8c", "#cf5b3f", "#9a6a13", "#247a47", "#6c5ce7"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f6f7fb"/>',
        '<text x="40" y="42" font-family="Microsoft YaHei, Segoe UI, Arial" font-size="28" font-weight="700" fill="#17201f">30 天 token 估算</text>',
    ]

    for index, record in enumerate(sorted(records, key=lambda item: item.total_tokens, reverse=True)):
        y = top + index * row_height
        bar_width = max(8, int(record.total_tokens / max_tokens * chart_width))
        color = colors[index % len(colors)]
        parts.extend(
            [
                f'<text x="40" y="{y + 26}" font-family="Microsoft YaHei, Segoe UI, Arial" font-size="18" fill="#17201f">{html.escape(record.workflow)}</text>',
                f'<rect x="{left}" y="{y}" width="{chart_width}" height="26" rx="6" fill="#e4ecea"/>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="26" rx="6" fill="{color}"/>',
                f'<text x="{left + chart_width + 18}" y="{y + 20}" font-family="Microsoft YaHei, Segoe UI, Arial" font-size="17" fill="#66716f">{token_label(record.total_tokens)}</text>',
            ]
        )

    parts.append("</svg>")
    return "\n".join(parts)


def write_outputs(records: list[WorkflowRecord], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "report.md"
    chart_path = out_dir / "token_chart.svg"
    report_path.write_text(render_markdown(records), encoding="utf-8")
    chart_path.write_text(render_svg_chart(records), encoding="utf-8")
    return report_path, chart_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a MiMo Orbit workflow report from CSV data.")
    parser.add_argument("--input", type=Path, required=True, help="Path to agent workflow CSV.")
    parser.add_argument("--out", type=Path, required=True, help="Output directory.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    records = load_records(args.input)
    report_path, chart_path = write_outputs(records, args.out)
    summary = summarize(records)
    print(f"Generated {report_path}")
    print(f"Generated {chart_path}")
    print(f"Estimated tokens: {int(summary['total_tokens']):,}")


if __name__ == "__main__":
    main()
