// Geeft de pagina een ondertekend kaartje voor het versturen van een formulier. Zie _guard.js.
const guard = require('./_guard.js');
module.exports = (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') return res.status(405).json({ ok: false });
  if (!guard.fromOurSite(req)) return res.status(403).json({ ok: false });
  return res.status(200).json(Object.assign({ ok: true }, guard.issue()));
};
