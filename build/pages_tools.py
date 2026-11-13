from lib import *
from pages_loans import steps_html

def rng(id_, label, mn, mx, val, step, fmt="inr", suffix=""):
    return f'<div class="f range"><label for="{id_}">{label}: <output id="{id_}-o"></output></label><input type="range" id="{id_}" min="{mn}" max="{mx}" value="{val}" step="{step}" data-fmt="{fmt}" data-suffix="{suffix}"></div>'

def num(id_, label, val="", ph=""):
    return f'<div class="f"><label for="{id_}">{label}</label><input id="{id_}" type="number" inputmode="decimal" value="{val}" placeholder="{ph}" min="0"></div>'

def tool_shell(slug, name, intro, inputs, result, extra="", body_extra="", faqs=None, tool=None):
    path = f"/tools/{slug}/"
    faqs = faqs or []
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Tools","/tools/"),(name,None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>{esc(name)}</h1><p class="lead">{esc(intro)}</p></div></div>
<section class="sec"><div class="wrap"><div class="tool"><div class="card raise" style="display:grid;gap:14px;align-content:start">{inputs}</div><div>{result}</div></div>{extra}
<div class="note">Results are indicative and for planning only. Actual offers depend on the lender, your credit profile and fees. NEXUS is a loan facilitator, not a lender.</div></div></section>
{body_extra}
{('<section class="sec soft"><div class="wrap" style="max-width:860px"><h2>Frequently asked questions</h2>'+faq_html(faqs)+'</div></section>') if faqs else ''}
{cta_band()}'''
    schemas = [{"@context":"https://schema.org","@type":"WebApplication","name":name,"url":BASE+path,"applicationCategory":"FinanceApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"INR"}}]
    if faqs: schemas.append(faq_ld(faqs))
    render(path, trunc(f"{name}: Free Online Tool | NEXUS Lending Partners", 66),
           trunc(f"{intro} Free, no sign-up. Send your result to NEXUS on WhatsApp for guidance.", 158),
           body, schemas, [("Tools","/tools/"),(name,None)], body_attr=f'data-tool="{tool}"', priority="0.8")

def result_emi():
    return '''<div class="result"><h3>Your monthly EMI</h3><div class="big" id="o-emi">₹0</div>
