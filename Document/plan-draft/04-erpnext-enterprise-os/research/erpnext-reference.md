# 📚 ข้อมูลอ้างอิง ERPNext / Frappe ที่ใช้ในงาน 4

> รวบรวมและตรวจเมื่อ **16 ต.ค. 2569** — ข้อมูลเวอร์ชันและเอกสารเปลี่ยนได้ ให้ตรวจซ้ำก่อนเริ่มแต่ละ Stage
> สถานะข้อมูล: ✅ ตรวจจากแหล่งทางการ/โค้ดต้นฉบับ · 🟡 จากความรู้ทั่วไปหรือแหล่งรอง ต้องตรวจซ้ำ
> ← [หน้าแรกงาน 4](../README.md)

---

## 1. เวอร์ชันที่ต้อง pin

| ส่วน | ค่า | สถานะ | แหล่ง |
|---|---|---|---|
| ERPNext รุ่นล่าสุด | **v16.51.1** (ออก 15 ต.ค. 2569) | ✅ | [GitHub API: frappe/erpnext releases](https://github.com/frappe/erpnext/releases) |
| erpnext_thailand | มี branch `main` และ **`version-16`** → ใช้คู่กับ ERPNext v16 | ✅ | [GitHub: ecosoft-frappe/erpnext_thailand](https://github.com/ecosoft-frappe/erpnext_thailand) |
| Frappe HR (hrms) | ใช้ branch `version-16` ให้ตรงกับ ERPNext | 🟡 | [GitHub: frappe/hrms](https://github.com/frappe/hrms) |
| DB ของ ERPNext | MariaDB เป็นหลัก | 🟡 | — |

> กฎ: pin ทั้ง 3 app ไว้ที่ `version-16` ใน `apps.json` · อัปเกรดเมื่อ test ภาษีไทย ([04 ข้อ 14](../04-enterprise-os.md#14-ภาษีไทย-ตรวจผลกับ-erpnext)) ผ่านบน branch ใหม่แล้วเท่านั้น

---

## 2. ติดตั้งด้วย frappe_docker

| เรื่อง | รายละเอียด | สถานะ |
|---|---|---|
| ลองเร็ว | `docker compose -f pwd.yml up -d` → เปิดพอร์ต 8080 → login `Administrator` / `admin` | ✅ |
| ข้อจำกัดของ `pwd.yml` | สำหรับทดลองระยะสั้นเท่านั้น **ติดตั้ง custom app ไม่ได้** | ✅ |
| ใช้จริง | เริ่มจาก `compose.yaml` + ไฟล์ใน `overrides/` | ✅ |
| Build image ที่รวม app เพิ่ม (erpnext_thailand, hrms, ai_bridge) | ดู `docs/02-setup/02-build-setup.md` | ✅ (ชื่อไฟล์) |
| ตัวอย่างเซิร์ฟเวอร์เดียว | `docs/02-setup/07-single-server-example.md` | ✅ (ชื่อไฟล์) |
| สิ่งที่ต้องมี | Docker, Docker Compose v2, git | ✅ |

แหล่ง: [frappe/frappe_docker](https://github.com/frappe/frappe_docker)

---

## 3. Webhook (ERPNext → Gateway)

| เรื่อง | รายละเอียด | สถานะ |
|---|---|---|
| Header ลายเซ็น | `X-Frappe-Webhook-Signature` | ✅ |
| วิธีคำนวณ | **base64**( HMAC-SHA256( secret, JSON ของ payload ) ) — ไม่ใช่ hex | ✅ |
| JSON ที่ถูกเซ็น | serialize ด้วย `frappe.as_json` | ✅ |
| เปิดใช้ | ติ๊ก Enable Security + ใส่ Webhook Secret ในเอกสาร Webhook | ✅ |
| Event ที่ส่งได้ | `after_insert` · `on_update` · `on_submit` · `on_cancel` · `on_trash` · `on_update_after_submit` · `on_change` · `workflow_transition` | ✅ |
| ข้อจำกัด | `on_submit` / `on_cancel` / `on_update_after_submit` ใช้ได้กับ DocType ที่ submit ได้เท่านั้น | ✅ |

> ⚠️ ลายเซ็นคำนวณจาก JSON ที่ Frappe serialize เอง — ถ้าตรวจกับ raw body แล้วไม่ตรง ให้ serialize payload แบบเดียวกับ Frappe ก่อนตรวจ · **เขียน integration test ยิง webhook จริงจาก ERPNext** แทนการเดารูปแบบ

แหล่ง: [frappe/frappe — webhook.py](https://github.com/frappe/frappe/blob/develop/frappe/integrations/doctype/webhook/webhook.py)

---

## 4. API และการยืนยันตัวตน

| เรื่อง | รายละเอียด | สถานะ |
|---|---|---|
| อ่าน/เขียนเอกสาร | `/api/resource/<DocType>` และ `/api/resource/<DocType>/<name>` | 🟡 |
| เรียกฟังก์ชัน | `/api/method/<dotted.path>` (ต้องเป็นฟังก์ชันที่ `@frappe.whitelist()`) | 🟡 |
| Token | header `Authorization: token <api_key>:<api_secret>` (สร้างในหน้า User) | 🟡 |
| OAuth 2.0 | Frappe เป็น OAuth provider ได้ (ตั้งใน OAuth Client) — ใช้ให้ผู้ใช้ login เข้า AI Workspace | 🟡 |
| สิทธิ์ระดับข้อมูล | User Permission จำกัดผู้ใช้ให้เห็นเฉพาะ Branch / Warehouse / Cost Center ที่กำหนด | 🟡 |

---

## 5. DocType ที่งาน 4 ใช้ (จัดตามแผนก)

| แผนก | DocType |
|---|---|
| ขาย | Quotation · Sales Order · Delivery Note · Sales Invoice · Customer · Contract |
| จัดซื้อ | Material Request · Request for Quotation · Supplier Quotation · Purchase Order · Purchase Receipt · Purchase Invoice · Supplier |
| คลัง / ผลิต | Item · Warehouse · Stock Entry · BOM · Work Order · Job Card · Workstation · Operation |
| บัญชี / การเงิน | Payment Entry · Journal Entry · Payment Terms Template · Mode of Payment · Bank Reconciliation Tool · Cost Center · Accounting Dimension · Accounting Period · Period Closing Voucher · Budget |
| ครุภัณฑ์ | Asset · Asset Category · Asset Movement · Asset Maintenance · Asset Repair |
| HR (Frappe HR) | Employee · Department · Designation · Branch · Shift Type · Employee Checkin · Attendance · Leave Application · Expense Claim · Employee Advance · Overtime Type · Overtime Slip · Salary Structure · Payroll Entry · Salary Slip · Additional Salary |
| ระบบ | User · Role · Role Profile · Workflow · Naming Series · Print Format · Webhook · Auto Email Report · Dashboard Chart · Number Card |

### รายละเอียดที่ตรวจแล้ว

| ฟีเจอร์ | สิ่งที่พบ | สถานะ |
|---|---|---|
| OT (Frappe HR) | **Overtime Type** กำหนดกฎ: เพดานชั่วโมงต่อวัน · salary component ที่จ่าย · วิธีคิด (อัตราคงที่ต่อชั่วโมง หรือคิดจาก salary component) → **Overtime Slip** ดึงชั่วโมงจาก Attendance → อนุมัติแล้วสร้าง Additional Salary เข้ารอบเงินเดือน | ✅ |
| OT ตัวคูณตามประเภทวัน (1.5 / 2 / 3 เท่า) | **ไม่พบในเอกสารทางการ** — ต้องแยก Overtime Type ตามประเภทวัน หรือคำนวณเพิ่มใน [งาน 5](../../05-thai-payroll-erpnext/README.md) | ✅ (ว่าไม่มี) |
| Asset Repair | สถานะ Pending / Completed / Cancelled | ✅ |
| Asset Maintenance | ประเภท Preventive Maintenance / Calibration · สถานะงาน Planned / Overdue / Cancelled | ✅ |
| ตรวจนับครุภัณฑ์ | **ไม่พบฟีเจอร์ตรวจนับโดยตรง** → ทำฟอร์มเล็กๆ ใน `ai_bridge` | ✅ (ว่าไม่มี) |
| เงินเดือนไทย (ประกันสังคม, ภ.ง.ด.1) | **ไม่พบ app สำหรับ ERPNext** (Odoo มี sc_th_payroll) | ✅ (ว่าไม่มี) |

แหล่ง: [Frappe HR — Overtime](https://docs.frappe.io/hr/overtime) · [ERPNext — Asset Repair](https://docs.frappe.io/erpnext/user/manual/en/asset-repair) · [ERPNext — Asset Maintenance](https://docs.frappe.io/erpnext/user/manual/en/asset-maintenance)

---

## 6. License และเครื่องหมายการค้า

| เรื่อง | สรุป | สถานะ |
|---|---|---|
| License ERPNext | GPL v3 · เอกสาร CC-BY-SA 3.0 | ✅ |
| ใช้ชื่อ/โลโก้ "ERPNext" เพื่อ**อธิบาย**บริการ | ทำได้ (เช่น "บริการวางระบบ ERPNext") · ใช้โลโก้ในหน้าที่อธิบายบริการได้ | ✅ |
| ใช้ "ERPNext" ใน**ชื่อสินค้า / บริษัท / โลโก้ / แบรนด์** | ต้องได้รับอนุญาต — และให้เฉพาะโครงการไม่แสวงกำไร | ✅ |
| ใช้ในชื่อโดเมน | ห้าม | ✅ |
| ใช้ในโฆษณา (AdWords ฯลฯ) | ห้าม | ✅ |
| การให้บริการ host ERPNext แก่บริษัทอื่น | หน้า policy **ไม่ได้กล่าวถึงโดยตรง** · ระบุว่าไม่ได้ต้องการจำกัดธุรกิจรอบ ERPNext | ✅ |

> ผลต่องานนี้: ในพอร์ตเรียก "Enterprise OS บน ERPNext" ได้ (อธิบาย) · **ถ้าขายจริง ต้องตั้งชื่อสินค้าของตัวเอง** ไม่มีคำว่า ERPNext — ดู [04e](../04e-saas-business-model.md)

แหล่ง: [ERPNext License & Trademark](https://frappe.io/erpnext/license-trademark)

---

## 7. Frappe Cloud (บริการ host ทางการ — คู่แข่ง/ทางเลือก)

| แผน | ราคาเริ่มต้น | รวม |
|---|---|---|
| Sites (เซิร์ฟเวอร์ร่วม) | $5 / เดือน | ติดตั้ง app, backup นอกเครื่อง, monitoring, custom domain, deploy custom app |
| Servers (เครื่องแยก) | $40 / เดือน | site/bench ไม่จำกัด, snapshot, auto-scaling, เลือก SLA ได้ |

ตรวจจากหน้าราคาเมื่อ 16 ต.ค. 2569 (หน้าเว็บไม่ระบุวันที่ และแสดงเฉพาะราคาเริ่มต้น) — [frappe.io/cloud/pricing](https://frappe.io/cloud/pricing)
