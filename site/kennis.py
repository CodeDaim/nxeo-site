# Kennisbank: de ingang tot alles wat NXEO over AI zichtbaarheid heeft geschreven, plus de begrippenlijst.
# Wordt door build.py gebruikt voor de pagina's 'kennisbank' en 'begrippen'.
import json, html, re

# groepen: (titel nl, titel en, [nl slugs van artikelen of #pagina sleutels])
GROUPS = [
 ('Begin hier', 'Start here', ['hoe-word-je-genoemd-door-ai', 'wat-is-geo-en-wat-is-het-verschil-met-seo', 'is-chatgpt-de-google-van-2026', 'als-ai-jouw-bedrijf-niet-noemt-besta-je-niet', 'wat-is-nxeo']),
 ('Per AI systeem', 'Per AI system', ['hoe-chatgpt-bepaalt-welke-bedrijven-het-noemt', 'gemini-noemt-mijn-bedrijf-niet', 'claude-gebruikt-brave-om-jouw-bedrijf-te-vinden', 'genoemd-worden-in-perplexity', 'genoemd-worden-in-microsoft-copilot', 'in-de-ai-overzichten-van-google-komen', 'mijn-positie-versterken-op-google']),
 ('Meten waar je staat', 'Measure where you stand', ['mijn-bedrijf-genoemd-in-ai', 'waarom-sta-ik-niet-in-de-aanbevelingen-van-ai', 'je-concurrent-wordt-wel-genoemd-in-chatgpt', 'ai-zegt-iets-verkeerds-over-mijn-bedrijf', 'hoe-lang-duurt-het-voordat-ai-je-bedrijf-noemt']),
 ('Zelf aan de slag', 'Do it yourself', ['welke-vragen-stellen-klanten-aan-ai', 'veelgestelde-vragen-pagina-die-ai-kan-citeren', 'lokaal-gevonden-worden-in-ai', 'reviews-en-vermeldingen-waarom-ai-op-anderen-vertrouwt', 'wordpress-controlelijst-vindbaar-voor-ai', 'meer-leads-uit-je-website-met-betere-vindbaarheid', 'ai-zichtbaarheid-zelf-doen-bureau-of-software']),
]
T = {'nl': dict(bub='Alles over genoemd worden door AI', h1='De kennisbank.', lead='Uitleg, stappen en begrippen over zichtbaarheid in ChatGPT, Gemini, Claude, Perplexity en Google. Gratis te lezen, zonder vakjargon.', b1='Begin bij de gids', b2='Bekijk de begrippen',
   more=('Verder kijken', [('begrippen', 'Begrippenlijst'), ('branches', 'Per branche'), ('koppelingen', 'Per websitesysteem'), ('faq', 'Veelgestelde vragen'), ('blog', 'Alle artikelen op datum')]),
   g_bub='Wat betekent dat?', g_h1='Begrippen, in gewone taal.', g_lead='De woorden die je tegenkomt als het over AI en vindbaarheid gaat. Kort uitgelegd, met een link als je er meer over wilt lezen.', g_more='Lees meer', g_back='Naar de kennisbank'),
 'en': dict(bub='Everything about being mentioned by AI', h1='The knowledge base.', lead='Explanations, steps and terms about visibility in ChatGPT, Gemini, Claude, Perplexity and Google. Free to read, without jargon.', b1='Start with the guide', b2='View the glossary',
   more=('Look further', [('begrippen', 'Glossary'), ('branches', 'By sector'), ('koppelingen', 'By website system'), ('faq', 'Frequently asked questions'), ('blog', 'All articles by date')]),
   g_bub='What does that mean?', g_h1='Terms, in plain language.', g_lead='The words you come across when it is about AI and findability. Explained briefly, with a link if you want to read more.', g_more='Read more', g_back='To the knowledge base')}