<dl><dt>Principal amount</dt><dd id="o-pri"></dd><dt>Total interest</dt><dd id="o-int"></dd><dt>Total payment</dt><dd id="o-tot"></dd></dl>
<div class="bar" aria-hidden="true"><i id="b1" style="background:#19B5AE"></i><i id="b2" style="background:#F2B84B"></i></div>
<div class="legend"><span>■ Principal</span><span style="color:#F2B84B">■ Interest</span></div><br>
<button class="btn btn-wa" id="send-wa" type="button">Send this to NEXUS on WhatsApp</button></div>'''

def build_tools():
    emi_faqs = [("How is EMI calculated?","EMI = P × r × (1+r)^n ÷ ((1+r)^n − 1), where P is the principal, r the monthly interest rate and n the number of months."),
                ("Does a longer tenure reduce cost?","It lowers your EMI but raises total interest. Choose the shortest tenure you can comfortably afford."),
                ("Are processing fees included?","No. This calculator shows interest only. Add the lender's processing fee and other charges from the Key Fact Statement.")]
    sched = '<section class="sec soft"><div class="wrap"><h2>Year-wise repayment schedule</h2><div class="tablewrap"><table class="t"><thead><tr><th>Year</th><th>Principal paid</th><th>Interest paid</th><th>Balance</th></tr></thead><tbody id="sched"></tbody></table></div></div></section>'
    tool_shell("emi-calculator","EMI Calculator","Work out your monthly instalment, total interest and total repayment for any loan in seconds.",
      rng("amt","Loan amount",50000,10000000,500000,10000)+rng("rate","Interest rate (% per year)",5,36,12,0.1,"num","%")+rng("ten","Tenure (years)",1,30,3,1,"num"," yrs"),
      result_emi(), body_extra=sched, faqs=emi_faqs, tool="emi")
    tool_shell("home-loan-emi-calculator","Home Loan EMI Calculator","Plan your home loan: see the EMI, total interest and year-wise balance for up to 30 years.",
      rng("amt","Loan amount",500000,100000000,5000000,100000)+rng("rate","Interest rate (% per year)",6,15,8.75,0.05,"num","%")+rng("ten","Tenure (years)",1,30,20,1,"num"," yrs"),
      result_emi(), body_extra=sched, faqs=[("Which interest rate should I enter?","Use the rate in your offer or an indicative current rate. Floating rates can change with the benchmark."),("Does this include property costs?","No. Budget separately for stamp duty, registration, legal fees and your down payment.")], tool="emi")
    tool_shell("loan-eligibility-calculator","Loan Eligibility Calculator","Get an indicative loan amount from your income, existing EMIs and the share of income lenders allow for EMIs (FOIR).",
      num("inc","Net monthly income (₹)","60000")+num("emis","Existing monthly EMIs (₹)","5000")+rng("foir","Share of income allowed for EMIs (FOIR %)",30,70,50,5,"num","%")+rng("rate","Interest rate (% per year)",6,30,11,0.1,"num","%")+rng("ten","Tenure (years)",1,30,5,1,"num"," yrs"),
      '''<div class="result"><h3>Indicative eligible loan</h3><div class="big" id="o-max">₹0</div><dl><dt>Maximum new EMI</dt><dd id="o-memi"></dd><dt>Existing EMIs</dt><dd id="o-ex"></dd></dl><p id="o-msg" class="fine" style="color:#bcd5ea"></p><button class="btn btn-wa" id="send-wa" type="button">Check real options on WhatsApp</button></div>''',
      faqs=[("What is FOIR?","Fixed Obligations to Income Ratio is the share of income that goes to EMIs and fixed obligations. Many lenders allow roughly 40% to 55%."),("Is this my approved amount?","No. It is an estimate. Lenders also check credit score, job or business stability and documents.")], tool="eligibility")
    tool_shell("balance-transfer-calculator","Balance Transfer Calculator","See whether moving your loan to a lower rate really saves money after processing and other fees.",
      num("outs","Outstanding loan amount (₹)","2500000")+num("r1","Current interest rate (%)","9.5")+num("r2","New interest rate (%)","8.5")+rng("rem","Remaining tenure (years)",1,30,15,1,"num"," yrs")+num("fee","New lender processing fee (% of loan)","0.5")+num("oth","Other costs: legal, valuation, foreclosure (₹)","10000"),
      '''<div class="result"><h3>Estimated net saving</h3><div class="big" id="o-net">₹0</div><dl><dt>Current EMI</dt><dd id="o-m1"></dd><dt>New EMI</dt><dd id="o-m2"></dd><dt>Monthly difference</dt><dd id="o-ms"></dd><dt>Total transfer costs</dt><dd id="o-cost"></dd></dl><p id="o-verdict" class="fine" style="color:#bcd5ea"></p><button class="btn btn-wa" id="send-wa" type="button">Discuss a transfer on WhatsApp</button></div>''',
      faqs=[("Is a balance transfer always worth it?","No. Fees, a longer tenure or a rate that resets can cancel the saving. Ask your current lender to match the rate first."),("Is foreclosure on my old loan free?","On floating-rate loans to individuals there is no prepayment charge under RBI rules. Fixed-rate and business loans may charge. Check your sanction letter.")], tool="bt")
    tool_shell("prepayment-calculator","Loan Prepayment Calculator","Find out how much interest and time you save by paying a lump sum towards your loan.",
      rng("amt","Loan amount",50000,50000000,2500000,50000)+rng("rate","Interest rate (% per year)",5,30,10,0.1,"num","%")+rng("ten","Tenure (years)",1,30,15,1,"num"," yrs")+num("prepay","Prepayment amount (₹)","200000")+num("after","Pay it after month number","12"),
      '''<div class="result"><h3>Interest you could save</h3><div class="big" id="o-sav">₹0</div><dl><dt>Current EMI</dt><dd id="o-emi"></dd><dt>Interest without prepayment</dt><dd id="o-base"></dd><dt>Original tenure</dt><dd id="o-old"></dd><dt>New tenure (EMI unchanged)</dt><dd id="o-new"></dd></dl><button class="btn btn-wa" id="send-wa" type="button">Ask NEXUS how to prepay smartly</button></div>''',
      faqs=[("Should I prepay or invest?","If your loan rate is higher than the return you can reliably earn, prepaying is a sure saving. Keep an emergency fund first."),("Will EMI reduce or tenure?","This tool keeps EMI unchanged and shows the shorter tenure. Ask your lender whether you can choose to reduce EMI instead.")], tool="prepay")
    tool_shell("gold-loan-calculator","Gold Loan Calculator","Estimate your gold loan amount and monthly interest from weight, purity and the gold rate.",
      num("grams","Weight of gold ornaments (grams)","50")+num("grate","Today's 24-carat gold rate (₹ per gram)","7500")+'<div class="f"><label for="purity">Purity</label><select id="purity"><option value="22" selected>22 carat</option><option value="24">24 carat</option><option value="20">20 carat</option><option value="18">18 carat</option></select></div>'+num("ltv","Loan-to-value offered by lender (%)","75")+rng("rate","Interest rate (% per year)",7,30,12,0.1,"num","%")+rng("mon","Loan period (months)",3,36,12,1,"num"," months"),
      '''<div class="result"><h3>Indicative gold loan</h3><div class="big" id="o-loan">₹0</div><dl><dt>Gold value</dt><dd id="o-val"></dd><dt>Monthly interest (if interest-only)</dt><dd id="o-int"></dd><dt>Total interest over period</dt><dd id="o-tot"></dd></dl><button class="btn btn-wa" id="send-wa" type="button">Find gold loan lenders on WhatsApp</button></div>''',
      extra='<p class="fine">Enter the current gold rate from a trusted source. Lenders value only the pure gold content, after deducting stones and making charges, and the loan-to-value is capped by RBI norms.</p>',
      faqs=[("Is this the exact amount I will get?","No. The lender's physical appraisal decides weight, purity and the rate applied."),("What happens if gold prices fall?","If the loan value approaches the market value of your gold, lenders may ask you to repay part or add security. Check your agreement.")], tool="gold")
    cmp_inputs = '<div id="cmp" class="tablewrap"><table class="t"><thead><tr><th></th><th>Offer 1</th><th>Offer 2</th><th>Offer 3</th></tr></thead><tbody>' + \
      ''.join(f'<tr><td>{lab}</td>' + ''.join(f'<td><input id="{pre}{i}" type="number" inputmode="decimal" min="0" value="{val if i<3 else ""}" style="width:100%;padding:8px;border:1.5px solid var(--line);border-radius:8px"></td>' for i in (1,2,3)) + '</tr>'
        for lab, pre, val in [("Loan amount (₹)","a","500000"),("Interest rate (%)","r","12"),("Tenure (years)","t","3"),("Processing fee (%)","f","2")]) + '</tbody></table></div>'
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Tools","/tools/"),("Loan Offer Comparison",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Loan Offer Comparison Tool</h1><p class="lead">Put up to three offers side by side and see the true total cost, not just the EMI.</p></div></div>
<section class="sec"><div class="wrap">{cmp_inputs}<h2 style="margin-top:28px">Comparison</h2><div class="tablewrap"><table class="t"><thead><tr><th>Offer</th><th>EMI</th><th>Total interest</th><th>Processing fee</th><th>Total cost (interest + fee)</th></tr></thead><tbody><tr id="c1"></tr><tr id="c2"></tr><tr id="c3"></tr></tbody></table></div><p id="cmp-note" class="tip"></p>
<p><a class="btn btn-wa" target="_blank" rel="noopener" href="{wa_url("Hello NEXUS, I have loan offers to compare. Please help me choose.")}">{WA_SVG} Get NEXUS to review my offers</a></p>
<div class="note">Compare the APR and prepayment terms in each lender's Key Fact Statement too. Insurance and other bundled charges raise the real cost.</div></div></section>{cta_band()}'''
    render("/tools/compare-loans/","Loan Offer Comparison Tool: Compare EMI and Total Cost | NEXUS","Compare up to three loan offers by EMI, total interest and fees to find the genuinely cheapest option. Free tool from NEXUS Lending Partners.",body,[{"@context":"https://schema.org","@type":"WebApplication","name":"Loan Offer Comparison Tool","url":BASE+"/tools/compare-loans/","applicationCategory":"FinanceApplication","operatingSystem":"Any"}],[("Tools","/tools/"),("Loan Offer Comparison",None)],body_attr='data-tool="compare"',priority="0.8")
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Tools","/tools/"),("Which Loan Is Right for Me?",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Which Loan Is Right for Me?</h1><p class="lead">Four quick questions. We point you to the right loan family, and you can continue on WhatsApp.</p></div></div>
<section class="sec"><div class="wrap" style="max-width:760px"><div id="quiz" class="card raise"></div></div></section>{cta_band()}'''
    render("/tools/loan-finder/","Which Loan Is Right for Me? Free Loan Finder Quiz | NEXUS","Not sure which loan to choose? Answer four quick questions to find the right loan type: personal, home, gold, business, education and more.",body,None,[("Tools","/tools/"),("Loan Finder",None)],body_attr='data-tool="finder"',priority="0.8")
    # docs checklist
    import json
    qs = {c["name"]: c["docs"] for c in CATS}
    docs_map = {c["name"]: {"name": c["name"], "docs": c["docs"]} for c in CATS}
    opts = "".join(f'<option value="{esc(c["name"])}">{esc(c["name"])}</option>' for c in CATS)
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Tools","/tools/"),("Document Checklist",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Loan Document Checklist</h1><p class="lead">Choose your loan type, tick off what you have and print the list. Apply once, with everything ready.</p></div></div>
<section class="sec"><div class="wrap" style="max-width:820px"><div class="f"><label for="doc-loan">Loan type</label><select id="doc-loan">{opts}</select></div><div id="doc-out" style="margin-top:20px"></div><div class="note">Your lender may ask for additional documents. Never send OTPs, PINs or passwords to anyone.</div></div></section>{cta_band()}'''
    sc = f"<script>window.NEXUS_DOCS={json.dumps(docs_map, ensure_ascii=False)};</script>"
    render("/tools/document-checklist/","Loan Document Checklist: Documents Required for Every Loan | NEXUS","Interactive, printable checklist of documents needed for personal, home, business, gold, vehicle, education, agri and other loans in India.",body,None,[("Tools","/tools/"),("Document Checklist",None)],body_attr='data-tool="docs"',priority="0.8",scripts=sc)
    body = f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Tools","/tools/"),("Credit Health Self-Check",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Credit Health Self-Check</h1><p class="lead">Six questions about your credit habits. You get practical tips. This is not your real credit score.</p></div></div>
