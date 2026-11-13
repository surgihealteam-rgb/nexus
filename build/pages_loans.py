from lib import *
from data_misc import CITIES, GENERAL_FAQS
from data_guides import GUIDES
import zlib

STEP4 = {
 "home-loan":"The lender completes KYC and income checks, then runs a legal title verification and a technical valuation of the property. Builder or society documents are reviewed.",
 "loan-against-property":"The lender completes KYC and income checks, then runs legal title verification and a technical valuation of the property before fixing the loan amount.",
 "gold-loan":"You visit the lender's branch for gold appraisal. Weight, purity and valuation are shown to you. KYC is completed at the branch or digitally.",
 "loan-against-securities":"You pledge eligible securities through your depository participant. The lender marks a lien on the holdings and sets your limit.",
 "vehicle-loan":"You choose the vehicle and take the dealer quotation. The lender verifies KYC and income and, for used vehicles, the valuation. Hypothecation is recorded on the RC.",
 "education-loan":"You submit the admission letter, fee structure and co-applicant details. For larger loans, collateral documents are verified as well.",
 "business-loan":"You share GST, ITR, bank statements and financials. The lender may visit the premises and verify the business.",
 "working-capital-and-invoice-finance":"You share GST, ITR, bank statements, stock and debtor statements. The lender may inspect stock and verify receivables.",
 "trade-and-export-finance":"You submit trade documents such as the order, invoice, shipping papers or LC. The bank checks compliance with trade and foreign exchange rules.",
 "agriculture-loan":"You submit land records and activity details. The bank may inspect the farm or project and verify local revenue records.",
 "government-scheme-loans":"You apply through the participating bank or official portal with category and project documents. Scheme eligibility is verified by the lender.",
 "corporate-and-project-finance":"An advisor reviews your information memorandum and approaches suitable lenders. Due diligence and term-sheet negotiation follow.",
}

def steps_for(c):
    s4 = STEP4.get(c["slug"], "You apply on the lender's secure platform or at a branch. KYC, income and, where relevant, other verification happen here.")
    return [
     ("Tell us what you need","Share the amount, purpose and basic details on WhatsApp or the form. We do not ask for ID numbers or OTPs at this stage."),
     ("We check fit and options","We compare your profile with the typical criteria of partner lenders and suggest the loan type and lenders that suit you. The final eligibility decision is the lender's."),
     ("Prepare your documents","You get a precise checklist for your loan type, so you apply once with everything matching."),
     ("Apply and verify with the lender", s4),
     ("Sanction and Key Fact Statement","You receive the sanction letter and the Key Fact Statement showing APR, EMI, fees and cooling-off terms. Read them fully before accepting."),
     ("Disbursal and after-care","The lender releases funds directly to your bank account. We stay available for questions about repayment, prepayment and your next need."),
    ]

def steps_html(steps):
    return '<ol class="stepv">' + "".join(f"<li><div><strong>{esc(t)}</strong><span>{esc(d)}</span></div></li>" for t, d in steps) + "</ol>"

def facts_html(c):
    items = [("Typical amount", c["amount"]), ("Tenure", c["tenure"]), ("Indicative rate", c["rate"]), ("Security", c["security"])]
    return '<div class="facts">' + "".join(f'<div class="fact"><b>{k}</b><span>{esc(v)}</span></div>' for k, v in items) + "</div>"

def pick(lst, key, n):
    start = zlib.crc32(key.encode()) % len(lst)
    return [lst[(start + i) % len(lst)] for i in range(min(n, len(lst)))]

def related_cards(slugs):
    out = []
    for s in slugs:
        c = CAT.get(s)
        if not c: continue
        out.append(f'<a class="card prod" href="/loans/{s}/">{icon(c["icon"])}<h3>{esc(c["name"])}</h3><p>{esc(c["tag"])}</p><span class="more">Learn more →</span></a>')
    return '<div class="grid-3">' + "".join(out) + "</div>"

