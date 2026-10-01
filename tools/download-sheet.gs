/**
 * Download form → Google Sheet, for fazmx.gamaleldien.com.
 *
 * Setup, once, in AZM X's Google account:
 *   1. Create a Google Sheet, for example "Azm X: downloads".
 *   2. Extensions → Apps Script. Replace the editor's contents with this file and save.
 *   3. Deploy → New deployment → type "Web app".
 *      Execute as: Me. Who has access: Anyone. Deploy, and allow the permissions it asks for.
 *   4. Copy the web app URL (it ends in /exec) into FORM_URL in src/index.src.html, then rebuild.
 *
 * Each submission adds one row to the "Downloads" tab: time, name, email, page.
 */
const TAB = "Downloads";
const HEADER = ["الوقت", "الاسم", "البريد الإلكتروني", "الصفحة"];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return reply({ ok: true });   // honeypot: people never see this field, bots fill it in

  const name = clean(p.name, 120);
  const email = clean(p.email, 200);
  if (!name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return reply({ ok: false, error: "invalid" });

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const book = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = book.getSheetByName(TAB) || book.insertSheet(TAB);
    if (sheet.getLastRow() === 0) sheet.appendRow(HEADER);
    sheet.appendRow([new Date(), name, email, clean(p.page, 200)]);
  } finally {
    lock.releaseLock();
  }
  return reply({ ok: true });
}

// Trim and cap a field. A value that starts with = + - or @ would run as a formula, so it gets a leading apostrophe.
function clean(value, max) {
  const s = String(value || "").trim().slice(0, max);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function reply(body) {
  return ContentService.createTextOutput(JSON.stringify(body)).setMimeType(ContentService.MimeType.JSON);
}
