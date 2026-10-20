# 👥 งานที่ 4g — Flow การทำงานของพนักงานแต่ละฝ่าย

> แต่ละตำแหน่งทำอะไรในระบบ ทีละขั้น · ตัดสินใจตรงไหน · ใครอนุมัติ · ส่งต่อให้ฝ่ายไหน · AI ช่วยตรงไหน
> ← [หน้าแรกงาน 4](README.md) · [04a ตำแหน่งและเอกสาร](04a-company-blueprint.md) · [04d สาย ERP](04d-erp-implementation.md) · [04f แผนผัง module](04f-module-map.md)

### วิธีอ่าน diagram

| สัญลักษณ์ | ความหมาย |
|---|---|
| 🟩 กล่องเขียว | เอกสาร/ขั้นตอนใน ERPNext |
| 🟦 กล่องฟ้า | AI ช่วย (ระบุระดับ L0–L3 · L1 = ร่างรอคนอนุมัติ) |
| 🟨 กล่องเหลือง | จุดอนุมัติ |
| 🟪 กล่องม่วง | ส่งต่อให้ฝ่ายอื่น / คนภายนอก |
| ◇ | จุดตัดสินใจ (แตกแขนง) |

> วงเงินอนุมัติและการแบ่งหน้าที่อ้างอิง [04a ข้อ 11](04a-company-blueprint.md#11-แปลงผังบริษัทเป็น-erpnext) · ระดับอิสระของ AI อ้างอิง [04 ข้อ 9.3](04-enterprise-os.md#93-ระดับอิสระ-autonomy-dial)

---

## สารบัญ
0. [แผนที่ส่งต่องานระหว่างฝ่าย](#0-แผนที่ส่งต่องานระหว่างฝ่าย)
1. [ขาย](#1-ขาย)
2. [Pre-sales](#2-pre-sales)
3. [กฎหมาย](#3-กฎหมาย)
4. [จัดซื้อ](#4-จัดซื้อ)
5. [คลังและขนส่ง](#5-คลังและขนส่ง)
6. [สาขา 2 ศูนย์ประกอบ](#6-สาขา-2-ศูนย์ประกอบ)
7. [บัญชี](#7-บัญชี)
8. [การเงิน](#8-การเงิน)
9. [HR](#9-hr)
10. [IT](#10-it)
11. [ผู้บริหาร](#11-ผู้บริหาร)
12. [ธุรการ / สารบรรณ](#12-ธุรการ--สารบรรณ)
13. [PMO และ Customer Support](#13-pmo-และ-customer-support)
14. [รอบงานประจำวัน / สัปดาห์ / เดือน / ปี](#14-รอบงานประจำวัน--สัปดาห์--เดือน--ปี)

---

## 0. แผนที่ส่งต่องานระหว่างฝ่าย

```mermaid
flowchart TD
    CUS["ลูกค้า"]
    VEN["ผู้ขาย"]
    SAL["ขาย"]
    PRE["Pre-sales"]
    LEG["กฎหมาย"]
    PRC["จัดซื้อ"]
    WH["คลัง / ขนส่ง"]
    MFG["สาขา 2 ผลิต"]
    ACC["บัญชี"]
    FIN["การเงิน"]
    HR["HR"]
    IT["IT"]
    EXE["ผู้บริหาร"]
    AI["ชั้น AI"]

    CUS -->|"ขอราคา"| SAL
    PRE -->|"สเปค / BOQ"| SAL
    SAL -->|"ร่างสัญญา"| LEG
    LEG -->|"สัญญาลงนาม"| SAL
    SAL -->|"Sales Order"| WH
    SAL -->|"สั่งประกอบ"| MFG
    MFG -->|"ขอวัตถุดิบ"| PRC
    PRC -->|"PO"| VEN
    VEN -->|"ของ"| WH
    VEN -->|"ใบกำกับภาษี"| AI
    AI -->|"ร่างตั้งหนี้"| ACC
    WH -->|"ใบรับของ"| ACC
    MFG -->|"สินค้าสำเร็จรูป"| WH
    WH -->|"ส่งของ + หลักฐาน"| ACC
    ACC -->|"ใบกำกับ + วางบิล"| CUS
    CUS -->|"ชำระเงิน"| FIN
    ACC -->|"รายการรอจ่าย"| FIN
    FIN -->|"จ่ายเงิน"| VEN
    HR -->|"เข้า / ออกงาน"| IT
    HR -->|"ค่าแรง OT"| ACC
    ACC -->|"งบการเงิน"| EXE
    EXE -->|"อนุมัติวงเงินสูง"| PRC

    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef ext fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class AI ai
    class CUS,VEN ext
```

---

## 1. ขาย

**ตำแหน่ง:** Account Manager · Sales Manager · Sales Director (อนุมัติส่วนลดสูง)

```mermaid
flowchart TD
    S0["ลูกค้าขอราคา<br/>อีเมล · LINE · โทร"] --> S1{"ลูกค้าใหม่?"}
    S1 -->|"ใช่"| S2["สร้าง Customer<br/>ดึงที่อยู่จากเลขผู้เสียภาษี"]
    S1 -->|"ไม่"| S3{"ต้องทำสเปค?"}
    S2 --> S3
    S3 -->|"ใช่"| H1["ส่ง Pre-sales ทำ BOQ"]
    H1 --> S4
    S3 -->|"ไม่"| S4["สร้าง Quotation"]
    AI1["AI ร่างจากใบเก่าของลูกค้า (L1)"] -.-> S4
    S4 --> S5{"ส่วนลด?"}
    S5 -->|"ไม่เกิน 5%"| S7["ส่งลูกค้า"]
    S5 -->|"5–15%"| A1["Sales Manager อนุมัติ"]
    S5 -->|"เกิน 15%"| A2["Sales Director อนุมัติ"]
    A1 --> S7
    A2 --> S7
    S7 --> S8{"ลูกค้าตกลง?"}
    S8 -->|"ไม่"| S9["บันทึก Lost + เหตุผล"]
    S8 -->|"ขอแก้"| S4
    S8 -->|"ตกลง"| S10{"ต้องมีสัญญา?"}
    S10 -->|"ใช่"| H2["ส่งกฎหมาย"]
    H2 --> S11
    S10 -->|"ไม่"| S11["สร้าง Sales Order<br/>ตรวจวงเงินเครดิต"]
    S11 --> S12{"มีของในคลัง?"}
    S12 -->|"มี"| H3["คลังจัดส่ง"]
    S12 -->|"ต้องประกอบ"| H4["สาขา 2 เปิด Work Order"]
    H3 --> S13["ติดตามรับเงิน"]
    H4 --> S13
    S13 --> S14{"เกินกำหนดชำระ?"}
    S14 -->|"ใช่"| AI2["AI ร่างอีเมลตามหนี้ (L1)"]
    S14 -->|"ไม่"| S15["ปิดการขาย"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class S2,S4,S11,S9 doc
    class AI1,AI2 ai
    class A1,A2 appr
    class H1,H2,H3,H4 hand
```

| ขั้น | ทำที่ | เอกสาร | ส่งต่อ | AI |
|---|---|---|---|---|
| รับคำขอ | อีเมล / LINE → Router ส่งเข้าขาย | — | — | จัดหมวดคำขอ (L1) |
| ลูกค้าใหม่ | ERPNext Desk | Customer | — | — |
| ใบเสนอราคา | Desk | Quotation | Pre-sales (ถ้าต้องสเปค) | ร่างจากใบเก่า (L1) |
| อนุมัติส่วนลด | Desk (Workflow) | Quotation | Sales Manager / Director | — |
| ปิดการขาย | Desk | Sales Order | กฎหมาย · คลัง · สาขา 2 | — |
| ติดตามเงิน | AI Workspace | AR Aging | การเงิน | ร่างอีเมลตามหนี้ (L1) |

---

## 2. Pre-sales

**ตำแหน่ง:** Solution Engineer

```mermaid
flowchart TD
    P0["รับคำขอจากขาย"] --> P1["คุยความต้องการลูกค้า"]
    P1 --> P2{"ประเภทงาน?"}
    P2 -->|"ขายเครื่อง"| P3["เลือกสเปคจาก Item / BOM"]
    P2 -->|"โครงการ"| P4["ประเมิน man-day + ขอบเขต"]
    P3 --> P5{"ต้องประกอบที่สาขา 2?"}
    P5 -->|"ใช่"| H1["เช็กเวลาผลิตกับหัวหน้าสาขา 2"]
    P5 -->|"ไม่"| P6
    H1 --> P6["ทำ BOQ"]
    P4 --> P7["ร่าง Proposal / SOW"]
    AI1["AI ร่างจาก proposal เก่า (RAG · L1)"] -.-> P7
    P6 --> H2["ส่งกลับขายใส่ Quotation"]
    P7 --> H2

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class P3,P6 doc
    class AI1 ai
    class H1,H2 hand
```

---

## 3. กฎหมาย

**ตำแหน่ง:** Legal Counsel · ผู้มีอำนาจลงนาม (กรรมการ)

```mermaid
flowchart TD
    L0["งานสัญญาเข้า<br/>จากขาย / จัดซื้อ"] --> L1["เปิด Contract"]
    L1 --> AI1["AI ตรวจ clause เทียบ Playbook<br/>แนบความเห็น (L2)"]
    AI1 --> L2{"ความเสี่ยง?"}
    L2 -->|"สูง"| L3["Legal แก้ไข / ต่อรอง"]
    L3 --> L4{"คู่สัญญายอม?"}
    L4 -->|"ไม่"| L5["แจ้งขาย / จัดซื้อ ตัดสินใจ"]
    L4 -->|"ยอม"| L6
    L2 -->|"ต่ำ"| L6["Legal อนุมัติ"]
    L6 --> A1["ผู้มีอำนาจลงนาม"]
    A1 --> L7["แนบไฟล์ที่ลงนามแล้ว"]
    L7 --> H1["แจ้งขาย / จัดซื้อ ไปต่อได้"]
    L7 --> AI2["AI เตือนก่อนหมดอายุ / ต่ออายุ"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class L1,L7 doc
    class AI1,AI2 ai
    class L6,A1 appr
    class L5,H1 hand
```

งานอื่นของกฎหมาย: NDA · หนังสือมอบอำนาจ · ตรวจ template ที่ฝ่ายอื่นใช้ (สัญญาจ้าง, ใบเสนอราคา) · อนุมัติทำลายเอกสารที่ครบอายุเก็บ

---

## 4. จัดซื้อ

**ตำแหน่ง:** Buyer · Procurement Manager · ผู้อนุมัติตามวงเงิน

```mermaid
flowchart TD
    R0{"คำขอซื้อมาจาก?"}
    R0 -->|"ฝ่ายต่างๆ"| R1["Material Request"]
    R0 -->|"สต๊อกถึงจุดสั่งซื้อ"| R1
    AI1["AI พยากรณ์วัตถุดิบหมด<br/>ร่างล่วงหน้า (L1)"] -.-> R1
    R1 --> R2{"วงเงิน?"}
    R2 -->|"ไม่เกิน 50k"| A1["หัวหน้าฝ่าย"]
    R2 -->|"50k–500k"| A2["ผู้อำนวยการ"]
    R2 -->|"เกิน 500k"| A3["CFO / CEO"]
    A1 --> R3
    A2 --> R3
    A3 --> R3{"ต้องเทียบราคา?"}
    R3 -->|"ใช่"| R4["RFQ → Supplier Quotation"]
    R4 --> AI2["AI สรุปเทียบราคา (L0)"]
    AI2 --> R5["เลือกผู้ขาย"]
    R3 -->|"ไม่"| R5
    R5 --> R6{"ผู้ขายใหม่?"}
    R6 -->|"ใช่"| R7["สร้าง Supplier<br/>บัญชีธนาคารต้องอนุมัติ 2 คน"]
    R6 -->|"ไม่"| R8
    R7 --> R8{"ต้องมีสัญญา?"}
    R8 -->|"ใช่"| H1["ส่งกฎหมาย"]
    R8 -->|"ไม่"| R9
    H1 --> R9["สร้าง Purchase Order"]
    R9 --> A4["อนุมัติ PO<br/>ผู้สร้าง ≠ ผู้อนุมัติ"]
    A4 --> H2["ส่ง PO ให้ผู้ขาย"]
    H2 --> R10{"ของมาครบ ตรง?"}
    R10 -->|"ครบ"| H3["คลังรับของ"]
    R10 -->|"ไม่ครบ / ไม่ตรง"| R11["ติดต่อผู้ขาย<br/>รับบางส่วน / คืน"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class R1,R4,R7,R9,R11 doc
    class AI1,AI2 ai
    class A1,A2,A3,A4 appr
    class H1,H2,H3 hand
```

---

## 5. คลังและขนส่ง

**ตำแหน่ง:** Warehouse Officer · Logistics / Messenger · คนขับ

### 5.1 รับของเข้า

```mermaid
flowchart TD
    W0["ของจากผู้ขายมาถึง"] --> W1["เทียบกับ PO"]
    W1 --> W2{"จำนวน / สภาพ ถูกต้อง?"}
    W2 -->|"ครบ"| W3["Purchase Receipt"]
    W2 -->|"ขาด"| W4["รับบางส่วน"]
    W2 -->|"เสียหาย"| W5["ปฏิเสธ / คืนของ"]
    W4 --> W3
    W5 --> H1["แจ้งจัดซื้อ"]
    W3 --> W6["สแกนใบกำกับที่มากับของ"]
    W6 --> AI1["APX อ่าน · ตรวจ · จับคู่"]
    AI1 --> H2["ส่งบัญชีตรวจ"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class W3,W4 doc
    class AI1 ai
    class H1,H2 hand
```

### 5.2 ส่งของออก

```mermaid
flowchart TD
    D0["Sales Order พร้อมส่ง"] --> D1["หยิบของ + Delivery Note"]
    D1 --> D2["จัดเที่ยว Delivery Trip<br/>Google Maps คำนวณเวลาถึง"]
    AI1["AI เสนอรวมเที่ยวตามพื้นที่ (L0)"] -.-> D2
    D2 --> D3{"ส่งเองหรือจ้างขนส่ง?"}
    D3 -->|"รถตัวเอง"| D4["คนขับออกส่ง<br/>GPS เดิมของรถ"]
    D3 -->|"บริษัทขนส่ง"| D5["บันทึกเลขพัสดุ"]
    D4 --> D6["ถ่ายรูปใบส่งของที่ลูกค้าเซ็น<br/>ผ่าน LINE OA"]
    D5 --> D7["ดึงสถานะจากบริษัทขนส่ง"]
    D6 --> AI2["AI ตรวจลายเซ็น / จำนวน / พิกัด"]
    D7 --> D8
    AI2 --> D8{"ตรง?"}
    D8 -->|"ตรง"| D9["สถานะ: ส่งแล้ว"]
    D8 -->|"ไม่ตรง"| D10["กล่องตรวจ"]
    D9 --> H1["บัญชีวางบิลได้"]
    D9 --> AI3["LINE แจ้งลูกค้า (L1 → L2)"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class D1,D2,D5,D9 doc
    class AI1,AI2,AI3 ai
    class H1,D10 hand
```

### 5.3 งานภายในคลัง

| งาน | เอกสาร | ใครอนุมัติ |
|---|---|---|
| จ่ายของตามใบเบิก | Material Request → Stock Entry (Material Issue) | หัวหน้าฝ่ายผู้ขอ |
| โอนของระหว่างสาขา | Stock Entry (Material Transfer) | สโตร์ทั้งสองฝั่ง |
| ตรวจนับสต๊อกรายเดือน | Stock Reconciliation | หัวหน้าคลัง |
| วางบิล / รับเช็คตามรอบ (Messenger) | เอกสารวางบิล · Payment Entry | — |

---

## 6. สาขา 2 ศูนย์ประกอบ

**ตำแหน่ง:** หัวหน้าสาขา 2 · หัวหน้าไลน์ · ช่างประกอบ (รายวัน) · QC · สโตร์สาขา 2

```mermaid
flowchart TD
    M0["Sales Order สินค้าประกอบ"] --> M1["หัวหน้าสาขาเปิด Work Order"]
    M1 --> M2{"วัตถุดิบพอ?"}
    M2 -->|"ไม่พอ"| H1["Material Request → จัดซื้อ"]
    AI1["AI พยากรณ์ล่วงหน้า (L1)"] -.-> H1
    H1 --> M3
    M2 -->|"พอ"| M3["สโตร์โอนวัตถุดิบเข้า WIP"]
    M3 --> M4["ช่างลงเวลา + Job Card<br/>ประกอบ → ทดสอบ"]
    M4 --> M5{"QC ผ่าน?"}
    M5 -->|"ไม่ผ่าน"| M6{"แก้ได้?"}
    M6 -->|"ได้"| M4
    M6 -->|"ไม่ได้"| M7["บันทึกของเสีย"]
    M5 -->|"ผ่าน"| M8["Stock Entry: Manufacture<br/>เข้าคลังสินค้าสำเร็จรูป"]
    M8 --> H2["คลังจัดส่งลูกค้า"]
    M4 --> M9{"ทำ OT?"}
    M9 -->|"ใช่"| A1["หัวหน้าไลน์อนุมัติ Overtime Slip"]
    A1 --> AI2["AI ตรวจ OT เทียบเวลาเข้า-ออก"]
    AI2 --> H3["HR / Payroll (งาน 5)"]
    M4 --> M10{"เครื่องมือเสีย?"}
    M10 -->|"ใช่"| H4["HelpBot → Asset Repair"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class M1,M3,M4,M7,M8 doc
    class AI1,AI2 ai
    class A1 appr
    class H1,H2,H3,H4 hand
```

| ตำแหน่ง | ทำอะไรทุกวัน |
|---|---|
| หัวหน้าสาขา 2 | เปิด/ปิด Work Order · ดูต้นทุนต่อเครื่อง · ดูวัตถุดิบวิกฤต |
| หัวหน้าไลน์ | แจกงาน · อนุมัติ OT · ตรวจ Job Card |
| ช่างประกอบ | ลงเวลาเข้า-ออก · บันทึกงานใน Job Card |
| QC | Quality Inspection ผ่าน/ไม่ผ่าน · บันทึกของเสีย |
| สโตร์สาขา 2 | รับวัตถุดิบ · จ่ายเข้าผลิต · ตรวจนับ |

---

## 7. บัญชี

**ตำแหน่ง:** AP Accountant · AR Accountant · GL / Tax Accountant · Chief Accountant

### 7.1 เจ้าหนี้ (AP) — ใบกำกับผู้ขาย

```mermaid
flowchart TD
    AP0["ใบกำกับภาษีผู้ขาย<br/>อีเมล / คลังสแกน"] --> AI1["APX อ่าน + ตรวจกฎ<br/>13 หลัก · VAT 7% · ยอดรวม"]
    AI1 --> AP1{"ใบซ้ำ?"}
    AP1 -->|"ซ้ำ"| AP2["ปฏิเสธ + แจ้งเตือน"]
    AP1 -->|"ไม่ซ้ำ"| AI2["จับคู่ PO + ใบรับของ<br/>ร่าง Purchase Invoice (L1)"]
    AI2 --> AP3{"3-way match ผ่าน?"}
    AP3 -->|"ผ่าน"| AP4["AP ตรวจช่องที่ AI ไม่มั่นใจ"]
    AP3 -->|"ไม่ผ่าน"| H1["กล่องปัญหา → จัดซื้อ / ผู้ขาย"]
    H1 --> AI2
    AP4 --> A1["AP อนุมัติ → Submit<br/>ตั้งเจ้าหนี้ + ภาษีซื้อ"]
    A1 --> H2["เข้าคิวจ่าย (การเงิน)"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class AP2,AP4 doc
    class AI1,AI2 ai
    class A1 appr
    class H1,H2 hand
```

### 7.2 ลูกหนี้ (AR) — ออกใบกำกับถึงรับเงิน

```mermaid
flowchart TD
    AR0["ส่งของแล้ว (มีหลักฐาน)"] --> AR1{"สินค้าหรือบริการ?"}
    AR1 -->|"สินค้า"| AR2["Sales Invoice<br/>ภาษีขายเกิดตอนส่งมอบ"]
    AR1 -->|"บริการ"| AR3["ใบแจ้งหนี้<br/>ภาษีขายยังไม่ถึงกำหนด"]
    AR2 --> AR4["ใบวางบิลตามรอบลูกค้า"]
    AR3 --> AR4
    AR4 --> H1["Messenger / อีเมล ส่งลูกค้า"]
    H1 --> AR5{"การเงินยืนยันเงินเข้า?"}
    AR5 -->|"ยัง · เกินกำหนด"| AI1["AI ร่างอีเมลตามหนี้ (L1)"]
    AR5 -->|"เข้าแล้ว"| AR6{"ลูกค้าหัก ณ ที่จ่าย?"}
    AR6 -->|"หัก"| AR7["Payment Entry + รับ 50 ทวิ"]
    AR6 -->|"ไม่หัก"| AR8["Payment Entry"]
    AR7 --> AR9["ใบเสร็จ / ใบกำกับภาษี (บริการ)"]
    AR8 --> AR9
    AR9 --> AR10{"ลูกค้าคืนของ / ขอลดราคา?"}
    AR10 -->|"ใช่"| AR11["ใบลดหนี้ อ้างใบเดิม"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class AR2,AR3,AR4,AR7,AR8,AR9,AR11 doc
    class AI1 ai
    class H1 hand
```

### 7.3 ปิดงวดรายเดือน / รายปี

```mermaid
flowchart TD
    C0["สิ้นเดือน"] --> AI1["Close Assistant<br/>checklist เอกสารค้าง (L2)"]
    AI1 --> C1["ตามเอกสารที่ขาด"]
    C1 --> H1["การเงินกระทบยอดธนาคาร"]
    H1 --> C2["รายการปรับปรุง (Journal Entry)<br/>ค่าเสื่อม · ค้างจ่าย · ค้างรับ"]
    C2 --> A1["Chief Accountant อนุมัติ"]
    A1 --> C3["รายงานภาษี<br/>ภ.พ.30 · ภ.ง.ด.3 / 53 · ภ.ง.ด.1 + ประกันสังคม"]
    C3 --> C4{"งบทดลองลงตัว?"}
    C4 -->|"ไม่"| C2
    C4 -->|"ลงตัว"| A2["Chief Accountant ปิดงวด (ล็อก)"]
    A2 --> C5["งบการเงินรายเดือน"]
    C5 --> AI2["AI ร่างคำอธิบายผล (L1)"]
    AI2 --> H2["ส่งผู้บริหาร"]
    C5 --> C6{"เดือน 12?"}
    C6 -->|"ใช่"| C7["ปิดบัญชีประจำปี<br/>→ ผู้สอบบัญชี → ยื่นงบ + ภ.ง.ด.50"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class C1,C2,C3,C5,C7 doc
    class AI1,AI2 ai
    class A1,A2 appr
    class H1,H2 hand
```

---

## 8. การเงิน

**ตำแหน่ง:** Finance Officer · Finance Manager · Credit Controller · CFO (วงเงินสูง)

```mermaid
flowchart TD
    F0{"งานเข้ามาแบบไหน?"}
    F0 -->|"เจ้าหนี้ครบกำหนด"| F1["จัดรอบจ่าย"]
    F1 --> F2{"ต้องหัก ณ ที่จ่าย?"}
    F2 -->|"ใช่"| F3["คำนวณ + ออก 50 ทวิ"]
    F2 -->|"ไม่"| A1
    F3 --> A1["Finance Manager อนุมัติ<br/>(วงเงินสูง: CFO)"]
    A1 --> F4["โอน / เช็ค → Payment Entry"]
    F4 --> H1["แจ้งผู้ขาย"]

    F0 -->|"เงินเข้าบัญชี"| F5["นำเข้า statement ธนาคาร"]
    F5 --> AI1["AI เสนอคู่กับใบแจ้งหนี้ (L1)"]
    AI1 --> F6{"คู่ถูก?"}
    F6 -->|"ใช่"| F7["ยืนยัน → Payment Entry"]
    F6 -->|"ไม่"| F8["จับคู่เอง"]
    F8 --> F7

    F0 -->|"ลูกหนี้เกินกำหนด"| AI2["AI ร่างอีเมลตามหนี้ (L1)"]
    AI2 --> F9{"เกิน 60 วัน?"}
    F9 -->|"ใช่"| F10["Credit Control ระงับเครดิต<br/>แจ้งขาย"]

    F0 -->|"ขอเปลี่ยนบัญชีธนาคารผู้ขาย"| F11["โทรยืนยันกับผู้ขายจริง"]
    F11 --> A2["อนุมัติ 2 คน"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class F1,F3,F4,F5,F7,F8,F10 doc
    class AI1,AI2 ai
    class A1,A2 appr
    class H1 hand
```

> AI **ไม่มีเครื่องมือจ่ายเงิน** — ทุกการจ่ายผ่านคน 2 คนเสมอ

---

## 9. HR

**ตำแหน่ง:** HR / Recruiter · HR Admin / Payroll · หัวหน้าแต่ละฝ่าย (อนุมัติลา/OT)

```mermaid
flowchart TD
    subgraph JOIN["รับพนักงานใหม่"]
        J0["ฝ่ายขออัตรา"] --> A1["ผู้บริหารอนุมัติ"]
        A1 --> J1["ประกาศรับสมัคร"]
        AI1["AI ร่าง JD (L1)"] -.-> J1
        J1 --> J2["สัมภาษณ์ → เลือก"]
        J2 --> J3["สัญญาจ้าง (template ที่ Legal อนุมัติ)"]
        J3 --> J4["สร้าง Employee"]
        J4 --> H1["HelpBot สร้างบัญชี + สิทธิ์ + เครื่อง"]
    end

    subgraph WORK["ระหว่างทำงาน"]
        K0["ลงเวลาเข้า-ออก"] --> K1["Attendance อัตโนมัติ"]
        K2["ใบลา"] --> A2["หัวหน้าอนุมัติ"]
        K3["Overtime Slip"] --> A3["หัวหน้าอนุมัติ"]
    end

    subgraph PAY["ปิดเงินเดือนรายเดือน"]
        Y0["Payroll Entry"] --> Y1["Salary Slip<br/>+ ประกันสังคม + ภาษี (งาน 5)"]
        Y1 --> AI2["AI ตรวจความผิดปกติ (แจ้งเตือน)"]
        AI2 --> A4["HR Manager อนุมัติ"]
        A4 --> H2["บัญชีบันทึก → การเงินโอน"]
        H2 --> Y2["ภ.ง.ด.1 + ประกันสังคม"]
    end

    subgraph LEAVE["ลาออก"]
        Q0["ตั้งวันทำงานวันสุดท้าย"] --> H3["HelpBot ปิดบัญชี + คืนเครื่อง"]
        H3 --> Q1["จ่ายเงินครั้งสุดท้าย"]
        Q1 --> Q2["หนังสือรับรองการทำงาน"]
    end

    JOIN ~~~ WORK
    PAY ~~~ LEAVE
    K1 --> Y0
    A2 --> Y0
    A3 --> Y0

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class J3,J4,K1,K2,K3,Y0,Y1,Y2,Q1,Q2 doc
    class AI1,AI2 ai
    class A1,A2,A3,A4 appr
    class H1,H2,H3 hand
```

> ข้อมูลเงินเดือนเป็น **confidential** — เห็นได้เฉพาะ HR / Payroll · AI รันในเครื่องเท่านั้น

---

## 10. IT

**ตำแหน่ง:** IT Manager · IT Support · System Admin · IT Security · IT Asset Admin

### 10.1 Helpdesk

```mermaid
flowchart TD
    T0["พนักงานแจ้งปัญหา<br/>LINE · อีเมล · AI Workspace"] --> AI1["HelpBot จัดประเภท"]
    AI1 --> T1{"ประเภท?"}
    T1 -->|"วิธีใช้ / ลืมรหัส"| AI2["ตอบด้วยคู่มือ (RAG)<br/>หรือส่งลิงก์ reset"]
    T1 -->|"ขอสิทธิ์"| T2{"ข้อมูลลับ?"}
    T2 -->|"ไม่"| A1["หัวหน้าอนุมัติ"]
    T2 -->|"ลับ"| A2["หัวหน้า + เจ้าของข้อมูลอนุมัติ"]
    A1 --> T3["ให้สิทธิ์ (L1)"]
    A2 --> T3
    T1 -->|"เครื่องเสีย"| T4["Asset Repair"]
    T1 -->|"เน็ตล่ม / ระบบล่ม"| T5["Ticket P1 + แจ้ง on-call"]
    T1 -->|"ความปลอดภัย"| T6["Escalate IT Security ทันที"]
    T1 -->|"ไม่แน่ใจ"| T7["IT Support รับเคส"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class T3,T4,T5 doc
    class AI1,AI2 ai
    class A1,A2 appr
    class T6,T7 hand
```

### 10.2 งานประจำของ IT

| งาน | รอบ | ใคร | ทำที่ |
|---|---|---|---|
| สร้าง/ปิดบัญชีตาม HR | ทุกครั้งที่มีคนเข้า/ออก | HelpBot + IT Admin | อัตโนมัติจาก event |
| มอบ/รับคืนเครื่อง | ทุกครั้ง | IT Asset Admin | Asset Movement |
| ดู security alert + audit | รายวัน | IT Security | AI Workspace |
| ทบทวนสิทธิ์ทุกฝ่าย | รายไตรมาส | IT Manager + หัวหน้าฝ่าย | รายการสิทธิ์ → หัวหน้ายืนยัน → ถอดที่ไม่ใช้ |
| ทดลอง restore backup | รายเดือน | System Admin | ทั้ง MariaDB และ PostgreSQL |
| เปลี่ยนโมเดล AI / เลื่อนระดับอิสระ | เมื่อมีโมเดลใหม่ | IT Manager อนุมัติ | Eval Dashboard |

---

## 11. ผู้บริหาร

**ตำแหน่ง:** CEO · CFO · CTO · COO

```mermaid
flowchart TD
    E0["เปิด Dashboard ตอนเช้า<br/>ยอดขาย · เงินสด · ลูกหนี้/เจ้าหนี้<br/>วัตถุดิบวิกฤต · งานรออนุมัติ"] --> E1{"มีงานรออนุมัติ?"}
    E1 -->|"มี"| E2{"ประเภท?"}
    E2 -->|"PO เกิน 500k"| A1["อนุมัติ / ตีกลับ"]
    E2 -->|"รอบจ่ายเงินวงเงินสูง"| A1
    E2 -->|"ส่วนลดเกิน 15%"| A1
    E2 -->|"สัญญาสำคัญ"| A1
    E1 -->|"ไม่มี"| E3
    A1 --> E3{"อยากรู้อะไรเพิ่ม?"}
    E3 -->|"ถามเร็ว"| AI1["Copilot ตอบตามสิทธิ์ (L3)<br/>เช่น ต้นทุนต่อเครื่องสาขา 2"]
    E3 -->|"เจาะลึก"| E4["เปิดรายงาน ERPNext"]
    AI1 --> E5["ตัดสินใจ / สั่งงาน"]
    E4 --> E5
    E6["ต้นเดือน: รับงบ + คำอธิบาย AI"] --> E7["ประชุมผลประกอบการ"]
    E7 --> E8["ปรับเป้า / งบประมาณ"]

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    class E0,E4,E6 doc
    class AI1 ai
    class A1 appr
```

---

## 12. ธุรการ / สารบรรณ

**ตำแหน่ง:** Admin / สารบรรณ

```mermaid
flowchart TD
    subgraph IN["หนังสือเข้า"]
        I0["หนังสือ กระดาษ / อีเมล"] --> I1["สแกน"]
        I1 --> AI1["AI จัดหมวด + เสนอฝ่ายรับ (L1)"]
        AI1 --> I2["ลงทะเบียนหนังสือรับ"]
        I2 --> H1["ส่งต่อฝ่ายที่เกี่ยวข้อง"]
    end
    subgraph OUT["หนังสือออก"]
        O0["ฝ่ายร่างหนังสือ"] --> AI2["AI ช่วยร่าง / เกลาภาษา (L1)"]
        AI2 --> O1["สารบรรณตรวจรูปแบบ + ออกเลขที่"]
        O1 --> O2{"มีผลผูกพัน?"}
        O2 -->|"ใช่"| H2["กฎหมายตรวจ"]
        O2 -->|"ไม่"| A1
        H2 --> A1["ผู้มีอำนาจลงนาม"]
        A1 --> O3["ส่ง + ลงทะเบียนหนังสือส่ง"]
    end
    subgraph KEEP["เก็บรักษา"]
        K0["เอกสารครบอายุเก็บ"] --> H3["กฎหมายอนุมัติทำลาย"]
        H3 --> K1["บันทึกการทำลาย"]
    end
    IN ~~~ OUT ~~~ KEEP

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef appr fill:#fef3c7,stroke:#d97706,color:#78350f
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class I2,O1,O3,K1 doc
    class AI1,AI2 ai
    class A1 appr
    class H1,H2,H3 hand
```

---

## 13. PMO และ Customer Support

**ตำแหน่ง:** Project Manager · BA · Engineer · Helpdesk ลูกค้า (Phase MVP+ / Pro)

```mermaid
flowchart TD
    subgraph PMO["โครงการ (Project-to-Cash)"]
        P0["สัญญาโครงการลงนาม"] --> P1["เปิด Project + milestone"]
        P1 --> P2["ทีมบันทึก Timesheet"]
        P2 --> P3["ส่งมอบ milestone"]
        P3 --> P4{"ลูกค้าตรวจรับ?"}
        P4 -->|"ไม่ผ่าน"| P2
        P4 -->|"ขอเปลี่ยนขอบเขต"| P5["Change Request → ขาย / Pre-sales"]
        P4 -->|"ผ่าน"| H1["บัญชีออกใบแจ้งหนี้ค่าบริการ"]
    end
    subgraph SUP["ลูกค้าแจ้งปัญหา (MA)"]
        S0["ลูกค้าแจ้ง LINE / อีเมล"] --> AI1["HelpBot ฝั่งลูกค้า<br/>หาสัญญา MA"]
        AI1 --> S1{"อยู่ในสัญญา?"}
        S1 -->|"ไม่"| H2["ขายออกใบเสนอราคางานซ่อม"]
        S1 -->|"อยู่"| S2["Issue + SLA"]
        S2 --> S3{"แก้ทางไกลได้?"}
        S3 -->|"ได้"| S4["Helpdesk แก้ → ปิด"]
        S3 -->|"ไม่ได้"| S5["ส่งช่างหน้างาน + เบิกอะไหล่"]
        S5 --> S4
    end
    PMO ~~~ SUP

    classDef doc fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef ai fill:#dbeafe,stroke:#2563eb,color:#1e3a8a
    classDef hand fill:#f3e8ff,stroke:#9333ea,color:#581c87
    class P1,P2,P5,S2,S4,S5 doc
    class AI1 ai
    class H1,H2 hand
```

---

## 14. รอบงานประจำวัน / สัปดาห์ / เดือน / ปี

| ฝ่าย | รายวัน | รายสัปดาห์ | รายเดือน | รายปี |
|---|---|---|---|---|
| ขาย | ใบเสนอราคา · ติดตามลูกค้า | ทบทวน pipeline | ยอดขายเทียบเป้า | ตั้งเป้าปีหน้า |
| จัดซื้อ | ใบขอซื้อ · PO · ตามของ | ดูวัตถุดิบใกล้หมด | ประเมินผู้ขาย | ต่อสัญญาผู้ขาย |
| คลัง / ขนส่ง | รับของ · ส่งของ · หลักฐานส่งมอบ | วางแผนเที่ยวรถ | ตรวจนับสต๊อก | ตรวจนับใหญ่สิ้นปี |
| สาขา 2 | Work Order · Job Card · QC · ลงเวลา | ทบทวนแผนผลิต | ต้นทุนต่อเครื่อง | — |
| บัญชี | ตรวจใบกำกับ (APX) · ออกใบกำกับ | วางบิลตามรอบ | ภาษี · ปิดงวด · งบรายเดือน | ปิดบัญชีปี · ผู้สอบบัญชี · ภ.ง.ด.50 |
| การเงิน | จับคู่เงินเข้า | รอบจ่าย · กระแสเงินสด | กระทบยอดธนาคาร | — |
| HR | ลา · OT · ลงเวลา | — | เงินเดือน · ภ.ง.ด.1 · ประกันสังคม | 50 ทวิ พนักงาน · ภ.ง.ด.1ก · ประเมินผล |
| IT | helpdesk · security alert | — | ทดลอง restore | — · **รายไตรมาส: ทบทวนสิทธิ์** |
| ผู้บริหาร | Dashboard · อนุมัติ | — | ประชุมผลประกอบการ | อนุมัติงบการเงิน · งบประมาณ |
| ธุรการ | หนังสือเข้า-ออก | — | — | ทำลายเอกสารครบอายุ |

← [หน้าแรกงาน 4](README.md)