# begrippen: (id, nl term, nl uitleg, en term, en uitleg, link sleutel of '')
A = lambda s: 'art_' + s.replace('-', '_')
TERMS = [
 ('ai-zichtbaarheid', 'AI zichtbaarheid', 'Hoe vaak en hoe goed een bedrijf genoemd wordt in de antwoorden van AI systemen zoals ChatGPT en Gemini. Je meet het door echte klantvragen te stellen en te tellen in hoeveel antwoorden je voorkomt.', 'AI visibility', 'How often and how well a company is mentioned in the answers of AI systems such as ChatGPT and Gemini. You measure it by asking real customer questions and counting in how many answers you appear.', A('mijn-bedrijf-genoemd-in-ai')),
 ('geo', 'GEO', 'Generative Engine Optimization. Het werk dat je doet om genoemd te worden in een antwoord dat een AI systeem schrijft. Het grootste deel overlapt met gewone SEO.', 'GEO', 'Generative Engine Optimization. The work you do to be mentioned in an answer written by an AI system. Most of it overlaps with ordinary SEO.', A('wat-is-geo-en-wat-is-het-verschil-met-seo')),
 ('aeo', 'AEO', 'Answer Engine Optimization. Een andere naam voor ongeveer hetzelfde als GEO: zorgen dat je inhoud als antwoord gebruikt kan worden.', 'AEO', 'Answer Engine Optimization. Another name for roughly the same as GEO: making sure your content can be used as an answer.', A('wat-is-geo-en-wat-is-het-verschil-met-seo')),
 ('seo', 'SEO', 'Search Engine Optimization. Het werk dat je doet om hoog in de gewone zoekresultaten van Google te staan. Een goede basis hier helpt ook bij AI.', 'SEO', 'Search Engine Optimization. The work you do to rank high in the ordinary Google search results. A good basis here also helps with AI.', A('mijn-positie-versterken-op-google')),
 ('ai-overzicht', 'AI overzicht', 'Het geschreven antwoord dat Google bij sommige zoekopdrachten boven de gewone resultaten toont, met links naar de bronnen. In het Engels: AI Overview.', 'AI Overview', 'The written answer Google shows above the ordinary results for some searches, with links to the sources.', A('in-de-ai-overzichten-van-google-komen')),
 ('taalmodel', 'Taalmodel', 'De software achter een AI systeem. Het is getraind op heel veel tekst en schrijft op basis daarvan nieuwe tekst. Vaak afgekort tot LLM.', 'Language model', 'The software behind an AI system. It was trained on a very large amount of text and writes new text based on that. Often shortened to LLM.', ''),
 ('trainingsdata', 'Trainingsdata', 'De teksten waarmee een taalmodel is getraind. Wat daarin over je bedrijf stond, zit in het model zelf en verandert pas bij een nieuwe versie.', 'Training data', 'The texts a language model was trained on. What they said about your company is inside the model itself and only changes with a new version.', A('hoe-lang-duurt-het-voordat-ai-je-bedrijf-noemt')),
 ('live-zoeken', 'Live zoeken', 'Een AI systeem zoekt tijdens het beantwoorden op internet en gebruikt wat het vindt. Nieuwe pagina\'s kunnen daardoor binnen weken in antwoorden opduiken.', 'Live search', 'An AI system searches the internet while answering and uses what it finds. New pages can therefore show up in answers within weeks.', A('hoe-chatgpt-bepaalt-welke-bedrijven-het-noemt')),
 ('bron', 'Bron of citatie', 'De pagina waar een AI systeem een deel van zijn antwoord vandaan haalt, vaak met een link erbij. Genoemd worden en als bron dienen zijn twee verschillende dingen.', 'Source or citation', 'The page an AI system takes part of its answer from, often with a link. Being mentioned and being used as a source are two different things.', A('veelgestelde-vragen-pagina-die-ai-kan-citeren')),
 ('vermelding', 'Vermelding', 'Je bedrijfsnaam staat in het antwoord. Dat kan met of zonder link, en met een goede of een verkeerde omschrijving.', 'Mention', 'Your company name appears in the answer. That can be with or without a link, and with a right or a wrong description.', A('mijn-bedrijf-genoemd-in-ai')),
 ('koopvraag', 'Koopvraag', 'Een vraag van iemand die een bedrijf zoekt, zoals "wie kan dit voor mij doen" of "wat kost het". Dit zijn de vragen waarbij je genoemd wilt worden.', 'Buying question', 'A question from someone looking for a company, such as "who can do this for me" or "what does it cost". These are the questions you want to be mentioned for.', A('welke-vragen-stellen-klanten-aan-ai')),
 ('nulmeting', 'Nulmeting', 'Een eerste meting van waar je nu staat, voordat je iets verandert. Bij NXEO: op welke koopvragen ChatGPT je bedrijf noemt en wie er wel staat.', 'Baseline check', 'A first measurement of where you stand now, before you change anything. At NXEO: for which buying questions ChatGPT mentions your company and who appears instead.', 'nulmeting'),
 ('crawler', 'Crawler', 'Een programma dat websites bezoekt en leest. Zoekmachines en AI bedrijven hebben elk hun eigen crawlers.', 'Crawler', 'A program that visits and reads websites. Search engines and AI companies each have their own crawlers.', ''),
 ('robots-txt', 'robots.txt', 'Een klein bestand op je website waarin staat welke crawlers welke pagina\'s mogen lezen. Een fout hierin kan je onzichtbaar maken zonder dat je het merkt.', 'robots.txt', 'A small file on your website that says which crawlers may read which pages. A mistake here can make you invisible without you noticing.', A('wordpress-controlelijst-vindbaar-voor-ai')),
 ('oai-searchbot', 'OAI-SearchBot', 'De crawler van OpenAI voor de zoekfunctie van ChatGPT. Blokkeer je die, dan kan ChatGPT je pagina\'s niet als bron tonen.', 'OAI-SearchBot', 'OpenAI\'s crawler for the search feature of ChatGPT. If you block it, ChatGPT cannot show your pages as a source.', A('hoe-chatgpt-bepaalt-welke-bedrijven-het-noemt')),
 ('gptbot', 'GPTBot', 'De crawler van OpenAI die tekst verzamelt om modellen te trainen. Dat is een andere dan de crawler voor zoeken.', 'GPTBot', 'OpenAI\'s crawler that collects text to train models. It is a different one from the crawler for search.', ''),
 ('llms-txt', 'llms.txt', 'Een voorstel voor een bestand dat AI systemen een samenvatting van je website geeft. Het is geen standaard, en het is niet aangetoond dat de grote systemen het gebruiken. Verwacht er geen wonderen van.', 'llms.txt', 'A proposal for a file that gives AI systems a summary of your website. It is not a standard, and it has not been shown that the major systems use it. Do not expect miracles from it.', ''),
 ('gestructureerde-data', 'Gestructureerde data', 'Extra code in een pagina die in een vaste vorm zegt wat erop staat: een bedrijf, een vraag met antwoord, een prijs. Het helpt zoekmachines je inhoud te begrijpen.', 'Structured data', 'Extra code in a page that says in a fixed form what is on it: a company, a question with an answer, a price. It helps search engines understand your content.', ''),
 ('index', 'Index', 'De verzameling pagina\'s die een zoekmachine kent. Sta je er niet in, dan kan die zoekmachine je niet tonen, en een AI systeem dat erop leunt ook niet.', 'Index', 'The collection of pages a search engine knows. If you are not in it, that search engine cannot show you, and neither can an AI system that leans on it.', A('claude-gebruikt-brave-om-jouw-bedrijf-te-vinden')),
 ('bedrijfsprofiel', 'Google bedrijfsprofiel', 'Je gratis vermelding in Google Zoeken en Maps, met adres, openingstijden, diensten en reviews. Gemini leunt hier sterk op bij lokale vragen.', 'Google Business Profile', 'Your free listing in Google Search and Maps, with address, opening hours, services and reviews. Gemini leans on it heavily for local questions.', A('gemini-noemt-mijn-bedrijf-niet')),
 ('hallucinatie', 'Hallucinatie', 'Een AI systeem vertelt iets dat niet klopt, met dezelfde stelligheid als iets dat wel klopt. Over bedrijven komt een fout meestal uit een verouderde of foute bron.', 'Hallucination', 'An AI system says something that is not true, with the same confidence as something that is. About companies an error usually comes from an outdated or wrong source.', A('ai-zegt-iets-verkeerds-over-mijn-bedrijf')),
 ('prompt', 'Prompt', 'De vraag of opdracht die iemand aan een AI systeem geeft. Voor een bedrijf zijn de prompts van klanten het vertrekpunt.', 'Prompt', 'The question or instruction someone gives an AI system. For a company the prompts of customers are the starting point.', A('welke-vragen-stellen-klanten-aan-ai')),
 ('presence-score', 'Presence score', 'Het cijfer van 0 tot 100 waarmee NXEO voor klanten samenvat hoe vaak en hoe goed ze genoemd worden, over meerdere AI systemen.', 'Presence score', 'The figure from 0 to 100 with which NXEO sums up for customers how often and how well they are mentioned, across several AI systems.', 'faq'),
]


