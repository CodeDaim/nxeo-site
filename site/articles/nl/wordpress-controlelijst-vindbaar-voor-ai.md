---
title: WordPress controlelijst: kan AI jouw website lezen?
description: Zes instellingen in WordPress bepalen of ChatGPT, Gemini en Claude je website kunnen lezen. Met deze controlelijst loop je ze in tien minuten na, met per punt waar je moet klikken.
date: 2026-11-13
category: Praktijk
keyword: WordPress website vindbaar voor AI
kort: Eén vinkje onder Instellingen en Lezen kan je hele website onzichtbaar maken. Het staat vaker aan dan je denkt. | Beveiliging die onbekende bezoekers weert, houdt ook de zoekdiensten achter AI buiten. | Je hebt geen plugin of technische kennis nodig. Alleen tien minuten en toegang tot je dashboard.
---

Een groot deel van de websites van kleine en middelgrote bedrijven draait op WordPress. Dat is prima. WordPress levert van zichzelf pagina's op die goed te lezen zijn, voor mensen en voor systemen.

Toch zien we bij WordPress websites steeds dezelfde zes dingen misgaan. Geen van de zes heeft met de inhoud te maken. Het zijn instellingen. Ze zijn ooit door iemand aangezet, vaak met een goede reden, en daarna vergeten. Het gevolg is dat een AI systeem je website niet kan vinden of niet kan lezen, hoe goed je teksten ook zijn.

Deze controlelijst loopt ze na. Je hebt er toegang tot je WordPress dashboard voor nodig en ongeveer tien minuten. Wil je je WordPress website vindbaar voor AI maken, dan is dit de plek om te beginnen. Schrijven heeft pas zin als wat je schrijft ook gelezen kan worden.

## Waarom dit eerst moet

Een AI systeem dat een vraag beantwoordt, zoekt pagina's op via een zoekdienst en leest ze. Gemini doet dat via Google. Claude via Brave. ChatGPT gebruikt een mix. Als een van die zoekdiensten je pagina niet kent of niet mag lezen, besta je voor dat systeem niet.

