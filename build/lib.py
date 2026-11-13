import os, html, json, re
from PIL import Image
from config import *
from data_loans_a import CATS_A
from data_loans_b import CATS_B

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = CATS_A + CATS_B
CAT = {c["slug"]: c for c in CATS}
esc = html.escape
PAGES = []   # (path, priority)

LOGO_W, LOGO_H = Image.open(f"{OUT}/assets/logo-lockup-transparent.png").size

ICONS = {
 "user":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
 "home":'<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
 "building":'<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
 "coins":'<circle cx="9" cy="9" r="6"/><path d="M15 6.3A6 6 0 0 1 15 17.7M9 6v6M7 9h4"/>',
 "chart":'<path d="M3 20h18"/><path d="M6 16l4-5 3 3 5-7"/><path d="M16 7h2v2"/>',
 "car":'<path d="M4 15l1.6-5.2A2 2 0 0 1 7.5 8.4h9a2 2 0 0 1 1.9 1.4L20 15"/><rect x="3" y="15" width="18" height="4" rx="1.5"/><circle cx="7.5" cy="17" r=".6"/><circle cx="16.5" cy="17" r=".6"/>',
 "cap":'<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.4 2.7 3 6 3s6-1.6 6-3v-4.5"/>',
 "briefcase":'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2M3 13h18"/>',
 "cycle":'<path d="M20 12a8 8 0 0 0-14-5.3L4 9"/><path d="M4 4v5h5"/><path d="M4 12a8 8 0 0 0 14 5.3L20 15"/><path d="M20 20v-5h-5"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 "leaf":'<path d="M5 19C5 10 10 5 20 4c0 10-5 15-14 15z"/><path d="M5 19l8-8"/>',
 "flag":'<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
 "bolt":'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "tower":'<path d="M4 21V9l8-6 8 6v12"/><path d="M9 21v-6h6v6M8 11h2M14 11h2"/>',
 "merge":'<path d="M5 4v6c0 3 3 4 7 6M19 4v6c0 3-3 4-7 6M12 16v5"/><path d="M9 19l3 3 3-3"/>',
 "star":'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 "check":'<path d="M5 12l4 4 10-10"/>',
 "shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "eye":'<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "link":'<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3A4 4 0 0 0 11 18.7l1-1"/>',
 "heart":'<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/>',
 "calc":'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M12 12h2M16 12h0M8 16h2M12 16h2M16 16h0"/>',
 "doc":'<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "compare":'<path d="M8 4v16M16 4v16M4 8l4-4 4 4M12 16l4 4 4-4"/>',
 "quiz":'<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 .9-1 1.7M12 17h0"/>',
}

def icon(key, cls="ic"):
    return f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS.get(key, ICONS["star"])}</svg></span>'

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.8 2 6.8L3 29l6.6-1.9c1.9 1 4 1.6 6.3 1.6 7.2 0 13-5.7 13-12.8C29 8.7 23.2 3 16 3zm0 23.2c-2 0-3.9-.6-5.5-1.6l-.4-.2-3.9 1.1 1.1-3.8-.3-.4a10.3 10.3 0 0 1-1.6-5.5C5.4 10.1 10.1 5.5 16 5.5s10.6 4.6 10.6 10.3S21.9 26.2 16 26.2zm5.8-7.7c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.3.3-.5.1-.2.1-.4 0-.5l-1-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1.1 1.1-1.1 2.6s1.1 3 1.3 3.2c.2.2 2.2 3.4 5.4 4.7 3.2 1.3 3.2.9 3.7.8.6-.1 1.9-.8 2.1-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'

