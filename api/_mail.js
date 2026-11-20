// Opmaak van de bevestigingsmail aan de aanvrager. Zelfde blauwe blok als bovenaan de website.
const SITE = 'https://nxeo.io';
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const FONT = "'Rethink Sans','Helvetica Neue',Helvetica,Arial,sans-serif";

const T = {
  nl: {
    hi: 'Hoi', next: 'Wat er nu gebeurt', yours: 'Jouw aanvraag', site: 'Website', pkg: 'Pakket', term: 'Looptijd', price: 'Prijs', comp: 'Concurrenten',
    q: 'Vraag je je iets af? Antwoord op deze mail, dan komt het bij ons team terecht.', sign: 'Tot snel,', team: 'Team NXEO',
    foot: 'Je krijgt deze mail omdat je een aanvraag hebt gedaan op nxeo.io.', privacy: 'Privacyverklaring', path: '/nl',
    types: {
      nulmeting: { subject: 'Je nulmeting is aangevraagd', pre: 'Binnen 48 uur heb je het rapport in je mail.', bubble: 'Noemt ChatGPT jouw bedrijf al?', title: 'We zoeken het voor je uit.', lead: 'Binnen 48 uur heb je het rapport in je mail. Gratis, en je zit nergens aan vast.',
        steps: [['We stellen echte koopvragen over jouw dienst', 'Aan ChatGPT, zoals jouw klanten ze ook stellen.'], ['We kijken waar je genoemd wordt', 'En wie er in jouw plaats staat als je ontbreekt.'], ['Je krijgt het rapport in je mail', 'Met de vragen waarop je genoemd wordt, de vragen die je verliest en de grootste gaten.']],
        btn: 'Lees hoe de nulmeting werkt', url: '/nl/nulmeting/' },
      start: { subject: 'Welkom bij NXEO', pre: 'We hebben je aanvraag ontvangen. De intake volgt binnen één werkdag.', bubble: 'Welkom bij NXEO', title: 'Welkom, {name}.', titleNoName: 'Welkom bij NXEO.', lead: 'We hebben je aanvraag ontvangen. Je hoeft nu niets te doen, wij nemen contact met je op.',
        steps: [['Intake binnen één werkdag', 'We nemen contact op en zetten de koppeling met je website klaar.'], ['Je nulmeting binnen 48 uur', 'Je ziet waar je nu staat en welke vragen je verliest.'], ['De eerste content gaat online', 'Je krijgt vooraf te zien wat er klaarstaat en keurt goed.']],
        btn: 'Bekijk de veelgestelde vragen', url: '/nl/veelgestelde-vragen/' },
      gesprek: { subject: 'Je gesprek met NXEO is aangevraagd', pre: 'We nemen binnen één werkdag contact op om een moment te kiezen.', bubble: 'Vijftien minuten, online', title: 'Tot snel, {name}.', titleNoName: 'Tot snel.', lead: 'We nemen binnen één werkdag contact met je op om een moment te kiezen dat jou past.',
        steps: [['We kiezen samen een moment', 'Je krijgt een voorstel per mail.'], ['We kijken live naar jouw bedrijf', 'Vijftien minuten online, in ChatGPT en Google.'], ['Je beslist zelf of je start', 'Zonder verplichting.']],
        btn: 'Bekijk de pakketten', url: '/nl/prijzen/' },
      doorloop: { subject: 'We lopen je website samen door', pre: 'We nemen binnen één werkdag contact op om een moment te kiezen.', bubble: 'Vijftien minuten, online', title: 'Tot snel, {name}.', titleNoName: 'Tot snel.', lead: 'We nemen binnen één werkdag contact met je op om een moment te kiezen. Je hoeft niets voor te bereiden.',
        steps: [['We kiezen samen een moment', 'Je krijgt een voorstel per mail.'], ['We lopen samen door je website', 'We kijken of AI je website kan lezen en hoe AI je nu noemt.'], ['Je krijgt drie stappen mee', 'Waar je zelf mee verder kunt, ook als je het daarna zelf doet.']],
        btn: 'Bekijk de koppelingen', url: '/nl/werkt-met/' },
      sollicitatie: { subject: 'Je bericht aan NXEO is binnen', pre: 'We lezen het en laten snel van ons horen.', bubble: 'Werken bij NXEO?', title: 'Fijn dat je reageert, {name}.', titleNoName: 'Fijn dat je reageert.', lead: 'We hebben je bericht ontvangen. We lezen het rustig en laten snel van ons horen.',
        steps: [['We lezen je bericht', 'En je cv, als je die hebt meegestuurd.'], ['We plannen een kennismaking', 'Een kwartier online, op een moment dat jou past.'], ['We kijken samen of het past', 'Open, van twee kanten.']],
        btn: 'Bekijk de pagina nog eens', url: '/nl/werken-bij/' },
    },
  },
  en: {
    hi: 'Hi', next: 'What happens now', yours: 'Your request', site: 'Website', pkg: 'Plan', term: 'Term', price: 'Price', comp: 'Competitors',
    q: 'Wondering about something? Reply to this email and it reaches our team.', sign: 'Speak soon,', team: 'Team NXEO',
    foot: 'You are receiving this email because you made a request on nxeo.io.', privacy: 'Privacy statement', path: '/en',
    types: {
      nulmeting: { subject: 'Your baseline check has been requested', pre: 'Within 48 hours the report is in your inbox.', bubble: 'Does ChatGPT mention your company yet?', title: 'We will find out for you.', lead: 'Within 48 hours the report is in your inbox. Free, and without any commitment.',
        steps: [['We ask real buying questions about your service', 'To ChatGPT, the way your customers ask them.'], ['We see where you are mentioned', 'And who appears in your place when you are missing.'], ['You receive the report by email', 'With the questions you are mentioned for, the questions you lose and the biggest gaps.']],
        btn: 'Read how the baseline check works', url: '/en/free-check/' },
      start: { subject: 'Welcome to NXEO', pre: 'We have received your request. The onboarding follows within one working day.', bubble: 'Welcome to NXEO', title: 'Welcome, {name}.', titleNoName: 'Welcome to NXEO.', lead: 'We have received your request. There is nothing you need to do now, we will get in touch.',
        steps: [['Onboarding within one working day', 'We get in touch and set up the connection with your website.'], ['Your baseline check within 48 hours', 'You see where you stand now and which questions you are losing.'], ['The first content goes online', 'You see beforehand what is ready and you approve it.']],
        btn: 'View the frequently asked questions', url: '/en/faq/' },
      gesprek: { subject: 'Your call with NXEO has been requested', pre: 'We will get in touch within one working day to pick a time.', bubble: 'Fifteen minutes, online', title: 'Speak soon, {name}.', titleNoName: 'Speak soon.', lead: 'We will get in touch within one working day to pick a time that suits you.',
        steps: [['We pick a time together', 'You receive a proposal by email.'], ['We look at your company live', 'Fifteen minutes online, in ChatGPT and Google.'], ['You decide whether to start', 'Without obligation.']],
        btn: 'View the plans', url: '/en/pricing/' },
      doorloop: { subject: 'We will go through your website together', pre: 'We will get in touch within one working day to pick a time.', bubble: 'Fifteen minutes, online', title: 'Speak soon, {name}.', titleNoName: 'Speak soon.', lead: 'We will get in touch within one working day to pick a time. There is nothing to prepare.',
        steps: [['We pick a time together', 'You receive a proposal by email.'], ['We go through your website together', 'We check whether AI can read your website and how AI mentions you today.'], ['You leave with three next steps', 'Yours to act on, also if you carry on without us.']],
        btn: 'View the integrations', url: '/en/works-with/' },
      sollicitatie: { subject: 'Your message to NXEO has arrived', pre: 'We will read it and get back to you soon.', bubble: 'Working at NXEO?', title: 'Good to hear from you, {name}.', titleNoName: 'Good to hear from you.', lead: 'We have received your message. We will read it properly and get back to you soon.',
        steps: [['We read your message', 'And your CV, if you sent one.'], ['We plan a short introduction', 'Fifteen minutes online, at a time that suits you.'], ['We see together whether it fits', 'Openly, from both sides.']],
        btn: 'View the page again', url: '/en/careers/' },
    },
  },
};

