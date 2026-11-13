(function(){
'use strict';
var WA = (window.NEXUS && window.NEXUS.wa) || '916300695591';
function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
function inr(n){n=Math.round(n);if(!isFinite(n))return '₹0';return '₹'+n.toLocaleString('en-IN')}
function waLink(t){return 'https://wa.me/'+WA+'?text='+encodeURIComponent(t)}
function openWA(t){window.open(waLink(t),'_blank','noopener')}
window.NEXUS_openWA=openWA;

/* nav */
var burger=$('.burger'),nav=$('nav.main');
if(burger){burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)})}
$$('.dd > button').forEach(function(b){b.addEventListener('click',function(e){
  if(window.innerWidth<=860){b.parentNode.classList.toggle('open');e.preventDefault()}
})});

/* lead forms -> WhatsApp */
function cleanPhone(v){return (v||'').replace(/[^0-9+]/g,'')}
function buildMsg(f){
  var d=new FormData(f), L=[];
  var loan=d.get('loan')||'a loan';
  L.push('Hello NEXUS Lending Partners, I need help with: '+loan+'.');
  if(d.get('name'))L.push('Name: '+d.get('name'));
  if(d.get('phone'))L.push('Phone: '+d.get('phone'));
  if(d.get('city'))L.push('City: '+d.get('city'));
  if(d.get('amount'))L.push('Amount needed: '+d.get('amount'));
  if(d.get('income'))L.push('Monthly income: '+d.get('income'));
  if(d.get('employment'))L.push('Employment: '+d.get('employment'));
  $$('[data-q]',f).forEach(function(el){if(el.value)L.push(el.getAttribute('data-q')+': '+el.value)});
  if(d.get('note'))L.push('Note: '+d.get('note'));
  L.push('(Sent from the NEXUS website. I agree to be contacted. I have not shared any OTP, PIN or ID numbers.)');
  return L.join('\n');
}
$$('form[data-lead]').forEach(function(f){
  var err=$('.err',f);
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var ph=cleanPhone(f.phone&&f.phone.value);
    if(f.phone&&f.phone.required&&ph.replace(/\D/g,'').length<10){if(err){err.textContent='Please enter a valid 10-digit mobile number.';err.style.display='block'}return}
    if(f.consent&&!f.consent.checked){if(err){err.textContent='Please tick the consent box so we can contact you.';err.style.display='block'}return}
    if(err)err.style.display='none';
    openWA(buildMsg(f));
    var ok=$('.sent',f);if(ok)ok.style.display='block';
  });
});
/* apply page: category-specific questions */
var sel=$('#apply-loan'),box=$('#apply-extra');
if(sel&&box&&window.NEXUS_QS){
  var render=function(){
    var qs=window.NEXUS_QS[sel.value]||[];box.innerHTML='';
    qs.forEach(function(q,i){
      var w=document.createElement('div');w.className='f';
      var l=document.createElement('label');l.textContent=q;l.setAttribute('for','q'+i);
      var inp=document.createElement('input');inp.id='q'+i;inp.type='text';inp.setAttribute('data-q',q);inp.autocomplete='off';
      w.appendChild(l);w.appendChild(inp);box.appendChild(w);
    });
  };
  sel.addEventListener('change',render);
  var qp=new URLSearchParams(location.search).get('loan');
  if(qp){for(var i=0;i<sel.options.length;i++){if(sel.options[i].getAttribute('data-slug')===qp||sel.options[i].value===qp){sel.selectedIndex=i}}}
  render();
}

/* EMI math */
function emi(P,rYr,n){var r=rYr/12/100;if(r===0)return P/n;var k=Math.pow(1+r,n);return P*r*k/(k-1)}
function bindRange(id){var el=$('#'+id);if(!el)return null;var o=$('#'+id+'-o');
  var sync=function(){if(o)o.textContent=el.getAttribute('data-fmt')==='inr'?inr(el.value):(el.value+(el.getAttribute('data-suffix')||''))};
  el.addEventListener('input',sync);sync();return el}