De oorzaken die we het vaakst vinden als een bedrijf nergens genoemd wordt, staan in [waarom sta ik niet in de aanbevelingen van AI](#art_waarom_sta_ik_niet_in_de_aanbevelingen_van_ai). De technische oorzaak is daar één van de zeven. Bij WordPress is hij in de meeste gevallen terug te voeren op een van de zes punten hieronder.

## 1. Lezen: vraag je zoekmachines om weg te blijven?

**Waar:** Instellingen, dan Lezen. Onderaan staat "Zichtbaarheid voor zoekmachines".

**Wat je zoekt:** een vinkje bij "Zoekmachines ontmoedigen om deze site te indexeren".

Dit is de bekendste valkuil van WordPress, en hij komt nog steeds voor. Tijdens de bouw van een website zet de bouwer dit vinkje aan, zodat de halve website niet in Google verschijnt. Dat is verstandig. Bij de oplevering moet het weer uit. Soms gebeurt dat niet.

Staat het vinkje aan, dan vraagt je website aan elke zoekmachine om hem over te slaan. De meeste doen dat netjes. Je kunt een jaar lang elke week schrijven zonder dat er één pagina wordt opgenomen.

**Wat je doet:** haal het vinkje weg en sla op. Daarna duurt het enkele dagen tot weken voordat zoekdiensten je pagina's opnemen.

**Zo controleer je het van buitenaf:** typ in Google het woord site, een dubbele punt en je domeinnaam, zonder spaties. Krijg je geen enkel resultaat, dan is dit de eerste plek om te kijken.

## 2. Permalinks: zegt je adres waar de pagina over gaat?

**Waar:** Instellingen, dan Permalinks.

**Wat je zoekt:** welke structuur is gekozen.

Een permalink is het adres van een pagina. WordPress kan dat op verschillende manieren opbouwen. De eenvoudigste vorm is een vraagteken met een nummer erachter. Dat werkt, maar het zegt niets. Een adres waarin de titel van het bericht staat, vertelt een mens en een systeem meteen waar de pagina over gaat.

Vergelijk een adres dat eindigt op een vraagteken, de letter p en het getal 123 met een adres dat eindigt op wat kost een dakkapel. Het tweede is een stukje inhoud. Het eerste is een kastnummer.

**Wat je doet:** kies "Berichtnaam".

**Let op:** doe dit niet zomaar op een website die al jaren bestaat en goed gevonden wordt. Als je de structuur wijzigt, veranderen de adressen van al je berichten. Oude links wijzen dan nergens meer naar. Staat je website al op Berichtnaam, dan hoef je niets te doen. Staat hij op iets anders en heb je veel bestaande berichten, overleg dan eerst met de partij die je website beheert, zodat oude adressen worden doorverwezen.

## 3. Beveiliging: wie houd je buiten?

**Waar:** in je beveiligingsplugin, en soms bij je hostingpartij of bij een dienst die je website sneller en veiliger maakt.

**Wat je zoekt:** instellingen die onbekende, verdachte of geautomatiseerde bezoekers blokkeren.

Een beveiligingsplugin beschermt je website tegen inbraak. Een deel van die bescherming bestaat uit het weren van bezoekers die geen mensen zijn. Daar gaat het mis. Een zoekdienst is ook een bezoeker die geen mens is. En niet elke zoekdienst meldt zich met een naam die de plugin herkent.

Daarnaast hebben sommige diensten een aparte schakelaar gekregen om AI bezoekers te blokkeren. Die staat soms standaard aan. De gedachte is dat je niet wilt dat je teksten zonder toestemming gebruikt worden. Voor een uitgever is dat een begrijpelijke keuze. Voor een bedrijf dat genoemd wil worden, is het de deur dichtdoen voor de klant.

**Wat je doet:**

1. Open de instellingen van je beveiligingsplugin en zoek naar onderdelen met woorden als bots, crawlers of geautomatiseerd verkeer.
2. Kijk of er een lijst is van geblokkeerde bezoekers. Staan daar namen van zoekmachines of AI diensten in?
3. Vraag je hostingpartij of er op hun niveau iets geblokkeerd wordt.
4. Gebruik je een dienst die voor je website staat om hem sneller te maken, kijk dan daar naar een instelling over AI bezoekers.

Weet je het niet zeker, vraag het dan aan wie je website beheert. De vraag is eenvoudig: houden wij zoekmachines of AI diensten buiten, en zo ja welke en waarom?

## 4. Thema en pagebuilder: staat je tekst echt in de pagina?

**Waar:** op je website zelf, niet in het dashboard.

**Wat je zoekt:** tekst die pas zichtbaar wordt na een klik, of die pas later wordt ingeladen.

Thema's en pagebuilders bieden mooie onderdelen: tabbladen, uitklapblokken, schuivende panelen. In de meeste gevallen staat de tekst daarvan gewoon in de pagina en is hij alleen verborgen tot je klikt. Dat is geen probleem. Een systeem leest hem.

Het wordt een probleem als de tekst pas wordt opgehaald op het moment dat iemand klikt, of als de hele pagina pas wordt opgebouwd nadat er een script is uitgevoerd. Veel systemen lezen de pagina zoals hij binnenkomt. Ze klikken niet en ze wachten niet.

**Zo test je het:**

1. Open een pagina met tabbladen of uitklapblokken. Klik niets open.
2. Selecteer alle tekst op de pagina en kopieer hem.
3. Plak hem in een leeg document.

Staat de tekst uit de dichte blokken erbij, dan is het goed. Ontbreekt hij, dan ziet een systeem hem ook niet.

**Wat je doet:** zet belangrijke informatie niet alleen in zo'n blok. Prijzen, werkgebied en wat je doet horen gewoon zichtbaar op de pagina. Hoe je vragen en antwoorden goed opbouwt, lees je in [een veelgestelde vragen pagina die AI kan citeren](#art_veelgestelde_vragen_pagina_die_ai_kan_citeren).

Hetzelfde geldt voor tekst in afbeeldingen. Een banner met je diensten erin is voor een systeem een plaatje zonder inhoud.

## 5. Categorieën en tags: hoeveel lege pagina's heb je?

**Waar:** Berichten, dan Categorieën. En Berichten, dan Tags.

**Wat je zoekt:** hoeveel het er zijn, en hoeveel berichten er in elk zitten.

WordPress maakt voor elke categorie en elke tag automatisch een eigen pagina met de berichten die erbij horen. Dat is handig als een categorie twintig berichten heeft. Het is een probleem als je zestig tags hebt met elk één bericht.

Je hebt dan zestig pagina's waar bijna niets op staat, en die allemaal op elkaar lijken. Een zoekdienst die je website bezoekt, besteedt daar tijd aan die hij beter aan je echte pagina's had kunnen besteden. En het geeft een rommelig beeld van waar je website over gaat.

**Wat je doet:**

- Houd een handvol categorieën aan die overeenkomen met je diensten of onderwerpen.
- Gebruik tags alleen als je er een duidelijk doel mee hebt. Voor de meeste bedrijven is dat niet zo.
- Verwijder tags en categorieën die je niet gebruikt. De berichten zelf blijven staan.

Vijf categorieën met elk tien berichten vertellen een systeem waar je verstand van hebt. Zestig tags met elk één bericht vertellen niets.

## 6. Sitemap: staan je belangrijkste pagina's erin?

**Waar:** in je browser. Typ je domeinnaam met daarachter een schuine streep en wp-sitemap.xml.

**Wat je zoekt:** of het adres werkt, en wat erin staat.

Een sitemap is een overzicht van alle pagina's op je website, bedoeld voor zoekdiensten. WordPress maakt er sinds een paar jaar zelf een. Heb je een plugin voor vindbaarheid, dan neemt die het vaak over en staat het overzicht op een ander adres. Je wordt dan meestal vanzelf doorgestuurd.

**Waar je op let:**

1. **Werkt het adres?** Krijg je een foutmelding, dan is de sitemap uitgeschakeld of geblokkeerd.
2. **Staan je belangrijkste pagina's erin?** Je diensten, je werkgebied, je recente berichten.
3. **Staat er rommel in?** Testpagina's, bedankpagina's, oude concepten die per ongeluk gepubliceerd zijn.

**Wat je doet:** ontbreekt een belangrijke pagina, controleer dan of hij gepubliceerd is en niet op privé of concept staat. Staat er rommel in, verwijder die pagina's of sluit ze uit in je plugin voor vindbaarheid.

Heb je Search Console ingesteld, dan kun je daar het adres van je sitemap opgeven. Google laat dan zien hoeveel pagina's het heeft gevonden en opgenomen.

## Wat je daarna hebt

Als deze zes punten in orde zijn, kan een systeem je website vinden en lezen. Dat is de voorwaarde. Het is nog niet het resultaat.

Of je daarna genoemd wordt, hangt af van wat er te lezen valt. Staat er wat je doet, voor wie en waar? Staan de antwoorden op de vragen van je klanten erop? Dat is het echte werk, en het staat beschreven in [hoe ChatGPT bepaalt welke bedrijven het noemt](#art_hoe_chatgpt_bepaalt_welke_bedrijven_het_noemt).

De volgorde is belangrijk. We zien bedrijven die maanden schrijven op een website waar het vinkje uit punt 1 nog aan stond. Al dat werk was er, en niemand kon het lezen.

## De hele lijst op een rij

1. **Lezen.** Het vinkje bij zoekmachines ontmoedigen staat uit.
2. **Permalinks.** De structuur staat op Berichtnaam.
3. **Beveiliging.** Zoekmachines en AI diensten worden niet geblokkeerd.
4. **Thema.** Belangrijke tekst staat in de pagina, ook zonder klik.
5. **Categorieën.** Een handvol, elk met meerdere berichten.
6. **Sitemap.** Het adres werkt en je belangrijkste pagina's staan erin.

Loop hem na een grote wijziging opnieuw na. Na een nieuw thema, een nieuwe beveiligingsplugin of een verhuizing naar een andere hostingpartij kan er iets zijn teruggezet zonder dat iemand het merkt.

## Veelgestelde vragen

### Heb ik een speciale plugin voor AI nodig?

Nee. Er zijn plugins die beloven je website klaar te maken voor AI. Google zegt zelf dat er voor zijn AI antwoorden geen aparte techniek nodig is. Een website die bereikbaar is, in tekst is opgebouwd en een logische structuur heeft, voldoet.

### Moet ik een apart bestand met instructies voor AI plaatsen?

Dat wordt wel geadviseerd. Google geeft aan dat het voor zijn AI antwoorden niet nodig is, en we hebben geen overtuigend bewijs gezien dat andere grote systemen er iets mee doen. Het kan geen kwaad. Verwacht er niets van. Meer hierover in [wat is GEO en wat is het verschil met SEO](#art_wat_is_geo_en_wat_is_het_verschil_met_seo).

### Mijn website staat goed in Google. Is dit dan nog nodig?

Punt 1, 2 en 6 zijn dan waarschijnlijk in orde. Punt 3 niet per se. Een beveiliging kan Google doorlaten en andere zoekdiensten tegenhouden. Dat verklaart waarom een bedrijf soms wel in Gemini genoemd wordt en niet in Claude. Zie [Claude gebruikt Brave om jouw bedrijf te vinden](#art_claude_gebruikt_brave_om_jouw_bedrijf_te_vinden).

### Ik durf niet aan de instellingen te komen. Wat nu?

Stuur deze lijst naar wie je website beheert en vraag om de zes punten na te lopen. Het is voor iemand die WordPress kent een kwartier werk. Of [loop je website samen met ons door](#meekijken). Dat kost vijftien minuten en is gratis.

### Hoe weet ik of het geholpen heeft?

Test over vier tot zes weken of je genoemd wordt, met de methode uit [wordt mijn bedrijf genoemd in AI](#art_mijn_bedrijf_genoemd_in_ai). Hoe lang het duurt, staat in [hoe lang duurt het voordat AI je bedrijf noemt](#art_hoe_lang_duurt_het_voordat_ai_je_bedrijf_noemt).

## Laat ons meekijken

Kom je er zelf niet uit, of wil je zeker weten dat het goed staat? [Loop je website samen met ons door](#meekijken). Vijftien minuten online, gratis, en je hoeft niets voor te bereiden.

Wil je weten of AI systemen je WordPress website nu kunnen lezen, en wat ze erover zeggen? Met de [gratis nulmeting](#nulmeting) zie je het binnen 48 uur. Wil je daarna dat er elke week content in je WordPress bijkomt zonder dat jij het hoeft te schrijven, lees dan hoe [NXEO met WordPress](#cms_wordpress) werkt.
