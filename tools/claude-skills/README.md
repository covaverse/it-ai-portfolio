# 🧰 แพ็ก Skill สำหรับพัฒนางาน 4 (ยังไม่ติดตั้ง)

> รวม skill / plugin ที่จำเป็นและน่าเชื่อถือสำหรับงาน 4 (Enterprise OS บน ERPNext) — **ติดตั้งทีเดียวด้วยคำสั่งเดียวเมื่อพร้อม**
> รีวิวต้นทางแล้วเมื่อ 16 ต.ค. 2569 · รายการและ commit ที่ pin อยู่ใน [`skills.json`](skills.json) · ความปลอดภัยทั้งระบบดู [04l](../../Document/plan-draft/04-erpnext-enterprise-os/04l-security-baseline.md)

## ติดตั้ง

ใน PowerShell — ใช้ path เต็ม จึงรันจากโฟลเดอร์ไหนก็ได้:

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\Desktop\Workhard\IT-AI-Portfolio\tools\claude-skills\install.ps1" -DryRun
```

```powershell
powershell -ExecutionPolicy Bypass -File "$HOME\Desktop\Workhard\IT-AI-Portfolio\tools\claude-skills\install.ps1"
```

- `-DryRun` ดึงและตรวจทุกอย่างแต่ไม่ติดตั้ง — รันก่อนเสมอ
- เสร็จแล้วเปิด Claude Code session ใหม่ (หรือ `/reload-plugins`) · context7 จะให้ login ครั้งแรกที่ใช้
- ถอดออก: ใส่ `-Uninstall` · ทับของเดิม: ใส่ `-Force`
- ลงเฉพาะบางกลุ่ม: `-Trust frappe-org,anthropic` (🟣 + 🟢) · เพิ่ม 🔵 ทีหลังด้วย `-Trust security-firm,partner` · 🟠 ด้วย `-Trust individual`
- ถ้าไม่มี `claude` CLI สคริปต์จะบอกรายชื่อให้ลงผ่านแอป: **+ › Plugins › Add plugin**

## มีอะไรในแพ็ก

🟢 Anthropic · 🔵 บริษัทที่รู้จัก / partner · 🟣 ทีม Frappe (org เดียวกับ ERPNext) · 🟠 นักพัฒนารายบุคคล (อ่านโค้ดแล้ว · ปรับแก้เก็บไว้ในแพ็ก)

| ชื่อ | ผู้เผยแพร่ | แบบ | ใช้ทำอะไรในงาน 4 | สิ่งที่มันรันได้ |
|---|---|---|---|---|
| `frappe-app-dev` | 🟣 Frappe | skill | เขียน custom app `ai_bridge` · DocType · hooks · API · permissions · bench | Markdown ล้วน |
| `frappe-code-review` | 🟣 Frappe | skill | checklist review แอป Frappe (รวมความปลอดภัย) | Markdown ล้วน |
| `security-guidance` | 🟢 Anthropic | plugin | เตือนช่องโหว่ทันทีขณะเขียนโค้ด + ตรวจ diff ตอนจบงาน | hook (bash) ทุกครั้งที่แก้ไฟล์ / ส่งข้อความ / จบเทิร์น |
| `claude-security` | 🟢 Anthropic | plugin | `/claude-security` สแกนทั้ง repo หรือ diff หลาย agent แล้วเขียน patch ให้รีวิว — รันทุก Gate | hook (sh) แสดง tip · ใช้โทเคนมากต่อการสแกน · ต้องมี `python3` |
| `static-analysis` | 🔵 Trail of Bits | plugin | สแกนด้วย Semgrep / CodeQL | สคริปต์เรียกเครื่องมือ (ต้องติดตั้ง Semgrep / CodeQL เอง) |
| `insecure-defaults` | 🔵 Trail of Bits | plugin | หาค่าเริ่มต้นที่ไม่ปลอดภัยใน config / โค้ด | สคริปต์ตรวจ 1 ตัว |
| `supply-chain-risk-auditor` | 🔵 Trail of Bits | plugin | ตรวจไลบรารี PyPI / npm ก่อนเพิ่มเข้าโปรเจกต์ | สคริปต์ · เรียกข้อมูล advisory ออนไลน์ |
| `differential-review` | 🔵 Trail of Bits | plugin | review ความปลอดภัยของการเปลี่ยนแปลงก่อน merge | Markdown ล้วน |
| `mcp-builder` | 🟢 Anthropic | skill | ออกแบบ MCP server ของ Tool Registry (P3) | สคริปต์ประเมิน MCP — เรียก Anthropic API เมื่อสั่งรันเท่านั้น |
| `webapp-testing` | 🟢 Anthropic | skill | E2E Playwright กับ AI Workspace / ERPNext ในเครื่อง | สคริปต์เปิด server ในเครื่องเมื่อสั่งรัน |
| `frontend-design` | 🟢 Anthropic | skill | ออกแบบหน้า AI Workspace | Markdown ล้วน |
| `context7` | 🔵 Upstash | plugin | เอกสารเวอร์ชันล่าสุดของ FastAPI · Next.js · pgvector · LangGraph | MCP ภายนอก `mcp.context7.com` — ส่งชื่อไลบรารีและคำถามออกนอกเครื่อง |
| `how` | 🟠 Lauren Tan ([pstack](https://github.com/cursor/plugins/tree/main/pstack) · MIT) | skill (ฉบับปรับ) | อธิบายว่าโค้ดส่วนหนึ่งทำงานยังไง และโค้ดใหม่ควรอยู่ตรงไหน เช่น Frappe ตอนขั้น 0.3 | Markdown ล้วน · สั่ง subagent แบบอ่านอย่างเดียว (`Explore` / `Plan`) |
| `create-verification-skill` | 🟠 Lauren Tan (pstack · MIT) | skill (ฉบับปรับ) | สร้าง `verify-p4` ตาม [04c ข้อ 5.6](../../Document/plan-draft/04-erpnext-enterprise-os/04c-build-guide.md#56-skill-ตรวจงาน-verify-p4): launch · doctor · drive · evidence · cleanup + แผนที่ฟีเจอร์ | Markdown ล้วน · ตอนสร้างจะเปิดแอปจริง 1 รอบเพื่อพิสูจน์ |
| `maintain-verification-skill` | 🟠 Lauren Tan (pstack · MIT) | skill (ฉบับปรับ) | ตรวจว่า `verify-p4` กับแผนที่ฟีเจอร์ยังตรงกับแอปก่อน `git tag` | Markdown ล้วน · subagent อ่านโค้ดทีละฟีเจอร์ แล้วขับแอปจริง |
| `blast-radius` | 🟠 Lauren Tan (pstack · MIT) | skill (ฉบับปรับ) | หาว่าการแก้จะไปพังที่อื่นนอก diff ไหม และพิสูจน์ข้อที่ทำให้ปลอดภัยด้วยการรันโค้ด | Markdown ล้วน |
| `correct` | 🟠 Lauren Tan (pstack · MIT) | skill (ฉบับปรับ) | เปลี่ยนเรื่องที่ต้องแก้ให้ AI ซ้ำ ๆ เป็น architecture · type · lint · test | Markdown ล้วน |
| `tdd` | 🟠 Lauren Tan (pstack · MIT) | skill | แก้บั๊กโดยเขียนเทสที่ล้มก่อน เมื่อมีเทสที่ทำได้ถูก ๆ | Markdown ล้วน |
| `typescript-best-practices` | 🟠 Lauren Tan (pstack · MIT) | skill (ฉบับปรับ) | type safety ของ AI Workspace (Next.js) | Markdown ล้วน |
| `unslop` | 🟠 Lauren Tan (pstack · MIT) | skill (ฉบับปรับ) | ตัดสำนวน AI ออกจาก README · PR · เอกสารภาษาอังกฤษของพอร์ต | Markdown ล้วน |
| `/security-review` | 🟢 มากับ Claude Code | — | ตรวจความปลอดภัย 1 รอบต่อ branch | ไม่ต้องติดตั้ง |

**skill 🟠 ทั้ง 8 ตัวเก็บฉบับปรับไว้ใน [`local/`](local/)** ต้นฉบับคือ pstack ซึ่งเขียนให้ Cursor (subagent `generalPurpose` และโมเดลตามบทบาทในไฟล์ `pstack-models.mdc`) จึงแก้ให้ใช้ agent ของ Claude Code แต่ละตัวมีบรรทัด "Adapted for Claude Code" บอกว่าแก้อะไรไป และมีไฟล์ LICENSE ของต้นฉบับตามเงื่อนไข MIT รีวิว pstack ทั้ง 54 skill เมื่อ 17 ต.ค. 2569 แล้วเลือกเก็บไว้ 8 ตัว ตัวที่เหลือซ้ำกับของที่มีหรือใช้ได้แค่ใน Cursor ส่วนหลักการ 24 ข้อของ pstack เก็บเป็นโน้ตใน `~/.claude/skills/brain/starter/brain/principles/` ไม่ได้ติดตั้งเป็น skill · `how` เดิมที่ดัดแปลงจาก `poteto/how@b1ef429` มีโหมด critique แต่ต้นทางตัดโหมดนี้ออกไปแล้ว ถ้าต้องการวิจารณ์โครงสร้างให้ใช้ `/review` ฉบับเดิมสำรองไว้ที่ `~/.claude/disabled/pack-backup/how-poteto-b1ef429/` · **skill อีก 5 ตัวไม่เก็บสำเนาไว้ในแพ็ก** สคริปต์ดึงจาก repo ต้นทางตรง commit ที่รีวิวแล้ว (`frappe/skills` ไม่มีไฟล์ LICENSE จึงไม่ควรทำสำเนาเก็บ)

## Commit ที่รีวิวแล้ว

| Repo | Commit | วันที่ |
|---|---|---|
| `frappe/skills` | `c1118cb` | 14 ต.ค. 2569 |
| `anthropics/skills` | `dbd4588` | 9 ต.ค. 2569 |
| `trailofbits/skills` (marketplace) | `5c99c03` | 15 ต.ค. 2569 |
| `anthropics/claude-plugins-official` (marketplace) | `ea10b21` | 15 ต.ค. 2569 |
| `cursor/plugins` → `pstack/` v0.15.25 (ต้นฉบับของ skill 🟠 ทั้ง 8 ตัวใน `local/`) | `101b274` | 16 ต.ค. 2569 |

ตรวจเมื่อ 17 ต.ค. 2569: `frappe/skills` และ `anthropics/skills` ยังไม่มี commit ใหม่หลังจาก commit ที่ pin ไว้ จึงเป็นเวอร์ชันล่าสุดอยู่แล้ว

- marketplace ทั้งสองไม่มี tag ให้ pin — สคริปต์จะ**เตือน**ถ้าเวอร์ชันล่าสุดต่างจากที่รีวิว ให้อ่านการเปลี่ยนแปลงก่อน
- marketplace ทางการของ Anthropic อัปเดตเองอัตโนมัติ · marketplace ของ Trail of Bits ไม่อัปเดตเอง (ค้างที่เวอร์ชันตอนติดตั้ง)
- อัปเดต skill: แก้ `commit` ใน `skills.json` → รัน `install.ps1 -Force`

## ต้องแก้ก่อนใช้ claude-security: `python3`

เครื่องนี้มี Python 3.12 เป็นคำสั่ง `python` แต่ `python3` ชี้ไปที่ตัวลัดของ Microsoft Store (ไม่ใช่ Python จริง) — `-DryRun` จะเตือนเรื่องนี้

1. Settings › Apps › Advanced app settings › **App execution aliases** → ปิด `python.exe` และ `python3.exe` (App Installer)
2. สร้าง `python3.exe` ข้าง `python.exe`:

```powershell
Copy-Item "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" "$env:LOCALAPPDATA\Programs\Python\Python312\python3.exe"
```

3. เปิด PowerShell ใหม่ แล้วตรวจด้วย `python3 --version`

## ชุดเสริม (ไม่ลงอัตโนมัติ)

ลงเพิ่มทีละตัวเมื่อต้องการ:

| ชื่อ | ผู้เผยแพร่ | ใช้ทำอะไร | คำสั่ง |
|---|---|---|---|
| Superpowers | 🔵 obra (Jesse Vincent) | วินัยการทำงาน: TDD · debugging · ตรวจก่อนบอกว่าเสร็จ (มี hook ตอนเริ่ม session) | `claude plugin install superpowers@claude-plugins-official` |
| feature-dev | 🟢 Anthropic | agent สำรวจ → ออกแบบ → review ทีละฟีเจอร์ | `claude plugin install feature-dev@claude-plugins-official` |
| pr-review-toolkit | 🟢 Anthropic | review PR หลายมุม รวมหา error ที่ถูกกลืน | `claude plugin install pr-review-toolkit@claude-plugins-official` |
| commit-commands | 🟢 Anthropic | commit / push / เปิด PR | `claude plugin install commit-commands@claude-plugins-official` |
| playwright | 🔵 Microsoft | ให้ Claude คลิกทดสอบ E2E เอง (ซ้ำกับ browser pane บางส่วน) | `claude plugin install playwright@claude-plugins-official` |
| 42Crunch API security | 🔵 42Crunch | audit / scan API จาก OpenAPI | ลงผ่าน Anthropic Directory ในแอป |

## ไม่แนะนำ

| ตัว | เหตุผล |
|---|---|
| MCP ERPNext ของ community (casys · muthanii · vyogotech ฯลฯ) | ให้ AI เข้าถึง ERP กว้าง — ขัดกับหลักที่ Gateway คุมสิทธิ์เอง |
| `deep-app-audit` · `ship-it` ของ `frappe/skills` | รันสคริปต์ / subagent / เปิด PR เอง — ลงเมื่อรีวิวโค้ดแล้วเท่านั้น |
| Superpowers ฉบับก๊อป (ZSL · Decibel · sdd · beads) | community · ยังไม่ยืนยันผู้เขียน |
| `brainmaxxing` (Lauren Tan) | ซ้ำกับ memory ของ Claude Code · skill `ruminate` อ่านประวัติแชททั้งหมด ซึ่งมีความลับที่เคยพิมพ์ในแชท แล้วอาจเขียนลงไฟล์ที่ขึ้น GitHub · **ติดตั้งนอกแพ็กแล้ว** ([ดูด้านล่าง](#ติดตั้งนอกแพ็ก)) |
| `noodle` (Lauren Tan) | เป็นโปรแกรม Go เต็มตัว (server + UI) ไม่ใช่ skill · ติดตั้งโดยให้ agent ทำตามไฟล์บนเน็ต · ซ้ำกับ subagent / session ของ Claude Code · **ติดตั้งนอกแพ็กแล้ว** ([ดูด้านล่าง](#ติดตั้งนอกแพ็ก)) |
| `pstack-claude` | คนอื่นแปลงจาก pstack ของ Lauren Tan (ฉบับ Cursor) · ซ้ำกับ ponytail |
| RAG / Agent Evaluation รุ่น 0.1 · prompt-enhancer | community · บางตัวมี hook แก้ prompt |
| docker-skills | อ้างว่าเป็นของ Docker, Inc. แต่ directory ยังจัดเป็น community |
| Supabase · Odoo Tools · plugin-dev · agent-sdk-dev | ไม่ตรงสแต็กของงาน 4 |

## ติดตั้งนอกแพ็ก

> ติดตั้งเมื่อ 17 ต.ค. 2569 ตามที่เจ้าของสั่ง เพื่อใช้งานจริง · **`install.ps1` ไม่จัดการกลุ่มนี้** (ไม่อยู่ใน `skills.json` และไม่มีสำเนาใน `local/`) · แต่ละโฟลเดอร์ใน `~/.claude/skills/` มีไฟล์ `.claude-skill-origin` ที่บอกต้นทางและ commit แทนไฟล์ `.claude-skills-pack`

| ชื่อ | ต้นทาง (commit) | ฉบับ | ใช้กับ |
|---|---|---|---|
| `brain` · `reflect` · `ruminate` · `meditate` · `plan` · `review` | `poteto/brainmaxxing` `ec4d8e4` | ฉบับปรับ: path ของสคริปต์ชี้ไปที่ `~/.claude/skills` · `ruminate` อ่านและเขียน UTF-8 (ของเดิมพังเมื่อเจอภาษาไทย) · `meditate` ถามก่อนแก้ และทำแค่รายงานเรื่อง memory กับ `CLAUDE.md` · `review` รองรับ Plastic · หลักการในชุดตั้งต้น `brain/starter/` อัปเดตเป็น 24 ข้อของ pstack แล้ว (17 ต.ค. 2569) | 102 (มี `brain/` แล้ว) |
| `debugging` | `poteto/noodle` `82d2921` | ฉบับปรับ: ตัดส่วน Noodle/tmux ออก · เพิ่ม Plastic | ทุกโปรเจกต์ |
| `todo` · `refine` | `poteto/noodle` `82d2921` | ต้นฉบับ | ใช้ได้เมื่อมี `brain/` |
| ~~`unslop` · `ts-best-practices`~~ | `poteto/noodle` `82d2921` | **แทนที่แล้ว 17 ต.ค. 2569** | ใช้ `unslop` และ `typescript-best-practices` ของแพ็ก (มาจาก pstack ซึ่งใหม่กว่า) แทน สำเนาเดิมเก็บไว้ที่ `~/.claude/disabled/` |
| skill `noodle` + `noodle.exe` v0.1.5 | `poteto/noodle` `82d2921` · release `noodle_windows_amd64.zip` (sha256 ตรงกับ `checksums.txt`) | **ปิดใช้งาน 17 ต.ค. 2569** | ย้ายไปไว้ที่ `~/.claude/disabled/` (`noodle-skill/` และ `noodle.exe`) จึงไม่อยู่ใน PATH และไม่ขึ้นในรายการ skill ถ้าจะเปิดใช้อีก ให้ย้ายกลับไปที่ `~/.claude/skills/noodle/` และใส่ exe ไว้ในโฟลเดอร์ที่อยู่ใน PATH |

**ก่อนใช้ในโปรเจกต์ใหม่**

- **brainmaxxing:** สั่ง Claude ว่า "ตั้ง brain ในโปรเจกต์นี้" Claude จะคัดลอก `~/.claude/skills/brain/starter/brain/` ไปเป็น `brain/` แล้วต่อท้าย `CLAUDE-snippet.md` ลงใน `CLAUDE.md`
- **noodle:** โปรเจกต์ต้องเป็น git repo เพราะ noodle ใช้ git worktree และต้องมี:
  - `.noodle.toml`
  - skill `schedule` + `execute` ที่เขียนสำหรับโปรเจกต์นั้น
  - backlog `todos.md`
  - `.noodle/` ใน `.gitignore`

  ขั้นตอนเต็มอยู่ใน `INSTALL.md` ของ poteto/noodle ส่วนโปรเจกต์ 102 ใช้ Plastic จึงยังใช้ noodle ไม่ได้

**ข้อระวัง (เหตุผลที่ไม่รวมไว้ในแพ็ก)**

- `ruminate` อ่านประวัติแชททั้งหมด ถ้า `brain/` ของโปรเจกต์ขึ้น GitHub (เช่นงาน 4) ให้ตรวจโน้ตทุกไฟล์ก่อน commit และให้ gitleaks ใน CI ช่วยจับความลับ
- `brain/` ซ้ำกับ memory ของ Claude Code บางส่วน ถ้ากฎใน brain ใหม่กว่าโน้ตใน memory ให้เขียนไว้ว่ากฎนั้นใช้แทนโน้ตไหน
- noodle สั่ง agent ทำงานเองเป็นลูป จึงใช้โทเคนมาก
- **noodle v0.1.5 ใช้บน Windows ไม่ได้** (ทดสอบ 17 ต.ค. 2569) `noodle start` ปิดตัวภายในราว 4 วินาทีด้วย `watch runtime directory: fsnotify: queue or buffer overflow` สาเหตุคือ `loop/loop.go` ถือว่า error ทุกตัวของ fsnotify ร้ายแรง รวมถึงกรณี buffer เต็มที่ Windows ส่งมาบ่อยด้วย ไม่มีค่าตั้งไหนแก้ได้ ต้องรันบน Linux/WSL หรือรอ upstream แก้
- **โหมด `manual` ยังส่ง agent ทำงานเองตอนเปิด** ถ้ายังไม่มี `.agents/skills/schedule/SKILL.md` noodle จะส่ง agent "bootstrap" (ใช้ Opus) ไปเขียน skill นี้และ commit ทันที ถ้าต้องการเปิดดูเฉย ๆ ให้ใส่ skill `schedule` ไว้ก่อน

**ถอดออก:** ลบโฟลเดอร์ที่มีไฟล์ `.claude-skill-origin` ใน `~/.claude/skills/` และลบโฟลเดอร์ `~/.claude/disabled/` ด้วยมือ (`-Uninstall` ของแพ็กไม่แตะกลุ่มนี้)

## ข้อควรรู้

- plugin รันด้วยสิทธิ์ของคุณ — hook ของ `security-guidance` ทำงานทุกครั้งที่แก้ไฟล์ จึงอาจทำให้แต่ละเทิร์นช้าลงเล็กน้อย
- plugin / skill ที่เปิดอยู่จะใส่ชื่อและคำอธิบายลง context ทุกเทิร์น — ไม่ใช้ตัวไหนให้ปิดด้วย `claude plugin disable <name>@<marketplace>`
- skill ที่แพ็กติดตั้งจะมีไฟล์ `.claude-skills-pack` ข้างใน — `-Uninstall` ลบเฉพาะโฟลเดอร์ที่มีไฟล์นี้ ไม่แตะ skill อื่นของคุณ · skill ที่ติดตั้งนอกแพ็กจะใช้ไฟล์ `.claude-skill-origin` แทน
- skill ช่วยเฉพาะความปลอดภัยของ**โค้ด** — ชั้นอื่น (2FA · เครือข่าย · backup · แจ้งเตือน) อยู่ใน [04l](../../Document/plan-draft/04-erpnext-enterprise-os/04l-security-baseline.md)