function build(type, lang, f) {
  const t = T[lang] || T.nl; const c = t.types[type] || t.types.gesprek;
  const first = esc((f.name || '').trim().split(/\s+/)[0]);
  const title = first && c.title.includes('{name}') ? c.title.replace('{name}', first) : (c.titleNoName || c.title);
  const rows = [[t.site, f.site], [t.pkg, f.pkg], [t.term, f.term], [t.price, f.price], [t.comp, f.comp]].filter((r) => r[1]);
  const steps = c.steps.map((s, i) => `<tr><td width="44" valign="top" style="padding:0 0 18px"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td width="30" height="30" align="center" bgcolor="#EEF1FF" style="border-radius:10px;font:700 14px/30px ${FONT};color:#002EFE">${i + 1}</td></tr></table></td><td valign="top" style="padding:3px 0 18px;font:400 15px/1.5 ${FONT};color:#5B6577"><b style="display:block;color:#1A2332;font-weight:600;font-size:16px">${esc(s[0])}</b>${esc(s[1])}</td></tr>`).join('');
  const summary = rows.length ? `<tr><td class="pad" style="padding:0 40px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#F2F3F7" style="border-radius:18px"><tr><td style="padding:20px 22px 10px;font:600 13px/1.4 ${FONT};color:#002EFE">${t.yours}</td></tr>${rows.map((r) => `<tr><td style="padding:0 22px 10px;font:400 15px/1.5 ${FONT};color:#5B6577">${r[0]}<br><b style="color:#1A2332;font-weight:600">${esc(r[1])}</b></td></tr>`).join('')}<tr><td height="10" style="font-size:0;line-height:0">&nbsp;</td></tr></table></td></tr>` : '';
  const html = `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>${esc(c.subject)}</title><link href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"><style>@media (max-width:620px){.wrap{width:100%!important}.pad{padding-left:24px!important;padding-right:24px!important}.h1{font-size:34px!important}}</style></head>
<body style="margin:0;padding:0;background:#F2F3F7">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#F2F3F7">${esc(c.pre)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#F2F3F7"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;background:#ffffff;border-radius:28px;overflow:hidden">
<tr><td class="pad" align="center" bgcolor="#002EFE" style="background:#002EFE;background-image:linear-gradient(135deg,#002EFE,#4E6BFF);padding:36px 40px 44px;border-radius:28px 28px 0 0">
<a href="${SITE}${t.path}/" style="text-decoration:none"><img src="${SITE}/assets/img/nxeo_light.png" width="104" alt="NXEO" style="display:block;border:0;width:104px;height:auto;margin:0 auto 30px"></a>
<table role="presentation" cellpadding="0" cellspacing="0" align="center"><tr><td bgcolor="#ffffff" style="border-radius:24px 24px 24px 7px;padding:12px 22px;font:700 16px/1.2 ${FONT};color:#002EFE">${esc(c.bubble)}</td></tr></table>
<div class="h1" style="font:700 42px/1.05 ${FONT};letter-spacing:-1.5px;color:#ffffff;margin:22px 0 14px">${title}</div>
<div style="font:400 17px/1.5 ${FONT};color:#E6EBFF;max-width:440px;margin:0 auto">${esc(c.lead)}</div>
</td></tr>
<tr><td class="pad" style="padding:36px 40px 6px;font:700 20px/1.2 ${FONT};letter-spacing:-.4px;color:#1A2332">${t.next}</td></tr>
<tr><td class="pad" style="padding:18px 40px 4px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${steps}</table></td></tr>
${summary}
<tr><td class="pad" align="left" style="padding:22px 40px 8px"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td bgcolor="#002EFE" style="border-radius:999px;background:#002EFE;background-image:linear-gradient(135deg,#002EFE,#4E6BFF)"><a href="${SITE}${c.url}" style="display:inline-block;padding:14px 26px;font:600 16px/1 ${FONT};color:#ffffff;text-decoration:none">${esc(c.btn)} &rarr;</a></td></tr></table></td></tr>
<tr><td class="pad" style="padding:22px 40px 36px;font:400 15px/1.6 ${FONT};color:#5B6577">${t.q}<br><br>${t.sign}<br><b style="color:#1A2332;font-weight:600">${t.team}</b></td></tr>
</table>
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px"><tr><td align="center" style="padding:22px 24px 8px;font:400 12px/1.6 ${FONT};color:#8A93A3">${t.foot}<br><a href="${SITE}${t.path}/" style="color:#8A93A3">nxeo.io</a> &nbsp;·&nbsp; <a href="${SITE}${lang === 'en' ? '/en/privacy/' : '/nl/privacy/'}" style="color:#8A93A3">${t.privacy}</a> &nbsp;·&nbsp; <a href="mailto:hello@nxeo.io" style="color:#8A93A3">hello@nxeo.io</a></td></tr></table>
</td></tr></table></body></html>`;
  const text = `${t.hi}${first ? ' ' + first : ''},\n\n${c.lead}\n\n${t.next}\n${c.steps.map((s, i) => `${i + 1}. ${s[0]}. ${s[1]}`).join('\n')}\n\n${rows.length ? t.yours + '\n' + rows.map((r) => `${r[0]}: ${r[1]}`).join('\n') + '\n\n' : ''}${c.btn}: ${SITE}${c.url}\n\n${t.q}\n\n${t.sign}\n${t.team}`;
  return { subject: c.subject, html, text };
}
// Interne melding naar sales@: zelfde blok, maar kort en zakelijk. Alles wat je nodig hebt om te reageren staat bovenaan.
const NAMES = { nulmeting: 'Gratis nulmeting', start: 'Start met NXEO', gesprek: 'Gesprek', doorloop: 'Website samen doorlopen', sollicitatie: 'Sollicitatie' };
const LAB = { name: 'Naam', company: 'Bedrijf', site: 'Website', email: 'E-mail', phone: 'Telefoon', role: 'Functie', cv: 'Cv', pkg: 'Pakket', term: 'Looptijd', price: 'Prijs', comp: 'Concurrenten', lang: 'Taal', page: 'Pagina' };
function internal(type, f) {
  const first = esc((f.name || '').trim().split(/\s+/)[0]);
  const bare = (f.site || '').replace(/^https?:\/\//, '').replace(/\/$/, '');
  const href = f.site ? (/^https?:\/\//.test(f.site) ? f.site : 'https://' + f.site) : '';
  const link = (u, t) => `<a href="${esc(u)}" style="color:#002EFE;text-decoration:none;font-weight:600">${esc(t)}</a>`;
  const val = (k) => k === 'email' ? link('mailto:' + f.email, f.email) : k === 'site' ? link(href, bare) : k === 'phone' ? link('tel:' + f.phone.replace(/[^\d+]/g, ''), f.phone) : k === 'lang' ? (f.lang === 'en' ? 'Engels' : 'Nederlands') : esc(f[k]);
  const keys = Object.keys(LAB).filter((k) => f[k]);
  const rows = keys.map((k, i) => `<tr><td width="110" valign="top" style="padding:11px 0;${i ? 'border-top:1px solid #E6E8EE;' : ''}font:400 14px/1.5 ${FONT};color:#5B6577">${LAB[k]}</td><td valign="top" style="padding:11px 0;${i ? 'border-top:1px solid #E6E8EE;' : ''}font:500 15px/1.5 ${FONT};color:#1A2332;word-break:break-word">${val(k)}</td></tr>`).join('');
  const msg = f.msg ? `<tr><td class="pad" style="padding:8px 40px 0"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#F2F3F7" style="border-radius:18px"><tr><td style="padding:18px 22px 4px;font:600 13px/1.4 ${FONT};color:#002EFE">Bericht</td></tr><tr><td style="padding:0 22px 20px;font:400 15px/1.6 ${FONT};color:#1A2332">${esc(f.msg).replace(/\n/g, '<br>')}</td></tr></table></td></tr>` : '';
  const subject = 'Nieuwe aanvraag: ' + (NAMES[type] || type).toLowerCase() + (bare ? ' · ' + bare : '');
  const who = [f.name, f.company].filter(Boolean).map(esc).join(', ');
  const html = `<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>${esc(subject)}</title><link href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"><style>@media (max-width:620px){.wrap{width:100%!important}.pad{padding-left:24px!important;padding-right:24px!important}.h1{font-size:28px!important}}</style></head>
<body style="margin:0;padding:0;background:#F2F3F7">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#F2F3F7"><tr><td align="center" style="padding:28px 12px">
<table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:600px;background:#ffffff;border-radius:28px;overflow:hidden">
<tr><td class="pad" align="left" bgcolor="#002EFE" style="background:#002EFE;background-image:linear-gradient(135deg,#002EFE,#4E6BFF);padding:30px 40px 32px;border-radius:28px 28px 0 0">
<img src="${SITE}/assets/img/nxeo_light.png" width="84" alt="NXEO" style="display:block;border:0;width:84px;height:auto;margin:0 0 24px">
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td bgcolor="#ffffff" style="border-radius:20px 20px 20px 6px;padding:9px 16px;font:700 14px/1.2 ${FONT};color:#002EFE">Nieuwe aanvraag</td></tr></table>
<div class="h1" style="font:700 32px/1.1 ${FONT};letter-spacing:-1px;color:#ffffff;margin:16px 0 8px">${esc(NAMES[type] || type)}</div>
<div style="font:400 16px/1.5 ${FONT};color:#E6EBFF">${[who, esc(bare)].filter(Boolean).join(' &nbsp;·&nbsp; ') || esc(f.email)}</div>
</td></tr>
<tr><td class="pad" style="padding:22px 40px 10px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows}</table></td></tr>
${msg}
<tr><td class="pad" align="left" style="padding:22px 40px 14px"><table role="presentation" cellpadding="0" cellspacing="0"><tr><td bgcolor="#002EFE" style="border-radius:999px;background:#002EFE;background-image:linear-gradient(135deg,#002EFE,#4E6BFF)"><a href="mailto:${esc(f.email)}" style="display:inline-block;padding:14px 26px;font:600 16px/1 ${FONT};color:#ffffff;text-decoration:none">Beantwoord ${first || 'de aanvraag'} &rarr;</a></td></tr></table></td></tr>
<tr><td class="pad" style="padding:6px 40px 34px;font:400 14px/1.6 ${FONT};color:#5B6577">Een antwoord op deze mail gaat direct naar de aanvrager. De aanvrager krijgt zelf ook een bevestiging.</td></tr>
</table>
</td></tr></table></body></html>`;
  const text = (NAMES[type] || type) + '\n\n' + keys.map((k) => LAB[k] + ': ' + (k === 'lang' ? (f.lang === 'en' ? 'Engels' : 'Nederlands') : f[k])).join('\n') + (f.msg ? '\n\nBericht:\n' + f.msg : '');
  return { subject, html, text };
}
module.exports = { build, internal };
