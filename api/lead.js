// Ontvangt de formulieren van de website en stuurt ze als mail door via Brevo.
// Nodig in Vercel (Settings, Environment Variables): BREVO_API_KEY
// Optioneel: LEAD_FROM (standaard "NXEO website <website@nxeo.io>"), LEAD_TO (standaard sales@nxeo.io)
const TYPES = {
  nulmeting: { nl: 'Nieuwe aanvraag: gratis nulmeting', to: 'sales@nxeo.io' },
  start: { nl: 'Nieuwe aanvraag: start met NXEO', to: 'sales@nxeo.io' },
  gesprek: { nl: 'Nieuwe aanvraag: gesprek', to: 'sales@nxeo.io' },
  doorloop: { nl: 'Nieuwe aanvraag: website samen doorlopen', to: 'sales@nxeo.io' },
};
const mail = require('./_mail.js');
const clean = (v, max) => String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim().slice(0, max);
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// Brevo, transactionele mail: https://developers.brevo.com/reference/sendtransacemail
const addr = (v) => { const m = /^(.*)<([^>]+)>\s*$/.exec(v); return m ? { name: m[1].trim(), email: m[2].trim() } : { email: v.trim() }; };
async function send(key, mail) {
  const body = { sender: addr(mail.from), to: mail.to.map((e) => ({ email: e })), replyTo: { email: mail.reply_to }, subject: mail.subject, textContent: mail.text };
  if (mail.html) body.htmlContent = mail.html;
  const r = await fetch('https://api.brevo.com/v3/smtp/email', { method: 'POST', headers: { 'api-key': key, 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error('brevo ' + r.status + ' ' + (await r.text()).slice(0, 300));
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'method' });
  const key = process.env.BREVO_API_KEY;
  if (!key) return res.status(503).json({ ok: false, error: 'not_configured' });
  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { b = null; } }
  if (!b || typeof b !== 'object') return res.status(400).json({ ok: false, error: 'body' });
  if (clean(b.website_url, 200)) return res.status(200).json({ ok: true }); // verborgen veld: alleen robots vullen dit in
  const type = TYPES[b.type];
  const email = clean(b.email, 200);
  if (!type || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(email)) return res.status(400).json({ ok: false, error: 'invalid' });
  const lang = b.lang === 'en' ? 'en' : 'nl';
  const f = { name: clean(b.name, 120), company: clean(b.company, 160), site: clean(b.site, 300), email, phone: clean(b.phone, 60), pkg: clean(b.pkg, 60), term: clean(b.term, 60), price: clean(b.price, 60), msg: clean(b.msg, 3000), lang, page: clean(b.page, 300) };
  const n = mail.internal(b.type, f);
  const from = process.env.LEAD_FROM || 'NXEO website <website@nxeo.io>';
  try {
    await send(key, { from, to: [process.env.LEAD_TO || type.to], reply_to: email, subject: type.nl + (f.site ? ' · ' + f.site.replace(/^https?:\/\//, '').replace(/\/$/, '') : ''), text: n.text, html: n.html });
  } catch (e) {
    console.error(e.message);
    return res.status(502).json({ ok: false, error: 'send' });
  }
  try {
    const c = mail.build(b.type, lang, f);
    await send(key, { from, to: [email], reply_to: 'sales@nxeo.io', subject: c.subject, text: c.text, html: c.html });
  } catch (e) { console.error('confirm ' + e.message); }
  return res.status(200).json({ ok: true });
};
