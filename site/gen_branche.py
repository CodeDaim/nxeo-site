# Bouwt de pagina's "NXEO voor ..." per branche, met de bouwstenen van de homepage.
# Draai: python3 gen_branche.py  (schrijft content/{nl,en}/br_*.html, branches.html en de i18n regels)
# Regels: geen verzonnen cijfers of klanten. De vragen en onderwerpen zijn voorbeelden van wat een klant aan AI vraagt.
import json, re

# Per branche: key, en per taal: slug, meervoud, enkelvoud (met lidwoord in het Engels), woord voor klanten,
# vraag in de tekstballon, vijf voorbeeldvragen (wie doet dit, wie is de beste, vergelijken, snel, wat kost het),
# vier onderwerpen (titel, soort) en de eerste veelgestelde vraag.
B = [
 dict(key='loodgieters',
  nl=dict(slug='loodgieters', pl='loodgieters', sg='loodgieter', k='klanten', bub='Wie is een goede loodgieter in de buurt?',
   q=['Welke loodgieter komt bij mij in de buurt?', 'Wie is de beste loodgieter in mijn stad?', 'Cv ketel vervangen of repareren, wat is slimmer?', 'Welke loodgieter kan vandaag nog komen bij een lekkage?', 'Wat kost het om een lekkage te laten repareren?'],
   t=[('Wat kost een lekkage laten repareren?', 'Artikel'), ('Cv ketel vervangen of repareren?', 'Artikel'), ('Loodgieter in jouw werkgebied', 'Pagina'), ('Wat doe je bij een gesprongen leiding?', 'Artikel')]),
  en=dict(slug='plumbers', pl='plumbers', sg='a plumber', k='customers', bub='Who is a good plumber near me?',
   q=['Which plumber comes out to my area?', 'Who is the best plumber in my city?', 'Replace or repair a boiler, which is smarter?', 'Which plumber can still come today for a leak?', 'What does it cost to have a leak repaired?'],
   t=[('What does repairing a leak cost?', 'Article'), ('Replace or repair your boiler?', 'Article'), ('Plumber in your service area', 'Page'), ('What to do when a pipe bursts?', 'Article')])),
 dict(key='timmermannen', story=True,
  nl=dict(slug='timmermannen', pl='timmermannen', sg='timmerman', k='klanten', bub='Wie is een goede timmerman in de buurt?',
   q=['Welke timmerman maakt een kast op maat?', 'Wie is de beste timmerman in mijn regio?', 'Kast op maat of een kast van de bouwmarkt, wat is het verschil?', 'Welke timmerman kan op korte termijn een kozijn herstellen?', 'Wat kost een inbouwkast op maat?'],
   t=[('Wat kost een inbouwkast op maat?', 'Artikel'), ('Houtrot in een kozijn: herstellen of vervangen?', 'Artikel'), ('Timmerman in jouw werkgebied', 'Pagina'), ('Hoe lang duurt het plaatsen van een dakkapel?', 'Artikel')]),
  en=dict(slug='carpenters', pl='carpenters', sg='a carpenter', k='customers', bub='Who is a good carpenter near me?',
   q=['Which carpenter builds a made to measure wardrobe?', 'Who is the best carpenter in my area?', 'Made to measure or flat pack, what is the difference?', 'Which carpenter can repair a window frame at short notice?', 'What does a fitted wardrobe cost?'],
   t=[('What does a fitted wardrobe cost?', 'Article'), ('Wood rot in a frame: repair or replace?', 'Article'), ('Carpenter in your service area', 'Page'), ('How long does fitting a dormer take?', 'Article')])),
 dict(key='schilders',
  nl=dict(slug='schilders', pl='schilders', sg='schilder', k='klanten', bub='Wie is een goede schilder in de buurt?',
   q=['Welke schilder doet ook buitenwerk?', 'Wie is de beste schilder in mijn regio?', 'Zelf schilderen of een schilder inhuren, wat scheelt het?', 'Welke schilder kan nog voor de winter komen?', 'Wat kost het om een huis buiten te laten schilderen?'],
   t=[('Wat kost buitenschilderwerk?', 'Artikel'), ('Hoe vaak moet je kozijnen laten schilderen?', 'Artikel'), ('Schilder in jouw werkgebied', 'Pagina'), ('Schilderen in de winter: kan dat?', 'Artikel')]),
  en=dict(slug='painters', pl='painters', sg='a painter', k='customers', bub='Who is a good painter near me?',
   q=['Which painter also does exterior work?', 'Who is the best painter in my area?', 'Paint it yourself or hire a painter, what is the difference?', 'Which painter can still come before winter?', 'What does painting the outside of a house cost?'],
   t=[('What does exterior painting cost?', 'Article'), ('How often should window frames be painted?', 'Article'), ('Painter in your service area', 'Page'), ('Painting in winter: is that possible?', 'Article')])),
 dict(key='hoveniers',
  nl=dict(slug='hoveniers', pl='hoveniers', sg='hovenier', k='klanten', bub='Wie is een goede hovenier in de buurt?',
   q=['Welke hovenier legt een complete tuin aan?', 'Wie is de beste hovenier in mijn regio?', 'Tegels of gras, wat is beter voor een kleine tuin?', 'Welke hovenier kan dit voorjaar nog beginnen?', 'Wat kost het om een tuin te laten aanleggen?'],
   t=[('Wat kost een tuin laten aanleggen?', 'Artikel'), ('Een tuin met weinig onderhoud: wat werkt echt?', 'Artikel'), ('Hovenier in jouw werkgebied', 'Pagina'), ('Wanneer is de beste tijd om een tuin aan te leggen?', 'Artikel')]),
  en=dict(slug='gardeners', pl='landscape gardeners', sg='a landscape gardener', k='customers', bub='Who is a good landscape gardener near me?',
   q=['Which gardener lays out a complete garden?', 'Who is the best landscape gardener in my area?', 'Paving or lawn, which is better for a small garden?', 'Which gardener can still start this spring?', 'What does having a garden landscaped cost?'],
   t=[('What does landscaping a garden cost?', 'Article'), ('A low maintenance garden: what really works?', 'Article'), ('Gardener in your service area', 'Page'), ('When is the best time to lay out a garden?', 'Article')])),
 dict(key='aannemers',
  nl=dict(slug='aannemers', pl='aannemers', sg='aannemer', k='klanten', bub='Wie is een goede aannemer voor een verbouwing?',
   q=['Welke aannemer bouwt een aanbouw?', 'Wie is de beste aannemer in mijn regio?', 'Aanbouw of opbouw, wat past bij mijn huis?', 'Welke aannemer kan binnen drie maanden beginnen?', 'Wat kost een aanbouw per vierkante meter?'],
   t=[('Wat kost een aanbouw?', 'Artikel'), ('Heb ik een vergunning nodig voor een aanbouw?', 'Artikel'), ('Aannemer in jouw werkgebied', 'Pagina'), ('Hoe lang duurt een verbouwing?', 'Artikel')]),
  en=dict(slug='builders', pl='builders', sg='a builder', k='customers', bub='Who is a good builder for a renovation?',
   q=['Which builder does extensions?', 'Who is the best builder in my area?', 'Extend outwards or upwards, what suits my house?', 'Which builder can start within three months?', 'What does an extension cost per square metre?'],
   t=[('What does an extension cost?', 'Article'), ('Do I need a permit for an extension?', 'Article'), ('Builder in your service area', 'Page'), ('How long does a renovation take?', 'Article')])),
 dict(key='tandartsen', care=True,
  nl=dict(slug='tandartsen', pl='tandartsen', sg='tandarts', k='patiënten', bub='Welke tandarts neemt nog nieuwe patiënten aan?',
   q=['Welke tandarts in de buurt neemt nieuwe patiënten aan?', 'Wie is een goede tandarts als je bang bent?', 'Kroon of facing, wat is het verschil?', 'Bij welke tandarts kan ik vandaag terecht met kiespijn?', 'Wat kost een implantaat?'],
   t=[('Wat kost een implantaat?', 'Artikel'), ('Kroon of facing: wat is het verschil?', 'Artikel'), ('Tandarts in jouw wijk', 'Pagina'), ('Bang voor de tandarts: wat kun je doen?', 'Artikel')]),
  en=dict(slug='dentists', pl='dentists', sg='a dentist', k='patients', bub='Which dentist is taking on new patients?',
   q=['Which dentist nearby is taking on new patients?', 'Who is a good dentist if you are anxious?', 'Crown or veneer, what is the difference?', 'Which dentist can see me today with toothache?', 'What does an implant cost?'],
   t=[('What does an implant cost?', 'Article'), ('Crown or veneer: what is the difference?', 'Article'), ('Dentist in your neighbourhood', 'Page'), ('Afraid of the dentist: what can you do?', 'Article')])),
 dict(key='fysiotherapeuten', care=True,
  nl=dict(slug='fysiotherapeuten', pl='fysiotherapeuten', sg='fysiotherapeut', k='patiënten', bub='Welke fysiotherapeut is goed bij rugklachten?',
   q=['Welke fysiotherapeut in de buurt behandelt rugklachten?', 'Wie is een goede sportfysiotherapeut in mijn stad?', 'Fysiotherapie of manuele therapie, wat is het verschil?', 'Waar kan ik deze week nog terecht?', 'Wat kost fysiotherapie zonder aanvullende verzekering?'],
   t=[('Wat kost fysiotherapie zonder aanvullende verzekering?', 'Artikel'), ('Fysiotherapie of manuele therapie?', 'Artikel'), ('Fysiotherapeut in jouw wijk', 'Pagina'), ('Wanneer ga je met rugpijn naar de fysio?', 'Artikel')]),
  en=dict(slug='physiotherapists', pl='physiotherapists', sg='a physiotherapist', k='patients', bub='Which physiotherapist is good for back pain?',
   q=['Which physiotherapist nearby treats back pain?', 'Who is a good sports physiotherapist in my city?', 'Physiotherapy or manual therapy, what is the difference?', 'Where can I still be seen this week?', 'What does physiotherapy cost without extra insurance?'],
   t=[('What does physiotherapy cost without extra insurance?', 'Article'), ('Physiotherapy or manual therapy?', 'Article'), ('Physiotherapist in your neighbourhood', 'Page'), ('When to see a physio for back pain?', 'Article')])),
 dict(key='makelaars',
  nl=dict(slug='makelaars', pl='makelaars', sg='makelaar', k='klanten', bub='Wie is een goede makelaar in mijn stad?',
   q=['Welke makelaar verkoopt appartementen in mijn wijk?', 'Wie is de beste verkoopmakelaar in mijn stad?', 'Aankoopmakelaar of zelf bieden, wat is slimmer?', 'Welke makelaar kan mijn huis snel in de verkoop zetten?', 'Wat kost een makelaar bij verkoop?'],
   t=[('Wat kost een makelaar bij verkoop?', 'Artikel'), ('Aankoopmakelaar: wanneer loont het?', 'Artikel'), ('Makelaar in jouw wijk', 'Pagina'), ('Hoe lang duurt het om een huis te verkopen?', 'Artikel')]),
  en=dict(slug='estate-agents', pl='estate agents', sg='an estate agent', k='customers', bub='Who is a good estate agent in my city?',
   q=['Which estate agent sells apartments in my neighbourhood?', 'Who is the best selling agent in my city?', 'A buying agent or bid yourself, which is smarter?', 'Which estate agent can list my house quickly?', 'What does an estate agent cost when selling?'],
   t=[('What does an estate agent cost when selling?', 'Article'), ('A buying agent: when is it worth it?', 'Article'), ('Estate agent in your neighbourhood', 'Page'), ('How long does selling a house take?', 'Article')])),
 dict(key='accountants', care=True,
  nl=dict(slug='accountants', pl='accountants', sg='accountant', k='klanten', bub='Welke accountant is goed voor een zzp\'er?',
   q=['Welke accountant werkt voor zzp\'ers?', 'Wie is een goede accountant voor een klein bedrijf?', 'Boekhouder of accountant, wat is het verschil?', 'Welke accountant kan mijn aangifte nog voor de deadline doen?', 'Wat kost een accountant per jaar?'],
   t=[('Wat kost een accountant per jaar?', 'Artikel'), ('Boekhouder of accountant: wat is het verschil?', 'Artikel'), ('Accountant in jouw regio', 'Pagina'), ('Van eenmanszaak naar bv: wanneer is het zover?', 'Artikel')]),
  en=dict(slug='accountants', pl='accountants', sg='an accountant', k='clients', bub='Which accountant is good for a freelancer?',
   q=['Which accountant works for freelancers?', 'Who is a good accountant for a small business?', 'Bookkeeper or accountant, what is the difference?', 'Which accountant can still file my return before the deadline?', 'What does an accountant cost per year?'],
   t=[('What does an accountant cost per year?', 'Article'), ('Bookkeeper or accountant: what is the difference?', 'Article'), ('Accountant in your region', 'Page'), ('From sole trader to limited company: when?', 'Article')])),
 dict(key='advocaten', care=True,
  nl=dict(slug='advocaten', pl='advocaten', sg='advocaat', k='cliënten', bub='Welke advocaat helpt bij ontslag?',
   q=['Welke advocaat is gespecialiseerd in arbeidsrecht?', 'Wie is een goede advocaat bij een scheiding?', 'Advocaat of mediator, wat past bij mijn situatie?', 'Welke advocaat kan mij deze week nog spreken?', 'Wat kost een advocaat per uur?'],
   t=[('Wat kost een advocaat per uur?', 'Artikel'), ('Advocaat of mediator: wat past bij jou?', 'Artikel'), ('Advocaat in jouw regio', 'Pagina'), ('Ontslagen: wat zijn je eerste stappen?', 'Artikel')]),
  en=dict(slug='lawyers', pl='lawyers', sg='a lawyer', k='clients', bub='Which lawyer helps with a dismissal?',
   q=['Which lawyer specialises in employment law?', 'Who is a good lawyer for a divorce?', 'Lawyer or mediator, what suits my situation?', 'Which lawyer can still speak to me this week?', 'What does a lawyer cost per hour?'],
   t=[('What does a lawyer cost per hour?', 'Article'), ('Lawyer or mediator: what suits you?', 'Article'), ('Lawyer in your region', 'Page'), ('Dismissed: what are your first steps?', 'Article')])),
 dict(key='restaurants',
  nl=dict(slug='restaurants', pl='restaurants', sg='restaurant', k='gasten', bub='Waar kan ik lekker eten met een groep?',
   q=['Welk restaurant is geschikt voor een groep van twaalf?', 'Wat is het beste restaurant in mijn stad?', 'Welk restaurant is het fijnst voor een zakelijke lunch?', 'Waar kan ik vanavond nog reserveren?', 'Wat kost een diner voor twee?'],
   t=[('Eten met een groep: zo werkt het bij ons', 'Pagina'), ('Wat kun je bij ons eten als vegetariër?', 'Artikel'), ('Zakelijke lunch in jouw stad', 'Pagina'), ('Allergieën en dieetwensen: wat kan er?', 'Artikel')]),
  en=dict(slug='restaurants', pl='restaurants', sg='a restaurant', k='guests', bub='Where can I eat well with a group?',
   q=['Which restaurant suits a group of twelve?', 'What is the best restaurant in my city?', 'Which restaurant is best for a business lunch?', 'Where can I still book for tonight?', 'What does dinner for two cost?'],
   t=[('Dining with a group: how it works with us', 'Page'), ('What can you eat with us as a vegetarian?', 'Article'), ('Business lunch in your city', 'Page'), ('Allergies and dietary wishes: what is possible?', 'Article')])),
 dict(key='kappers',
  nl=dict(slug='kappers', pl='kappers', sg='kapper', k='klanten', bub='Wie is een goede kapper in de buurt?',
   q=['Welke kapper is goed met krullen?', 'Wie is de beste kapper in mijn stad?', 'Balayage of highlights, wat is het verschil?', 'Bij welke kapper kan ik vandaag nog terecht?', 'Wat kost knippen en kleuren?'],
   t=[('Wat kost knippen en kleuren?', 'Artikel'), ('Balayage of highlights: wat is het verschil?', 'Artikel'), ('Kapper in jouw wijk', 'Pagina'), ('Krullen laten knippen: waar let je op?', 'Artikel')]),
  en=dict(slug='hairdressers', pl='hairdressers', sg='a hairdresser', k='customers', bub='Who is a good hairdresser near me?',
   q=['Which hairdresser is good with curls?', 'Who is the best hairdresser in my city?', 'Balayage or highlights, what is the difference?', 'Which hairdresser can still fit me in today?', 'What does a cut and colour cost?'],
   t=[('What does a cut and colour cost?', 'Article'), ('Balayage or highlights: what is the difference?', 'Article'), ('Hairdresser in your neighbourhood', 'Page'), ('Having curls cut: what to look for?', 'Article')])),
]

