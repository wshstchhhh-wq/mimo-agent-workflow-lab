from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "proof" / "mimo_orbit_proof_card.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, xy, max_width: int, fnt, fill, line_gap: int = 10):
    x, y = xy
    lines = []
    current = ""
    segments = []
    token = ""
    for ch in text:
        if ch.isascii() and (ch.isalnum() or ch in "/._+-"):
            token += ch
        else:
            if token:
                segments.append(token)
                token = ""
            segments.append(ch)
    if token:
        segments.append(token)

    for seg in segments:
        probe = current + seg
        if draw.textbbox((0, 0), probe, font=fnt)[2] <= max_width:
            current = probe
        else:
            if current:
                lines.append(current)
            current = seg
    if current:
        lines.append(current)

    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
    return y


def pill(draw, xy, text, fill, outline, text_fill, fnt):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    w = bbox[2] - bbox[0] + 36
    h = bbox[3] - bbox[1] + 22
    draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=fill, outline=outline, width=2)
    draw.text((x + 18, y + 10), text, font=fnt, fill=text_fill)
    return x + w + 14


def main():
    W, H = 1600, 1000
    bg = (247, 245, 238)
    ink = (22, 22, 22)
    muted = (96, 94, 88)
    accent = (0, 0, 0)
    line = (210, 204, 190)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    title = font(54, True)
    h2 = font(31, True)
    body = font(26)
    small = font(22)
    tiny = font(19)

    d.text((80, 70), "MiMo Orbit 申请证明材料", font=title, fill=ink)
    d.text((82, 142), "Agent Workflow Lab | 30 天连续评测资源规划", font=h2, fill=muted)
    d.line((80, 195, 1520, 195), fill=line, width=2)

    y = 235
    d.text((90, y), "项目目标", font=h2, fill=ink)
    y += 48
    y = draw_wrapped(
        d,
        "构建个人/小团队可复用的 AI Agent 工作流，用于数据分析、资料整理、代码生成、报告/表格自动化、学习复盘和轻量前端工具。重点评测 MiMo V2.5 在长上下文、多智能体协作、中文技术报告和代码修改中的稳定性。",
        (90, y),
        680,
        body,
        ink,
        8,
    )

    x2, y2 = 850, 235
    d.text((x2, y2), "核心工具与模型", font=h2, fill=ink)
    y2 += 55
    x = x2
    for item in ["Codex", "Claude Code", "MiMo API", "GPT", "Claude", "DeepSeek"]:
        if x > 1350:
            x = x2
            y2 += 62
        x = pill(d, (x, y2), item, (255, 255, 255), (28, 28, 28), ink, small)
    y2 += 95
    d.text((x2, y2), "计划产出", font=h2, fill=ink)
    y2 += 48
    y2 = draw_wrapped(
        d,
        "可复现脚本、运行日志、Markdown 报告、Excel 图表、PNG 图表、工作流复盘、GitHub README 案例。",
        (x2, y2),
        610,
        body,
        ink,
        8,
    )

    d.rounded_rectangle((80, 610, 1520, 875), radius=16, fill=(255, 255, 255), outline=line, width=2)
    d.text((115, 645), "Token 需求估算", font=h2, fill=ink)
    rows = [
        ("端到端案例", "20-30 个", "约 80-150 万 token/个"),
        ("跨模型评测", "35 组任务", "MiMo vs GPT/Claude/DeepSeek"),
        ("长上下文/多 Agent 压测", "18 组", "代码修改、重试、验证"),
        ("30 天总需求", "2.4-3.6 亿", "完整评测周期估算"),
    ]
    yy = 705
    for a, b, c in rows:
        d.text((120, yy), a, font=body, fill=muted)
        d.text((500, yy), b, font=body, fill=ink)
        d.text((780, yy), c, font=body, fill=muted)
        yy += 42

    d.line((80, 910, 1520, 910), fill=line, width=2)
    d.text((90, 937), "说明：此图为项目说明与计划证明，不是历史账单截图。真实账单、终端日志、GitHub 链接可作为更强补充。", font=tiny, fill=muted)
    d.text((90, 967), "生成日期：2026-05-01 | 目录：D:/codex/mimo", font=tiny, fill=muted)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
