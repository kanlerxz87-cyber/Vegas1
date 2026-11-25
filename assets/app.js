// Vegas1 — tiny client-side helpers (no dependencies, works on GitHub Pages)
document.addEventListener('DOMContentLoaded',()=>{
  // Table search filter: input[data-filter] filters rows in the next table
  document.querySelectorAll('input[data-filter]').forEach(inp=>{
    const table=document.querySelector(inp.dataset.filter);
    if(!table) return;
    inp.addEventListener('input',()=>{
      const q=inp.value.toLowerCase();
      table.querySelectorAll('tbody tr').forEach(tr=>{
        tr.style.display=tr.textContent.toLowerCase().includes(q)?'':'none';
      });
    });
  });
  // 7-night calculator: nightly rate -> total with resort fee + tax (13.38% Strip, per sources)
  const rate=document.getElementById('nightlyRate'), fee=document.getElementById('resortFee'), nights=document.getElementById('nights'), out=document.getElementById('totalOut');
  function calc(){
    if(!rate||!out) return;
    const r=parseFloat(rate.value)||0, f=parseFloat(fee.value)||0, n=parseInt(nights.value)||7;
    const sub=(r+f)*n, tax=sub*0.1338, total=sub+tax;
    out.textContent=`7-night-style total (${n} nights): $${sub.toFixed(2)} + 13.38% tax $${tax.toFixed(2)} = $${total.toFixed(2)} for 2 adults. Verify resort fee on the official hotel page before booking.`;
  }
  [rate,fee,nights].forEach(el=>el&&el.addEventListener('input',calc)); calc();
  // Date-window checker: is the chosen check-in inside Feb 15–Mar 23 2027?
  const d=document.getElementById('checkin'), msg=document.getElementById('dateMsg');
  if(d&&msg){ d.addEventListener('change',()=>{
    const v=d.value; if(!v) return;
    const dt=new Date(v+'T12:00:00');
    const start=new Date('2027-02-15T12:00:00'), end=new Date('2027-03-23T12:00:00');
    const inWin=dt>=start&&dt<=end;
    const dow=dt.toLocaleDateString('en-US',{weekday:'long'});
    msg.innerHTML=inWin?`<span class="badge ok">Inside window</span> ${dow} ${v} — inside Feb 15–Mar 23 2027. Preferred start Feb 15–18. Avoid Feb 14 Super Bowl weekend pricing.`
      :`<span class="badge unverified">Outside window</span> ${dow} ${v} — outside Feb 15–Mar 23 2027.`;
  });}
});