C = {'nl': dict(
 title='NXEO voor {pl} | Genoemd door ChatGPT', desc='Wie een {sg} zoekt, vraagt het steeds vaker aan ChatGPT. NXEO meet of jouw bedrijf genoemd wordt, schrijft wat ontbreekt en plaatst het op je website.',
 h1='Genoemd worden als {sg}.', lead='Wie een {sg} zoekt, vraagt het steeds vaker aan ChatGPT. Dat noemt een paar namen. NXEO zorgt dat de jouwe daar tussen kan staan.',
 ph='jouwwebsite.nl', al='Je website', btn='Check mijn zichtbaarheid', note='Gratis · binnen 48 uur in je mail · geen verplichting',
 src='Voorbeeld: antwoord van ChatGPT', tabs=['Zonder NXEO', 'Met NXEO'], a0='Veelgenoemde partijen zijn:', a1='Een vaak genoemde partij voor deze vraag is:',
 rows0=[('Concurrent A', '8 van 10 antwoorden'), ('Concurrent B', '6 van 10'), ('Concurrent C', '4 van 10')], rows1=[('Jouw bedrijf', '7 van 10 antwoorden', 1), ('Concurrent A', '6 van 10', 0), ('Concurrent B', '3 van 10', 0)],
 m0='Jouw bedrijf wordt niet genoemd.', m1='Genoemd, met de juiste omschrijving en een link naar je site.',
 q_eb='De vragen', q_h='Dit vragen {k} aan AI.', q_p='Geen losse zoekwoorden, maar hele vragen. Ze vallen in vijf soorten. Bij elke soort wil je genoemd worden.',
 qt=['Wie doet dit?', 'Wie is de beste?', 'Wat is het verschil?', 'Wie kan snel?', 'Wat kost het?'],
 w_eb='Wat wij schrijven', w_h='Elke titel is een vraag van jouw {k}.',
 l_h='Antwoorden op de vragen die {k} echt stellen', l_p='Geen nieuwsberichten, maar pagina\'s en artikelen die een vraag beantwoorden. Zo heeft AI iets om aan te halen.',
 an=['We meten bij welke vragen je ontbreekt', 'We schrijven het antwoord, in jouw woorden', 'Jij keurt goed, wij plaatsen het'],
 c1=('Een kwartier per week', 'Wij schrijven en plaatsen. Jij leest mee en keurt goed.'), c1o=['Wij schrijven', 'Jij keurt goed'],
 c2=('Op je eigen website', 'De content komt in de website die je al hebt, in je eigen opmaak.'), c2o=['Jouw systeem', 'Jouw opmaak'],
 c3=('Alles blijft van jou', 'Stop je, dan blijft alles op je website staan.'), c3o=['Pagina\'s', 'Artikelen'],
 also=('Goed om te weten', 'Vanaf €99 per maand', 'Gratis nulmeting vooraf', 'Geen advertentiebudget nodig'),
 s_eb='Hoe het werkt', s_h='Van onzichtbaar naar genoemd. In drie stappen.',
 st_eb='Uit onze eigen praktijk', st_h='Twee aanvragen in één week.', st_p='Op onze eigen website plaatsten we een paar artikelen over timmermannen. Vijf à zes weken later kwamen er in één week twee aanvragen binnen, allebei van een timmerman uit dezelfde regio. Vrijwel niemand anders had over dat onderwerp voor die groep geschreven.', st_b='Lees het hele verhaal',
 fh='Vragen van {pl}',
 f_time=('Ik heb geen tijd om te schrijven. Hoeveel werk is het voor mij?', 'Een kwartier per week. Wij schrijven en plaatsen, jij leest mee en keurt goed. Zonder jouw akkoord gaat er niets online.'),
 f_know=('Kennen jullie mijn vak wel?', 'We schrijven op basis van wat jij ons bij de intake vertelt en van wat er al op je website staat. Jij leest alles na voordat het online gaat, dus er komt niets te staan dat niet klopt.'),
 f_care=('Mag ik zo over mijn vak schrijven?', 'We schrijven uitleg en antwoorden op vragen, geen beloftes over een uitkomst. Jij kent de regels van je beroep en leest alles na voordat het online gaat. Past iets niet, dan vervangen we het.'),
 f_local=('Werkt het ook als ik alleen in mijn eigen regio werk?', 'Juist dan. We schrijven op waar je werkt en waar niet, zodat AI weet voor welke vragen jouw bedrijf een goed antwoord is.'),
 f_cost=('Wat kost het?', 'Vanaf €99 per maand, plus eenmalig €195 opstartkosten. De eerste looptijd is zes maanden, daarna zeg je maandelijks op. Je begint met een gratis nulmeting.'),
 more='Andere branches', all='Alle branches',
 o_slug='voor', o_title='NXEO voor jouw branche | Genoemd door ChatGPT', o_desc='NXEO voor loodgieters, timmermannen, schilders, tandartsen, makelaars en meer. Bekijk welke vragen jouw klanten aan AI stellen en hoe je daar genoemd wordt.',
 o_bub='Werkt dit ook in mijn branche?', o_h1='Overal waar klanten vooraf vragen stellen.', o_lead='Wie een bedrijf zoekt, vraagt het steeds vaker aan AI. Welke vragen dat zijn, verschilt per vak. Kies het jouwe.',
 o_eb='Branches', o_h='Kies jouw vak.', o_more='Bekijk', o_ch='Staat jouw branche er niet bij?', o_cp='Het werkt voor elk bedrijf waar klanten eerst vragen stellen voordat ze kiezen. De nulmeting laat zien hoe het er bij jou voor staat.', o_cb='Vraag de nulmeting aan',
 link='Voor jouw branche', crumb='Branches'),
'en': dict(
 title='NXEO for {pl} | Mentioned by ChatGPT', desc='People looking for {sg} increasingly ask ChatGPT. NXEO measures whether your company is mentioned, writes what is missing and publishes it on your website.',
 h1='Be mentioned as {sgn}.', lead='People looking for {sg} increasingly ask ChatGPT. It names a few companies. NXEO makes sure yours can be among them.',
 ph='yourwebsite.com', al='Your website', btn='Check my visibility', note='Free · in your inbox within 48 hours · no obligation',
 src='Example: ChatGPT answering', tabs=['Without NXEO', 'With NXEO'], a0='Often mentioned companies are:', a1='A company often mentioned for this question is:',
 rows0=[('Competitor A', '8 of 10 answers'), ('Competitor B', '6 of 10'), ('Competitor C', '4 of 10')], rows1=[('Your company', '7 of 10 answers', 1), ('Competitor A', '6 of 10', 0), ('Competitor B', '3 of 10', 0)],
 m0='Your company is not mentioned.', m1='Mentioned, with the right description and a link to your site.',
 q_eb='The questions', q_h='This is what {k} ask AI.', q_p='Not loose keywords, but whole questions. They fall into five types. You want to be mentioned for each of them.',
 qt=['Who does this?', 'Who is the best?', 'What is the difference?', 'Who can do it fast?', 'What does it cost?'],
 w_eb='What we write', w_h='Every title is a question from your {k}.',
 l_h='Answers to the questions {k} really ask', l_p='Not news items, but pages and articles that answer a question. That gives AI something to quote.',
 an=['We measure where you are missing', 'We write the answer, in your words', 'You approve, we publish'],
 c1=('Fifteen minutes a week', 'We write and publish. You read along and approve.'), c1o=['We write', 'You approve'],
 c2=('On your own website', 'The content goes into the website you already have, in your own styling.'), c2o=['Your system', 'Your styling'],
 c3=('Everything stays yours', 'If you stop, everything stays on your website.'), c3o=['Pages', 'Articles'],
 also=('Good to know', 'From €99 per month', 'Free baseline check first', 'No advertising budget needed'),
 s_eb='How it works', s_h='From invisible to mentioned. In three steps.',
 st_eb='From our own practice', st_h='Two requests in one week.', st_p='On our own website we published a few articles about carpenters. Five to six weeks later two requests came in within one week, both from a carpenter in the same region. Hardly anyone else had written about that subject for that group.', st_b='Read the whole story',
 fh='Questions from {pl}',
 f_time=('I have no time to write. How much work is it for me?', 'Fifteen minutes a week. We write and publish, you read along and approve. Nothing goes online without your approval.'),
 f_know=('Do you know my trade?', 'We write based on what you tell us during onboarding and on what is already on your website. You read everything before it goes online, so nothing appears that is not right.'),
 f_care=('Am I allowed to write about my profession like this?', 'We write explanations and answers to questions, not promises about an outcome. You know the rules of your profession and read everything before it goes online. If something does not fit, we replace it.'),
 f_local=('Does it also work if I only work in my own region?', 'Especially then. We write down where you work and where you do not, so AI knows for which questions your company is a good answer.'),
 f_cost=('What does it cost?', 'From €99 per month, plus a one time setup fee of €195. The first term is six months, after that you cancel monthly. You start with a free baseline check.'),
 more='Other sectors', all='All sectors',
 o_slug='for', o_title='NXEO for your sector | Mentioned by ChatGPT', o_desc='NXEO for plumbers, carpenters, painters, dentists, estate agents and more. See which questions your customers ask AI and how you get mentioned there.',
 o_bub='Does this work in my sector too?', o_h1='Wherever customers ask questions first.', o_lead='People looking for a company increasingly ask AI. Which questions they ask differs per trade. Choose yours.',
 o_eb='Sectors', o_h='Choose your trade.', o_more='View', o_ch='Is your sector not listed?', o_cp='It works for any company where customers ask questions before they choose. The baseline check shows where you stand.', o_cb='Request the baseline check',
 link='For your sector', crumb='Sectors')}

