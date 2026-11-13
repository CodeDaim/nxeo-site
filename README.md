# nxeo.io

Statische site, gebouwd met één Python script.

- `site/content/<taal>/` de inhoud per pagina en per taal (nl, en)
- `site/i18n/<taal>.json` slugs, titels en meta beschrijvingen
- `site/assets/` stylesheet, script en afbeeldingen
- `site/build.py` bouwt alles naar `site/dist/` (`python3 site/build.py`)
- `site/dist/` de gebouwde site, dit is wat online staat

Nieuwe taal: map `site/content/de/` plus `site/i18n/de.json`, daarna opnieuw bouwen.

Branches: `staging` is de testomgeving, `main` is nxeo.io.
