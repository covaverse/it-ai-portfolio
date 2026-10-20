// สร้างฉบับเผยแพร่ที่เข้ารหัสจาก viewer/index.html → viewer/publish/index.html
// รัน:  python viewer/build.py  แล้ว  VIEWER_PASSWORD='...' node viewer/publish.mjs
// รหัสผ่านรับจาก env เท่านั้น ไม่ถูกเขียนลงไฟล์ · เนื้อหา gzip แล้วเข้ารหัส AES-256-GCM (กุญแจจาก PBKDF2-SHA256)
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { randomBytes, pbkdf2Sync, createCipheriv, createDecipheriv } from "node:crypto";
import { gzipSync, gunzipSync } from "node:zlib";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const ITER = 600_000;                                   // ค่าแนะนำของ OWASP สำหรับ PBKDF2-SHA256
const pass = process.env.VIEWER_PASSWORD || "";
if (pass.length < 8) throw new Error("ตั้ง VIEWER_PASSWORD อย่างน้อย 8 ตัวอักษร");

const html = readFileSync(join(HERE, "index.html"), "utf8");
const m = html.match(/^let DATA = (.*);$/m);
if (!m || m[1] === "/*__DATA__*/null") throw new Error("รัน python viewer/build.py ก่อน");
const plain = gzipSync(Buffer.from(m[1], "utf8"));

const salt = randomBytes(16), iv = randomBytes(12);
const key = pbkdf2Sync(pass, salt, ITER, 32, "sha256");
const c = createCipheriv("aes-256-gcm", key, iv);
const data = Buffer.concat([c.update(plain), c.final(), c.getAuthTag()]);   // WebCrypto ต้องการ ciphertext‖tag

// ตรวจว่าถอดกลับได้จริงก่อนเขียนไฟล์
const d = createDecipheriv("aes-256-gcm", key, iv);
d.setAuthTag(data.subarray(-16));
const back = gunzipSync(Buffer.concat([d.update(data.subarray(0, -16)), d.final()])).toString("utf8");
if (back !== m[1]) throw new Error("ถอดรหัสกลับไม่ตรง");

const enc = { salt: salt.toString("base64"), iv: iv.toString("base64"), iter: ITER, data: data.toString("base64") };
const out = html.replace(m[0], "let DATA = null;").replace("const ENC = /*__ENC__*/null;", `const ENC = ${JSON.stringify(enc)};`);
if (out.includes(m[1].slice(0, 200))) throw new Error("ยังมีเนื้อหาไม่เข้ารหัสหลุดอยู่");

mkdirSync(join(HERE, "publish"), { recursive: true });
writeFileSync(join(HERE, "publish", "index.html"), out);
writeFileSync(join(HERE, "publish", "README.md"),
  "# enterprise-os-plan\n\nหน้าแผนงานส่วนตัวแบบเข้ารหัส — เปิดที่ GitHub Pages ของ repo นี้แล้วใส่รหัสผ่าน\n" +
  "เนื้อหาถูกเข้ารหัส AES-256-GCM ในไฟล์ `index.html` · repo นี้ไม่มีไฟล์ต้นฉบับ\n");
console.log(`✅ viewer/publish/index.html (${(out.length / 1024).toFixed(0)} KB · เนื้อหาเข้ารหัส ${(data.length / 1024).toFixed(0)} KB)`);