ICO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/></svg>'


def cap(s): return s[0].upper() + s[1:]


def steps_block(lang):
    # dezelfde drie stappen als op de homepage, zodat het verhaal overal gelijk is
    s = open('content/%s/home.html' % lang).read()
    i = s.index('<div class="steps3">'); j = s.index('<div class="divider-cta"', i)
    return s[i:j].rstrip()


def page(b, lang):
    c, t = C[lang], b[lang]
    f = dict(pl=t['pl'], sg=t['sg'], k=t['k'], sgn=t['sg'])
    x = lambda s: s.format(**f)
    form = lambda cls: '<form class="combo%s" data-baseline novalidate><span class="ico" aria-hidden="true">%s</span><input name="site" type="url" placeholder="%s" required autocomplete="url" aria-label="%s"><button class="btn btn-blue" type="submit">%s <span class="arr">→</span></button></form>' % (cls, ICO, c['ph'], c['al'], c['btn'])
    own = lambda l: '<div class="own">' + ''.join('<span>%s</span>' % v for v in l) + '</div>'
    lst = lambda rows: ''.join('<div class="li%s"><span class="rank">%d</span>%s<span class="dim">%s</span></div>' % (' you' if (len(r) > 2 and r[2]) else '', i + 1, r[0], r[1]) for i, r in enumerate(rows))
    faqs = [c['f_time'], c['f_care'] if b.get('care') else c['f_know'], c['f_local'], c['f_cost']]
    others = [o for o in B if o['key'] != b['key']]
    story = ''
    if b.get('story'):
        story = ('  <div class="sec" style="padding-top:0">\n    <div class="wrap">\n      <div class="br-story" data-reveal><div><span class="eyebrow">%s</span><h2>%s</h2></div><div><p>%s</p><a class="btn btn-ghost" href="#art_hoe_chatgpt_bepaalt_welke_bedrijven_het_noemt" data-link>%s <span class="arr">→</span></a></div></div>\n    </div>\n  </div>\n\n' % (c['st_eb'], c['st_h'], c['st_p'], c['st_b']))
    h = f'''<section class="page br-page" id="page-br_{b['key']}">
  <div class="hero hero-c nul-hero">
    <div class="hero-bg" aria-hidden="true"></div>
    <div class="wrap hero-stack">
      <div class="bubble bubble-blue" aria-hidden="true">{t['bub']}</div>
      <h1>{x(c['h1'])}<span class="cursor" aria-hidden="true"></span></h1>
      <p class="def">{x(c['lead'])}</p>
      {form(' audit-combo')}
      <p class="hero-note">{c['note']}</p>
    </div>
    <div class="wrap">
      <div class="chat" aria-label="{c['src']}">
        <div class="chat-head">
          <span class="ai-src"><img src="{{{{openai_mark}}}}" alt="">{c['src']}</span>
          <div class="tabs" role="tablist"><button class="tab" role="tab" aria-selected="true" data-demo="before">{c['tabs'][0]}</button><button class="tab" role="tab" aria-selected="false" data-demo="after">{c['tabs'][1]}</button></div>
        </div>
        <div class="msg ai"><div class="panes">
          <div class="ans is-on" data-demo-pane="before"><p>{c['a0']}</p><div class="list">{lst(c['rows0'])}</div><p><mark>{c['m0']}</mark><span class="cursor" aria-hidden="true"></span></p></div>
          <div class="ans" data-demo-pane="after"><p>{c['a1']}</p><div class="list">{lst(c['rows1'])}</div><p><mark class="good">{c['m1']}</mark><span class="cursor" aria-hidden="true"></span></p></div>
        </div></div>
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="wrap">
      <div class="sec-head" data-reveal><span class="eyebrow">{c['q_eb']}</span><h2>{x(cap(c['q_h']))}</h2><p class="lead">{c['q_p']}</p></div>
      <div class="br-qs">{''.join('<div class="br-q" data-reveal><span class="k">%s</span><div class="bubble br-bub">%s</div></div>' % (c['qt'][i], q) for i, q in enumerate(t['q']))}</div>
    </div>
  </div>

  <div class="sec" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head" data-reveal><span class="eyebrow">{c['w_eb']}</span><h2>{x(c['w_h'])}</h2></div>
      <div class="bento2">
        <div class="bx bx-web cm-lead" data-reveal>
          <div class="bx-text"><h4>{x(c['l_h'])}</h4><p>{c['l_p']}</p><ul class="cm-an">{''.join('<li><span>%d</span><b>%s</b></li>' % (i + 1, v) for i, v in enumerate(c['an']))}</ul></div>
          <div class="bx-well"><div class="mini-rows cm-mr br-rows">{''.join('<div class="mini mini-row"><span class="lbl">%s</span><span class="st ok">%s</span></div>' % r for r in t['t'])}</div></div>
        </div>
        <div class="bx" data-reveal><div class="bx-text"><h4>{c['c1'][0]}</h4><p>{c['c1'][1]}</p></div><div class="bx-art">{own(c['c1o'])}</div></div>
        <div class="bx bx-lav" data-reveal><div class="bx-text"><h4>{c['c2'][0]}</h4><p>{c['c2'][1]}</p></div><div class="bx-art">{own(c['c2o'])}</div></div>
        <div class="bx bx-tint" data-reveal><div class="bx-text"><h4>{c['c3'][0]}</h4><p>{c['c3'][1]}</p></div><div class="bx-art">{own(c['c3o'])}</div></div>
        <div class="bx-also" data-reveal><b>{c['also'][0]}</b>{''.join('<span>%s</span>' % v for v in c['also'][1:])}</div>
      </div>
    </div>
  </div>

{story}  <div class="sec" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head center" data-reveal><span class="eyebrow">{c['s_eb']}</span><h2>{c['s_h']}</h2></div>
      {steps_block(lang)}
    </div>
  </div>

  <div class="sec" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head center" data-reveal><h2>{x(c['fh'])}</h2></div>
      <div class="faq faq-teaser" data-reveal>{''.join('<details><summary>%s</summary><p>%s</p></details>' % q for q in faqs)}</div>
      <div class="br-more" data-reveal><b>{c['more']}</b>{''.join('<a href="#br_%s" data-link>%s</a>' % (o['key'], cap(o[lang]['pl'])) for o in others)}<a class="all" href="#branches" data-link>{c['all']} <span class="arr">→</span></a></div>
    </div>
  </div>
</section>
'''
    return h, dict(slug=c['o_slug'] + '/' + t['slug'], title=x(c['title']), desc=x(c['desc']))


