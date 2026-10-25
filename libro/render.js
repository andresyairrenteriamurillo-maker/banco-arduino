const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const dir=process.argv[2];const which=(process.argv[3]||'cover,body,back').split(',');
for(const n of which){const p=await b.newPage();
await p.goto('file://'+dir+'/'+n+'.html',{waitUntil:'load',timeout:600000});await p.waitForTimeout(800);
const opts={path:dir+'/'+n+'.pdf',format:'Letter',printBackground:true,timeout:0};
if(n==='body'){Object.assign(opts,{displayHeaderFooter:true,headerTemplate:'<span></span>',
 footerTemplate:'<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5px;color:#6B7785;padding:0 0.62in;display:flex;justify-content:space-between"><span>Banco Arduino · Ing. Jair Murillo · Libro 2026 – 2027</span><span style="font-weight:700;color:#16202E" class="pageNumber"></span></div>',
 margin:{top:'0.6in',bottom:'0.62in',left:'0.62in',right:'0.62in'}});}
else Object.assign(opts,{margin:{top:0,bottom:0,left:0,right:0}});
await p.pdf(opts);console.log('pdf',n);await p.close();}
await b.close();})();
