---
title: WordPress checklist: can AI read your website?
description: Six settings in WordPress decide whether ChatGPT, Gemini and Claude can read your website. This checklist takes you through them in ten minutes, with where to click for each point.
date: 2026-11-13
category: In practice
keyword: WordPress website readable for AI
ref: wordpress-controlelijst-vindbaar-voor-ai
kort: One tick box under Settings and Reading can make your whole website invisible. It is switched on more often than you think. | Security that keeps out unknown visitors also shuts out the search services behind AI. | You do not need a plugin or technical knowledge. Only ten minutes and access to your dashboard.
---

A large share of the websites of small and medium sized companies runs on WordPress. That is fine. Out of the box, WordPress produces pages that are easy to read, for people and for systems.

Still, on WordPress websites we keep seeing the same six things go wrong. None of the six has anything to do with the content. They are settings. Someone switched them on at some point, often for a good reason, and then forgot about them. The result is that an AI system cannot find your website or cannot read it, however good your texts are.

This checklist goes through them. You need access to your WordPress dashboard and about ten minutes. If you want to make your WordPress website readable for AI, this is the place to start. Writing only makes sense once what you write can be read.

## Why this comes first

An AI system that answers a question looks up pages through a search service and reads them. Gemini does that through Google. Claude through Brave. ChatGPT uses a mix. If one of those search services does not know your page or is not allowed to read it, you do not exist for that system.