# ================================================================ category page
def build_category(c):
    path = f"/loans/{c['slug']}/"
    faqs = c["faqs"]
    subs = c["subs"]
    sub_cards = "".join(f'<a class="card prod" href="/loans/{c["slug"]}/{s["slug"]}/"><h3>{esc(s["name"])}</h3><p>{esc(trunc(s["desc"], 120))}</p><span class="more">View details →</span></a>' for s in subs)
    toc = [("overview","Overview"),("facts","Key facts"),("who","Who it is for"),("features","Features"),("eligibility","Eligibility"),("documents","Documents"),("process","How to apply"),("fees","Fees & charges"),("tips","Smart tips"),("types","Types of "+c["name"].lower()),("faq","FAQs")]
    tocs = "".join(f'<a href="#{i}">{esc(n)}</a>' for i, n in toc)
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Loans","/loans/"),(c["name"],None)]).replace('class="crumbs wrap"','class="crumbs"')}
<div class="grid"><div><span class="kicker">{esc(c["security"])}</span><h1>{esc(c["name"])} in India</h1><p class="lead">{esc(c["tag"])}</p>
<div class="cta-row"><a class="btn btn-wa" href="{wa_url("Hello NEXUS, I need a "+c["name"]+".")}" target="_blank" rel="noopener">{WA_SVG} Ask on WhatsApp</a><a class="btn btn-ghost" href="/apply/?loan={c["slug"]}">Start application</a></div></div>
<div>{lead_form(c["name"], title="Apply for a "+c["name"], extra_id="h")}</div></div></div></div>
<div class="wrap layout"><article class="article">
<h2 id="overview">What is a {esc(c["name"].lower())}?</h2>{"".join(f"<p>{esc(p)}</p>" for p in c["intro"])}
<h2 id="facts">{esc(c["name"])}: key facts at a glance</h2>{facts_html(c)}{note_box()}
<h2 id="who">Who can apply</h2>{ul(c["who"])}
<h2 id="features">Features and benefits</h2>{ul(c["features"])}
<h2 id="eligibility">Eligibility criteria</h2><p>Each lender sets its own rules. These are typical conditions:</p>{ul(c["elig"])}
<h2 id="documents">Documents required</h2><p>Keep these ready to avoid delays. Your lender may ask for more depending on your profile. Use our <a href="/tools/document-checklist/">document checklist tool</a> for a printable list.</p>{ul(c["docs"])}
<h2 id="process">How to apply for a {esc(c["name"].lower())} with NEXUS</h2>{steps_html(steps_for(c))}
<h2 id="fees">Fees and charges to look out for</h2>{ul(c["fees"])}
<h2 id="tips">Smart tips before you apply</h2><div class="tip">{ul(c["tips"])}</div>
<h2 id="types">Types of {esc(c["name"].lower())}</h2><p>Explore each type for specific eligibility, documents and tips.</p><div class="grid-2">{sub_cards}</div>
<h2 id="faq">Frequently asked questions</h2>{faq_html(faqs, True)}
<h2>Related loans</h2>{related_cards(c["related"])}
</article>
<aside class="side"><div class="card toc"><strong>On this page</strong>{tocs}</div>{lead_form(c["name"], title="Talk to a loan advisor", extra_id="s")}
<div class="card"><strong>Useful tools</strong><p class="fine">Plan before you apply.</p><ul><li><a href="/tools/emi-calculator/">EMI calculator</a></li><li><a href="/tools/loan-eligibility-calculator/">Eligibility calculator</a></li><li><a href="/tools/compare-loans/">Compare loan offers</a></li><li><a href="/tools/document-checklist/">Document checklist</a></li></ul></div></aside></div>
{cta_band()}'''
    title = trunc(f"{c['name']} in India: Eligibility, Documents, Apply", 62)
    desc = trunc(f"{c['tag']} Eligibility, documents, fees, process and FAQs, with free guidance from NEXUS Lending Partners, Hyderabad.", 158)
    svc = {"@context": "https://schema.org", "@type": "Service", "name": c["name"], "serviceType": "Loan facilitation",
           "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "India"}, "description": c["tag"],
           "url": BASE + path}
    render(path, title, desc, body, [svc, faq_ld(faqs)], [("Loans", "/loans/"), (c["name"], None)], priority="0.9")

# ================================================================ sub page
def build_sub(c, s):
    path = f"/loans/{c['slug']}/{s['slug']}/"
    others = [x for x in c["subs"] if x["slug"] != s["slug"]]
    faqs = [s["faq"]] + pick(c["faqs"], s["slug"], 3)
    docs = list(dict.fromkeys(s["docs"] + c["docs"]))
    other_links = "".join(f'<li><a href="/loans/{c["slug"]}/{x["slug"]}/">{esc(x["name"])}</a></li>' for x in others[:12])
    name = s["name"]
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Loans","/loans/"),(c["name"],f"/loans/{c['slug']}/"),(name,None)]).replace('class="crumbs wrap"','class="crumbs"')}
<div class="grid"><div><span class="kicker">{esc(c["name"])}</span><h1>{esc(name)} in India</h1><p class="lead">{esc(first_sentence(s["desc"]))}</p>
<div class="cta-row"><a class="btn btn-wa" href="{wa_url("Hello NEXUS, I need help with: "+name+".")}" target="_blank" rel="noopener">{WA_SVG} Ask on WhatsApp</a><a class="btn btn-ghost" href="/apply/?loan={c["slug"]}">Start application</a></div></div>
<div>{lead_form(c["name"], title="Check options for a "+name.lower()[:40], extra_id="h")}</div></div></div></div>
<div class="wrap layout"><article class="article">
<h2>About {esc(name.lower())}</h2><p>{esc(s["desc"])}</p><p><strong>Best suited for:</strong> {esc(s["best"])}</p>
<div class="tip"><strong>NEXUS tip:</strong> {esc(s["tip"])}</div>
<h2>{esc(name)}: key facts</h2><p>These are typical figures for the wider category of {esc(c["name"].lower())}. Your lender's offer may differ.</p>{facts_html(c)}{note_box()}
<h2>Eligibility</h2>{ul(c["elig"])}
<h2>Documents required</h2>{ul(docs)}
<p>Use our <a href="/tools/document-checklist/">document checklist</a> to prepare everything before you apply.</p>
<h2>How the process works</h2>{steps_html(steps_for(c))}
<h2>Fees and charges</h2>{ul(c["fees"])}
<h2>{esc(name)}: frequently asked questions</h2>{faq_html(faqs, True)}
<h2>More about {esc(c["name"].lower())}</h2><p>Read the full guide on <a href="/loans/{c["slug"]}/">{esc(c["name"])}</a>, or explore related types:</p><ul>{other_links}</ul>
<h2>Related loans</h2>{related_cards(c["related"][:3])}
</article>
<aside class="side">{lead_form(c["name"], title="Talk to a loan advisor", extra_id="s")}
<div class="card"><strong>Plan your loan</strong><ul><li><a href="/tools/emi-calculator/">EMI calculator</a></li><li><a href="/tools/loan-eligibility-calculator/">Eligibility calculator</a></li><li><a href="/guides/apr-vs-interest-rate-key-fact-statement/">APR and Key Fact Statement</a></li></ul></div></aside></div>
{cta_band()}'''
    title = trunc(f"{name} in India: Eligibility, Documents & Process | NEXUS", 66)
    desc = trunc(f"{first_sentence(s['desc'])} Eligibility, documents, fees and how to apply, with free guidance from NEXUS Lending Partners.", 158)
    svc = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": "Loan facilitation",
           "provider": {"@id": ORG_ID}, "areaServed": {"@type": "Country", "name": "India"}, "description": s["desc"], "url": BASE + path}
    render(path, title, desc, body, [svc, faq_ld(faqs)], [("Loans", "/loans/"), (c["name"], f"/loans/{c['slug']}/"), (name, None)], priority="0.7")

