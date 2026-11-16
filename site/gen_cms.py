# Bouwt de pagina's onder "Werkt met" met de bouwstenen van de homepage.
# Draai: python3 gen_cms.py  (schrijft content/{nl,en}/cms_*.html, koppelingen.html en de i18n regels)
import json

ICON = {
 'builder': '<svg viewBox="0 0 24 24" fill="none" stroke="#002EFE" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 9h18M9 9v11"/></svg>',
 'code': '<svg viewBox="0 0 24 24" fill="none" stroke="#002EFE" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 7.5L4 12l4.5 4.5M15.5 7.5L20 12l-4.5 4.5M13.5 5l-3 14"/></svg>',
 'ai': '<svg viewBox="0 0 24 24" fill="#002EFE"><path d="M12 2.5l1.9 5.6c.3.9 1 1.6 1.9 1.9l5.7 2-5.7 1.9c-.9.3-1.6 1-1.9 1.9L12 21.5l-1.9-5.7c-.3-.9-1-1.6-1.9-1.9l-5.7-1.9 5.7-2c.9-.3 1.6-1 1.9-1.9L12 2.5z"/></svg>',
 'plug': '<svg viewBox="0 0 24 24" fill="none" stroke="#002EFE" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3v5M15 3v5M6.5 8h11v3.5a5.5 5.5 0 01-11 0V8zM12 17v4"/></svg>',
}