The causes we find most often when a company is not mentioned anywhere are in [why am I not in AI recommendations](#art_waarom_sta_ik_niet_in_de_aanbevelingen_van_ai). The technical cause is one of the seven there. With WordPress it can in most cases be traced back to one of the six points below.

## 1. Reading: are you asking search engines to stay away?

**Where:** Settings, then Reading. At the bottom you will find "Search engine visibility".

**What you are looking for:** a tick next to "Discourage search engines from indexing this site".

This is the best known pitfall in WordPress, and it still occurs. While a website is being built, the builder switches this on so that the half finished website does not appear in Google. That is sensible. At delivery it has to be switched off again. Sometimes that does not happen.

If the box is ticked, your website asks every search engine to skip it. Most comply. You can write every week for a year without a single page being indexed.

**What to do:** remove the tick and save. After that it takes a few days to a few weeks before search services index your pages.

**How to check it from the outside:** type into Google the word site, a colon and your domain name, without spaces. If you get no results at all, this is the first place to look.

## 2. Permalinks: does your address say what the page is about?

**Where:** Settings, then Permalinks.

**What you are looking for:** which structure has been chosen.

A permalink is the address of a page. WordPress can build it in different ways. The plainest form is a question mark followed by a number. That works, but it says nothing. An address containing the title of the post tells a person and a system straight away what the page is about.

Compare an address that ends in a question mark, the letter p and the number 123 with an address that ends in what does a dormer cost. The second is a piece of content. The first is a locker number.

**What to do:** choose "Post name".

**Take care:** do not simply do this on a website that has existed for years and is found well. If you change the structure, the addresses of all your posts change. Old links then point nowhere. If your website is already set to Post name, you do not need to do anything. If it is set to something else and you have many existing posts, first consult the party that manages your website, so that old addresses are redirected.

## 3. Security: whom are you keeping out?

**Where:** in your security plugin, and sometimes with your hosting company or with a service that makes your website faster and safer.

**What you are looking for:** settings that block unknown, suspicious or automated visitors.

A security plugin protects your website against break ins. Part of that protection consists of keeping out visitors that are not people. That is where it goes wrong. A search service is also a visitor that is not a person. And not every search service announces itself with a name the plugin recognises.

In addition, some services have been given a separate switch to block AI visitors. It is sometimes on by default. The thinking is that you do not want your texts used without permission. For a publisher that is an understandable choice. For a company that wants to be mentioned, it is closing the door on the customer.

**What to do:**

1. Open the settings of your security plugin and look for sections with words like bots, crawlers or automated traffic.
2. See whether there is a list of blocked visitors. Are there names of search engines or AI services in it?
3. Ask your hosting company whether anything is blocked at their level.
4. If you use a service that sits in front of your website to make it faster, look there for a setting about AI visitors.

If you are not sure, ask whoever manages your website. The question is simple: are we keeping search engines or AI services out, and if so which ones and why?

## 4. Theme and page builder: is your text really in the page?

**Where:** on your website itself, not in the dashboard.

**What you are looking for:** text that only becomes visible after a click, or that is only loaded later.

Themes and page builders offer handsome components: tabs, collapsible blocks, sliding panels. In most cases their text is simply in the page and is only hidden until you click. That is not a problem. A system reads it.

It becomes a problem when the text is only fetched at the moment someone clicks, or when the whole page is only built after a script has run. Many systems read the page as it arrives. They do not click and they do not wait.

**How to test it:**

1. Open a page with tabs or collapsible blocks. Click nothing open.
2. Select all the text on the page and copy it.
3. Paste it into an empty document.

If the text from the closed blocks is there, it is fine. If it is missing, a system does not see it either.

**What to do:** do not put important information only in such a block. Prices, service area and what you do belong visibly on the page. How to build questions and answers properly is covered in [an FAQ page AI can quote](#art_veelgestelde_vragen_pagina_die_ai_kan_citeren).

The same goes for text in images. A banner with your services in it is a picture without content to a system.

## 5. Categories and tags: how many empty pages do you have?

**Where:** Posts, then Categories. And Posts, then Tags.

**What you are looking for:** how many there are, and how many posts are in each.

WordPress automatically creates a page of its own for every category and every tag, listing the posts that belong to it. That is handy when a category has twenty posts. It is a problem when you have sixty tags with one post each.

You then have sixty pages with almost nothing on them, all resembling each other. A search service that visits your website spends time on them that it could better have spent on your real pages. And it gives a messy picture of what your website is about.

**What to do:**

- Keep a handful of categories that match your services or topics.
- Only use tags if you have a clear purpose for them. For most companies that is not the case.
- Delete tags and categories you do not use. The posts themselves stay.

Five categories with ten posts each tell a system what you know about. Sixty tags with one post each tell it nothing.

## 6. Sitemap: are your most important pages in it?

**Where:** in your browser. Type your domain name followed by a forward slash and wp-sitemap.xml.

**What you are looking for:** whether the address works, and what is in it.

A sitemap is an overview of all the pages on your website, meant for search services. WordPress has created one by itself for a few years now. If you have a plugin for findability, it often takes over and the overview is at a different address. You are then usually redirected automatically.

**What to watch for:**

1. **Does the address work?** If you get an error, the sitemap is switched off or blocked.
2. **Are your most important pages in it?** Your services, your service area, your recent posts.
3. **Is there clutter in it?** Test pages, thank you pages, old drafts that were published by accident.

**What to do:** if an important page is missing, check whether it is published and not set to private or draft. If there is clutter, delete those pages or exclude them in your findability plugin.

If you have set up Search Console, you can enter the address of your sitemap there. Google then shows how many pages it has found and indexed.

## What you have after that

When these six points are in order, a system can find and read your website. That is the condition. It is not yet the result.

Whether you are then mentioned depends on what there is to read. Does it say what you do, for whom and where? Are the answers to your customers' questions on it? That is the real work, and it is described in [how ChatGPT decides which companies to mention](#art_hoe_chatgpt_bepaalt_welke_bedrijven_het_noemt).

The order matters. We see companies that write for months on a website where the tick box from point 1 was still on. All that work was there, and nobody could read it.

## The whole list in a row

1. **Reading.** The box for discouraging search engines is not ticked.
2. **Permalinks.** The structure is set to Post name.
3. **Security.** Search engines and AI services are not blocked.
4. **Theme.** Important text is in the page, even without a click.
5. **Categories.** A handful, each with several posts.
6. **Sitemap.** The address works and your most important pages are in it.

Go through it again after a major change. After a new theme, a new security plugin or a move to another hosting company, something may have been reset without anyone noticing.

## Frequently asked questions

### Do I need a special plugin for AI?

No. There are plugins that promise to make your website ready for AI. Google itself says no separate technology is needed for its AI answers. A website that is reachable, built in text and logically structured is enough.

### Should I add a separate file with instructions for AI?

That is sometimes advised. Google indicates that it is not needed for its AI answers, and we have not seen convincing evidence that other large systems do anything with it. It does no harm. Expect nothing from it. More on this in [what is GEO and how does it differ from SEO](#art_wat_is_geo_en_wat_is_het_verschil_met_seo).

### My website ranks well in Google. Is this still needed?

Points 1, 2 and 6 are then probably in order. Point 3 not necessarily. Security can let Google through and stop other search services. That explains why a company is sometimes mentioned in Gemini and not in Claude. See [Claude uses Brave to find your company](#art_claude_gebruikt_brave_om_jouw_bedrijf_te_vinden).

### I do not dare touch the settings. What now?

Send this list to whoever manages your website and ask them to go through the six points. For someone who knows WordPress it is a quarter of an hour of work. Or [go through your website together with us](#meekijken). It takes fifteen minutes and it is free.

### How do I know whether it helped?

Test in four to six weeks whether you are mentioned, with the method from [is my company mentioned in AI](#art_mijn_bedrijf_genoemd_in_ai). How long it takes is covered in [how long until AI mentions your company](#art_hoe_lang_duurt_het_voordat_ai_je_bedrijf_noemt).

## Let us take a look

Cannot work it out yourself, or want to be sure it is set up properly? [Go through your website together with us](#meekijken). Fifteen minutes online, free, and there is nothing to prepare.

Would you like to know whether AI systems can read your WordPress website now, and what they say about it? With the [free baseline check](#nulmeting) you see it within 48 hours. If you would then like content added to your WordPress every week without having to write it yourself, read how [NXEO with WordPress](#cms_wordpress) works.
