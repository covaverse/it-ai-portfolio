# 🧱 งานที่ 4c — คู่มือก่อสร้าง: ERPNext + ชั้น AI ที่คุมเอง

> คู่มือลงมือสร้าง [งานที่ 4](04-enterprise-os.md) ทีละขั้น ตั้งแต่ติดตั้งเครื่องมือจนส่งมอบ
> 04 บอกว่า "ระบบหน้าตาเป็นยังไง" — ไฟล์นี้บอกว่า **"สร้างอะไรก่อน-หลัง ด้วยอะไร และรู้ได้ยังไงว่าขั้นนั้นเสร็จจริง"**
> ← [งานที่ 4](04-enterprise-os.md) · [04a](04a-company-blueprint.md) · [04b](04b-depa-product-track.md) · [MD หลัก](../README.md)

| หัวข้อ | สรุป |
|---|---|
| **ภาพรวม** | ซื้อบ้านที่โครงสร้างเสร็จแล้ว (ERPNext) → จัดห้องให้เป็นบริษัทไทย (ตั้งค่า) → **วางระบบ smart home ของเราเอง (ชั้น AI)** ซึ่งต้องมีฐานและเสาของตัวเอง |
| **เริ่มที่** | Stage 1: Docker + ERPNext + erpnext_thailand + repo ของชั้น AI + CI |
| **ขั้นที่สำคัญที่สุด** | Stage 3: เสาของชั้น AI — AI ใช้สิทธิ์ของใคร · ระดับอิสระ · การอนุมัติ · audit · webhook ไม่ซ้ำ |
| **เวลา (เต็มเวลา)** | MVP ~8–9 สัปดาห์ · ครบ ~11–12 สัปดาห์ (part-time คูณ ~2) |
| **เครื่องคุณตอนนี้** | มีแล้ว: Git 2.51 · Python 3.12 · Node 22 · pnpm 10 — **ยังขาด: Docker Desktop, uv** |

---

