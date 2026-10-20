"""สร้าง viewer/index.html สำหรับงาน 4 (Enterprise OS บน ERPNext)

รัน:  python viewer/build.py   แล้วดับเบิลคลิก viewer/index.html
แก้ MD เมื่อไรให้รันใหม่ · ตอนเปิดต้องต่อเน็ต (โหลด marked + mermaid จาก CDN)
ขั้นตอน Roadmap ดึงจากตารางใน MD ตาม SOURCES — ถ้า build ล้มแปลว่าหัวข้อ/ตารางต้นทางเปลี่ยนรูปแบบ
"""
import hashlib
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P4 = "04-erpnext-enterprise-os/"
SKILL_COPIES = ROOT / "tools" / "claude-skills" / "local"   # skill ของคนอื่น (MIT) — ไม่รวมใน viewer ที่เผยแพร่

NAME = "งาน 4 · Enterprise OS"
TITLE = "🗺️ Roadmap งาน 4 · Enterprise OS บน ERPNext"
LEAD = ("ลำดับการพัฒนาจาก 04k + ขั้นย่อยของแต่ละ Stage จาก 04c (เต็มเวลา) · ติ๊กเมื่อทำเสร็จ — เก็บในเบราว์เซอร์นี้ · "
        "กด \"อ่านรายละเอียด\" เพื่อเปิดหัวข้อต้นทาง")
K, C = P4 + "04k-dev-roadmap.md", P4 + "04c-build-guide.md"
OUTSIDE = "นอกงาน 4"   # ไฟล์อื่นในพอร์ต: ไม่แสดงในเมนู/ค้นหา แต่เปิดจากลิงก์ได้

GROUPS = [  # เฉพาะงาน 4 · เรียงตามลำดับอ่าน
    ("เริ่มที่นี่", [K, P4 + "README.md"]),
    ("สเปกและการออกแบบ", [P4 + f for f in (
        "04-enterprise-os.md", "04f-module-map.md", "04g-department-flows.md", "04a-company-blueprint.md")]),
    ("ลงมือสร้าง", [C] + [P4 + f for f in ("04l-security-baseline.md", "04d-erp-implementation.md", "04h-connectors.md")]),
    ("ธุรกิจและแผน", [P4 + f for f in (
        "04i-sme-segments.md", "04j-feasibility-business-plan.md", "04b-depa-product-track.md",
        "04e-saas-business-model.md")]),
    ("ข้อมูลอ้างอิง", [P4 + "research/" + f for f in (
        "erpnext-reference.md", "thai-tax-labor-reference.md", "prior-art-market.md")]),
]

SOURCES = [  # (กลุ่มใน Roadmap, ไฟล์, หัวข้อขึ้นต้นด้วย, แบบ)
    ("Phase 0 · เตรียม", K, "Phase 0", "table"),
    ("Phase 1 · MVP (Stage 0–7)", C, None, "stages"),
    ("Phase 2 · MVP+", K, "Phase 2", "table"),
    ("Phase 3 · ต่อยอดตามลูกค้า", K, "Phase 3", "table"),
    ("คู่ขนาน · ธุรกิจ depa และประสบการณ์จริง", K, "คู่ขนาน", "table"),
    ("งานเสริม · ผลงานตรงประกาศงาน", K, "งานเสริม", "table"),
]
LAST_STAGE = 7                 # Stage 8 = ต่อยอด อยู่ใน Phase 3 ของ 04k แล้ว
MOVED = {"5.4", "5.5"}         # ขั้นย่อยของ Stage 5 ที่ 04k ย้ายไป Phase 2
MILESTONES = (K, "Milestone")
GANTT = (K, "ภาพรวมลำดับการพัฒนา")
BADGE_COLS = {"สัปดาห์", "ลำดับ", "#", "ช่วง", "Milestone"}
HEADING = re.compile(r"(#{1,6})\s+(.*)")
STAGE = re.compile(r"\d+\. (Stage \d+) — (.+)")


def slug(text: str) -> str:  # เหมือน check_links — anchor ตรงกับลิงก์ใน MD
    text = text.strip().lower()
    keep = "".join(c for c in text if c in " -_" or unicodedata.category(c)[0] in "LMN")
    return keep.replace(" ", "-")


def headings(lines):
    fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
        elif not fence and (m := HEADING.match(line)):
            yield i, len(m.group(1)), m.group(2).strip()


def sections(lines, match):
    hs = list(headings(lines))
    for k, (i, level, text) in enumerate(hs):
        if match(text):
            end = next((j for j, lv, _ in hs[k + 1:] if lv <= level), len(lines))
            yield text, lines[i + 1:end]


def section(lines, prefix, path):
    for found in sections(lines, lambda t: t.startswith(prefix)):
        return found
    raise SystemExit(f"❌ {path}: ไม่เจอหัวข้อที่ขึ้นต้นด้วย '{prefix}'")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def first_table(sec):
    rows, fence = [], False
    for line in sec:
        if line.startswith("```"):
            fence = not fence
        elif not fence and line.startswith("|"):
            rows.append(line)
        elif rows:
            break
    if len(rows) < 3:
        return None, []
    return cells(rows[0]), [cells(r) for r in rows[2:]]