/* generic calculators, wired by data-tool */
var tool=document.body.getAttribute('data-tool');
function sendBtn(text){var b=$('#send-wa');if(b){b.onclick=function(){openWA(text())}}}
if(tool==='emi'){
  var A=bindRange('amt'),R=bindRange('rate'),T=bindRange('ten');
  var calc=function(){
    var P=+A.value,r=+R.value,n=+T.value*12,m=emi(P,r,n),tot=m*n,int=tot-P;
    $('#o-emi').textContent=inr(m);$('#o-int').textContent=inr(int);$('#o-tot').textContent=inr(tot);$('#o-pri').textContent=inr(P);
    var pp=Math.round(P/tot*100);$('#b1').style.width=pp+'%';$('#b2').style.width=(100-pp)+'%';
    // schedule (yearly)
    var bal=P,rows='',mr=r/12/100;
    for(var y=1;y<=Math.ceil(n/12);y++){var ip=0,pp2=0;for(var k=0;k<12&&((y-1)*12+k)<n;k++){var i1=bal*mr,p1=m-i1;ip+=i1;pp2+=p1;bal-=p1}
      rows+='<tr><td>Year '+y+'</td><td>'+inr(pp2)+'</td><td>'+inr(ip)+'</td><td>'+inr(Math.max(bal,0))+'</td></tr>'}
    $('#sched').innerHTML=rows;
  };
  [A,R,T].forEach(function(e){e.addEventListener('input',calc)});calc();
  sendBtn(function(){return 'Hello NEXUS, I used the EMI calculator: loan '+inr(A.value)+' at '+R.value+'% for '+T.value+' years gives an EMI of about '+$('#o-emi').textContent+'. Please help me find suitable lenders.'});
}
if(tool==='eligibility'){
  var inc=$('#inc'),emis=$('#emis'),rr=bindRange('rate'),tt=bindRange('ten'),fo=bindRange('foir');
  var c2=function(){
    var income=+inc.value||0,ex=+emis.value||0,maxE=Math.max(0,income*(+fo.value)/100-ex),n=+tt.value*12,r=+rr.value/12/100;
    var loan=r===0?maxE*n:maxE*(Math.pow(1+r,n)-1)/(r*Math.pow(1+r,n));
    $('#o-max').textContent=inr(loan);$('#o-memi').textContent=inr(maxE);$('#o-ex').textContent=inr(ex);
    $('#o-msg').textContent=maxE<=0?'Your existing EMIs already use the allowed share of income. Consider closing small loans or adding a co-applicant.':'Indicative only. The lender decides after verifying income, credit score and documents.';
  };
  [inc,emis,rr,tt,fo].forEach(function(e){e.addEventListener('input',c2)});c2();
  sendBtn(function(){return 'Hello NEXUS, my indicative eligibility from your calculator is '+$('#o-max').textContent+' (income '+inr(inc.value)+', existing EMIs '+inr(emis.value)+'). Please suggest suitable lenders.'});
}
if(tool==='prepay'){
  var A3=bindRange('amt'),R3=bindRange('rate'),T3=bindRange('ten'),pp3=$('#prepay'),after=$('#after');
  var c3=function(){
    var P=+A3.value,r=+R3.value/12/100,n=+T3.value*12,m=emi(P,+R3.value,n),pre=+pp3.value||0,am=+after.value||12;
    var bal=P,paid=0,k=0,tot=0;
    // baseline interest
    var base=m*n-P;
    bal=P;tot=0;
    for(k=1;k<=n&&bal>0.5;k++){var i1=bal*r,pr=m-i1;if(k===am)pr+=Math.min(pre,bal-pr);bal-=pr;tot+=i1;if(bal<=0.5)break}
    var saved=base-tot;
    $('#o-emi').textContent=inr(m);$('#o-new').textContent=Math.min(k,n)+' months';$('#o-old').textContent=n+' months';
    $('#o-sav').textContent=inr(Math.max(0,saved));$('#o-base').textContent=inr(base);
  };
  [A3,R3,T3,pp3,after].forEach(function(e){e.addEventListener('input',c3)});c3();
  sendBtn(function(){return 'Hello NEXUS, I want to reduce interest on my loan. Prepayment calculator shows possible interest saving of '+$('#o-sav').textContent+'. Please guide me.'});
}
if(tool==='bt'){
  var o1=$('#outs'),r1=$('#r1'),r2=$('#r2'),rem=bindRange('rem'),fee=$('#fee'),oth=$('#oth');
  var c4=function(){
    var P=+o1.value||0,n=+rem.value*12,m1=emi(P,+r1.value,n),m2=emi(P,+r2.value,n);
    var costs=(P*(+fee.value||0)/100)+(+oth.value||0);
    var sav=(m1-m2)*n-costs;
    $('#o-m1').textContent=inr(m1);$('#o-m2').textContent=inr(m2);$('#o-ms').textContent=inr(m1-m2);
    $('#o-cost').textContent=inr(costs);$('#o-net').textContent=inr(sav);
    $('#o-verdict').textContent=sav>0?('A transfer may save about '+inr(sav)+' over the remaining tenure after fees, if the new rate is truly offered.'):'At these numbers a transfer does not save money after costs. Ask your current lender for a rate reduction instead.';
  };
  [o1,r1,r2,rem,fee,oth].forEach(function(e){e.addEventListener('input',c4)});c4();
  sendBtn(function(){return 'Hello NEXUS, I want to check a balance transfer. Outstanding '+inr(o1.value)+', current rate '+r1.value+'%, remaining '+rem.value+' years. Estimated net saving '+$('#o-net').textContent+'.'});
}
if(tool==='gold'){
  var g=$('#grams'),rate=$('#grate'),pur=$('#purity'),ltv=$('#ltv'),ir=bindRange('rate'),mo=bindRange('mon');
  var c5=function(){
    var gold=(+g.value||0)*(+rate.value||0)*(+pur.value)/24,loan=gold*(+ltv.value)/100,r=+ir.value/12/100,n=+mo.value;
    var mi=loan*r;$('#o-val').textContent=inr(gold);$('#o-loan').textContent=inr(loan);$('#o-int').textContent=inr(mi);
    $('#o-tot').textContent=inr(loan*(+ir.value)/100*(n/12));
  };
  [g,rate,pur,ltv,ir,mo].forEach(function(e){e.addEventListener('input',c5)});c5();
  sendBtn(function(){return 'Hello NEXUS, I want a gold loan. Approx '+g.value+' g of gold. Indicative loan '+$('#o-loan').textContent+'. Please share lender options in my city.'});
}
if(tool==='compare'){
  var run=function(){
    var rows=[];
    [1,2,3].forEach(function(i){
      var P=+$('#a'+i).value,r=+$('#r'+i).value,t=+$('#t'+i).value,f=+$('#f'+i).value||0;
      if(!P||!r||!t){$('#c'+i).innerHTML='<td colspan="1">Enter the offer details</td>';return}
      var n=t*12,m=emi(P,r,n),tot=m*n,fee=P*f/100,all=tot+fee;
      rows.push({i:i,all:all,m:m,int:tot-P,fee:fee});
      $('#c'+i).innerHTML='<td><b>Offer '+i+'</b></td><td>'+inr(m)+'</td><td>'+inr(tot-P)+'</td><td>'+inr(fee)+'</td><td><b>'+inr(all)+'</b></td>';
    });
    rows.sort(function(a,b){return a.all-b.all});
    $('#cmp-note').textContent=rows.length>1?('Lowest total cost: Offer '+rows[0].i+'. Difference versus the highest: '+inr(rows[rows.length-1].all-rows[0].all)+'. Remember to compare APR and prepayment terms on the Key Fact Statement.'):'Enter at least two offers to compare.';
  };
  $$('#cmp input').forEach(function(e){e.addEventListener('input',run)});run();
}
if(tool==='docs'){
  var ds=$('#doc-loan'),out=$('#doc-out');
  var rd=function(){var d=window.NEXUS_DOCS[ds.value];out.innerHTML='';if(!d)return;
    var h=document.createElement('h3');h.textContent='Documents for '+d.name;out.appendChild(h);
    var ul=document.createElement('ul');ul.className='checklist';
    d.docs.forEach(function(x,i){var li=document.createElement('li');var c=document.createElement('input');c.type='checkbox';c.id='d'+i;var l=document.createElement('label');l.setAttribute('for','d'+i);l.textContent=x;li.appendChild(c);li.appendChild(l);ul.appendChild(li)});
    out.appendChild(ul);
    var b=document.createElement('button');b.className='btn btn-wa';b.textContent='Ask NEXUS to review my documents on WhatsApp';b.onclick=function(){openWA('Hello NEXUS, I am preparing for a '+d.name+'. Please review my document list and guide me.')};out.appendChild(b);
    var p=document.createElement('button');p.className='btn btn-ghost';p.style.marginLeft='10px';p.textContent='Print checklist';p.onclick=function(){window.print()};out.appendChild(p);
  };
  ds.addEventListener('change',rd);rd();
}
if(tool==='health'){
  var f6=$('#health'),res=$('#health-res');
  f6.addEventListener('submit',function(e){
    e.preventDefault();
    var s=0,tips=[];
    var pay=f6.pay.value,util=f6.util.value,enq=f6.enq.value,age=f6.age.value,mix=f6.mix.value,def=f6.def.value;
    s+= {always:35,rare:22,often:8}[pay];if(pay!=='always')tips.push('Set auto-debit for every EMI and card bill. Late payments hurt the most.');
    s+= {low:25,mid:15,high:5}[util];if(util!=='low')tips.push('Bring card usage below 30% of your limit by paying early or asking for a higher limit.');
    s+= {few:15,some:9,many:3}[enq];if(enq!=='few')tips.push('Pause new applications for a few months. Shortlist lenders before applying.');
    s+= {old:10,mid:6,new:3}[age];
    s+= {both:8,one:5,none:2}[mix];
    s+= {no:7,yes:0}[def];if(def==='yes')tips.push('Clear overdue or settled accounts and ask the lender to update the credit bureau.');
    var label=s>=80?'Strong':s>=62?'Good':s>=45?'Fair':'Needs work';
    res.innerHTML='<div class="card raise"><h3>Your credit health: '+label+'</h3><p>Score out of 100: <b>'+s+'</b>. This is a self-check based on your answers, <b>not</b> your actual credit score. Get your real score from a credit bureau.</p>'+(tips.length?'<ul><li>'+tips.join('</li><li>')+'</li></ul>':'<p>Keep up the good habits.</p>')+'<button class="btn btn-wa" id="hw">Discuss on WhatsApp</button></div>';
    $('#hw').onclick=function(){openWA('Hello NEXUS, I did the credit health self-check and got "'+label+'". Please suggest loans I may qualify for.')};
    res.scrollIntoView({behavior:'smooth',block:'nearest'});
  });
}
if(tool==='finder'){
  var step=0,ans={};
  var Qs=[
   {k:'purpose',q:'What do you need the money for?',o:[['Personal needs (medical, wedding, travel, gadgets)','personal-loan'],['Buy, build or renovate a home','home-loan'],['Raise money against my property','loan-against-property'],['Urgent cash against gold','gold-loan'],['Buy a vehicle','vehicle-loan'],['Education in India or abroad','education-loan'],['Grow or start a business','business-loan'],['Cash flow, overdraft or invoices','working-capital-and-invoice-finance'],['Import or export deals','trade-and-export-finance'],['Farming or rural activity','agriculture-loan'],['A government scheme (Mudra, PMEGP, etc.)','government-scheme-loans'],['Reduce my existing EMIs or card dues','debt-consolidation-and-balance-transfer'],['Borrow against shares, mutual funds or FD','loan-against-securities'],['Very small short-term amount','instant-small-credit'],['Large corporate or project funding','corporate-and-project-finance']]},
   {k:'amount',q:'About how much do you need?',o:[['Under ₹1 lakh'],['₹1 to 10 lakh'],['₹10 to 50 lakh'],['₹50 lakh to ₹5 crore'],['Above ₹5 crore']]},
   {k:'speed',q:'How soon do you need the money?',o:[['Within 1 to 2 days'],['Within a week'],['Within a month'],['No rush, I want the lowest cost']]},
   {k:'collat',q:'Do you own an asset you can pledge (property, gold, shares, vehicle)?',o:[['Yes, and I am comfortable pledging it'],['Yes, but I prefer not to pledge'],['No']]}
  ];
  var NAMES={'personal-loan':'Personal Loan','home-loan':'Home Loan','loan-against-property':'Loan Against Property','gold-loan':'Gold Loan','vehicle-loan':'Vehicle Loan','education-loan':'Education Loan','business-loan':'Business Loan (MSME)','working-capital-and-invoice-finance':'Working Capital & Invoice Finance','trade-and-export-finance':'Trade & Export Finance','agriculture-loan':'Agriculture & Rural Loans','government-scheme-loans':'Government Scheme Loans','debt-consolidation-and-balance-transfer':'Debt Consolidation & Balance Transfer','loan-against-securities':'Loan Against Securities','instant-small-credit':'Instant & Small-Ticket Credit','corporate-and-project-finance':'Corporate & Project Finance'};
  var q=$('#quiz');
  var show=function(){
    if(step>=Qs.length){fin();return}
    var Q=Qs[step];q.innerHTML='<p class="fine">Question '+(step+1)+' of '+Qs.length+'</p><h2>'+Q.q+'</h2><div class="quiz-opts"></div>';
    var w=$('.quiz-opts',q);
    Q.o.forEach(function(op){var b=document.createElement('button');b.textContent=op[0];b.onclick=function(){ans[Q.k]=op;step++;show()};w.appendChild(b)});
  };
  var fin=function(){
    var slug=ans.purpose[1],name=(NAMES[slug]||ans.purpose[0]);
    var link='/loans/'+slug+'/';
    var extra='';
    if(ans.speed[0].indexOf('1 to 2')>-1)extra+='<li>Since you need money quickly, keep KYC, bank statements and income proof ready now. Secured loans take longer because of valuation and legal checks.</li>';
    if(ans.collat[0]==='Yes, and I am comfortable pledging it')extra+='<li>Because you can pledge an asset, secured options such as <a href="/loans/gold-loan/">gold loan</a>, <a href="/loans/loan-against-property/">loan against property</a> or <a href="/loans/loan-against-securities/">loan against securities</a> are usually cheaper than unsecured credit.</li>';
    if(ans.amount[0]==='Under ₹1 lakh')extra+='<li>For small amounts, compare the processing fee as well as the rate. See <a href="/loans/instant-small-credit/">instant and small-ticket credit</a>.</li>';
    q.innerHTML='<div class="card raise"><span class="kicker">Suggested for you</span><h2>Start with: <a href="'+link+'">'+name+'</a></h2><ul>'+extra+'<li>Read the <a href="'+link+'">full guide</a> for eligibility, documents and fees.</li><li>Use the <a href="/tools/document-checklist/">document checklist</a> so you apply once with everything ready.</li></ul><p class="fine">This is a general suggestion, not financial advice or a loan offer.</p><div class="cta-row"><button class="btn btn-wa" id="qw">Continue on WhatsApp</button><button class="btn btn-ghost" id="qr">Start again</button></div></div>';
    $('#qw').onclick=function(){openWA('Hello NEXUS, from your loan finder I need help with: '+name+'. Amount: '+ans.amount[0]+'. Timeline: '+ans.speed[0]+'. Asset to pledge: '+ans.collat[0]+'.')};
    $('#qr').onclick=function(){step=0;ans={};show()};
  };
  show();
}
})();