def _rows(items):
    return ''.join('<a href="#%s" data-link><b>%s</b><span class="arr">→</span></a>' % (k, html.escape(n)) for k, n in items)


def hub(lang, arts_nl, arts_lang, name):
    t = T[lang]; nl = lang == 'nl'
    by_nl = {a['slug']: a for a in arts_nl}
    def title(slug):
        key = A(slug)
        for a in arts_lang:
            if a['key'] == key: return key, a['title']
        return None
    cards = ''
    for g in GROUPS:
        items = [x for x in (title(s) for s in g[2]) if x]
        cards += '<div class="pm-card" data-reveal><h2>%s<span>%d</span></h2><div class="pm-rows">%s</div></div>' % (g[0] if nl else g[1], len(items), _rows(items))
    cards += '<div class="pm-card" data-reveal><h2>%s</h2><div class="pm-rows">%s</div></div>' % (t['more'][0], _rows(t['more'][1]))
    return ('<section class="page kb-page" id="page-kennisbank">\n  <div class="hero hero-c cm-hero kp-hero">\n    <div class="hero-stack">\n      <div class="bubble bubble-blue">%s</div>\n      <h1>%s<span class="cursor" aria-hidden="true"></span></h1>\n      <p class="def">%s</p>\n'
            '      <div class="cm-btns"><a class="btn btn-white" href="#%s" data-link>%s <span class="arr">→</span></a><a class="btn btn-glass" href="#begrippen" data-link>%s</a></div>\n    </div>\n  </div>\n'
            '  <div class="sec">\n    <div class="wrap">\n      <div class="pm-grid kb-grid">%s</div>\n    </div>\n  </div>\n</section>\n') % (t['bub'], t['h1'], t['lead'], A('hoe-word-je-genoemd-door-ai'), t['b1'], t['b2'], cards)


