# NEXUS Lending Partners website: deployment notes

Static website, 219 pages, no build step needed to host. Upload the contents of this folder to any static host.

## Host it (pick one)
- **Cloudflare Pages / Netlify / Vercel:** drag and drop this folder, then connect the domain `nexuslendingpartners.com`. `_redirects` serves the custom 404.
- **GitHub Pages:** push the folder, enable Pages. `CNAME` is already set.
- **Any cPanel host:** upload everything into `public_html`.

## Before you go live (important)
1. **Fill in legal details** in `build/config.py`: `LEGAL_ENTITY`, `CIN_OR_REG`, `GRIEVANCE_OFFICER`. Then run `python3 build/build.py` to regenerate. The footer and grievance page show them automatically.
2. **Name a grievance officer.** RBI norms expect lending service providers to publish one.
3. **Have a lawyer review** Privacy Policy, Terms, Disclaimer and Digital Lending Disclosures. They are templates.
4. **Lender logos and partner names:** none are shown, on purpose. Add a logo only with the lender's written permission.
5. **Add real trust proof as you earn it:** genuine customer reviews, registration numbers, awards. Do not add invented reviews or numbers.
6. **WhatsApp:** all forms open `wa.me/916300695591`. For a bot, automation and multiple agents, move this number to the WhatsApp Business API (Gupshup, Interakt, WATI, Twilio).
7. **Google:** submit `https://nexuslendingpartners.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools, create a Google Business Profile for the Kukatpally office, and add analytics if you want traffic data.
8. **Gold calculator:** the gold rate field is a placeholder. Customers type today's rate.

## Structure
- `/` home, `/loans/` hub, `/loans/<family>/` (15 families), `/loans/<family>/<type>/` (150+ pages)
- `/tools/` (10 calculators and checkers), `/guides/` (20 guides), `/loans-in/<city>/` (19 location pages)
- `/faq/`, `/glossary/`, `/documents-required/`, `/apply/`, `/contact/`, `/about/`, company and legal pages
- `sitemap.xml`, `robots.txt`, structured data (Organization, Service, FAQPage, BreadcrumbList, Article, HowTo, WebApplication)

## Editing content
Content lives in `build/data_*.py` and `build/config.py`. Edit, then run `python3 build/build.py`.
