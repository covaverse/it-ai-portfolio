# 📚 ของที่มีอยู่แล้วและตลาด (Prior Art & Market)

> ตรวจเมื่อ **15–16 ต.ค. 2569** (ดาว/license จาก GitHub API) · ใช้ประกอบ [04 ข้อ 2](../04-enterprise-os.md#2-ของที่มีอยู่แล้ว-prior-art) และ [04e](../04e-saas-business-model.md)
> ← [หน้าแรกงาน 4](../README.md)

---

## 1. ERP และส่วนเสริมภาษาไทย

| โปรเจกต์ | ดาว | License | สถานะ | เราใช้ยังไง |
|---|---|---|---|---|
| [frappe/erpnext](https://github.com/frappe/erpnext) | 40k | GPL-3.0 | v16.51.1 (15 ต.ค. 2569) | ระบบหลัก |
| [frappe/hrms](https://github.com/frappe/hrms) | — | GPL-3.0 | — | HR, ลงเวลา, OT, เงินเดือน (แกน) |
| [ecosoft-frappe/erpnext_thailand](https://github.com/ecosoft-frappe/erpnext_thailand) | 27 | MIT | branch `version-16` | ภาษีไทย |
| [kittiu/thai_tax](https://github.com/kittiu/thai_tax) | — | — | เก็บถาวรแล้ว (6 พ.ย. 2568) | ตัวเก่า — ไม่ใช้ |
| [odoo/odoo](https://github.com/odoo/odoo) | 55k | LGPL-3 (Community) | branch 20.0 | ทางเลือกตัวต่อในอนาคต |
| [OCA/l10n-thailand](https://github.com/OCA/l10n-thailand) | 71 | AGPL-3.0 | branch 19.0 | อ่านอ้างอิงเท่านั้น |
| [SC Thailand Payroll (Odoo)](https://apps.odoo.com/apps/modules/17.0/sc_th_payroll) | — | ตรวจหน้า app | Odoo 17 | ตัวเทียบขอบเขตของ [งาน 5](../../05-thai-payroll-erpnext/README.md) |

## 2. ERP แบบ AI ทำงานแทน (เกิดปี 2569 ทั้งหมด)

| โปรเจกต์ | ดาว | License | แนวทาง |
|---|---|---|---|
| [erp-mafia/accounted](https://github.com/erp-mafia/accounted) | 415 | AGPL (ตาม README) | 150+ MCP tools · agent เสนอ คนอนุมัติ · กฎหมายสวีเดน |
| [avansaber/erpclaw](https://github.com/avansaber/erpclaw) | 117 | GPL-3.0 | สั่งงานบัญชี/คลัง/ขาย/ซื้อด้วยภาษาคน |
| [lambdadevelopment/lambda-erp](https://github.com/lambdadevelopment/lambda-erp) | 38 | Apache-2.0 | ผ่านแชต · PDF ผู้ขาย → Purchase Invoice |
| [ERPNext Copilot](https://discuss.frappe.io/t/open-source-erpnext-ai-assistant-with-permission-aware-queries/164109) | — | ไม่ระบุ | แผนคิวรี → ตรวจ → รันผ่าน API ตามสิทธิ์ผู้ใช้ |

## 3. AI ตรวจเอกสารซื้อ (แนวเดียวกับ APX)

| โปรเจกต์ | ดาว | License | หมายเหตุ |
|---|---|---|---|
| [mshojaei77/invoice-to-pay-agent](https://github.com/mshojaei77/invoice-to-pay-agent) | 6 | MIT | OCR/VLM, 3-way match, approval, eval, audit |
| [emmaGH1/APilot](https://github.com/emmaGH1/APilot) | — | — | LLM อ่าน · กฎตัดสิน · คิวให้คนตรวจ |
| [devilmango/automated_invoice_reconciliation](https://github.com/devilmango/automated_invoice_reconciliation) | 0 | MIT | เครื่อง 3-way match (YAML tolerance) |
| [scb-10x/typhoon-ocr](https://github.com/scb-10x/typhoon-ocr) | 148 | Apache-2.0 | OCR ไทย → markdown (ต้องดึงช่องเอง) |

**ข้อสรุป:** ไม่พบตัวไหนอ่าน "ใบกำกับภาษีไทย" แบบแยกช่องพร้อมตัวเลขความแม่นยำ

## 4. ตลาดบริการรายเดือน

| ผู้เล่น | รูปแบบ | ราคา (ตรวจ 16 ต.ค. 2569) |
|---|---|---|
| Frappe Cloud | host ERPNext ทางการ | Sites เริ่ม $5/เดือน · Servers เริ่ม $40/เดือน ([pricing](https://frappe.io/cloud/pricing)) |
| บริษัทวางระบบ ERPNext ในไทย | ค่าวางระบบ + ดูแลรายปี | ไม่เปิดเผยราคา |
| โปรแกรมบัญชีออนไลน์ไทย | SaaS รายเดือน/รายปี บางรายมีแพ็กเกจเริ่มฟรี | **ยังไม่ได้ยืนยันราคา** — ตรวจหน้าราคาของแต่ละเจ้า |
| Odoo (Online / พาร์ทเนอร์) | SaaS + พาร์ทเนอร์วางระบบ | ตรวจหน้าราคา Odoo |

## 5. กฎ License สรุป

| ประเภท | ทำอะไรได้ |
|---|---|
| MIT / Apache-2.0 | นำโค้ดมาใช้ได้ (คงข้อความ license) |
| GPL-3.0 | อ่านศึกษาได้ · ถ้านำโค้ดมาแก้แล้วแจกจ่าย ต้องเปิดซอร์สด้วย license เดียวกัน · app ที่ฝังใน ERPNext/HRMS ให้เปิดเป็น GPL-3 |
| AGPL-3.0 | อ่านอย่างเดียว · ถ้านำมาใช้ในบริการออนไลน์ต้องเปิดซอร์สทั้งหมด |
| เครื่องหมายการค้า ERPNext | ใช้อธิบายบริการได้ · ห้ามใช้ในชื่อสินค้า/บริษัท/โดเมน/โฆษณา ([policy](https://frappe.io/erpnext/license-trademark)) |