def glossary(lang, url):
    t = T[lang]; i = 1 if lang == 'nl' else 3
    terms = sorted(TERMS, key=lambda x: x[i].lower())
    letters = []
    body = ''
    for x in terms:
        L = x[i][0].upper()
        if L not in letters:
            letters.append(L)
        more = ('<a href="#%s" data-link>%s <span class="arr">→</span></a>' % (x[5], t['g_more'])) if x[5] else ''
        body += '<div class="gl-term" id="%s"><h2>%s</h2><p>%s</p>%s</div>' % (x[0], html.escape(x[i]), html.escape(x[i + 1]), more)
    schema = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": 'Begrippen' if lang == 'nl' else 'Glossary', "url": url, "inLanguage": lang,
              "hasDefinedTerm": [{"@type": "DefinedTerm", "name": x[i], "description": x[i + 1], "url": url + '#' + x[0]} for x in terms]}
    return ('<section class="page kb-page" id="page-begrippen">\n  <div class="hero hero-c cm-hero kp-hero">\n    <div class="hero-stack">\n      <div class="bubble bubble-blue">%s</div>\n      <h1>%s<span class="cursor" aria-hidden="true"></span></h1>\n      <p class="def">%s</p>\n    </div>\n  </div>\n'
            '  <div class="sec">\n    <div class="wrap">\n      <div class="gl-grid">%s</div>\n      <p class="gl-back"><a class="btn btn-ghost" href="#kennisbank" data-link>%s <span class="arr">→</span></a></p>\n    </div>\n  </div>\n'
            '<script type="application/ld+json">%s</script>\n</section>\n') % (t['g_bub'], t['g_h1'], t['g_lead'], body, t['g_back'], json.dumps(schema, ensure_ascii=False))