<section class="sec"><div class="wrap" style="max-width:760px"><form id="health" class="card raise" style="display:grid;gap:14px">
<div class="f"><label>How often do you pay EMIs and card bills on time?</label><select name="pay"><option value="always">Always on time</option><option value="rare">Rarely late</option><option value="often">Often late</option></select></div>
<div class="f"><label>How much of your credit card limit do you use?</label><select name="util"><option value="low">Under 30%</option><option value="mid">30% to 60%</option><option value="high">Over 60%</option></select></div>
<div class="f"><label>Loan or card applications in the last 6 months</label><select name="enq"><option value="few">0 to 1</option><option value="some">2 to 3</option><option value="many">4 or more</option></select></div>
<div class="f"><label>Age of your oldest credit account</label><select name="age"><option value="old">5+ years</option><option value="mid">2 to 5 years</option><option value="new">Under 2 years</option></select></div>
<div class="f"><label>Your credit mix</label><select name="mix"><option value="both">Both loans and cards</option><option value="one">Only loans or only cards</option><option value="none">No credit history yet</option></select></div>
<div class="f"><label>Any overdue, written-off or settled accounts?</label><select name="def"><option value="no">No</option><option value="yes">Yes</option></select></div>
<button class="btn btn-primary" type="submit">See my self-check</button></form><div id="health-res" style="margin-top:20px"></div>
<div class="note">This is a simple self-check for awareness. Your actual score comes from credit bureaus. See our guide on <a href="/guides/how-to-improve-cibil-score/">improving your score</a>.</div></div></section>{cta_band()}'''
    render("/tools/credit-health-check/","Credit Health Self-Check: Quick Tips to Improve Your Credit | NEXUS","A six-question credit health self-check with practical tips to improve your chances of loan approval. Free tool from NEXUS Lending Partners.",body,None,[("Tools","/tools/"),("Credit Health Self-Check",None)],body_attr='data-tool="health"',priority="0.7")
    cards = "".join(f'<a class="card prod" href="/tools/{s}/">{icon(i)}<h3>{esc(n)}</h3><span class="more">Open →</span></a>' for (s, n), i in zip(TOOLS, ["calc","home","user","merge","cycle","coins","compare","quiz","doc","shield"]))
    render("/tools/","Free Loan Tools: EMI, Eligibility, Balance Transfer, Gold Loan Calculators | NEXUS","Free calculators and checkers: EMI, home loan EMI, eligibility, balance transfer, prepayment, gold loan, offer comparison, document checklist and credit health check.",
      f'''<div class="pagehead"><div class="wrap">{crumbs_html([("Tools",None)]).replace('class="crumbs wrap"','class="crumbs"')}<h1>Free Loan Tools and Calculators</h1><p class="lead">Plan before you borrow. Every tool is free, needs no sign-up and can be sent to us on WhatsApp.</p></div></div><section class="sec"><div class="wrap"><div class="grid-3">{cards}</div></div></section>{cta_band()}''',
      None,[("Tools",None)],priority="0.8")