## สารบัญ
1. [บ้าน ↔ ระบบ](#1-บ้าน--ระบบ)
2. [กฎลำดับการก่อสร้าง 6 ข้อ](#2-กฎลำดับการก่อสร้าง-6-ข้อ)
3. [เสาเข็ม 12 ต้นที่ห้ามข้าม](#3-เสาเข็ม-12-ต้นที่ห้ามข้าม)
4. [Stage 0 — แบบบ้าน](#4-stage-0--แบบบ้าน)
5. [Stage 1 — ฐานราก](#5-stage-1--ฐานราก)
6. [Stage 2 — จัดบ้านให้เป็นบริษัทไทย (ตั้งค่า ERPNext)](#6-stage-2--จัดบ้านให้เป็นบริษัทไทย-ตั้งค่า-erpnext)
7. [Stage 3 — เสาและคานของชั้น AI](#7-stage-3--เสาและคานของชั้น-ai)
8. [Stage 4 — ห้องตัวอย่าง (APX แบบบางครบเส้น)](#8-stage-4--ห้องตัวอย่าง-apx-แบบบางครบเส้น)
9. [Stage 5 — Agent ทีละตัว](#9-stage-5--agent-ทีละตัว)
10. [Stage 6 — AI Workspace และ Dashboard](#10-stage-6--ai-workspace-และ-dashboard)
11. [Stage 7 — ตรวจรับ](#11-stage-7--ตรวจรับ)
12. [Stage 8 — ต่อเติม](#12-stage-8--ต่อเติม)
13. [แผนรายสัปดาห์](#13-แผนรายสัปดาห์)
14. [งานที่คนมักทำผิด](#14-งานที่คนมักทำผิด)

---

## 1. บ้าน ↔ ระบบ

| ชั้นของบ้าน | ในระบบคือ | ใครสร้าง |
|---|---|---|
| แบบบ้าน | ผูก flow กับ DocType · policy ระดับอิสระ · แผนชุดทดสอบ | เรา |
| ฐานราก | Docker · ERPNext stack · repo ชั้น AI · PostgreSQL · CI · test harness | เรา (ประกอบของสำเร็จ) |
| โครงสร้างบ้าน | บัญชี เอกสาร สิทธิ์ workflow ภาษีไทย | **ERPNext + erpnext_thailand** |
| จัดห้อง | ตั้งค่าบริษัท ภาษี role workflow ด้วยสคริปต์ + seed | เรา |
| **ฐานและเสาของ smart home** | Gateway: สิทธิ์ · ระดับอิสระ · อนุมัติ · audit · webhook · LLM gateway · tool registry | **เรา — หัวใจของงาน** |
| ห้องตัวอย่าง | APX แบบบางที่วิ่งครบเส้น | เรา |
| อุปกรณ์ smart home | Agent: APX · ตรวจสัญญา · Copilot · ตามหนี้ · ปิดงวด · HelpBot | เรา |
| ตกแต่ง | AI Workspace · Dashboard · Eval dashboard | เรา |
| ตรวจรับ | E2E · security · backup · deploy · วิดีโอ | เรา |

```mermaid
flowchart BT
    S0["Stage 0 · แบบบ้าน<br/>flow → DocType · policy · แผน eval"]
    S1["Stage 1 · ฐานราก<br/>Docker · ERPNext · repo · Postgres · CI"]
    S2["Stage 2 · จัดบ้าน<br/>ตั้งค่า ERPNext ด้วยสคริปต์ + test ภาษีไทย"]
    S3["Stage 3 · เสาของชั้น AI<br/>สิทธิ์ · ระดับอิสระ · อนุมัติ · audit · webhook · LLM"]
    S4["Stage 4 · ห้องตัวอย่าง<br/>APX แบบบางครบเส้น"]
    S5A["5.1 APX เต็ม"]
    S5B["5.2 RAG + ตรวจสัญญา"]
    S5C["5.3 Copilot"]
    S5D["5.4 ตามหนี้ + ปิดงวด + HelpBot"]
    S6["Stage 6 · AI Workspace + Eval dashboard"]
    S7["Stage 7 · ตรวจรับ"]
    S0 --> S1 --> S2 --> S3 --> S4 --> S5A
    S4 --> S5B --> S5C
    S5A --> S5D
    S5C --> S5D
    S5D --> S6 --> S7
```

---

## 2. กฎลำดับการก่อสร้าง 6 ข้อ

| # | กฎ | ทำไม |
|---|---|---|
| 1 | **ตั้งค่า ERPNext ด้วยสคริปต์ ไม่คลิกมือ** | ทำซ้ำได้บนเครื่องอื่น ใช้ใน CI ได้ และคนอื่นรันตามได้ |
| 2 | **ห้ามแก้โค้ดแกน ERPNext** — ใช้ custom app / hooks / API เท่านั้น | อัปเกรดได้ ไม่ติดหนี้ทางเทคนิค |
| 3 | **เสาของชั้น AI ก่อน agent** | agent ทุกตัวต้องผ่านสิทธิ์ ระดับอิสระ และ audit แบบเดียวกัน |
| 4 | **บางแต่ครบเส้นก่อนหนา** | APX แบบบางพิสูจน์ว่าเสาทุกต้นใช้ได้จริง ก่อนสร้าง agent ตัวที่ 2 |
| 5 | **ชุดทดสอบก่อนเลื่อนระดับอิสระ** | เลื่อนระดับเพราะตัวเลข ไม่ใช่ความรู้สึก |
| 6 | **test พร้อมเสาแต่ละต้น** | test ตอนท้ายจะไม่มีวันได้เขียน |

---

## 3. เสาเข็ม 12 ต้นที่ห้ามข้าม

| # | เสาเข็ม | ทำตอน | ถ้าข้าม |
|---|---|---|---|
| 1 | Pin เวอร์ชัน ERPNext · erpnext_thailand · Frappe HR · โมเดล AI | Stage 1 | อัปเกรดเองโดยไม่รู้ตัวแล้วพัง |
| 2 | Migration (Alembic) สำหรับ DB ของเรา | Stage 1 | สร้าง DB ซ้ำบนเครื่องอื่นไม่ได้ |
| 3 | CI + test harness | Stage 1 | bug สะสม |
| 4 | ตั้งค่า ERPNext เป็นโค้ด + seed ผ่าน API | Stage 2 | เดโมพังแล้วสร้างใหม่ไม่ได้ |
| 5 | Test ภาษีไทย (GL ที่ต้องได้) | Stage 2 | อัปเกรดแล้วภาษีผิดโดยไม่รู้ |
| 6 | AI ใช้ token ของผู้สั่ง · งานเบื้องหลังใช้ `ai-agent` ที่สร้างได้แค่ Draft | Stage 3 | AI เห็น/ทำเกินสิทธิ์ |
| 7 | ระดับอิสระ + เพดานถาวร | Stage 3 | AI ลงบัญชีเองโดยไม่มีใครยืนยัน |
| 8 | Audit hash chain | Stage 3 | ประวัติ AI ย้อนไม่ได้ |
| 9 | Webhook ตรวจลายเซ็น + กันซ้ำ | Stage 3 | event ปลอม / ทำงานซ้ำ |
| 10 | Data classification (local เป็นค่าเริ่มต้น) | Stage 3 | ข้อมูลลับออกนอกองค์กร |
| 11 | ไม่ให้ LLM เขียน SQL · เอกสาร = ข้อมูล ไม่ใช่คำสั่ง | Stage 3 | prompt injection / ข้อมูลรั่ว |
| 12 | ชุดทดสอบ + วงจรเปลี่ยนโมเดล | Stage 3–5 | เปลี่ยนโมเดลแล้วไม่รู้ว่าดีขึ้นหรือแย่ลง |

---

## 4. Stage 0 — แบบบ้าน

**เวลา:** ~3–5 วัน

| ชิ้นงาน | ทำอะไร | อ้างอิง |
|---|---|---|
| ผูก flow กับ DocType | ตาราง "ขั้น → DocType → ใครทำ → AI ช่วย" ของ O2C / P2P / ปิดงบ | [04 ข้อ 4–6](04-enterprise-os.md#4-flow-a--ขาย--รับเงิน) |
| Role ต่อตำแหน่ง | แปลง 48 ตำแหน่งเป็น Role Profile ของ ERPNext | [04a ข้อ 11](04a-company-blueprint.md#11-แปลงผังบริษัทเป็น-erpnext) |
| Policy ฉบับแรก | `autonomy.yaml` + `data_classification.yaml` | [04 ข้อ 9.3, 12](04-enterprise-os.md#93-ระดับอิสระ-autonomy-dial) |
| แผนชุดทดสอบ | ชุดไหน กี่ข้อ หาข้อมูลจากไหน (ใบกำกับสมมติ/ปกปิด) | [04 ข้อ 13](04-enterprise-os.md#13-eval-และวงจรอัปเกรดโมเดล) |
| ADR | 005 (ไม่สร้าง ERP เอง) · 006 (AI ใช้สิทธิ์ของใคร) · 007 (ระดับอิสระ) | [04 ข้อ 1](04-enterprise-os.md#1-ทำไมไม่สร้าง-erp-เอง-adr-005) |

**Gate:** ตารางผูก flow ครบ 3 flow · autonomy.yaml มีทุก action ใน Tool Catalog · มีคนรู้บัญชีช่วยดูตาราง GL ที่ต้องได้ ([04 ข้อ 14](04-enterprise-os.md#14-ภาษีไทย-ตรวจผลกับ-erpnext))

---

## 5. Stage 1 — ฐานราก

**เวลา:** ~4–5 วัน · **เป้าหมาย:** ERPNext ไทยเปิดได้ + Gateway ตอบ `/health` + CI เขียว (รวมสแกนความปลอดภัย)

### 5.1 เครื่องมือ

| เครื่องมือ | ใช้ทำอะไร | สถานะในเครื่องคุณ |
|---|---|---|
| Git · Python 3.12 · Node 22 · pnpm | — | ✅ |
| **Docker Desktop** (WSL2) | ERPNext stack, PostgreSQL, Ollama, Langfuse | ❌ ต้องติดตั้ง |
| **uv** | จัดการ Python package ของชั้น AI | ❌ ต้องติดตั้ง |
| DBeaver | เปิดดูทั้ง MariaDB และ PostgreSQL | — |

```powershell
winget install --id Docker.DockerDesktop -e
winget install --id astral-sh.uv -e
```

> ERPNext stack ใช้หน่วยความจำมาก (หลายคอนเทนเนอร์) — ตั้ง Docker Desktop ให้ใช้ RAM อย่างน้อย 8 GB · ถ้ายังไม่เปิด WSL2 ให้รัน `wsl --install` แล้วรีสตาร์ต

### 5.2 ERPNext ด้วย frappe_docker

> ข้อมูลตรวจเมื่อ 16 ต.ค. 2569 — รายละเอียดใน [research/erpnext-reference.md](research/erpnext-reference.md#2-ติดตั้งด้วย-frappe_docker)

1. Clone [frappe/frappe_docker](https://github.com/frappe/frappe_docker)
2. **ลองเร็ว:** `docker compose -f pwd.yml up -d` → เปิด `http://localhost:8080` → login `Administrator` / `admin` · ไฟล์นี้ใช้ทดลองเท่านั้น **ติดตั้ง erpnext_thailand ไม่ได้**
3. **ใช้จริง:** build image ที่รวม app เพิ่มตาม `docs/02-setup/02-build-setup.md` แล้วรันด้วย `compose.yaml` + ไฟล์ใน `overrides/` (ตัวอย่างเครื่องเดียว: `docs/02-setup/07-single-server-example.md`)
4. Pin ทุก app ที่ **`version-16`** — erpnext_thailand มี branch `version-16` ให้ตรงกับ ERPNext v16 (ล่าสุด v16.51.1)

```json
[
  { "url": "https://github.com/frappe/erpnext", "branch": "version-16" },
  { "url": "https://github.com/frappe/hrms", "branch": "version-16" },
  { "url": "https://github.com/ecosoft-frappe/erpnext_thailand", "branch": "version-16" },
  { "url": "https://github.com/<you>/ai_bridge", "branch": "main" }
]
```

5. สร้าง site → ติดตั้ง app ทั้งหมด → สร้าง **API key/secret ของ user ผู้ดูแลการตั้งค่า** (ใช้ใน Stage 2 เท่านั้น)

### 5.3 Repo ชั้น AI

```powershell
mkdir ai-backoffice; cd ai-backoffice; git init
mkdir services\gateway, apps, erpnext\setup, frappe-apps, eval, seed, docs\adr

cd services\gateway
uv init --app
uv add fastapi "uvicorn[standard]" sqlalchemy "psycopg[binary]" alembic pydantic-settings httpx mcp
uv add --dev pytest ruff respx
uv run alembic init migrations

cd ..\..\apps; pnpm create next-app@latest web --ts --tailwind --app --eslint
```

### 5.4 docker-compose ส่วนของเรา (ต่อกับ network ของ ERPNext stack)

```yaml
services:
  aidb:
    image: pgvector/pgvector:pg16
    environment: { POSTGRES_USER: ai_owner, POSTGRES_PASSWORD: dev_only, POSTGRES_DB: ai_layer, TZ: UTC }
    volumes: [aidbdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD-SHELL", "pg_isready -U ai_owner -d ai_layer"], interval: 5s }

  gateway:
    build: ./services/gateway
    env_file: .env
    depends_on: { aidb: { condition: service_healthy } }
    ports: ["8000:8000"]

  worker:
    build: ./services/gateway
    command: ["uv", "run", "python", "-m", "inbox_worker"]
    env_file: .env
    depends_on: { aidb: { condition: service_healthy } }

  web:
    build: ./apps/web
    ports: ["3000:3000"]

  ollama:
    image: ollama/ollama
    volumes: [ollama:/root/.ollama]
    # เครื่องที่มีการ์ดจอ NVIDIA: เพิ่ม deploy.resources.reservations.devices ตามเอกสาร Docker

volumes: { aidbdata: {}, ollama: {} }
```

```env
# .env.example — คัดลอกเป็น .env (ห้าม commit .env)
ERP_URL=http://frontend:8080              # ชื่อ service ของ ERPNext ใน frappe_docker
ERP_AGENT_KEY=                            # API key ของ ai-agent (สร้างใน Stage 3)
ERP_AGENT_SECRET=
ERP_WEBHOOK_SECRET=
ERP_OAUTH_CLIENT_ID=
DATABASE_URL=postgresql+psycopg://ai_owner:dev_only@aidb:5432/ai_layer
LLM_BASE_URL=http://ollama:11434/v1
LLM_MODEL=<รุ่นที่ผ่าน eval>
```

### 5.5 Test harness + CI

- `tests/conftest.py`: session ต่อ test ที่ rollback ทุกครั้ง (รูปแบบเดียวกับงาน 1–3)
- เรียก ERPNext ใน **unit test** ด้วย mock (`respx`) · เรียก ERPNext จริงใน **integration test** (CI เปิด ERPNext stack)
- CI: `ruff` → `pytest` (unit) → เปิด ERPNext + ตั้งค่า (Stage 2) → integration test → `pnpm build`
- สแกนความปลอดภัยใน CI: gitleaks (secret) · pip-audit + npm audit (ไลบรารี) · Trivy (อิมเมจ) · Semgrep + Bandit (โค้ด) · เปิด Dependabot และ push protection ของ GitHub ([04l](04l-security-baseline.md#3-12-ชั้นป้องกัน))

### 5.6 Skill ตรวจงาน `verify-p4`

skill ประจำโปรเจกต์ที่บอก Claude ว่าเปิดระบบยังไง ตรวจอะไร และเก็บหลักฐานอะไร · ไอเดียจาก [verification-skill-example](https://github.com/poteto/verification-skill-example) ของ Lauren Tan แต่เขียนเองทั้งหมด (ต้นฉบับไม่มีสคริปต์ให้ใช้)

```text
.claude/skills/verify-p4/
  SKILL.md        # doctor → เปิดระบบ → ตรวจตามแผนที่ → เก็บหลักฐาน → ปิด
  features/
    README.md     # ลำดับตรวจทั้งระบบ · รันก่อน git tag
    <ฝ่าย>.md      # 1 ไฟล์ต่อฝ่ายจาก 04g: มีอะไร · ผู้ใช้เข้าถึงยังไง · ตรวจด้วยคำสั่งไหน · จุดที่มักพัง
```

- **Stage 1 ทำแค่โครง (~ครึ่งวัน):** `doctor` = `docker compose ps` ครบ · `GET /health` ตอบ ok · login ERPNext ได้ · โฟลเดอร์ `features/` ยังว่าง
- **ทุก Gate ต่อจากนี้:** เพิ่มหรือแก้ไฟล์ฟีเจอร์ของสิ่งที่เพิ่งสร้างใน commit เดียวกับโค้ด แล้วรัน `verify-p4` ก่อน `git tag`
- ขับหน้าเว็บด้วย skill `webapp-testing` (Playwright) · หลักฐาน = ภาพหน้าจอ · ผล API · แถวใน audit log · ใช้ข้อมูลสมมติเท่านั้น (ฟีเจอร์แต่ละฝ่ายดูจาก [04g](04g-department-flows.md))

**Gate Stage 1:**
- [ ] เปิด ERPNext ได้ เห็นเมนูของ erpnext_thailand
- [ ] `GET /health` ของ Gateway ตอบ `{"db": "ok", "erp": "ok", "llm": "ok"}`
- [ ] skill `verify-p4` รัน `doctor` ผ่านครบ
- [ ] CI เขียว รวมสแกนความปลอดภัย ไม่มี High ค้าง · `git tag stage-1`

---

## 6. Stage 2 — จัดบ้านให้เป็นบริษัทไทย (ตั้งค่า ERPNext)

**เวลา:** ~4–5 วัน · **ทุกอย่างเป็นสคริปต์ใน `erpnext/setup/`** รันซ้ำได้ไม่พัง

| ลำดับ | ตั้งค่าอะไร | อ้างอิง |
|---|---|---|
| 1 | บริษัท ปีบัญชี สกุลเงิน ผังบัญชี | [04a ข้อ 3](04a-company-blueprint.md#3-company-profile-ของบริษัทสมมติ) |
| 2 | ภาษี: VAT 7%, ประเภทหัก ณ ที่จ่าย, บัญชีภาษีขายยังไม่ถึงกำหนด (ตามคู่มือ erpnext_thailand) | erpnext_thailand README |
| 3 | Naming Series ของเอกสารภาษี | — |
| 4 | Role Profile ต่อตำแหน่ง + ผู้ใช้ demo | [04a ข้อ 11](04a-company-blueprint.md#11-แปลงผังบริษัทเป็น-erpnext) |
| 5 | Workflow อนุมัติ (Material Request, Purchase Order, Quotation) ตามวงเงิน | [04a ข้อ 11](04a-company-blueprint.md#11-แปลงผังบริษัทเป็น-erpnext) |
| 6 | Seed: ลูกค้า ผู้ขาย สินค้า ธุรกรรม 3 เดือน | [04 ข้อ 18](04-enterprise-os.md#18-demo-strategy) |

```python
# erpnext/setup/erp_api.py — upsert ผ่าน REST API (รันซ้ำได้)
import os
from urllib.parse import quote
import httpx

ERP = os.environ["ERP_URL"]
AUTH = {"Authorization": f"token {os.environ['ERP_ADMIN_KEY']}:{os.environ['ERP_ADMIN_SECRET']}"}

def upsert(doctype: str, name: str, data: dict) -> None:
    url = f"{ERP}/api/resource/{quote(doctype)}"
    r = httpx.get(f"{url}/{quote(name)}", headers=AUTH)
    if r.status_code == 404:
        httpx.post(url, json={"name": name, **data}, headers=AUTH).raise_for_status()
    else:
        r.raise_for_status()
        httpx.put(f"{url}/{quote(name)}", json=data, headers=AUTH).raise_for_status()
```

### Test ภาษีไทย (ทำใน Stage นี้ ไม่ใช่ตอนท้าย)

สร้างเอกสารทุกสถานการณ์ใน [04 ข้อ 14](04-enterprise-os.md#14-ภาษีไทย-ตรวจผลกับ-erpnext) ผ่าน API → Submit → ดึง GL Entry → เทียบกับตาราง

```python
# tests/integration/test_thai_tax.py (โครง)
def test_sell_goods_with_vat(erp):
    inv = erp.create_and_submit("Sales Invoice", customer="C-001", items=[{"item_code": "HW-01", "qty": 1, "rate": 100000}])
    gl = erp.gl_entries(inv)
    assert gl["ลูกหนี้การค้า"].debit == 107000
    assert gl["ขาย"].credit == 100000
    assert gl["ภาษีขาย"].credit == 7000
```

**Gate Stage 2:** สคริปต์รันบน site ใหม่แล้วได้บริษัทครบ · test ภาษีไทยผ่านทุกสถานการณ์ · `git tag stage-2`

> **สาย ERP (MVP+):** สาขา 2 · ผลิต · สต๊อก · ใบเบิก · ครุภัณฑ์ · ลงเวลา · รายงานแผนก/สาขา ใช้วิธีเดียวกัน (ตั้งค่าด้วยสคริปต์ + test) ตามรายละเอียดใน [04d](04d-erp-implementation.md) — ทำหลัง MVP ส่งมอบแล้ว (~3–4.5 สัปดาห์) · เงินเดือนไทยอยู่ใน [งาน 5](../05-thai-payroll-erpnext/README.md)

---

## 7. Stage 3 — เสาและคานของชั้น AI

**เวลา:** ~9–11 วัน · **ขั้นที่สำคัญที่สุด** — ทุก agent สร้างบนสิ่งนี้

| # | เสา | ไฟล์ | Test ที่ต้องมี | วัน |
|---|---|---|---|---|
| 1 | **ERP client** (เรียก ERPNext ที่เดียว) | `erp/client.py` | retry เมื่อ ERPNext ล่ม · ไม่ log secret | 1 |
| 2 | **Identity**: login ผ่าน OAuth ของ Frappe · token ผู้สั่ง · user `ai-agent` | `auth.py` · `ai_bridge` (role AI Agent) | ai-agent Submit ไม่ได้ · token ผู้ใช้ A อ่านของที่ A ไม่มีสิทธิ์ไม่ได้ | 2 |
| 3 | **Policy**: `decide()` + autonomy.yaml + เพดาน + SoD | `policy/` | เพดานถาวรชนะเสมอ · ความมั่นใจต่ำ → L1 · ผู้ขอ = ผู้อนุมัติ → ปฏิเสธ | 1 |
| 4 | **Proposal + การอนุมัติ** | `proposals.py` | อนุมัติแล้ว Submit ด้วย token ผู้อนุมัติ · idempotency key กันทำซ้ำ | 1.5 |
| 5 | **Audit hash chain** | `audit.py` | แก้แถวกลาง → Verify เจอ | 0.5 |
| 6 | **Webhook + Event inbox** | `inbox.py` · `inbox_worker.py` | ไม่มีลายเซ็น → 401 · ส่งซ้ำ → ทำครั้งเดียว · handler พัง 5 ครั้ง → dead letter | 1.5 |
| 7 | **LLM gateway + data classification** | `llm.py` | เอกสาร confidential เรียก cloud → ถูกบล็อก · log token/เวลา | 1 |
| 8 | **Tool registry + MCP server** | `tools/` · `main.py` | agent เรียกเครื่องมือนอก allowlist → ปฏิเสธ | 1 |
| 9 | **Threat model** (STRIDE + OWASP LLM Top 10) ของ Gateway | `docs/threat-model.md` | ทุกภัยมีตัวป้องกันหรือ test ผูกไว้ ([04l](04l-security-baseline.md)) | 1 |

### ตัวอย่างเสาหลัก

```python
# policy.py — ระดับอิสระ (04 ข้อ 9.3)
def decide(action: str, confidence: float) -> int:
    p = POLICY[action]
    level = min(p.level, p.max)
    if confidence < p.min_confidence:
        level = min(level, 1)
    return level

assert decide("purchase_invoice.submit", 0.99) == 1   # เพดานถาวร
```

```python
# inbox.py — webhook จาก ERPNext: ตรวจลายเซ็น แล้วกันซ้ำด้วย UNIQUE
# Frappe เซ็นด้วย base64(HMAC-SHA256(secret, frappe.as_json(payload))) ใน header X-Frappe-Webhook-Signature
def frappe_signature(payload: dict) -> str:
    # ให้ตรงกับ frappe.as_json — ยืนยันรูปแบบด้วย integration test ที่ยิง webhook จริงจาก ERPNext
    body = json.dumps(payload, indent=1, sort_keys=True, separators=(",", ": "), default=str)
    return base64.b64encode(hmac.new(WEBHOOK_SECRET, body.encode(), hashlib.sha256).digest()).decode()

@app.post("/webhooks/erpnext")
async def erpnext_webhook(request: Request, db: Session = Depends(get_db)):
    ev = json.loads(await request.body())     # ตั้ง webhook ให้ส่ง doctype, name, event, modified
    if not hmac.compare_digest(frappe_signature(ev), request.headers.get("X-Frappe-Webhook-Signature", "")):
        raise HTTPException(401)
    key = f"{ev['doctype']}:{ev['name']}:{ev['event']}:{ev['modified']}"
    stmt = insert(EventInbox).values(source="erpnext", dedupe_key=key, event=ev["event"], payload=ev)
    inserted = db.execute(stmt.on_conflict_do_nothing(index_elements=["dedupe_key"])).rowcount
    return {"queued": bool(inserted)}
```

```python
# audit.py — hash chain
def audit(db, actor: str, action: str, detail: dict, proposal_id=None) -> None:
    db.execute(text("SELECT pg_advisory_xact_lock(1)"))   # ponytail: ต่อคิว audit ทั้งระบบ · แยก chain ถ้าช้า
    prev = db.scalar(select(AuditLog.hash).order_by(AuditLog.id.desc()).limit(1)) or ""
    payload = json.dumps({"actor": actor, "action": action, "detail": detail}, sort_keys=True, default=str)
    db.add(AuditLog(proposal_id=proposal_id, actor=actor, action=action, detail=detail,
                    prev_hash=prev, hash=hashlib.sha256((prev + payload).encode()).hexdigest()))
```

**Gate Stage 3:**
- [ ] ทุกเสามี test และผ่านใน CI
- [ ] ใช้ key ของ ai-agent ลอง Submit เอกสารจริงใน ERPNext → ถูกปฏิเสธ
- [ ] AI Workspace login ด้วยบัญชี ERPNext ได้
- [ ] `git tag stage-3`

---

## 8. Stage 4 — ห้องตัวอย่าง (APX แบบบางครบเส้น)

**เวลา:** ~3 วัน · เส้นทางบางที่สุดที่ผ่านเสาทุกต้น — หน้าตาเรียบๆ ได้

```mermaid
sequenceDiagram
    autonumber
    actor A as นักบัญชี
    participant W as AI Workspace
    participant G as Gateway
    participant O as OCR + LLM (Local)
    participant E as ERPNext
    A->>W: อัปโหลดใบกำกับภาษี 1 ใบ
    W->>G: ไฟล์ + token ของนักบัญชี
    G->>O: อ่าน → JSON
    G->>G: กฎตรวจ + decide() = L1
    G->>E: สร้าง Purchase Invoice Draft (ai-agent)
    G->>G: Proposal + audit
    W-->>A: แสดงร่าง + ช่องที่ไม่มั่นใจ
    A->>W: อนุมัติ
    G->>E: Submit ด้วย token นักบัญชี
    E-->>G: webhook on_submit
    G->>G: inbox → audit → บันทึกค่าที่คนแก้ลงชุด eval
```

| ทำ | ยังไม่ทำ (ไว้ Stage 5) |
|---|---|
| อัปโหลดทีละใบ · ผู้ขาย 1 ราย (seed) | รับทางอีเมล · หลายหน้า |
| กฎตรวจพื้นฐาน (13 หลัก, VAT, ยอดรวม) | จับคู่ PO · ตรวจซ้ำ |
| กล่องอนุมัติแบบรายการธรรมดา | Dashboard |

**Gate Stage 4:** Playwright E2E ของเส้นนี้ผ่าน · audit ครบทุกขั้น · ปิด worker แล้วเปิดใหม่ webhook ที่ค้างทำงานครบไม่ซ้ำ · deploy ขึ้น staging · `git tag stage-4`

> ติดหนักที่ขั้นนี้ = เสาใน Stage 3 มีปัญหา → แก้ตอนนี้ถูกกว่าแก้หลังมี 6 agent

---

## 9. Stage 5 — Agent ทีละตัว

| ลำดับ | Agent | ทำอะไรเพิ่ม | ชุดทดสอบ / เกณฑ์ | วัน |
|---|---|---|---|---|
| 5.1 | **APX เต็ม** | รับอีเมล · หลายหน้า · จับคู่ PO + Purchase Receipt · ตรวจซ้ำ · ไฮไลต์ช่องไม่มั่นใจ · **ตัวอ่านสลับได้ 2 แบบ** (OCR + LLM / โมเดลอ่านภาพตรง) | ใบกำกับ 300 ใบ · ช่องสำคัญ ≥ 95% · ตารางเทียบ 2 ตัวอ่าน (แม่น · เวลา · ต้นทุนต่อใบ) | 5–6 |
| 5.2 | **RAG แบบย่อ + ตรวจสัญญา** | สร้างเครื่อง RAG ในงาน 4 (ดึงข้อความ PDF ไทย · chunk · hybrid search + กรองสิทธิ์) · sync `allowed_roles` จาก ERPNext · แนบความเห็นใน Contract | สัญญา 50 ฉบับ · Recall ≥ 85% · ค้นข้ามสิทธิ์ = 0 | 10–13 |
| 5.3 | **Copilot** | แผนคิวรี (JSON) → ตรวจ allowlist → เรียก API ด้วย token ผู้ถาม → สรุป + ลิงก์ | คำถาม 100 ข้อ · ถูก ≥ 90% · ล้ำสิทธิ์ = 0 | 4 |
| 5.4 | ตามหนี้ + ปิดงวด | ร่างอีเมลจาก AR aging · checklist ปิดงวด · ร่างคำอธิบายงบ | ตรวจตัวเลขในข้อความตรงกับรายงาน 100% | 3 |
| 5.5 | HelpBot | Hire-to-Retire: Employee → User + Role Profile · ปิดบัญชีวันสุดท้าย · อนุมัติผ่านกล่องอนุมัติ (P5) · เขียนด้วย LangGraph ได้ (ADR-014) | บัญชีค้างของคนลาออก = 0 | 3–5 |
| 5.6 | **สะพานที่ 2: CSV / Excel** ([04h](04h-connectors.md)) | แยก `Connector` ออกจาก `erp/` · รูปแบบกลาง · ส่งออกไฟล์นำเข้าแทนการเขียนกลับ · ให้ coding agent เขียนสะพานจาก spec + tests | contract tests ชุดเดียวผ่านทั้ง ERPNext และ CSV · APX ทำงานได้ทั้ง 2 สะพานโดยไม่แก้ agent | 3 |

ทุก agent ต้องผ่าน **ชุด prompt injection** (PDF / อีเมล / สัญญาที่ซ่อนคำสั่ง) = 0 action เกินระดับ ก่อน merge

**Gate Stage 5:** ทุก agent ผ่านเกณฑ์ eval ของตัวเอง · รายงาน eval รวมอยู่ใน `eval/reports/` · `git tag stage-5`

---

## 10. Stage 6 — AI Workspace และ Dashboard

**เวลา:** ~6–8 วัน · **ไม่สร้างหน้าจอซ้ำกับ ERPNext Desk**

| หน้า | ทำอะไร |
|---|---|
| กล่องอนุมัติ | Proposal ทุกตัว · ดูเหตุผล/ความมั่นใจ · อนุมัติ/แก้/ปฏิเสธ |
| อัปโหลดเอกสาร | APX |
| Copilot | ถามข้อมูล + ลิงก์ไปเอกสารใน ERPNext |
| Eval Dashboard | ผลแต่ละชุด · เทียบโมเดล · ประวัติ changelog |
| ระดับอิสระ | ดู/ปรับระดับต่อ action (เฉพาะ admin · ห้ามเกินเพดาน) |
| Audit | ค้นหา + ปุ่ม Verify chain |
| ผู้บริหาร | กราฟรายได้ ค่าใช้จ่าย กระแสเงินสด AR/AP จากรายงาน ERPNext (component จากงาน 3) |

เพิ่มปุ่ม "ส่งให้ AI ตรวจ" ใน ERPNext Desk ผ่าน `ai_bridge` (Client Script) เพื่อให้คนทำงานใน Desk ไม่ต้องสลับหน้าจอ

---

## 11. Stage 7 — ตรวจรับ

**เวลา:** ~5–7 วัน

| หมวด | ตรวจอะไร |
|---|---|
| E2E | Playwright "A Day in the Life" ตาม [04 ข้อ 18](04-enterprise-os.md#18-demo-strategy) |
| Security | ทุกข้อใน [04 ข้อ 15](04-enterprise-os.md#15-security) ผ่าน · ZAP baseline · ASVS L2 · `claude-security` ทั้ง repo ไม่มี High ค้าง ([04l](04l-security-baseline.md#5-10-ข้อต้องทำก่อนรับลูกค้ารายแรก)) |
| ข้อมูล | Backup ทั้ง MariaDB (ERPNext) และ PostgreSQL (ชั้น AI) + ทดลอง restore จริง 1 ครั้ง |
| Deploy | VPS + Docker Compose · reverse proxy HTTPS (Caddy) + firewall เปิดแค่ 443 · DB ไม่ publish port · ช่วงเดโมใช้เครื่องที่มี GPU |
| Demo | บัญชีต่อตำแหน่ง · วิดีโอ 3–5 นาที · ฉากเปลี่ยนโมเดลสด (Local ↔ Azure OpenAI เฉพาะข้อมูลไม่ลับ) · **ฉากสลับสะพาน ERPNext ↔ CSV** |
| เอกสาร | README + ADR 005–007 + Prior Art + Limitations |

**Gate:** Checklist พอร์ตใน [04 ข้อ 19](04-enterprise-os.md#19-ความเสี่ยง--checklist--คำถามสัมภาษณ์) ครบ → `git tag v1.0-mvp`

---

## 12. Stage 8 — ต่อเติม

| ต่อเติม | ทำยังไง |
|---|---|
| สะพาน Odoo / Google Sheets / DB อ่านอย่างเดียว | interface แยกแล้วใน 5.6 → เพิ่มตัวใหม่ + ผ่าน contract tests ([04h ข้อ 4](04h-connectors.md#4-สัญญาของสะพาน)) · ทำเมื่อมีลูกค้าใช้ |
| test แยกลูกค้า | ค้นข้ามลูกค้า = 0 ทั้ง DB และคลัง RAG · ทำก่อนรับลูกค้ารายที่ 2 |
| ชุดนัดหมาย (Booking Pack) | [04h ข้อ 7.2](04h-connectors.md#72-ชุดนัดหมาย-booking-pack--ใช้ซ้ำกับธุรกิจบริการที่มีการนัด) · สร้างเมื่อมีสถาบันสอนนำร่อง ([04e ข้อ 10.3](04e-saas-business-model.md#103-กลุ่มเป้าหมาย)) |
| fine-tune เล็ก (Hugging Face) | ทางเลือก: reranker จากค่าที่คนแก้ใน APX · ต้องชนะตัวเดิมใน eval ถึงใช้ |
| APX หลายลูกค้า (04b) | `tenant_id` + Row-Level Security ใน DB ของเรา · เก็บ URL/key ERPNext ของแต่ละลูกค้าแบบเข้ารหัส |
| vLLM | เมื่อผู้ใช้พร้อมกันเยอะจน Ollama ไม่พอ |
| AI ภายนอกเรียก MCP server | เปิด endpoint + จำกัดสิทธิ์ต่อ client |
| Agent ใหม่ | เพิ่มเครื่องมือใน registry + policy + ชุดทดสอบ — ไม่ต้องแก้เสา |

---

## 13. แผนรายสัปดาห์

```mermaid
gantt
    title งาน 4 แบบ ERPNext + ชั้น AI (เต็มเวลา)
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    section แบบและฐาน
    Stage 0 แบบบ้าน                 :s0, 2027-02-25, 5d
    Stage 1 ฐานราก                  :s1, after s0, 5d
    Stage 2 ตั้งค่า ERPNext ไทย      :s2, after s1, 6d
    section ชั้น AI
    Stage 3 เสาของชั้น AI           :s3, after s2, 13d
    Stage 4 APX แบบบาง              :s4, after s3, 4d
    APX เต็ม                        :s5a, after s4, 6d
    RAG แบบย่อ และตรวจสัญญา         :s5b, after s5a, 12d
    Copilot                         :s5c, after s5b, 5d
    สะพานที่ 2 CSV                  :s5d, after s5c, 4d
    section ส่งมอบ
    Stage 6 AI Workspace            :s6, after s5d, 9d
    Stage 7 ตรวจรับ                 :s7, after s6, 8d
    section MVP plus
    ตามหนี้ ปิดงวด HelpBot           :s8, after s7, 8d
```

| Stage | Phase ใน [04 ข้อ 17](04-enterprise-os.md#17-ขนาดงานและ-roadmap) | วันทำงาน |
|---|---|---|
| 0 | Phase 0 | 3–5 |
| 1–2 | Phase 1 | 8–10 |
| 3 | Phase 2 | 9–11 |
| 4 + 5.1 | Phase 3 | 8–9 |
| 5.2–5.3 + 5.6 | Phase 4 | 17–20 |
| 6–7 | Phase 5 | 11–15 |
| 5.4–5.5 | MVP+ | 6 |

---

## 14. งานที่คนมักทำผิด

| ทำผิด | เกิดอะไรขึ้น | ทำแทน |
|---|---|---|
| ตั้งค่า ERPNext ด้วยการคลิก | สร้างใหม่ไม่ได้ เดโมพังแล้วกู้ไม่ได้ | สคริปต์ใน `erpnext/setup/` |
| แก้โค้ดแกน ERPNext | อัปเกรดไม่ได้ | custom app / hooks / API |
| ให้ AI ใช้ key ของ Administrator | AI ทำได้ทุกอย่าง · audit ไม่มีความหมาย | token ผู้สั่ง + ai-agent สร้างได้แค่ Draft |
| ให้ LLM เขียน SQL ลง MariaDB | ข้อมูลรั่ว · ข้ามระบบสิทธิ์ | แผนคิวรี → API |
| เลื่อนระดับอิสระเพราะ "รู้สึกว่าเก่งขึ้น" | ผิดพลาดแล้วไม่มีใครเห็น | เลื่อนเมื่อผ่าน `promote_when` เท่านั้น |
| ใช้ AI ที่ติดมากับ ERP/Odoo | ข้อมูลออกนอก · คุมไม่ได้ | ทุกอย่างผ่าน Gateway |
| สร้างหน้าจอซ้ำกับ ERPNext Desk | เสียเวลาสองเท่า | Workspace เฉพาะงาน AI |
| ไม่ pin เวอร์ชัน | วันหนึ่ง build ใหม่แล้วพัง | pin ทุกตัวใน `apps.json` และ lockfile |
| เก็บ test ภาษีไทยไว้ทีหลัง | อัปเกรดแล้วภาษีผิดโดยไม่รู้ | ทำใน Stage 2 |
| เขียนลงฐานข้อมูลของลูกค้าตรงๆ | ข้ามระบบสิทธิ์ของเขา · พังแล้วเราผิด | สะพานสร้างแค่ร่าง หรือส่งไฟล์นำเข้า |
| รับสะพานใหม่โดยไม่มี contract tests | ลูกค้าคนใหม่ทำของเก่าพัง | สะพานเสร็จ = ผ่าน tests ชุดเดียวกับตัวเดิม |
| ผูกสิทธิ์/อนุมัติไว้ใน framework ของ agent | เปลี่ยน framework แล้วความปลอดภัยหาย | สิทธิ์ อนุมัติ audit อยู่ที่ Gateway เสมอ (ADR-014) |

← [งานที่ 4](04-enterprise-os.md) · [MD หลัก](../README.md)