def wa_url(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"

def ok_icon():
    return f'<svg viewBox="0 0 24 24">{ICONS["check"]}</svg>'

def trunc(s, n):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:.") + "…"

def first_sentence(s):
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return m.group(1) if m else s

# ---------------------------------------------------------------- shared chrome
def nav_html():
    loans = "".join(f'<a href="/loans/{c["slug"]}/">{esc(c["name"])}</a>' for c in CATS)
    tools = "".join(f'<a href="/tools/{s}/">{esc(n)}</a>' for s, n in TOOLS)
    about = "".join(f'<a href="{u}">{esc(n)}</a>' for u, n in [("/about/","About NEXUS"),("/why-nexus/","Why NEXUS"),("/how-it-works/","How it works"),("/lending-partners/","Lending partners"),("/partner-with-us/","Partner with us"),("/faq/","FAQs"),("/glossary/","Loan glossary")])
    return f'''<nav class="main" id="nav" aria-label="Main">
<div class="dd mega"><button type="button" aria-haspopup="true">Loans ▾</button><div class="panel"><a class="all" href="/loans/">All loan types</a>{loans}</div></div>
<div class="dd"><button type="button" aria-haspopup="true">Tools ▾</button><div class="panel"><a class="all" href="/tools/">All tools</a>{tools}</div></div>
<a href="/guides/">Guides</a>
<a href="/loans-in/">Locations</a>
<div class="dd"><button type="button" aria-haspopup="true">Company ▾</button><div class="panel">{about}</div></div>
<a href="/contact/">Contact</a>
<a class="btn btn-wa btn-sm" href="/apply/">{WA_SVG} Apply on WhatsApp</a>
</nav>'''

TOOLS = [
 ("emi-calculator","EMI Calculator"),
 ("home-loan-emi-calculator","Home Loan EMI Calculator"),
 ("loan-eligibility-calculator","Loan Eligibility Calculator"),
 ("balance-transfer-calculator","Balance Transfer Calculator"),
 ("prepayment-calculator","Prepayment Calculator"),
 ("gold-loan-calculator","Gold Loan Calculator"),
 ("compare-loans","Loan Offer Comparison"),
 ("loan-finder","Which Loan Is Right for Me?"),
 ("document-checklist","Document Checklist"),
 ("credit-health-check","Credit Health Self-Check"),
]

def header_html():
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap"><div class="tl"><span>📍 {esc(ADDRESS_LINE)}</span></div><div class="tr tl"><a href="tel:{PHONE_TEL}">📞 {PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">✉ {EMAIL}</a></div></div></div>
<header class="site"><div class="wrap">
<a class="logo" href="/" aria-label="{BRAND} home"><img src="/assets/logo-lockup-transparent.png" width="{LOGO_W}" height="{LOGO_H}" alt="{BRAND} logo"></a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
{nav_html()}
</div></header>'''

DISCLOSURE = [
 "<strong>Important:</strong> NEXUS Lending Partners is a loan facilitation and advisory service. We are not a bank or NBFC, and we do not lend, disburse or collect loan money. Loans are offered and sanctioned only by partner banks and RBI-regulated lenders, who decide approval, interest rate and terms under their own credit policies.",
 "Interest rates, fees, amounts and tenures shown on this website are indicative and can change. Always refer to the lender's Key Fact Statement for the APR and every charge. We do not guarantee approval, loan amount, rate or timelines. Assistance from NEXUS is free for borrowers; lenders may pay NEXUS a commission when a loan is disbursed.",
 "NEXUS will never ask you for an advance fee, OTP, PIN, CVV or password. If someone does so in our name, report it to us at " + EMAIL + ". Report cyber fraud at cybercrime.gov.in or call 1930. Report unauthorised digital lending apps at sachet.rbi.org.in.",
]

def footer_html():
    loans = "".join(f'<li><a href="/loans/{c["slug"]}/">{esc(c["name"])}</a></li>' for c in CATS[:8])
    loans2 = "".join(f'<li><a href="/loans/{c["slug"]}/">{esc(c["name"])}</a></li>' for c in CATS[8:])
    tools = "".join(f'<li><a href="/tools/{s}/">{esc(n)}</a></li>' for s, n in TOOLS[:6])
    legal_ids = ""
    if LEGAL_ENTITY: legal_ids += f"<p>{esc(LEGAL_ENTITY)}" + (f" | Reg. no.: {esc(CIN_OR_REG)}" if CIN_OR_REG else "") + "</p>"
    grv = f"Grievance officer: {esc(GRIEVANCE_OFFICER)}, " if GRIEVANCE_OFFICER else "Grievance contact: "
    return f'''<footer class="site"><div class="wrap">
<div class="fgrid">
<div class="fbrand"><img src="/assets/logo-lockup.png" alt="{BRAND}" width="{LOGO_W//4}" height="{LOGO_H//4}" loading="lazy">
<p><strong>{BRAND}</strong><br>{esc(TAGLINE)}</p>
<p>{esc(ADDRESS_LINE)}</p>
<p>📞 <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br>✉ <a href="mailto:{EMAIL}">{EMAIL}</a><br>🕘 {HOURS}</p>
<p><a href="{INSTAGRAM}" rel="noopener me" target="_blank">Instagram @nexuslpofficial</a></p></div>
<div><h4>Loans</h4><ul>{loans}</ul></div>
<div><h4>More loans</h4><ul>{loans2}<li><a href="/loans/"><strong>All loan types →</strong></a></li></ul></div>
<div><h4>Tools &amp; guides</h4><ul>{tools}<li><a href="/tools/">All tools</a></li><li><a href="/guides/">Loan guides</a></li><li><a href="/documents-required/">Documents required</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About NEXUS</a></li><li><a href="/why-nexus/">Why NEXUS</a></li><li><a href="/how-it-works/">How it works</a></li><li><a href="/lending-partners/">Lending partners</a></li><li><a href="/partner-with-us/">Partner with us</a></li><li><a href="/loans-in/">Locations</a></li><li><a href="/faq/">FAQs</a></li><li><a href="/contact/">Contact</a></li><li><a href="/grievance-redressal/">Grievance redressal</a></li><li><a href="/consent-withdrawal/">Consent withdrawal</a></li><li><a href="/digital-lending-disclosures/">Digital lending disclosures</a></li><li><a href="https://sachet.rbi.org.in" rel="noopener" target="_blank">RBI Sachet portal</a></li></ul></div>
</div>
<div class="disclosure">{legal_ids}{"".join(f"<p>{p}</p>" for p in DISCLOSURE)}<p>{grv}<a href="mailto:{EMAIL}">{EMAIL}</a>. See our <a href="/grievance-redressal/">grievance redressal process</a>.</p></div>
<div class="copy"><span>© {YEAR} {BRAND}. All rights reserved.</span><span><a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-use/">Terms of Use</a> · <a href="/disclaimer/">Disclaimer</a> · <a href="/sitemap/">Sitemap</a></span></div>
</div></footer>
<a class="fab" href="{wa_url("Hello NEXUS Lending Partners, I need help with a loan.")}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{WA_SVG}<span>Chat on WhatsApp</span></a>
<div class="mbar"><a href="tel:{PHONE_TEL}">📞 Call</a><a class="w" href="{wa_url("Hello NEXUS Lending Partners, I need help with a loan.")}" target="_blank" rel="noopener">WhatsApp</a><a href="/apply/">Apply</a></div>'''

def crumbs_html(items):
    parts = ['<a href="/">Home</a>'] + [f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in items]
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">' + '<span>›</span>'.join(parts) + '</nav>'

def crumbs_ld(items):
    el = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
    for i, (n, u) in enumerate(items, 2):
        d = {"@type": "ListItem", "position": i, "name": n}
        if u: d["item"] = BASE + u
        el.append(d)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs, open_first=False):
    out = []
    for i, (q, a) in enumerate(faqs):
        out.append(f'<details class="faq"{" open" if open_first and i==0 else ""}><summary>{esc(q)}</summary><div class="ans">{esc(a)}</div></details>')
    return "\n".join(out)

ORG_ID = BASE + "/#org"
def org_ld():
    return {"@context": "https://schema.org", "@type": ["FinancialService", "LocalBusiness"], "@id": ORG_ID,
            "name": BRAND, "alternateName": "NEXUS Lending Partner", "url": BASE + "/",
            "logo": BASE + "/assets/logo-full-900.png", "image": BASE + "/assets/og-image.png",
            "description": "Loan facilitation and advisory service helping borrowers compare, prepare and apply for personal, home, business, gold, vehicle, education and other loans through regulated partner lenders.",
            "slogan": TAGLINE, "telephone": PHONE_TEL, "email": EMAIL,
            "address": {"@type": "PostalAddress", "streetAddress": ADDR["street"], "addressLocality": ADDR["city"],
                        "addressRegion": ADDR["region"], "postalCode": ADDR["postal"], "addressCountry": "IN"},
            "areaServed": {"@type": "Country", "name": "India"},
            "sameAs": [INSTAGRAM],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "09:30", "closes": "19:00"}],
            "priceRange": "Free for borrowers"}

def render(path, title, desc, body, schemas=None, crumbs=None, body_attr="", priority="0.7", noindex=False, og_image="/assets/og-image.png", scripts=""):
    canon = BASE + path
    ld = list(schemas or [])
    if crumbs is not None: ld.append(crumbs_ld(crumbs))
    ldtxt = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    htmltxt = f'''<!doctype html>
<html lang="en-IN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#07355F">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}{og_image}"><meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png"><link rel="apple-touch-icon" href="/assets/icon-180.png">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/style.css">
{ldtxt}
</head>
<body{(" " + body_attr) if body_attr else ""}>
{header_html()}
<main id="main">
{body}
</main>
{footer_html()}
<script>window.NEXUS={{wa:"{WA_NUMBER}"}};</script>
{scripts}
<script src="/assets/app.js" defer></script>
</body></html>'''
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    if path.endswith(".html"): fp = os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f: f.write(htmltxt)
    if not noindex: PAGES.append((path, priority))

# ---------------------------------------------------------------- reusable blocks
def loan_options(pre=None, by="name"):
    o = ['<option value="">Select loan type</option>']
    for c in CATS:
        sel = " selected" if pre and (pre == c["slug"] or pre == c["name"]) else ""
        o.append(f'<option value="{esc(c["name"])}" data-slug="{c["slug"]}"{sel}>{esc(c["name"])}</option>')
    return "".join(o)

def lead_form(pre=None, title="Get a callback on WhatsApp", sub="Tell us what you need. We continue the chat on WhatsApp and never ask for OTPs or ID numbers.", cta="Continue on WhatsApp", extra_id="", full=False):
    import zlib
    uid = extra_id or "f" + str(zlib.crc32(f"{pre}{title}".encode()) % 10000)
    inc = ""
    if full:
        inc = f'''<div class="row2"><div class="f"><label for="{uid}-inc">Monthly income (₹)</label><input id="{uid}-inc" name="income" inputmode="numeric" placeholder="e.g. 60000"></div>