# Gedeelde tekst. {n} = naam van het systeem, {s} = "WordPress website", {p} = bericht, {P} = Bericht, {ps} = berichten
C = {'nl': dict(
 b1='Start met NXEO', b2='Gratis nulmeting', dt=['Zonder NXEO', 'Met NXEO'],
 d0p='Laatste {ps}:', d0=[('Welkom op onze nieuwe website', 'maart 2021'), ('Wij zijn verhuisd', 'april 2021'), ('Fijne feestdagen', 'december 2022')], d0m='Laatste {p}: bijna vier jaar geleden.',
 d1p='Deze maand geplaatst:', d1=[('Wat kost een dakkapel op een rijtjeshuis?', '12 nov'), ('Heb ik een vergunning nodig voor een dakkapel?', '7 nov'), ('Prefab of traditioneel: wat past bij jouw dak?', '5 nov')], d1m='Elke week iets nieuws, op de vragen van je klanten.',
 s_eb='Hoe het werkt', s_h='Van koppeling tot {p}. In drie stappen.',
 st1=('Koppelen', 'Bij de intake zetten we de koppeling met je {s} klaar. Dat doen we één keer.', ['Eén keer instellen', 'Geen technische kennis nodig']),
 st2=('Goedkeuren', 'Je krijgt te zien wat er klaarstaat. Lezen, akkoord geven, klaar.', ['Een kwartier per week', 'Niets zonder akkoord']),
 st3=('Online', 'Het staat op je eigen website, als {p} of pagina, in je eigen opmaak.', ['In jouw opmaak', 'Blijft van jou']),
 conn='Verbonden', apt='Wat kost een dakkapel op een rijtjeshuis?', apm='Klaar voor akkoord', apok='Akkoord', apch='Aanpassen', burl='jouwwebsite.nl/kennis/wat-kost-een-dakkapel', bpub='Gepubliceerd',
 b_eb='Wat er op je website komt', b_h='Content die AI kan aanhalen. Niet zomaar een blog.',
 l_h='Elk stuk is zo opgebouwd dat AI er een deel uit kan gebruiken', l_p='Een AI systeem haalt geen hele pagina aan, maar één alinea. Daarom kan elk deel op zichzelf staan.',
 an=['De vraag in het adres', 'Eén titel, de vraag van de klant', 'Het antwoord in de eerste alinea', 'Een kop per deelvraag', 'Veelgestelde vragen als echte tekst', 'Links naar je eigen pagina\'s'],
 ph1='Wat kost een dakkapel op een rijtjeshuis?', pans='Een dakkapel van drie meter breed kost gemiddeld tussen de zes en tienduizend euro, inclusief plaatsen.', ph2a='Waar hangt de prijs van af?', ph2b='Heb ik een vergunning nodig?', pfq='Veelgestelde vragen', plink='Lees ook: dakkapel plaatsen in Apeldoorn', pnote='De bedragen in dit voorbeeld zijn verzonnen',
 c1=('Elke titel is een klantvraag', 'Geen "Nieuws" of "Update", maar wat iemand aan ChatGPT vraagt.'),
 c2=('{P} of pagina', 'Een antwoord op één vraag wordt een {p}. Uitleg over een dienst wordt een pagina.'),
 c4=('Alles blijft van jou', 'Stop je, dan blijft alles op je website staan.'),
 c1rows=[('Wat kost een dakkapel?', '{P}'), ('Vergunning nodig?', '{P}'), ('Dakkapel in Apeldoorn', 'Pagina'), ('Prefab of traditioneel?', '{P}'), ('Hoe lang duurt plaatsen?', '{P}'), ('Dakkapel in Epe', 'Pagina')],
 c2a=('{P}', 'Eén vraag, één antwoord'), c2b=('Pagina', 'Een dienst of een regio'), c4c=['Pagina\'s', 'Artikelen', 'Structuur', 'Meetdata'],
 k_eb='Zelf controleren', k_h='Loop je {n} na. In tien minuten.', kbs='Controlelijst', kt='Waar je moet kijken',
 kq='Zes dingen die we bij {n} steeds weer tegenkomen. Kom je er niet uit, dan kijken we met je mee.',
 kst=[('10 min', 'om alles na te lopen'), ('€0', 'aan kosten')],
 k_walk='Loop hem samen met ons door', k_walk2='Of loop hem samen met ons door', k_open='Open de controlelijst',
 fh='Vragen over NXEO en {n}',
 f_first=('Moet ik zelf iets installeren of instellen?', 'De koppeling met je {s} zetten we samen klaar bij de intake. Wat daarvoor nodig is, lopen we op dat moment met je door. Je hebt er geen technische kennis voor nodig.'),
 f_rest=[('Komt het in mijn blog of als losse pagina?', 'Allebei. Een antwoord op één vraag past als {p} in je blog of kennisbank. Uitleg over een dienst of een regio hoort op een eigen pagina.'),
         ('Gaat er iets online zonder dat ik het weet?', 'Nee. Je krijgt vooraf te zien wat er klaarstaat en keurt goed. Keur je iets af, dan vervangen we het zonder extra kosten.'),
         ('Kan ik de teksten daarna zelf aanpassen?', 'Ja. Het is gewone inhoud op je eigen website. Je past het aan op de manier die je gewend bent.'),
         ('Wat gebeurt er met de content als ik stop?', 'Die blijft staan. Alles wat we hebben gemaakt blijft van jou: de pagina\'s, de artikelen en je meetdata.')],
 title='NXEO met {n} | Word genoemd door AI', desc='NXEO meet hoe AI jouw bedrijf noemt, schrijft de content die ontbreekt en plaatst die op je {s}. Jij keurt goed, wij doen de rest.',
 bub='NXEO met {n}', lead='Wij schrijven wat ontbreekt en zetten het op je website. Jij keurt alleen goed.', dsrc='{PS} op je website',
 # overzicht
 o_slug='werkt-met', o_title='Werkt met jouw website | NXEO', o_desc='NXEO werkt met WordPress, Webflow, Shopify, Wix, Framer, de websitebouwers van hostingpartijen, gecodeerde websites en websites die met AI zijn gemaakt.',
 o_bub='Werkt met jouw website', o_h1='De website die je al hebt. Daar zetten we het in.', o_lead='Je hoeft niets om te bouwen en nergens naartoe te verhuizen. Wij plaatsen de content in het systeem waar je website nu op draait.',
 o_eb='Koppelingen', o_h='Kies waar je website op draait.', o_more='Bekijk', o_ch='Staat jouw systeem er niet bij?', o_cp='Dan maken we een koppeling op maat. In principe kunnen we alles koppelen wat een website kan tonen.', o_cb='Bekijk maatwerk',
 col='Werkt met', col_all='Alle koppelingen'),
'en': dict(
 b1='Start with NXEO', b2='Free baseline check', dt=['Without NXEO', 'With NXEO'],
 d0p='Latest {ps}:', d0=[('Welcome to our new website', 'March 2021'), ('We have moved', 'April 2021'), ('Season\'s greetings', 'December 2022')], d0m='Latest {p}: almost four years ago.',
 d1p='Published this month:', d1=[('What does a dormer cost on a terraced house?', '12 Nov'), ('Do I need a permit for a dormer?', '7 Nov'), ('Prefabricated or traditional: what suits your roof?', '5 Nov')], d1m='Something new every week, on your customers\' questions.',
 s_eb='How it works', s_h='From connection to {p}. In three steps.',
 st1=('Connect', 'During onboarding we set up the connection with your {s}. We do that once.', ['Set up once', 'No technical knowledge needed']),
 st2=('Approve', 'You see what is ready. Read, agree, done.', ['A quarter of an hour per week', 'Nothing without approval']),
 st3=('Online', 'It is on your own website, as {a} {p} or a page, in your own styling.', ['In your styling', 'Stays yours']),
 conn='Connected', apt='What does a dormer cost on a terraced house?', apm='Ready for approval', apok='Approve', apch='Edit', burl='yourwebsite.com/knowledge/what-does-a-dormer-cost', bpub='Published',
 b_eb='What goes onto your website', b_h='Content AI can quote. Not just another blog.',
 l_h='Every piece is built so that AI can use a part of it', l_p='An AI system does not quote a whole page, but one paragraph. That is why every part can stand alone.',
 an=['The question in the address', 'One title, the customer\'s question', 'The answer in the first paragraph', 'A heading per part of the question', 'Frequently asked questions as real text', 'Links to your own pages'],
 ph1='What does a dormer cost on a terraced house?', pans='A dormer of three metres wide costs on average between six and ten thousand euros, including fitting.', ph2a='What does the price depend on?', ph2b='Do I need a permit?', pfq='Frequently asked questions', plink='Also read: dormer fitting in Apeldoorn', pnote='The amounts in this example are made up',
 c1=('Every title is a customer question', 'Not "News" or "Update", but what someone asks ChatGPT.'),
 c2=('{P} or page', 'An answer to one question becomes {a} {p}. An explanation of a service becomes a page.'),
 c4=('Everything stays yours', 'If you stop, everything stays on your website.'),
 c1rows=[('What does a dormer cost?', '{P}'), ('Permit needed?', '{P}'), ('Dormers in Apeldoorn', 'Page'), ('Prefabricated or traditional?', '{P}'), ('How long does fitting take?', '{P}'), ('Dormers in Epe', 'Page')],
 c2a=('{P}', 'One question, one answer'), c2b=('Page', 'A service or a region'), c4c=['Pages', 'Articles', 'Structure', 'Measurement data'],
 k_eb='Check it yourself', k_h='Go through your {n}. In ten minutes.', kbs='Checklist', kt='Where to look',
 kq='Six things we come across with {n} again and again. If you get stuck, we will look along with you.',
 kst=[('10 min', 'to go through it all'), ('€0', 'in costs')],
 k_walk='Go through it with us', k_walk2='Or go through it with us', k_open='Open the checklist',
 fh='Questions about NXEO and {n}',
 f_first=('Do I have to install or set up anything myself?', 'We set up the connection with your {s} together during onboarding. We walk you through what is needed at that point. You do not need technical knowledge for it.'),
 f_rest=[('Does it go in my blog or as a separate page?', 'Both. An answer to one question fits as {a} {p} in your blog or knowledge base. An explanation of a service or a region belongs on a page of its own.'),
         ('Does anything go online without me knowing?', 'No. You see beforehand what is ready and you approve it. If you reject something, we replace it at no extra cost.'),
         ('Can I edit the texts myself afterwards?', 'Yes. It is ordinary content on your own website. You edit it the way you are used to.'),
         ('What happens to the content if I stop?', 'It stays. Everything we have created remains yours: the pages, the articles and your measurement data.')],
 title='NXEO with {n} | Get mentioned by AI', desc='NXEO measures how AI mentions your company, writes the content that is missing and publishes it on your {s}. You approve, we do the rest.',
 bub='NXEO with {n}', lead='We write what is missing and put it on your website. You only approve.', dsrc='{PS} on your website',
 o_slug='works-with', o_title='Works with your website | NXEO', o_desc='NXEO works with WordPress, Webflow, Shopify, Wix, Framer, the website builders of hosting companies, coded websites and websites made with AI.',
 o_bub='Works with your website', o_h1='The website you already have. That is where we put it.', o_lead='You do not have to rebuild anything or move anywhere. We publish the content in the system your website runs on today.',
 o_eb='Integrations', o_h='Choose what your website runs on.', o_more='View', o_ch='Is your system not listed?', o_cp='Then we build a custom connection. In principle we can connect anything that can show a website.', o_cb='View custom',
 col='Works with', col_all='All integrations')}