def overview(lang):
    c = C[lang]
    tiles = ''.join('<a class="kp br-tile" href="#br_%s" data-link><div class="bubble br-bub">%s</div><b>%s</b><i>%s <span class="arr">→</span></i></a>' % (b['key'], b[lang]['bub'], cap(b[lang]['pl']), c['o_more']) for b in B)
    return f'''<section class="page br-page" id="page-branches">
  <div class="hero hero-c cm-hero kp-hero">
    <div class="hero-stack">
      <div class="bubble bubble-blue">{c['o_bub']}</div>
      <h1>{c['o_h1']}<span class="cursor" aria-hidden="true"></span></h1>
      <p class="def">{c['o_lead']}</p>
      <div class="cm-btns"><a class="btn btn-white" href="#nulmeting" data-link>{c['o_cb']} <span class="arr">→</span></a></div>
    </div>
  </div>
  <div class="sec">
    <div class="wrap">
      <div class="sec-head" data-reveal><span class="eyebrow">{c['o_eb']}</span><h2>{c['o_h']}</h2></div>
      <div class="kp-grid" data-reveal>{tiles}</div>
      <div class="np-cta kp-cta" data-reveal><div><h3>{c['o_ch']}</h3><p>{c['o_cp']}</p></div><a class="btn btn-blue" href="#nulmeting" data-link>{c['o_cb']} <span class="arr">→</span></a></div>
    </div>
  </div>
</section>
'''