<div class="f"><label for="{uid}-emp">Employment</label><select id="{uid}-emp" name="employment"><option value="">Select</option><option>Salaried</option><option>Self-employed professional</option><option>Business owner</option><option>Farmer</option><option>Student</option><option>Retired / pensioner</option><option>Other</option></select></div></div>'''
    return f'''<form class="lead card raise" data-lead novalidate>
<h3>{esc(title)}</h3><p class="fine">{esc(sub)}</p>
<div class="f"><label for="{uid}-loan">Loan type</label><select id="{uid}-loan" name="loan" required>{loan_options(pre)}</select></div>
<div class="row2"><div class="f"><label for="{uid}-amt">Amount needed (₹)</label><input id="{uid}-amt" name="amount" inputmode="numeric" placeholder="e.g. 500000"></div>
<div class="f"><label for="{uid}-city">City</label><input id="{uid}-city" name="city" placeholder="e.g. Hyderabad"></div></div>
{inc}
<div class="row2"><div class="f"><label for="{uid}-name">Your name</label><input id="{uid}-name" name="name" autocomplete="name"></div>
<div class="f"><label for="{uid}-ph">Mobile number</label><input id="{uid}-ph" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="10-digit number"></div></div>
<label class="consent"><input type="checkbox" name="consent"> <span>I agree that NEXUS Lending Partners may contact me on WhatsApp or phone about my request and share my details with partner lenders to process it. I have read the <a href="/privacy-policy/">Privacy Policy</a>.</span></label>
<div class="err" role="alert"></div>
<button class="btn btn-wa" type="submit">{WA_SVG} {esc(cta)}</button>
<p class="fine sent" style="display:none">WhatsApp should have opened with your message. Press Send there to reach us.</p>
</form>'''

def cta_band(title="Not sure which loan fits? Talk to us.", text="Send us your requirement on WhatsApp. We will suggest the right loan type, give you a document checklist and connect you with suitable regulated lenders. No advance fees, ever."):
    return f'''<section class="sec dark"><div class="wrap" style="text-align:center;max-width:820px"><h2>{esc(title)}</h2><p>{esc(text)}</p>
<div class="cta-row" style="justify-content:center"><a class="btn btn-wa" href="{wa_url("Hello NEXUS Lending Partners, I need help choosing a loan.")}" target="_blank" rel="noopener">{WA_SVG} Chat on WhatsApp</a><a class="btn btn-teal" href="/apply/">Fill the quick form</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div></div></section>'''

def note_box():
    return '<div class="note"><strong>Please note:</strong> Rates, amounts and terms on this page are indicative and vary by lender and your profile. NEXUS is a loan facilitator, not a lender. Approval and pricing are decided by the lender. Check the Key Fact Statement for the APR and all charges.</div>'

def ul(items): return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"

def write_raw(path, text):
    fp = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(text)