def step_id(*parts):
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:10]


def row_steps(group, header, rows, src, anchor):
    out = []
    for r in rows:
        r = (r + [""] * len(header))[:len(header)]
        badge = r[0] if header[0] in BADGE_COLS else ""
        li = 1 if badge else 0
        days = next((r[i] for i, h in enumerate(header) if h == "วัน" or "เวลา" in h), "")
        detail = [[h, v] for i, (h, v) in enumerate(zip(header, r))
                  if i not in (0, li) and v and v not in ("—", days)]
        if badge and header[0] == "สัปดาห์":
            badge = f"สัปดาห์ {badge}"
        out.append({"id": step_id(group, badge, r[li]), "badge": badge, "label": r[li],
                    "days": days, "detail": detail, "src": src, "anchor": anchor})
    return out


def stage_steps(group, lines, src):
    out = []
    for title, sec in sections(lines, STAGE.fullmatch):
        stage, name = STAGE.fullmatch(title).groups()
        if int(stage.split()[1]) > LAST_STAGE:
            continue
        text = "\n".join(sec)
        days = (m.group(1).strip() if (m := re.search(r"\*\*เวลา:\*\*\s*([^·\n]+)", text)) else "")
        gate = ""
        for i, line in enumerate(sec):
            if line.startswith("**Gate"):
                gate = line.split(":**", 1)[1].strip()
                if not gate:
                    gate = " · ".join(x[6:].strip() for x in sec[i + 1:] if x.startswith("- [ ] "))
                break
        header, rows = first_table(sec)
        children = row_steps(group + stage, header, rows, src, slug(title)) if header else []
        children = [c for c in children if c["badge"] not in MOVED]
        out.append({"id": step_id(group, stage), "badge": stage, "label": name,
                    "days": days or "ทำเมื่อต้องใช้", "detail": [["Gate", gate]] if gate else [],
                    "src": src, "anchor": slug(title), "children": children})
    return out


def main():
    texts = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
             for p in sorted(ROOT.rglob("*.md")) if HERE not in p.parents and SKILL_COPIES not in p.parents}
    listed = [p for _, ps in GROUPS for p in ps]
    missing = [p for p in listed if p not in texts]
    if missing:
        raise SystemExit(f"❌ ไฟล์ใน GROUPS หายไป: {missing}")

    docs = []
    for name, paths in GROUPS + [(OUTSIDE, [p for p in texts if p not in listed])]:
        for p in paths:
            lines = texts[p].splitlines()
            title = next((t for _, lv, t in headings(lines) if lv == 1), "")
            if not title:
                raise SystemExit(f"❌ {p}: ไม่มีหัวข้อ # บรรทัดแรก")
            docs.append({"path": p, "title": title, "group": name, "md": texts[p]})

    groups = []
    for name, path, prefix, kind in SOURCES:
        lines = texts[path].splitlines()
        if kind == "stages":
            steps = stage_steps(name, lines, path)
        else:
            title, sec = section(lines, prefix, path)
            header, rows = first_table(sec)
            steps = row_steps(name, header, rows, path, slug(title)) if header else []
        if not steps:
            raise SystemExit(f"❌ {path}: ดึงขั้นตอนของ '{name}' ไม่ได้ — ตารางต้นทางเปลี่ยนรูปแบบ?")
        groups.append({"name": name, "src": path, "steps": steps})

    title, sec = section(texts[MILESTONES[0]].splitlines(), MILESTONES[1], MILESTONES[0])
    header, rows = first_table(sec)
    milestones = row_steps("milestone", header, rows, MILESTONES[0], slug(title))
    for m in milestones:
        m["label_head"] = header[1]
    title, sec = section(texts[GANTT[0]].splitlines(), GANTT[1], GANTT[0])
    block = re.search(r"```mermaid\n(.*?)```", "\n".join(sec), re.S)
    if not milestones or not block:
        raise SystemExit(f"❌ {K}: ไม่เจอตาราง Milestone หรือ Gantt")

    data = {"built": datetime.now().strftime("%d/%m/%Y %H:%M"), "docs": docs, "name": NAME,
            "title": TITLE, "lead": LEAD, "hidden": [OUTSIDE],
            "roadmap": {"groups": groups, "milestones": milestones,
                        "gantt": block.group(1), "gantt_src": [GANTT[0], slug(title)]}}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = (HERE / "template.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    (HERE / "index.html").write_text(html, encoding="utf-8")

    shown = sum(d["group"] != OUTSIDE for d in docs)
    print(f"✅ {shown} เอกสารงาน 4 (+{len(docs) - shown} ไฟล์นอกงาน 4 เปิดจากลิงก์ได้) → viewer/index.html")
    for g in groups:
        kids = sum(len(s.get("children", [])) for s in g["steps"])
        print(f"   {g['name']}: {len(g['steps'])} ขั้น" + (f" (+{kids} ขั้นย่อย)" if kids else ""))
    print(f"   Milestone: {len(milestones)}")


if __name__ == "__main__":
    assert slug("1. คำตอบตรงๆ: 04 ครบ?") == "1-คำตอบตรงๆ-04-ครบ"
    main()