# Per systeem. Velden die ontbreken komen uit C.
P = [
 dict(key='cms_wordpress', mark='wordpress_mark', article='art_wordpress_controlelijst_vindbaar_voor_ai',
  nl=dict(slug='werkt-met/wordpress', n='WordPress', s='WordPress website', p='bericht', ps='berichten', h1='Jouw WordPress website, genoemd door AI.', tile='Berichten en pagina\'s, in de opmaak van je thema.',
   lead='Wij schrijven wat ontbreekt en zetten het in je WordPress. Jij keurt alleen goed.', dsrc='Berichten in je WordPress',
   d0=[('Hallo wereld!', 'maart 2021'), ('Onze nieuwe website is live', 'april 2021'), ('Fijne feestdagen', 'december 2022')],
   b_eb='Wat er in je WordPress komt', b_h='Berichten die AI kan aanhalen. Niet zomaar een blog.',
   c3=('Je thema blijft je thema', 'We plaatsen inhoud. Thema, plugins en instellingen raken we niet aan.', ['Thema', 'Plugins', 'Instellingen']),
   k_h='Loop je WordPress na. In tien minuten.', kq='Zes dingen die we bij WordPress websites steeds weer tegenkomen. Per punt staat erbij waar je moet klikken.',
   chk=[('Lezen', 'Vragen zoekmachines je site over te slaan?'), ('Permalinks', 'Staat de structuur op Berichtnaam?'), ('Beveiliging', 'Houdt je plugin onbekende bezoekers buiten?'), ('Thema', 'Laadt tekst in tabbladen pas na een klik?'), ('Categorieën', 'Tientallen categorieën met elk één bericht?'), ('Sitemap', 'Staan je belangrijkste pagina\'s in wp-sitemap.xml?')],
   fq=('Veranderen jullie iets aan mijn thema of plugins?', 'Nee. We plaatsen inhoud: berichten en pagina\'s. Je thema, je plugins en je instellingen blijven zoals ze zijn.')),
  en=dict(slug='works-with/wordpress', n='WordPress', s='WordPress website', p='post', ps='posts', a='a', h1='Your WordPress website, mentioned by AI.', tile='Posts and pages, in the styling of your theme.',
   lead='We write what is missing and put it in your WordPress. You only approve.', dsrc='Posts in your WordPress',
   d0=[('Hello world!', 'March 2021'), ('Our new website is live', 'April 2021'), ('Season\'s greetings', 'December 2022')],
   b_eb='What goes into your WordPress', b_h='Posts AI can quote. Not just another blog.',
   c3=('Your theme stays your theme', 'We publish content. We do not touch your theme, plugins or settings.', ['Theme', 'Plugins', 'Settings']),
   k_h='Go through your WordPress. In ten minutes.', kq='Six things we come across on WordPress websites again and again. Each point says where to click.',
   chk=[('Reading', 'Are search engines asked to skip your site?'), ('Permalinks', 'Is the structure set to Post name?'), ('Security', 'Does your plugin keep unknown visitors out?'), ('Theme', 'Does text in tabs only load after a click?'), ('Categories', 'Dozens of categories with one post each?'), ('Sitemap', 'Are your main pages in wp-sitemap.xml?')],
   fq=('Do you change anything about my theme or plugins?', 'No. We publish content: posts and pages. Your theme, your plugins and your settings stay as they are.'))),

 dict(key='cms_webflow', mark='webflow_mark',
  nl=dict(slug='werkt-met/webflow', n='Webflow', s='Webflow website', p='CMS item', ps='CMS items', h1='Jouw Webflow website, genoemd door AI.', tile='Items in je CMS collectie, in je eigen ontwerp.',
   lead='Wij schrijven wat ontbreekt en zetten het in je Webflow CMS. Jij keurt alleen goed.', dsrc='Items in je Webflow CMS',
   b_eb='Wat er in je Webflow komt', st3=('Online', 'Het staat in je eigen CMS collectie en verschijnt in het ontwerp dat je al hebt.', ['In jouw ontwerp', 'Blijft van jou']),
   c3=('Je ontwerp blijft je ontwerp', 'We vullen je CMS. Aan je ontwerp, je interacties en je instellingen komen we niet.', ['Ontwerp', 'Interacties', 'Instellingen']),
   chk=[('Indexering', 'Staat indexeren door zoekmachines aan in de SEO instellingen?'), ('Subdomein', 'Wordt je webflow.io adres buiten zoekmachines gehouden?'), ('Sitemap', 'Wordt de sitemap automatisch gemaakt?'), ('Publiceren', 'Staan er CMS items nog op concept?'), ('Collectie', 'Heeft elk item een eigen titel en omschrijving?'), ('Robots.txt', 'Staat daar een regel in die bezoekers weert?')],
   fq=('Heb ik een Webflow pakket met CMS nodig?', 'Om items in een collectie te plaatsen heeft je site een Webflow pakket met CMS nodig. Bij de intake kijken we wat je nu hebt en of dat genoeg is.')),
  en=dict(slug='works-with/webflow', n='Webflow', s='Webflow website', p='CMS item', ps='CMS items', a='a', h1='Your Webflow website, mentioned by AI.', tile='Items in your CMS collection, in your own design.',
   lead='We write what is missing and put it in your Webflow CMS. You only approve.', dsrc='Items in your Webflow CMS',
   b_eb='What goes into your Webflow', st3=('Online', 'It is in your own CMS collection and appears in the design you already have.', ['In your design', 'Stays yours']),
   c3=('Your design stays your design', 'We fill your CMS. We do not touch your design, your interactions or your settings.', ['Design', 'Interactions', 'Settings']),
   chk=[('Indexing', 'Is indexing by search engines switched on in the SEO settings?'), ('Subdomain', 'Is your webflow.io address kept out of search engines?'), ('Sitemap', 'Is the sitemap generated automatically?'), ('Publishing', 'Are there CMS items still set to draft?'), ('Collection', 'Does every item have its own title and description?'), ('Robots.txt', 'Is there a rule in it that keeps visitors out?')],
   fq=('Do I need a Webflow plan with CMS?', 'To place items in a collection your site needs a Webflow plan with CMS. During onboarding we look at what you have now and whether that is enough.'))),

 dict(key='cms_shopify', mark='shopify_mark',
  nl=dict(slug='werkt-met/shopify', n='Shopify', s='Shopify winkel', p='blogbericht', ps='blogberichten', h1='Jouw Shopify winkel, genoemd door AI.', tile='Blogberichten en pagina\'s, naast je producten.',
   lead='Wij schrijven wat ontbreekt en zetten het in je Shopify winkel. Jij keurt alleen goed.', dsrc='Blogberichten in je Shopify',
   d0=[('Onze webshop is live', 'maart 2021'), ('Nieuwe collectie binnen', 'april 2021'), ('Gesloten met de feestdagen', 'december 2022')],
   d1=[('Welke fietstas past op een elektrische fiets?', '12 nov'), ('Waterdicht of waterafstotend: wat is het verschil?', '7 nov'), ('Hoe monteer je een fietstas zonder bagagedrager?', '5 nov')],
   b_eb='Wat er in je Shopify komt', burl='jouwwinkel.nl/blogs/advies/welke-fietstas-past', ph1='Welke fietstas past op een elektrische fiets?', pans='Op de meeste elektrische fietsen past een tas met een brede haak, omdat de bagagedrager dikker is dan bij een gewone fiets.', ph2a='Waar moet je op letten bij de haken?', ph2b='Past een dubbele tas ook?', plink='Bekijk: fietstassen voor elektrische fietsen', pnote='Voorbeeld voor een winkel in fietstassen', c1rows=[('Welke tas past?', '{P}'), ('Waterdicht of niet?', '{P}'), ('Fietstassen', 'Pagina'), ('Monteren zonder drager?', '{P}'), ('Hoeveel liter heb je nodig?', '{P}'), ('Retourneren', 'Pagina')], c2b=('Pagina', 'Uitleg, service of een thema'), st3=('Online', 'Het staat in je eigen winkel, als blogbericht of pagina, in de opmaak van je thema.', ['In jouw thema', 'Blijft van jou']),
   c3=('Je winkel blijft je winkel', 'We plaatsen blogberichten en pagina\'s. Thema, apps en producten raken we niet aan.', ['Thema', 'Apps', 'Producten']),
   chk=[('Wachtwoord', 'Staat de wachtwoordpagina van je winkel nog aan?'), ('Menu', 'Is je blog te bereiken vanuit het menu?'), ('Vermelding', 'Heeft elk bericht een eigen titel en omschrijving voor zoekmachines?'), ('Producten', 'Staat er je eigen tekst, of die van de leverancier?'), ('Apps', 'Laadt tekst uit een app pas nadat de pagina er staat?'), ('Sitemap', 'Werkt het adres van je winkel met sitemap.xml erachter?')],
   fq=('Raken jullie mijn producten of bestellingen aan?', 'Nee. We plaatsen blogberichten en pagina\'s. Aan producten, prijzen, voorraad en bestellingen komen we niet.')),
  en=dict(slug='works-with/shopify', n='Shopify', s='Shopify shop', p='blog post', ps='blog posts', a='a', h1='Your Shopify shop, mentioned by AI.', tile='Blog posts and pages, next to your products.',
   lead='We write what is missing and put it in your Shopify shop. You only approve.', dsrc='Blog posts in your Shopify',
   d0=[('Our online shop is live', 'March 2021'), ('New collection in', 'April 2021'), ('Closed over the holidays', 'December 2022')],
   d1=[('Which pannier fits an electric bike?', '12 Nov'), ('Waterproof or water repellent: what is the difference?', '7 Nov'), ('How do you fit a pannier without a rack?', '5 Nov')],
   b_eb='What goes into your Shopify', burl='yourshop.com/blogs/advice/which-pannier-fits', ph1='Which pannier fits an electric bike?', pans='Most electric bikes take a pannier with a wide hook, because the rack is thicker than on an ordinary bike.', ph2a='What should you look for in the hooks?', ph2b='Does a double pannier fit too?', plink='View: panniers for electric bikes', pnote='Example for a shop selling panniers', c1rows=[('Which pannier fits?', '{P}'), ('Waterproof or not?', '{P}'), ('Panniers', 'Page'), ('Fitting without a rack?', '{P}'), ('How many litres do you need?', '{P}'), ('Returns', 'Page')], c2b=('Page', 'Explanation, service or a theme'), st3=('Online', 'It is in your own shop, as a blog post or a page, in the styling of your theme.', ['In your theme', 'Stays yours']),
   c3=('Your shop stays your shop', 'We publish blog posts and pages. We do not touch your theme, apps or products.', ['Theme', 'Apps', 'Products']),
   chk=[('Password', 'Is the password page of your shop still switched on?'), ('Menu', 'Can your blog be reached from the menu?'), ('Listing', 'Does every post have its own title and description for search engines?'), ('Products', 'Is it your own text, or the supplier\'s?'), ('Apps', 'Does text from an app only load after the page is there?'), ('Sitemap', 'Does your shop address work with sitemap.xml after it?')],
   fq=('Do you touch my products or orders?', 'No. We publish blog posts and pages. We do not touch products, prices, stock or orders.'))),

 dict(key='cms_wix', mark='wix_dark', wide=True,
  nl=dict(slug='werkt-met/wix', n='Wix', s='Wix website', p='bericht', ps='berichten', h1='Jouw Wix website, genoemd door AI.', tile='Berichten en pagina\'s, in je eigen ontwerp.',
   lead='Wij schrijven wat ontbreekt en zetten het in je Wix website. Jij keurt alleen goed.', dsrc='Berichten in je Wix blog',
   b_eb='Wat er in je Wix komt',
   c3=('Je ontwerp blijft je ontwerp', 'We plaatsen inhoud. Aan je ontwerp, je apps en je instellingen komen we niet.', ['Ontwerp', 'Apps', 'Instellingen']),
   chk=[('Indexering', 'Mogen zoekmachines je site indexeren in de SEO instellingen?'), ('Domein', 'Staat je site op een eigen domein, of nog op een wixsite adres?'), ('Per pagina', 'Staat een belangrijke pagina verborgen voor zoekmachines?'), ('Blog', 'Heeft elk bericht een eigen titel en omschrijving?'), ('Tekst', 'Staat belangrijke tekst in een afbeelding?'), ('Sitemap', 'Werkt je domein met sitemap.xml erachter?')],
   fq=('Veranderen jullie iets aan mijn ontwerp?', 'Nee. We plaatsen inhoud: berichten en pagina\'s. Je ontwerp, je apps en je instellingen blijven zoals ze zijn.')),
  en=dict(slug='works-with/wix', n='Wix', s='Wix website', p='post', ps='posts', a='a', h1='Your Wix website, mentioned by AI.', tile='Posts and pages, in your own design.',
   lead='We write what is missing and put it in your Wix website. You only approve.', dsrc='Posts in your Wix blog',
   b_eb='What goes into your Wix',
   c3=('Your design stays your design', 'We publish content. We do not touch your design, your apps or your settings.', ['Design', 'Apps', 'Settings']),
   chk=[('Indexing', 'May search engines index your site in the SEO settings?'), ('Domain', 'Is your site on its own domain, or still on a wixsite address?'), ('Per page', 'Is an important page hidden from search engines?'), ('Blog', 'Does every post have its own title and description?'), ('Text', 'Is important text inside an image?'), ('Sitemap', 'Does your domain work with sitemap.xml after it?')],
   fq=('Do you change anything about my design?', 'No. We publish content: posts and pages. Your design, your apps and your settings stay as they are.'))),

 dict(key='cms_framer', mark='framer_mark',
  nl=dict(slug='werkt-met/framer', n='Framer', s='Framer website', p='CMS item', ps='CMS items', h1='Jouw Framer website, genoemd door AI.', tile='Items in je CMS, in je eigen ontwerp.',
   lead='Wij schrijven wat ontbreekt en zetten het in je Framer CMS. Jij keurt alleen goed.', dsrc='Items in je Framer CMS',
   b_eb='Wat er in je Framer komt', st3=('Online', 'Het staat in je eigen CMS en verschijnt in het ontwerp dat je al hebt.', ['In jouw ontwerp', 'Blijft van jou']),
   c3=('Je ontwerp blijft je ontwerp', 'We vullen je CMS. Aan je ontwerp, je animaties en je instellingen komen we niet.', ['Ontwerp', 'Animaties', 'Instellingen']),
   chk=[('Indexering', 'Staat een pagina uitgesloten van zoekmachines in de pagina instellingen?'), ('Domein', 'Wordt je framer adres ook gevonden, naast je eigen domein?'), ('CMS', 'Staan er items nog op concept?'), ('Titels', 'Heeft elke pagina een eigen titel en omschrijving?'), ('Tekst', 'Staat belangrijke tekst in een afbeelding of animatie?'), ('Sitemap', 'Werkt je domein met sitemap.xml erachter?')],
   fq=('Veranderen jullie iets aan mijn ontwerp?', 'Nee. We vullen je CMS met inhoud. Je ontwerp, je animaties en je instellingen blijven zoals ze zijn.')),
  en=dict(slug='works-with/framer', n='Framer', s='Framer website', p='CMS item', ps='CMS items', a='a', h1='Your Framer website, mentioned by AI.', tile='Items in your CMS, in your own design.',
   lead='We write what is missing and put it in your Framer CMS. You only approve.', dsrc='Items in your Framer CMS',
   b_eb='What goes into your Framer', st3=('Online', 'It is in your own CMS and appears in the design you already have.', ['In your design', 'Stays yours']),
   c3=('Your design stays your design', 'We fill your CMS. We do not touch your design, your animations or your settings.', ['Design', 'Animations', 'Settings']),
   chk=[('Indexing', 'Is a page excluded from search engines in the page settings?'), ('Domain', 'Is your framer address also found, next to your own domain?'), ('CMS', 'Are there items still set to draft?'), ('Titles', 'Does every page have its own title and description?'), ('Text', 'Is important text inside an image or animation?'), ('Sitemap', 'Does your domain work with sitemap.xml after it?')],
   fq=('Do you change anything about my design?', 'No. We fill your CMS with content. Your design, your animations and your settings stay as they are.'))),

 dict(key='cms_websitebouwers', icon='builder',
  nl=dict(slug='werkt-met/websitebouwers', n='websitebouwers', s='website', p='blogbericht', ps='blogberichten', h1='Website gemaakt bij je hostingpartij? Ook die noemt AI.', tile='Hostnet, Strato en andere bouwers van hostingpartijen.',
   bub='NXEO met websitebouwers', lead='Je website is gemaakt met de bouwer van Hostnet, Strato of een andere hostingpartij. Wij zetten de content erin. Jij keurt alleen goed.',
   title='NXEO met de websitebouwer van je hostingpartij', fh='Vragen over NXEO en websitebouwers',
   k_h='Loop je websitebouwer na. In tien minuten.', kq='Zes dingen die we bij websitebouwers van hostingpartijen steeds weer tegenkomen. Kom je er niet uit, dan kijken we met je mee.',
   c3=('Je website blijft zoals hij is', 'We plaatsen inhoud. Aan je ontwerp, je menu en je instellingen komen we niet.', ['Ontwerp', 'Menu', 'Instellingen']),
   chk=[('Zichtbaarheid', 'Is er een schakelaar die je site verbergt voor zoekmachines?'), ('Blog', 'Heeft je pakket een blog of nieuwsonderdeel?'), ('Titels', 'Kun je per pagina een titel en omschrijving invullen?'), ('Adressen', 'Staan er gewone woorden in het adres van een pagina?'), ('Tekst', 'Staat belangrijke tekst in een afbeelding?'), ('Sitemap', 'Werkt je domein met sitemap.xml erachter?')],
   fq=('Mijn websitebouwer staat er niet bij. Kan het dan ook?', 'Ja. We werken met de bouwers van Hostnet, Strato en vergelijkbare partijen. Bij de intake kijken we hoe content het best op jouw website komt.')),
  en=dict(slug='works-with/website-builders', n='website builders', s='website', p='blog post', ps='blog posts', a='a', h1='Website built with your hosting company? AI can mention that too.', tile='Hostnet, Strato and other builders from hosting companies.',
   bub='NXEO with website builders', lead='Your website was made with the builder from Hostnet, Strato or another hosting company. We put the content in. You only approve.',
   title='NXEO with your hosting company\'s website builder', fh='Questions about NXEO and website builders',
   k_h='Go through your website builder. In ten minutes.', kq='Six things we come across with website builders from hosting companies again and again. If you get stuck, we will look along with you.',
   c3=('Your website stays as it is', 'We publish content. We do not touch your design, your menu or your settings.', ['Design', 'Menu', 'Settings']),
   chk=[('Visibility', 'Is there a switch that hides your site from search engines?'), ('Blog', 'Does your plan include a blog or news section?'), ('Titles', 'Can you enter a title and description per page?'), ('Addresses', 'Are there plain words in the address of a page?'), ('Text', 'Is important text inside an image?'), ('Sitemap', 'Does your domain work with sitemap.xml after it?')],
   fq=('My website builder is not listed. Can it still be done?', 'Yes. We work with the builders from Hostnet, Strato and comparable companies. During onboarding we look at how content can best get onto your website.'))),

 dict(key='cms_code', icon='code',
  nl=dict(slug='werkt-met/gecodeerde-website', n='gecodeerde websites', s='website', p='artikel', ps='artikelen', h1='Website op maat gecodeerd? Ook daar zetten we het in.', tile='Zelf gebouwd of door een ontwikkelaar, met of zonder CMS.',
   bub='NXEO met gecodeerde websites', lead='Je website is op maat gebouwd. Wij leveren de content op de manier die bij jouw code past. Jij keurt alleen goed.',
   title='NXEO met een gecodeerde website | Word genoemd door AI', fh='Vragen over NXEO en gecodeerde websites',
   st1=('Koppelen', 'Bij de intake kijken we hoe content het best in jouw website komt, en zetten we de koppeling klaar.', ['Eén keer instellen', 'Past bij jouw code']),
   k_h='Loop je website na. In tien minuten.', kq='Zes dingen die we bij op maat gebouwde websites steeds weer tegenkomen. Kom je er niet uit, dan kijken we met je mee.',
   c3=('Je code blijft je code', 'We leveren inhoud aan. Aan je code, je ontwerp en je hosting komen we niet.', ['Code', 'Ontwerp', 'Hosting']),
   chk=[('Weergave', 'Staat de tekst al in de pagina voordat er een script draait?'), ('Titels', 'Heeft elke pagina een eigen titel en omschrijving?'), ('Sitemap', 'Wordt er een sitemap gemaakt en bijgewerkt?'), ('Robots.txt', 'Staat daar een regel in die bezoekers weert?'), ('Adressen', 'Heeft elke pagina een eigen adres?'), ('Beheer', 'Kan er content bij zonder dat een ontwikkelaar het doet?')],
   fq=('Moet mijn ontwikkelaar iets doen?', 'Dat hangt af van hoe je website is gebouwd. Soms kunnen we direct koppelen, soms is er eenmalig een kleine aanpassing nodig. Dat bespreken we bij de intake, zodat je vooraf weet waar je aan toe bent.')),
  en=dict(slug='works-with/coded-website', n='coded websites', s='website', p='article', ps='articles', a='an', h1='Website coded to order? We put it in there too.', tile='Built yourself or by a developer, with or without a CMS.',
   bub='NXEO with coded websites', lead='Your website was built to order. We deliver the content in the way that fits your code. You only approve.',
   title='NXEO with a coded website | Get mentioned by AI', fh='Questions about NXEO and coded websites',
   st1=('Connect', 'During onboarding we look at how content can best get into your website, and we set up the connection.', ['Set up once', 'Fits your code']),
   k_h='Go through your website. In ten minutes.', kq='Six things we come across on websites built to order again and again. If you get stuck, we will look along with you.',
   c3=('Your code stays your code', 'We deliver content. We do not touch your code, your design or your hosting.', ['Code', 'Design', 'Hosting']),
   chk=[('Rendering', 'Is the text already in the page before a script runs?'), ('Titles', 'Does every page have its own title and description?'), ('Sitemap', 'Is a sitemap generated and kept current?'), ('Robots.txt', 'Is there a rule in it that keeps visitors out?'), ('Addresses', 'Does every page have its own address?'), ('Upkeep', 'Can content be added without a developer doing it?')],
   fq=('Does my developer have to do anything?', 'That depends on how your website was built. Sometimes we can connect directly, sometimes a small change is needed once. We discuss that during onboarding, so you know beforehand where you stand.'))),

 dict(key='cms_ai', icon='ai',
  nl=dict(slug='werkt-met/ai-website', n='websites gemaakt met AI', s='website', p='artikel', ps='artikelen', h1='Website gemaakt met AI? Zorg dat AI hem ook kan lezen.', tile='Gebouwd met een AI bouwer, in een middag online gezet.',
   bub='NXEO met websites gemaakt met AI', lead='Een AI bouwer maakt in een middag een mooie website. Of een AI systeem hem daarna kan lezen, is een andere vraag. Wij regelen de content.',
   title='NXEO met een website gemaakt met AI | Word genoemd door AI', fh='Vragen over NXEO en websites gemaakt met AI',
   st1=('Koppelen', 'Bij de intake kijken we hoe content het best in jouw website komt, en zetten we de koppeling klaar.', ['Eén keer instellen', 'Geen technische kennis nodig']),
   k_h='Loop je website na. In tien minuten.', kq='Zes dingen die we bij websites uit een AI bouwer steeds weer tegenkomen. Kom je er niet uit, dan kijken we met je mee.',
   c3=('Je website blijft zoals hij is', 'We leveren inhoud aan. Aan je ontwerp, je opbouw en je hosting komen we niet.', ['Ontwerp', 'Opbouw', 'Hosting']),
   chk=[('Weergave', 'Staat de tekst al in de pagina voordat er een script draait?'), ('Adressen', 'Heeft elke pagina een eigen adres, of is het één lange pagina?'), ('Titels', 'Heeft elke pagina een eigen titel en omschrijving?'), ('Sitemap', 'Is er een sitemap?'), ('Domein', 'Staat de site op je eigen domein?'), ('Tekst', 'Zegt de tekst wat jij doet, of wat de bouwer bedacht?')],
   fq=('Mijn website is gemaakt met AI. Kan AI hem dan vanzelf lezen?', 'Niet altijd. Veel van deze websites bouwen de pagina pas op in de browser. Een systeem dat de pagina ophaalt, ziet dan weinig tekst. Bij de intake kijken we hoe dat bij jouw website zit.')),
  en=dict(slug='works-with/ai-built-website', n='websites made with AI', s='website', p='article', ps='articles', a='an', h1='Website made with AI? Make sure AI can read it too.', tile='Built with an AI builder, put online in an afternoon.',
   bub='NXEO with websites made with AI', lead='An AI builder makes a handsome website in an afternoon. Whether an AI system can read it afterwards is another question. We take care of the content.',
   title='NXEO with a website made with AI | Get mentioned by AI', fh='Questions about NXEO and websites made with AI',
   st1=('Connect', 'During onboarding we look at how content can best get into your website, and we set up the connection.', ['Set up once', 'No technical knowledge needed']),
   k_h='Go through your website. In ten minutes.', kq='Six things we come across on websites from an AI builder again and again. If you get stuck, we will look along with you.',
   c3=('Your website stays as it is', 'We deliver content. We do not touch your design, your structure or your hosting.', ['Design', 'Structure', 'Hosting']),
   chk=[('Rendering', 'Is the text already in the page before a script runs?'), ('Addresses', 'Does every page have its own address, or is it one long page?'), ('Titles', 'Does every page have its own title and description?'), ('Sitemap', 'Is there a sitemap?'), ('Domain', 'Is the site on your own domain?'), ('Text', 'Does the text say what you do, or what the builder came up with?')],
   fq=('My website was made with AI. Can AI then read it by itself?', 'Not always. Many of these websites only build the page in the browser. A system that fetches the page then sees little text. During onboarding we look at how that is for your website.'))),

 dict(key='cms_maatwerk', icon='plug',
  nl=dict(slug='werkt-met/maatwerk', n='maatwerk', s='website', p='artikel', ps='artikelen', h1='Staat jouw systeem er niet bij? We koppelen het.', tile='Een ander of eigen systeem. In principe kunnen we alles koppelen.',
   bub='Koppeling op maat', lead='Een ouder systeem, een eigen platform of iets wat we nog niet kennen. In principe kunnen we alles koppelen wat een website kan tonen.',
   title='Koppeling op maat | NXEO werkt met jouw website', fh='Vragen over een koppeling op maat',
   st1=('Koppelen', 'Je vertelt waar je website op draait. Wij zoeken uit hoe content er het best in komt en bouwen de koppeling.', ['Eén keer instellen', 'Wij zoeken het uit']),
   k_eb='Voor we beginnen', k_h='Zes vragen. Daarna weten we genoeg.', kbs='Intake', kt='Wat we van je willen weten',
   kq='Je hoeft het antwoord niet op alles te weten. In een gesprek van vijftien minuten lopen we het samen door.', kst=[('15 min', 'online'), ('€0', 'aan kosten')],
   c3=('Je systeem blijft je systeem', 'We leveren inhoud aan. Aan je systeem, je ontwerp en je instellingen komen we niet.', ['Systeem', 'Ontwerp', 'Instellingen']),
   chk=[('Systeem', 'Waar is je website mee gebouwd?'), ('Toegang', 'Wie kan ons toegang geven?'), ('Plek', 'Waar moet nieuwe content komen te staan?'), ('Beheer', 'Wie past je website nu aan?'), ('Talen', 'In welke talen is je website?'), ('Grenzen', 'Is er iets wat niet mag veranderen?')],
   fq=('Mijn systeem is zelf gebouwd of al wat ouder. Kan het dan?', 'In principe wel. We zoeken een manier die bij jouw systeem past. Blijkt het bij de intake toch niet te kunnen, dan zeggen we dat eerlijk voordat je iets betaalt.')),
  en=dict(slug='works-with/custom', n='custom', s='website', p='article', ps='articles', a='an', h1='Is your system not listed? We connect it.', tile='Another system or your own. In principle we can connect anything.',
   bub='Custom connection', lead='An older system, a platform of your own or something we do not know yet. In principle we can connect anything that can show a website.',
   title='Custom connection | NXEO works with your website', fh='Questions about a custom connection',
   st1=('Connect', 'You tell us what your website runs on. We work out how content can best get in and build the connection.', ['Set up once', 'We work it out']),
   k_eb='Before we start', k_h='Six questions. After that we know enough.', kbs='Onboarding', kt='What we would like to know',
   kq='You do not need to know the answer to everything. In a fifteen minute call we go through it together.', kst=[('15 min', 'online'), ('€0', 'in costs')],
   c3=('Your system stays your system', 'We deliver content. We do not touch your system, your design or your settings.', ['System', 'Design', 'Settings']),
   chk=[('System', 'What was your website built with?'), ('Access', 'Who can give us access?'), ('Place', 'Where should new content go?'), ('Upkeep', 'Who edits your website now?'), ('Languages', 'In which languages is your website?'), ('Limits', 'Is there anything that must not change?')],
   fq=('My system was built in house or is a bit older. Can it be done?', 'In principle, yes. We look for a way that fits your system. If it turns out during onboarding that it cannot be done after all, we say so honestly before you pay anything.'))),
]

GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/></svg>'

def fmt(x, v):
    if isinstance(x, str):
        for k, val in v.items(): x = x.replace('{' + k + '}', val)
        return x
    if isinstance(x, (list, tuple)): return type(x)(fmt(i, v) for i in x)
    return x

def data(p, lang):
    d = dict(C[lang]); d.update(p[lang])
    v = dict(n=d['n'], s=d['s'], p=d['p'], ps=d['ps'], P=d['p'][0].upper() + d['p'][1:], PS=d['ps'][0].upper() + d['ps'][1:], a=d.get('a', ''))
    return {k: fmt(x, v) for k, x in d.items()}

def tile(p, cls=''):
    if p.get('mark'): return '<span class="w%s%s"><img src="{{%s}}" alt=""></span>' % (' wide' if p.get('wide') else '', cls, p['mark'])
    return '<span class="w ic%s">%s</span>' % (cls, ICON[p['icon']])

def page(p, lang):
    t = data(p, lang); key = p['key']
    src = ('<img src="{{%s}}" alt="">' % p['mark']) if p.get('mark') and not p.get('wide') else ''
    li = lambda rows, you='': ''.join('<div class="li%s"><span class="rank">%d</span>%s<span class="dim">%s</span></div>' % (you, i + 1, a, b) for i, (a, b) in enumerate(rows))
    h = ('<section class="page" id="page-%s">\n  <div class="hero hero-c cm-hero">\n    <div class="hero-stack">\n'
         '      <div class="cm-pair" aria-hidden="true"><span><img src="{{nxeo_icon}}" alt=""></span><i>+</i>%s</div>\n'
         '      <div class="bubble bubble-blue">%s</div>\n      <h1>%s<span class="cursor" aria-hidden="true"></span></h1>\n      <p class="def">%s</p>\n'
         '      <div class="cm-btns"><a class="btn btn-white" href="#aanvraag" data-link>%s <span class="arr">→</span></a><a class="btn btn-glass" href="#nulmeting" data-link>%s</a></div>\n    </div>\n'
         '    <div class="wrap">\n      <div class="chat cm-chat" aria-label="%s">\n        <div class="chat-head"><span class="ai-src">%s%s</span><div class="tabs" role="tablist"><button class="tab" role="tab" aria-selected="true" data-demo="before">%s</button><button class="tab" role="tab" aria-selected="false" data-demo="after">%s</button></div></div>\n'
         '        <div class="msg ai"><div class="panes"><div class="ans is-on" data-demo-pane="before"><p>%s</p><div class="list">%s</div><p><mark>%s</mark><span class="cursor" aria-hidden="true"></span></p></div>'
         '<div class="ans" data-demo-pane="after"><p>%s</p><div class="list">%s</div><p><mark class="good">%s</mark><span class="cursor" aria-hidden="true"></span></p></div></div></div>\n      </div>\n    </div>\n  </div>\n') % (
         key, tile(p), t['bub'], t['h1'], t['lead'], t['b1'], t['b2'], t['dsrc'], src, t['dsrc'], t['dt'][0], t['dt'][1], t['d0p'], li(t['d0']), t['d0m'], t['d1p'], li(t['d1'], ' you'), t['d1m'])
    arts = ['<div class="cm-link"><span><img src="{{nxeo_icon}}" alt=""></span><u></u>%s<em class="pill-ok">%s</em></div>' % (tile(p), t['conn']),
            '<div class="mini cm-appr"><small>%s</small><b>%s</b><span class="ln"></span><span class="ln"></span><span class="ln s"></span><div class="act"><i class="ok">%s</i><i>%s</i></div></div>' % (t['apm'], t['d1'][0][0], t['apok'], t['apch']),
            '<div class="bx-browser cm-br" aria-hidden="true"><div class="bar"><i></i><i></i><i></i><span class="url">%s</span></div><div class="pg"><span class="ln t"></span><span class="ln"></span><span class="ln s"></span><span class="pub">%s</span></div></div>' % (t['burl'], t['bpub'])]
    st = [t['st1'], t['st2'], t['st3']]
    h += ('  <div class="sec">\n    <div class="wrap">\n      <div class="sec-head center" data-reveal><span class="eyebrow">%s</span><h2>%s</h2></div>\n      <div class="steps3">%s</div>\n    </div>\n  </div>\n') % (
         t['s_eb'], t['s_h'], ''.join('<div class="step-card" data-reveal><span class="num">0%d</span><div class="art">%s</div><h4>%s</h4><p>%s</p><div class="chips">%s</div></div>' % (i + 1, arts[i], a, b, ''.join('<span class="chip">%s</span>' % x for x in c)) for i, (a, b, c) in enumerate(st)))
    n = lambda i: '<em>%d</em>' % i
    post = ('<div class="cm-post"><div class="cm-url">%s<span>%s</span></div><div class="cm-pb"><h4>%s%s</h4><p>%s%s</p><h5>%s%s</h5><div class="ln"></div><div class="ln s"></div><h5>%s</h5><div class="ln"></div>'
            '<div class="cm-fq">%s<span>%s</span><i>+</i></div><a>%s%s</a></div><small>%s</small></div>') % (n(1), t['burl'], n(2), t['ph1'], n(3), t['pans'], n(4), t['ph2a'], t['ph2b'], n(5), t['pfq'], n(6), t['plink'], t['pnote'])
    c3 = t['c3']
    cs = [t['c1'], t['c2'], (c3[0], c3[1]), t['c4']]
    cards = ['<div class="mini-rows cm-mr">%s</div>' % ''.join('<div class="mini mini-row"><span class="lbl">%s</span><span class="st ok">%s</span></div>' % x for x in t['c1rows']),
             '<div class="cm-two"><div><b>%s</b><span>%s</span></div><div><b>%s</b><span>%s</span></div></div>' % (t['c2a'] + t['c2b']),
             '<div class="own">%s</div>' % ''.join('<span>%s</span>' % x for x in c3[2]),
             '<div class="own">%s</div>' % ''.join('<span>%s</span>' % x for x in t['c4c'])]
    h += ('  <div class="sec" style="padding-top:0">\n    <div class="wrap">\n      <div class="sec-head" data-reveal><span class="eyebrow">%s</span><h2>%s</h2></div>\n      <div class="bento2">\n'
          '        <div class="bx bx-web cm-lead" data-reveal><div class="bx-text"><h4>%s</h4><p>%s</p><ol class="cm-an">%s</ol></div><div class="bx-well">%s</div></div>\n%s      </div>\n    </div>\n  </div>\n') % (
          t['b_eb'], t['b_h'], t['l_h'], t['l_p'], ''.join('<li><span class="n">%d</span><b>%s</b></li>' % (i + 1, a) for i, a in enumerate(t['an'])), post,
          ''.join('        <div class="bx%s" data-reveal><div class="bx-text"><h4>%s</h4><p>%s</p></div><div class="bx-art">%s</div></div>\n' % (' cm-fill' if i == 0 else '', cs[i][0], cs[i][1], cards[i]) for i in range(4)))
    if p.get('article'):
        btns = '<a class="btn btn-white" href="#%s" data-link>%s <span class="arr">→</span></a><a class="btn btn-glass" href="#meekijken" data-link>%s</a>' % (p['article'], t['k_open'], t['k_walk2'])
    else:
        btns = '<a class="btn btn-white" href="#meekijken" data-link>%s <span class="arr">→</span></a>' % t['k_walk']
    brand = ('<img src="{{%s}}" alt="">' % p['mark']) if p.get('mark') and not p.get('wide') else ''
    kb = t['n'][0].upper() + t['n'][1:]
    h += ('  <div class="sec" style="padding-top:0">\n    <div class="wrap">\n      <div class="sec-head case-head" data-reveal><div class="ch-text"><span class="eyebrow">%s</span><h2>%s</h2></div></div>\n'
          '      <div class="case2 cm-case" data-reveal><div class="c2-left"><div class="c2-brand">%s%s<span>%s</span></div><p class="c2-quote">%s</p><div class="cm-cb">%s</div></div>'
          '<div class="c2-right"><div class="c2-title">%s</div><ol class="c2-tl">%s</ol><div class="c2-stats">%s</div></div></div>\n    </div>\n  </div>\n') % (
          t['k_eb'], t['k_h'], brand, kb, t['kbs'], t['kq'], btns, t['kt'], ''.join('<li><span class="dot"></span><span class="wk">%s</span><span class="lbl">%s</span></li>' % x for x in t['chk']), ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in t['kst']))
    faq = [t['f_first'], t['fq']] + list(t['f_rest'])
    h += ('  <div class="sec" style="padding-top:0">\n    <div class="wrap">\n      <div class="sec-head center" data-reveal><h2>%s</h2></div>\n      <div class="faq faq-teaser" data-reveal>%s</div>\n    </div>\n  </div>\n</section>\n') % (
          t['fh'], ''.join('<details><summary>%s</summary><p>%s</p></details>' % (a, b) for a, b in faq))
    return h, t