if __name__ == '__main__':
    for lang in ('nl', 'en'):
        j = json.load(open('i18n/%s.json' % lang))
        for b in B:
            if lang == 'en':
                b['en']['sgn'] = b['en']['sg']
            html, t = page(b, lang)
            open('content/%s/br_%s.html' % (lang, b['key']), 'w').write(html)
            j['pages']['br_' + b['key']] = {'slug': t['slug'], 'title': t['title'], 'description': t['desc']}
        open('content/%s/branches.html' % lang, 'w').write(overview(lang))
        c = C[lang]
        j['pages']['branches'] = {'slug': c['o_slug'], 'title': c['o_title'], 'description': c['o_desc']}
        json.dump(j, open('i18n/%s.json' % lang, 'w'), ensure_ascii=False, indent=2)
        # link in de footer, onder Product
        f = 'content/%s/footer.html' % lang; s = open(f).read()
        if '#branches' not in s:
            a = '<li><a href="#blog" data-link>Blog</a></li></ul></nav>'
            assert s.count(a) == 1
            s = s.replace(a, '<li><a href="#blog" data-link>Blog</a></li><li><a href="#branches" data-link>%s</a></li></ul></nav>' % c['link'])
            open(f, 'w').write(s)
    print('pages:', ' '.join('br_' + b['key'] for b in B), 'branches')