# ================================================================ loans hub
def build_loans_hub():
    blocks = []
    total = 0
    for c in CATS:
        total += len(c["subs"])
        links = "".join(f'<li><a href="/loans/{c["slug"]}/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in c["subs"])
        blocks.append(f'<div class="card"><div style="display:flex;gap:12px;align-items:center;margin-bottom:10px">{icon(c["icon"])}<h3 style="margin:0"><a href="/loans/{c["slug"]}/" style="text-decoration:none">{esc(c["name"])}</a></h3></div><p class="fine">{esc(c["tag"])}</p><ul>{links}</ul></div>')
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Loans",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>All Types of Loans in India</h1>
<p class="lead">{len(CATS)} loan families and {total}+ loan types in one place. Pick yours to see eligibility, documents, fees and the step-by-step process, then continue on WhatsApp.</p></div></div>
<section class="sec"><div class="wrap"><div class="grid-3">{"".join(blocks)}</div>{note_box()}</div></section>
<section class="sec soft"><div class="wrap grid-2"><div><h2>Not sure which loan you need?</h2><p>Answer four quick questions and we will point you to the right loan family, with the documents to keep ready.</p><a class="btn btn-primary" href="/tools/loan-finder/">Find my loan →</a></div>{lead_form(None, title="Tell us your requirement", extra_id="hub")}</div></section>{cta_band()}'''
    render("/loans/", "All Types of Loans in India: Eligibility & Documents | NEXUS",
           trunc(f"Browse {total}+ loan types in India: personal, home, business, gold, vehicle, education, agriculture, MSME, government scheme loans and more, with eligibility and documents.", 158),
           body, [{"@context":"https://schema.org","@type":"CollectionPage","name":"All Types of Loans in India","url":BASE+"/loans/"}], [("Loans", None)], priority="0.9")

# ================================================================ documents hub
def build_docs_hub():
    blocks = []
    for c in CATS:
        blocks.append(f'<div class="card"><h3><a href="/loans/{c["slug"]}/" style="text-decoration:none">{esc(c["name"])}</a></h3>{ul(c["docs"])}</div>')
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Documents required",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Documents Required for Every Type of Loan</h1><p class="lead">A complete list of documents typically asked for each loan family. Lenders may ask for more or fewer, so confirm with us before you apply.</p><a class="btn btn-primary" href="/tools/document-checklist/">Open the interactive checklist →</a></div></div>
<section class="sec"><div class="wrap"><div class="grid-2">{"".join(blocks)}</div></div></section>{cta_band()}'''
    render("/documents-required/", "Documents Required for Every Type of Loan in India | NEXUS Lending Partners",
           "Complete document checklist for personal, home, business, gold, vehicle, education, agriculture and other loans in India. Prepare once and apply faster.",
           body, None, [("Documents required", None)], priority="0.8")

# ================================================================ cities
def build_cities():
    cards = []
    for slug, name, state, kind, paras, pts in CITIES:
        cards.append(f'<a class="card prod" href="/loans-in/{slug}/"><h3>Loans in {esc(name)}</h3><p>{esc(state)}</p><span class="more">View →</span></a>')
        path = f"/loans-in/{slug}/"
        all_loans = "".join(f'<li><a href="/loans/{c["slug"]}/">{esc(c["name"])}</a></li>' for c in CATS)
        faqs = [
         (f"Does NEXUS provide loan assistance in {name}?", f"Yes. We assist customers in {name} and across India online and on WhatsApp. Our office is in Kukatpally, Hyderabad, and you can visit by appointment."),
         (f"Which loans are most popular in {name}?", "Popular needs include " + ", ".join(p.lower() for p in pts[:3]) + ". Needs vary by profile."),
         ("Do you charge borrowers a fee?","No. Our assistance is free to borrowers. Lenders charge their own fees, which are shown in the Key Fact Statement."),
        ]
        body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Locations","/loans-in/"),(name,None)]).replace('class="crumbs wrap"','class="crumbs"')}
<div class="grid"><div><span class="kicker">{esc(state)}</span><h1>Loans in {esc(name)}: Personal, Home, Business, Gold and More</h1><p class="lead">Compare options, prepare documents and apply with a team that explains every charge. Free guidance for borrowers in {esc(name)}.</p>
<div class="cta-row"><a class="btn btn-wa" href="{wa_url("Hello NEXUS, I am in "+name+" and need help with a loan.")}" target="_blank" rel="noopener">{WA_SVG} WhatsApp us</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a></div></div><div>{lead_form(None, title="Get help in "+name, extra_id="h")}</div></div></div></div>
<div class="wrap layout"><article class="article">
<h2>Loan help in {esc(name)}</h2>{"".join(f"<p>{esc(p)}</p>" for p in paras)}
<h2>Loans people in {esc(name)} commonly look for</h2>{ul(pts)}
<h2>All loan types we help with</h2><ul>{all_loans}</ul>
<h2>How to apply from {esc(name)}</h2>{steps_html(steps_for(CAT["personal-loan"]))}
<h2>FAQs for {esc(name)}</h2>{faq_html(faqs, True)}{note_box()}
</article><aside class="side">{lead_form(None, title="Talk to an advisor", extra_id="s")}</aside></div>{cta_band()}'''
        render(path, trunc(f"Loans in {name}: Personal, Home, Business, Gold Loan Help | NEXUS", 66),
               trunc(f"Looking for a loan in {name}? NEXUS Lending Partners helps you compare personal, home, business, gold, vehicle and education loans, with documents and process explained.", 158),
               body, [faq_ld(faqs)], [("Locations", "/loans-in/"), (name, None)], priority="0.7")
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Locations",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Loan Assistance Across India</h1><p class="lead">Our office is in Kukatpally, Hyderabad. We assist borrowers online and on WhatsApp in every state. Pick your city to see popular loans and how to apply.</p></div></div>
<section class="sec"><div class="wrap"><div class="grid-4">{"".join(cards)}</div></div></section>{cta_band()}'''
    render("/loans-in/", "Loan Assistance in Hyderabad and Across India | NEXUS Lending Partners",
           "NEXUS Lending Partners helps borrowers in Hyderabad, Bengaluru, Mumbai, Delhi NCR, Chennai, Pune and more with personal, home, business and gold loans.",
           body, None, [("Locations", None)], priority="0.8")

# ================================================================ home
def build_home():
    prod = "".join(f'<a class="card prod" href="/loans/{c["slug"]}/">{icon(c["icon"])}<h3>{esc(c["name"])}</h3><p>{esc(c["tag"])}</p><span class="more">Explore →</span></a>' for c in CATS)
    popular = []
    for slug, sub in [("personal-loan","salaried-personal-loan"),("personal-loan","instant-personal-loan"),("personal-loan","debt-consolidation-loan"),("home-loan","home-purchase-loan"),("home-loan","home-loan-balance-transfer"),("home-loan","nri-home-loan"),("loan-against-property","loan-against-residential-property"),("gold-loan","gold-jewellery-loan"),("vehicle-loan","new-car-loan"),("vehicle-loan","two-wheeler-loan"),("vehicle-loan","used-car-loan"),("education-loan","overseas-education-loan"),("business-loan","business-term-loan"),("business-loan","startup-business-loan"),("working-capital-and-invoice-finance","overdraft-facility"),("working-capital-and-invoice-finance","invoice-financing-and-discounting"),("government-scheme-loans","pm-mudra-yojana-loan"),("agriculture-loan","kisan-credit-card-loan"),("agriculture-loan","dairy-and-cattle-loan"),("loan-against-securities","loan-against-mutual-funds"),("instant-small-credit","buy-now-pay-later-bnpl"),("business-loan","doctor-and-clinic-loan"),("business-loan","women-entrepreneur-loan"),("special-purpose-loans","medical-treatment-and-hospitalisation-loan")]:
        s = next(x for x in CAT[slug]["subs"] if x["slug"] == sub)
        popular.append(f'<li><a href="/loans/{slug}/{sub}/">{esc(s["name"])}</a></li>')
    tools = "".join(f'<a class="card prod" href="/tools/{s}/">{icon(i)}<h3>{esc(n)}</h3><span class="more">Open tool →</span></a>' for (s, n), i in zip(TOOLS, ["calc","home","user","merge","cycle","coins","compare","quiz","doc","shield"]))
    steps = [("Tell us your need","Share the loan type, amount and city on WhatsApp or the form. It takes about two minutes."),
             ("We find the fit","We compare your profile with typical lender criteria and suggest options. No obligation."),
             ("Apply with the right documents","We give you an exact checklist so you apply once and avoid back-and-forth."),
             ("Sanction, disbursal and support","The lender sanctions and pays you directly. We stay with you after disbursal.")]
    steps_h = '<ol class="steps">' + "".join(f"<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>" for t, d in steps) + "</ol>"
    pillars = [("shield","Trust","We are upfront about who we are: a facilitator, not a lender. We name the lender before you share documents."),
               ("eye","Transparency","APR, fees, prepayment terms and our own commission model explained in plain words."),
               ("link","Right financial connections","We match your profile to lenders whose criteria fit, instead of sending you everywhere."),
               ("heart","Long-term relationships","We stay for your next loan, your balance transfer and your questions after disbursal.")]
    pil = '<div class="grid-4">' + "".join(f'<div class="card">{icon(i)}<h3 style="margin-top:12px">{t}</h3><p style="margin:0;color:var(--muted)">{d}</p></div>' for i, t, d in pillars) + "</div>"
    edge = [("No advance fees, ever","We never ask you to pay to get a loan approved."),("Free for borrowers","Our guidance costs you nothing. Lenders may pay us a commission on disbursal."),("All loan types in one place","From a ₹50,000 personal loan to project finance."),("Document readiness","Exact checklists per loan type so you apply once."),("Plain-language guidance","APR, KFS, moratorium and prepayment explained simply."),("WhatsApp-first support","Ask questions and track progress in a chat you already use."),("Privacy-first","We do not collect OTPs, PINs or passwords, and we collect only what is needed."),("Hyderabad-based team","A real office in Kukatpally you can visit by appointment.")]
    edge_h = '<div class="grid-4">' + "".join(f'<div class="card"><h3>{esc(t)}</h3><p style="margin:0;color:var(--muted);font-size:.93rem">{esc(d)}</p></div>' for t, d in edge) + "</div>"
    never = ["Ask you for an advance fee, 'insurance' or 'GST' to approve a loan","Ask for your OTP, PIN, CVV or passwords","Promise guaranteed approval or the 'lowest rate'","Receive or hold your loan money","Ask you to misstate income or documents","Share your data with anyone you have not agreed to"]
    always = ["Tell you plainly that we are not the lender","Name the lender and show the Key Fact Statement","Explain APR, fees and prepayment before you decide","Give you a precise document checklist","Respond to complaints through a published grievance process","Tell you honestly when a loan is not right for you"]
    faqs = [q for q in GENERAL_FAQS[0][1][:3]] + [GENERAL_FAQS[1][1][0], GENERAL_FAQS[2][1][0], GENERAL_FAQS[3][1][0], GENERAL_FAQS[1][1][4]]
    cities = "".join(f'<li><a href="/loans-in/{s}/">{esc(n)}</a></li>' for s, n, *_ in CITIES)
    gcards = "".join(f'<a class="card prod" href="/guides/{g["slug"]}/"><span class="fine">{esc(g["cat"])}</span><h3>{esc(g["title"])}</h3><span class="more">Read guide →</span></a>' for g in GUIDES[:6])
    body = f'''<section class="hero"><div class="wrap grid"><div>
<span class="kicker">Hyderabad · Serving borrowers across India</span>
<h1>Every Loan. <span class="a">One Trusted Partner.</span></h1>
<p class="lead">Compare, prepare and apply for personal, home, business, gold, vehicle, education and 100+ other loan types. We explain every rupee, work only with regulated lenders and never ask for an advance fee.</p>
<div class="cta-row"><a class="btn btn-wa" href="{wa_url("Hello NEXUS Lending Partners, I need help with a loan.")}" target="_blank" rel="noopener">{WA_SVG} Chat on WhatsApp</a><a class="btn btn-ghost" href="/loans/">Browse all loans</a></div>
<ul class="chips"><li><svg viewBox="0 0 24 24">{ICONS["check"]}</svg>No advance fees</li><li><svg viewBox="0 0 24 24">{ICONS["check"]}</svg>Free for borrowers</li><li><svg viewBox="0 0 24 24">{ICONS["check"]}</svg>Regulated lender partners</li><li><svg viewBox="0 0 24 24">{ICONS["check"]}</svg>WhatsApp-first support</li></ul>
</div><div>{lead_form(None, title="Find the right loan in 2 minutes", extra_id="hero")}</div></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><span class="kicker">Our promise</span><h2>{esc(TAGLINE)}</h2><p>Trust, transparency, the right financial connections and long-term relationships are not slogans for us. They are how we work.</p></div>{pil}</div></section>

<section class="sec soft"><div class="wrap"><div class="sec-head"><h2>Every loan you may need, in one place</h2><p>Pick a loan family to see eligibility, documents, fees, process and honest tips. Each page ends on WhatsApp so you can ask us anything.</p></div><div class="grid-4">{prod}</div><p style="text-align:center;margin-top:26px"><a class="btn btn-primary" href="/loans/">See all {sum(len(c["subs"]) for c in CATS)}+ loan types</a></p></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><span class="kicker">How it works</span><h2>From question to disbursal in four clear steps</h2><p>You stay in control at every step. The lender takes the final decision and pays you directly.</p></div>{steps_h}</div></section>

<section class="sec soft"><div class="wrap grid-2"><div><span class="kicker">See the real cost</span><h2>What a loan really costs: an illustration</h2><p>A loan is more than the monthly instalment. Look at total interest and fees before you decide. Here is a simple illustration of why we always ask you to read the Key Fact Statement.</p><p><a href="/tools/emi-calculator/">Try your own numbers in the EMI calculator →</a></p></div>
<div class="example"><table><tr><td>Loan amount</td><td>₹5,00,000</td></tr><tr><td>Interest rate (illustrative)</td><td>12% per year</td></tr><tr><td>Tenure</td><td>36 months</td></tr><tr><td>Monthly EMI</td><td>about ₹16,607</td></tr><tr><td>Total interest</td><td>about ₹97,860</td></tr><tr><td>Total repayment (before fees)</td><td>about ₹5,97,860</td></tr></table><p class="fine" style="margin-top:10px">Illustration only. Real offers depend on the lender, your profile and fees. Not a loan offer.</p></div></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><span class="kicker">Why NEXUS</span><h2>Built to be the most trusted way to borrow</h2></div>{edge_h}</div></section>

<section class="sec soft"><div class="wrap"><div class="sec-head"><h2>Our commitments, in black and white</h2></div><div class="two-col"><div class="card"><h3>What you can always expect</h3><ul class="yes">{"".join(f"<li>{esc(i)}</li>" for i in always)}</ul></div><div class="card"><h3>What we will never do</h3><ul class="no">{"".join(f"<li>{esc(i)}</li>" for i in never)}</ul></div></div></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><span class="kicker">Free tools</span><h2>Plan before you borrow</h2><p>Calculators and checkers that give you clarity before you talk to any lender. Every result can be sent to us on WhatsApp.</p></div><div class="grid-4">{tools}</div></div></section>

<section class="sec soft"><div class="wrap"><div class="sec-head"><h2>Popular loans people search for</h2></div><ul class="pill-list" style="justify-content:center">{"".join(popular)}</ul></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><span class="kicker">Learn first, borrow wisely</span><h2>Loan guides in plain language</h2></div><div class="grid-3">{gcards}</div><p style="text-align:center;margin-top:24px"><a class="btn btn-ghost" href="/guides/">All guides</a></p></div></section>

<section class="sec soft"><div class="wrap grid-2"><div><span class="kicker">Hyderabad and beyond</span><h2>Loan help where you are</h2><p>Our office is in Kukatpally, Hyderabad. We also assist borrowers online and on WhatsApp across India.</p><ul class="pill-list">{cities}</ul></div><div class="card"><h3>Partner lenders you can trust</h3><p>We work with banks, NBFCs and housing finance companies that are regulated by RBI. We choose lenders by transparency, service quality and fit for your profile, not just by commission. <a href="/lending-partners/">How we choose lenders →</a></p><h3>Partner with NEXUS</h3><p>Are you a DSA, agent or connector? Join us as a partner. <a href="/partner-with-us/">Learn more →</a></p></div></div></section>

<section class="sec"><div class="wrap" style="max-width:860px"><div class="sec-head"><h2>Frequently asked questions</h2></div>{faq_html(faqs)}<p style="text-align:center"><a href="/faq/">See all FAQs →</a></p></div></section>
{cta_band()}'''
    render("/", "NEXUS Lending Partners: Personal, Home, Business & Gold Loans",
           trunc("Every loan, one trusted partner. NEXUS Lending Partners in Hyderabad helps you compare, prepare and apply for personal, home, business, gold, vehicle and education loans. No advance fees.", 158),
           body, [org_ld(), {"@context":"https://schema.org","@type":"WebSite","name":BRAND,"url":BASE+"/","publisher":{"@id":ORG_ID}}, faq_ld(faqs)], None, priority="1.0")

def build_all_loans():
    for c in CATS:
        build_category(c)
        for s in c["subs"]:
            build_sub(c, s)
    build_loans_hub(); build_docs_hub(); build_cities(); build_home()