def overview(lang):
    c = C[lang]
    tiles = ''
    for p in P:
        t = data(p, lang)
        name = t['n'][0].upper() + t['n'][1:]
        tiles += '<a class="kp" href="#%s" data-link>%s<b>%s</b><p>%s</p><i>%s <span class="arr">→</span></i></a>' % (p['key'], tile(p), name, t['tile'], c['o_more'])
    return ('<section class="page" id="page-koppelingen">\n  <div class="hero hero-c cm-hero kp-hero">\n    <div class="hero-stack">\n      <div class="bubble bubble-blue">%s</div>\n      <h1>%s<span class="cursor" aria-hidden="true"></span></h1>\n      <p class="def">%s</p>\n'
            '      <div class="cm-btns"><a class="btn btn-white" href="#aanvraag" data-link>%s <span class="arr">→</span></a><a class="btn btn-glass" href="#nulmeting" data-link>%s</a></div>\n    </div>\n  </div>\n'
            '  <div class="sec">\n    <div class="wrap">\n      <div class="sec-head" data-reveal><span class="eyebrow">%s</span><h2>%s</h2></div>\n      <div class="kp-grid" data-reveal>%s</div>\n'
            '      <div class="np-cta kp-cta" data-reveal><div><h3>%s</h3><p>%s</p></div><a class="btn btn-blue" href="#cms_maatwerk" data-link>%s <span class="arr">→</span></a></div>\n    </div>\n  </div>\n</section>\n') % (
            c['o_bub'], c['o_h1'], c['o_lead'], c['b1'], c['b2'], c['o_eb'], c['o_h'], tiles, c['o_ch'], c['o_cp'], c['o_cb'])

