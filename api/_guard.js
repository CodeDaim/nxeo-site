// Onzichtbare spambeveiliging voor de formulieren. Geen puzzel en geen vinkje voor de bezoeker.
// 1. De pagina haalt een ondertekend kaartje op zodra iemand echt iets aanraakt (/api/token).
// 2. Bij versturen moet dat kaartje geldig zijn, niet te vers (een mens typt niet in een seconde) en niet te oud.
// 3. De browser lost een kleine rekensom op die aan het mailadres vastzit. Voor één mens merk je niets, voor duizenden berichten is het duur.
// 4. Het verzoek moet van onze eigen site komen, en de inhoud mag er niet uitzien als reclame.
const crypto = require('crypto');
const BITS = 12, MIN_MS = 2000, MAX_MS = 3 * 3600 * 1000;
const secret = () => crypto.createHash('sha256').update('nxeo-guard:' + (process.env.GUARD_SECRET || process.env.BREVO_API_KEY || 'dev')).digest();
const sign = (t, n) => crypto.createHmac('sha256', secret()).update(t + '.' + n).digest('hex').slice(0, 32);
const used = new Map();

function issue() {
  const t = Date.now().toString(36), n = crypto.randomBytes(8).toString('hex');
  return { token: t + '.' + n + '.' + sign(t, n), bits: BITS, wait: MIN_MS };
}
function zeroBits(buf) { let z = 0; for (const b of buf) { if (b === 0) { z += 8; continue; } z += Math.clz32(b) - 24; break; } return z; }

function fromOurSite(req) {
  const h = req.headers || {};
  const okHost = (u) => { try { const x = new URL(u).hostname; return x === 'nxeo.io' || x === 'www.nxeo.io' || x.endsWith('.vercel.app') || x === 'localhost' || x === '127.0.0.1'; } catch (e) { return false; } };
  const sfs = h['sec-fetch-site'];
  if (sfs) return sfs === 'same-origin';
  return okHost(h.origin || '') || okHost(h.referer || '');
}

// geeft '' als het in orde is, anders de reden
function check(req, b, email) {
  if (!fromOurSite(req)) return 'origin';
  const g = b && b.g;
  if (!g || typeof g.t !== 'string' || typeof g.n !== 'string' || g.t.length > 80 || g.n.length > 24) return 'token';
  const p = g.t.split('.');
  if (p.length !== 3) return 'token';
  let ok = false;
  try { ok = crypto.timingSafeEqual(Buffer.from(sign(p[0], p[1])), Buffer.from(p[2])); } catch (e) { ok = false; }
  if (!ok) return 'token';
  const age = Date.now() - parseInt(p[0], 36);
  if (!(age >= MIN_MS)) return 'fast';
  if (age > MAX_MS) return 'old';
  if (zeroBits(crypto.createHash('sha256').update(g.t + ':' + email.toLowerCase() + ':' + g.n).digest()) < BITS) return 'work';
  const now = Date.now();
  for (const [k, v] of used) if (now - v > MAX_MS) used.delete(k);
  if (used.has(g.t)) return 'replay';
  used.set(g.t, now);
  return '';
}

// inhoud die er bij een echte aanvraag niet in hoort
function looksLikeSpam(f) {
  const link = /(https?:\/\/|www\.)/i, tag = /<\s*(a|script|img|iframe)\b|\[url[=\]]/i;
  for (const k of ['name', 'company', 'phone', 'pkg', 'term', 'role']) if (f[k] && (link.test(f[k]) || /[<>]/.test(f[k]))) return true;
  const m = f.msg || '';
  if (tag.test(m)) return true;
  if ((m.match(/(https?:\/\/|www\.)/gi) || []).length > 2) return true;
  if (f.name && f.name.length > 3 && m && m.trim() === f.name.trim()) return true;
  return false;
}
module.exports = { issue, check, looksLikeSpam, fromOurSite };
