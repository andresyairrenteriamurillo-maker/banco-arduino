// Prueba cada proyecto: arma el circuito, revisa errores y ejecuta el código
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{
 const [html, json, out, only] = process.argv.slice(2);
 let P=JSON.parse(fs.readFileSync(json,'utf8')); if (only) P=P.filter(p=>(p.titulo+"|"+p.cat).includes(only));
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const p=await b.newPage({viewport:{width:1300,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('dialog',d=>d.accept());
 await p.goto('file://'+html); await p.waitForTimeout(1200);
 await p.evaluate(()=>{document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='✕')b.click()}); localStorage.setItem('banco-arduino-vista','edit');});
 await p.click('[data-view=edit]');
 const res=[];
 for (const pr of P){
  errs.length=0;
  const r=await p.evaluate(pr=>{ try { return window.__banco.armar(pr); } catch(e){ return {err:String(e)} } }, pr);
  await p.waitForTimeout(150);
  const iss=await p.evaluate(()=>window.__banco.issues().filter(i=>i.lvl==='err'||i.lvl==='warn'));
  const pop=await p.evaluate(()=>{const e=document.querySelector('#pop');return e.hidden?'':e.textContent.replace(/\s+/g,' ').slice(0,200)});
  await p.evaluate(c=>window.__banco.setCode(c), pr.codigo);
  await p.evaluate(()=>{ const s=document.querySelector('#serial'); s.textContent=''; });
  await p.click('#run'); await p.waitForTimeout(1300);
  const diag=await p.evaluate(()=>{const d=document.querySelector('#diag');return d.hidden?'':d.innerText.replace(/\s+/g,' ')});
  const ser=await p.evaluate(()=>document.querySelector('#serial').textContent.trim().split('\n').slice(-2).join(' | '));
  const running=await p.evaluate(()=>document.querySelector('#run').textContent.includes('Detener'));
  if (running) await p.click('#run');
  const bad = !!(r.err || r.pinsChanged || iss.length || /revisa esto/.test(pop) || diag || errs.length);
  res.push({titulo:pr.titulo, bad, err:r.err, pinsChanged:r.pinsChanged, iss, pop:/revisa esto/.test(pop)?pop:'', diag, ser, pageErr:errs.slice()});
  console.log((bad?'✗ ':'✓ ')+pr.titulo+(bad?'  '+JSON.stringify({err:r.err,pins:r.pinsChanged,iss:iss.map(i=>i.msg),pop:/revisa esto/.test(pop)?pop:'',diag,page:errs}):'  » '+ser.slice(0,80)));
 }
 fs.writeFileSync(out, JSON.stringify(res,null,1));
 console.log('MAL:', res.filter(x=>x.bad).length, 'de', res.length);
 await b.close();
})();