if __name__ == '__main__':
    import re
    for lang in ('nl', 'en'):
        j = json.load(open('i18n/%s.json' % lang))
        for p in P:
            html, t = page(p, lang)
            open('content/%s/%s.html' % (lang, p['key']), 'w').write(html)
            j['pages'][p['key']] = {'slug': t['slug'], 'title': t['title'], 'description': t['desc']}
        open('content/%s/koppelingen.html' % lang, 'w').write(overview(lang))
        c = C[lang]
        j['pages']['koppelingen'] = {'slug': c['o_slug'], 'title': c['o_title'], 'description': c['o_desc']}
        json.dump(j, open('i18n/%s.json' % lang, 'w'), ensure_ascii=False, indent=2)
        # footer kolom
        f = 'content/%s/footer.html' % lang; s = open(f).read()
        col = '<nav class="end-col" aria-label="%s"><h4>%s</h4><ul>%s<li><a href="#koppelingen" data-link>%s</a></li></ul></nav>' % (
            c['col'], c['col'], ''.join('<li><a href="#%s" data-link>%s</a></li>' % (p['key'], p[lang]['n']) for p in P[:5]), c['col_all'])
        s = re.sub(r'<nav class="end-col" aria-label="(Werkt met|Works with)">.*?</nav>', lambda m: col, s, flags=re.S)
        open(f, 'w').write(s)
    print('pages:', ' '.join(p['key'] for p in P), 'koppelingen')
