const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const p=await b.newPage({viewport:{width:1400,height:950},deviceScaleFactor:1.3});p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file:///home/claude/banco-arduino/index.html');await p.waitForTimeout(2500);
await p.evaluate(()=>document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='✕')b.click()}));
const CSSX='.chispa{display:none!important}.gfocus{filter:none!important;animation:none!important}#isoLabels,#isoBar,#isoTip,.pop,.iso .leads,.iso .hint,.iso .run{display:none!important}.iso,.mat{background:#fff!important}';await p.addStyleTag({content:CSSX});let done=0;
let P=JSON.parse(fs.readFileSync('proyectos_libro.json','utf8'));
const from=+(process.argv[2]||0), to=+(process.argv[3]||P.length);
const PF=`plans_${from}.json`;const plans=fs.existsSync(PF)?JSON.parse(fs.readFileSync(PF,'utf8')):{};
// catálogo y vista vacía
if(from===0&&!fs.existsSync('img/empty3d.png')){
  await p.click('[data-view=edit]');await p.waitForTimeout(400);
  await p.locator('#scene').screenshot({path:'img/empty2d.png'});
  await p.click('[data-view=iso]');await p.waitForTimeout(2000);
  await p.locator('#iso').screenshot({path:'img/empty3d.png'});
  const types=['led','rgb','button','switch','pot','buzzer','ldr','servo','motor','relay','lm35','dht11','sonar','pir','lcd','oled','keypad','huella','rfid','lock12','pump12','supply12','joystick','llama','obstaculo','sonido','inclinacion','vibracion','hall','tactil','suelo','gas','lluvia','nivel','acs712'];
  await p.click('[data-view=hub]');await p.waitForTimeout(500);
  for(const t of types){ const u=await p.evaluate(t=>window.__bancoThumb&&window.__bancoThumb(t, t==='led'?'rojo':undefined, 480),t); if(u) fs.writeFileSync('img/cat_'+t+'.png',Buffer.from(u.split(',')[1],'base64')); else console.log('sin thumb',t); }
}
const shot=async(sel,path)=>{try{await p.locator(sel).screenshot({path,animations:'disabled',timeout:40000});}catch(e){await p.waitForTimeout(1500);await p.locator(sel).screenshot({path,animations:'disabled',timeout:60000});}};
for(let i=from;i<Math.min(to,P.length);i++){
  const pr=P[i];
  try{
  if(plans[pr.titulo]&&fs.existsSync(`img/p${i}_3d.png`)) continue;
  const T0=Date.now();
  if((++done)%6===0){await p.reload();await p.waitForTimeout(2200);await p.evaluate(()=>document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='✕')b.click()}));await p.addStyleTag({content:CSSX});}
  await p.click('[data-view=edit]');await p.waitForTimeout(300);
  const r=await p.evaluate(pp=>window.__banco.armar(pp),pr);
  await p.waitForTimeout(700);
  plans[pr.titulo]=await p.evaluate(()=>window.__banco.planHTML());
  await shot('#scene',`img/p${i}_2d.png`);
  const T1=Date.now();
  await p.click('[data-view=iso]');await p.waitForTimeout(1600);const T2=Date.now();
  await shot('#iso',`img/p${i}_3d.png`);
  if(process.env.T) console.log('t',T1-T0,T2-T1,Date.now()-T2);
  }catch(e){console.log('FALLO',i,e.message.slice(0,120));}
  if(i%5==0){console.log(i,pr.titulo);fs.writeFileSync(PF,JSON.stringify(plans));}
}
fs.writeFileSync(PF,JSON.stringify(plans));
await b.close();})();
