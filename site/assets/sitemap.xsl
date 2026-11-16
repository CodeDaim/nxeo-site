<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" exclude-result-prefixes="s xhtml">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>

<xsl:template name="group">
  <xsl:param name="lang"/><xsl:param name="kind"/><xsl:param name="title"/>
  <xsl:variable name="rows" select="s:urlset/s:url[contains(s:loc,concat('/',$lang,'/'))][($kind='blog' and contains(s:loc,'/blog/')) or ($kind='cms' and (contains(s:loc,'/werkt-met/') or contains(s:loc,'/works-with/'))) or ($kind='main' and not(contains(s:loc,'/blog/')) and not(contains(s:loc,'/werkt-met/')) and not(contains(s:loc,'/works-with/')))]"/>
  <section>
    <h3><xsl:value-of select="$title"/><span><xsl:value-of select="count($rows)"/></span></h3>
    <div class="rows">
      <xsl:for-each select="$rows">
        <xsl:sort select="s:loc"/>
        <a class="row" href="{s:loc}">
          <b><xsl:value-of select="substring-after(s:loc,'://')"/></b>
          <time><xsl:value-of select="s:lastmod"/></time>
        </a>
      </xsl:for-each>
    </div>
  </section>
</xsl:template>

<xsl:template match="/">
<html lang="nl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="robots" content="noindex"/>
<title>Sitemap | NXEO</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@400;500;600;700&amp;display=swap"/>
<style>
*{box-sizing:border-box}
body{margin:0;background:#F2F3F7;color:#1A2332;font:16px/1.5 "Rethink Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
header{background:linear-gradient(135deg,#002EFE,#4E6BFF);color:#fff;padding:56px 24px 64px;text-align:center}
header .pill{display:inline-block;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:6px 14px;font-size:.88rem;font-weight:600;margin-bottom:18px}
header h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.05;letter-spacing:-.04em;margin:0 0 12px;font-weight:700}
header p{margin:0 auto;max-width:56ch;color:rgba(255,255,255,.9)}
header .stats{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:26px}
header .stats span{background:#fff;color:#002EFE;border-radius:999px;padding:8px 16px;font-weight:600;font-size:.92rem}
main{max-width:1180px;margin:0 auto;padding:40px 24px 80px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}
.col>h2{font-size:1.6rem;letter-spacing:-.03em;margin:0 0 18px}
section{background:#fff;border-radius:24px;padding:22px;box-shadow:0 18px 40px -26px rgba(26,35,50,.35);margin-bottom:20px}
h3{display:flex;align-items:center;gap:10px;margin:0 0 12px;font-size:1.05rem;letter-spacing:-.01em}
h3 span{background:#EEF1FF;color:#002EFE;border-radius:999px;font-size:.78rem;font-weight:700;padding:3px 10px}
.rows{display:grid;gap:2px}
.row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:center;padding:10px 12px;border-radius:12px;color:#1A2332;text-decoration:none}
.row:hover{background:#F2F3F7}
.row b{font-weight:500;font-size:.93rem;overflow-wrap:anywhere}
.row:hover b{color:#002EFE}
.row time{font-size:.8rem;color:#6B7689;white-space:nowrap}
footer{text-align:center;color:#6B7689;font-size:.88rem;padding:0 24px 48px}
footer a{color:#002EFE}
@media (max-width:860px){main{grid-template-columns:minmax(0,1fr)}.row time{display:none}}
</style>
</head>
<body>
<header>
  <div class="pill">Sitemap</div>
  <h1>Alle pagina's van NXEO</h1>
  <p>Dit overzicht is bedoeld voor zoekmachines. Het wordt bij elke publicatie opnieuw gemaakt.</p>
  <div class="stats">
    <span><xsl:value-of select="count(s:urlset/s:url)"/> pagina's</span>
    <span><xsl:value-of select="count(s:urlset/s:url[contains(s:loc,'/nl/')])"/> Nederlands</span>
    <span><xsl:value-of select="count(s:urlset/s:url[contains(s:loc,'/en/')])"/> English</span>
  </div>
</header>
<main>
  <div class="col">
    <h2>Nederlands</h2>
    <xsl:call-template name="group"><xsl:with-param name="lang" select="'nl'"/><xsl:with-param name="kind" select="'main'"/><xsl:with-param name="title" select="&quot;Pagina's&quot;"/></xsl:call-template>
    <xsl:call-template name="group"><xsl:with-param name="lang" select="'nl'"/><xsl:with-param name="kind" select="'cms'"/><xsl:with-param name="title" select="'Werkt met'"/></xsl:call-template>
    <xsl:call-template name="group"><xsl:with-param name="lang" select="'nl'"/><xsl:with-param name="kind" select="'blog'"/><xsl:with-param name="title" select="'Blog'"/></xsl:call-template>
  </div>
  <div class="col">
    <h2>English</h2>
    <xsl:call-template name="group"><xsl:with-param name="lang" select="'en'"/><xsl:with-param name="kind" select="'main'"/><xsl:with-param name="title" select="'Pages'"/></xsl:call-template>
    <xsl:call-template name="group"><xsl:with-param name="lang" select="'en'"/><xsl:with-param name="kind" select="'cms'"/><xsl:with-param name="title" select="'Works with'"/></xsl:call-template>
    <xsl:call-template name="group"><xsl:with-param name="lang" select="'en'"/><xsl:with-param name="kind" select="'blog'"/><xsl:with-param name="title" select="'Blog'"/></xsl:call-template>
  </div>
</main>
<footer>Terug naar <a href="/">de website</a></footer>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
