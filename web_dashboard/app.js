'use strict';
const themeToggle=document.getElementById('theme-toggle');
function applyTheme(theme){document.documentElement.dataset.theme=theme;themeToggle.setAttribute('aria-checked',String(theme==='dark'));}
applyTheme(document.documentElement.dataset.theme==='light'?'light':'dark');
themeToggle.addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';applyTheme(theme);BLUE=theme==='dark'?'#8bbfe8':'#245c88';ORANGE=theme==='dark'?'#efb86f':'#a95b12';if(allRows.length)render();try{localStorage.setItem('insurance-theme',theme)}catch{}});

const REGIONS=['northeast','northwest','southeast','southwest'];
const SMOKERS=['no','yes'];
const smokingName=value=>value==='yes'?'Smokers':'Non-smokers';
const smokingGroup=value=>value==='yes'?'smoking':'non-smoking';
const BANDS=['18-29','30-44','45-59','60-64'];
let BLUE=document.documentElement.dataset.theme==='dark'?'#8bbfe8':'#245c88';
let ORANGE=document.documentElement.dataset.theme==='dark'?'#efb86f':'#a95b12';
const fmt=n=>n.toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2});
const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
const quantile=(a,p)=>{const s=[...a].sort((a,b)=>a-b),i=(s.length-1)*p,l=Math.floor(i);return s[l]+(s[Math.ceil(i)]-s[l])*(i-l)};
function stats(rows){const a=rows.map(r=>r.charges),m=mean(a);return {n:a.length,mean:m,median:quantile(a,.5),sd:a.length>1?Math.sqrt(a.reduce((s,v)=>s+(v-m)**2,0)/(a.length-1)):NaN}}
let allRows=[];
for(const [id,values] of [['regions',REGIONS],['smokers',SMOKERS],['bands',BANDS]]){
 document.getElementById(id).innerHTML=values.map(v=>`<label><input type="checkbox" value="${v}" checked>${id==='smokers'?smokingName(v):v}</label>`).join('');
 document.getElementById(id).addEventListener('change',render);
}
document.getElementById('reset').addEventListener('click',()=>{document.querySelectorAll('input').forEach(c=>c.checked=true);render()});
const selected=id=>[...document.querySelectorAll(`#${id} input:checked`)].map(c=>c.value);
function shell(id,title,width,height,inner){document.getElementById(id).innerHTML=`<svg role="img" aria-label="${title}" viewBox="0 0 ${width} ${height}"><title>${title}</title>${inner}</svg>`}
function base(w,h,xlabel,ymax){let s='';const l=60,r=w-20,t=20,b=h-56;for(let i=0;i<=4;i++){let y=b-(b-t)*i/4;s+=`<path class="guide" d="M${l},${y}H${r}"/><text class="tick" x="${l-8}" y="${y+4}" text-anchor="end">${Math.round(ymax*i/4).toLocaleString('en-GB')}</text>`}s+=`<path class="axis" d="M${l},${t}V${b}H${r}"/><text x="${(l+r)/2}" y="${h-5}" text-anchor="middle">${xlabel}</text>`;return {s,l,r,t,b,y:v=>b-(b-t)*v/ymax}}
function histogram(rows){const w=550,h=320,a=rows.map(r=>r.charges),min=Math.min(...a),max=Math.max(...a),step=(max-min||1)/30;let bins=Array(30).fill(0);a.forEach(v=>bins[Math.min(29,Math.floor((v-min)/step))]++);const p=base(w,h,'Recorded charges (USD)',Math.max(...bins)*1.1);let s=p.s;bins.forEach((v,i)=>{const x=p.l+(p.r-p.l)*i/30,bw=(p.r-p.l)/30;s+=`<rect x="${x}" y="${p.y(v)}" width="${bw-.7}" height="${p.b-p.y(v)}" fill="${BLUE}"><title>${fmt(min+i*step)} to ${fmt(min+(i+1)*step)}: ${v} records</title></rect>`});[0,.5,1].forEach(k=>s+=`<text x="${p.l+(p.r-p.l)*k}" y="${p.b+20}" text-anchor="middle">${Math.round(min+(max-min)*k).toLocaleString('en-GB')}</text>`);const mx=p.l+(p.r-p.l)*(quantile(a,.5)-min)/(max-min||1);s+=`<path d="M${mx},${p.t}V${p.b}" stroke="var(--text)" stroke-dasharray="5 4"/>`;shell('hist','Distribution of recorded charges; vertical axis is record count',w,h,s)}
function boxplot(rows){const w=550,h=320,p=base(w,h,'Smoking status',Math.max(...rows.map(r=>r.charges))*1.1);let s=p.s;SMOKERS.forEach((g,i)=>{const a=rows.filter(r=>r.smoker===g).map(r=>r.charges),x=p.l+(p.r-p.l)*(i+.5)/2,c=i?ORANGE:BLUE;if(!a.length){s+=`<text x="${x}" y="${p.b+20}" text-anchor="middle">${smokingName(g)}</text>`;return}const q1=quantile(a,.25),q3=quantile(a,.75),med=quantile(a,.5),iqr=q3-q1,inside=a.filter(v=>v>=q1-1.5*iqr&&v<=q3+1.5*iqr),low=Math.min(...inside),high=Math.max(...inside);s+=`<path d="M${x},${p.y(high)}V${p.y(low)} M${x-25},${p.y(high)}H${x+25} M${x-25},${p.y(low)}H${x+25}" stroke="${c}"/><rect x="${x-50}" y="${p.y(q3)}" width="100" height="${Math.max(1,p.y(q1)-p.y(q3))}" fill="${c}" fill-opacity=".23" stroke="${c}"/><path d="M${x-50},${p.y(med)}H${x+50}" stroke="${c}" stroke-width="2"/>`;a.filter(v=>v<low||v>high).forEach(v=>s+=`<circle cx="${x}" cy="${p.y(v)}" r="2" fill="${c}" fill-opacity=".5"/>`);s+=`<text x="${x}" y="${p.b+20}" text-anchor="middle">${smokingName(g)}</text>`});shell('box','Charge distributions by smoking status; vertical axis is recorded charges',w,h,s)}
function regions(rows){const w=1050,h=300,groups=REGIONS.map(g=>({g,rows:rows.filter(r=>r.region===g)})).filter(g=>g.rows.length).map(g=>({...g,...stats(g.rows)})),p=base(w,h,'Region',Math.max(...groups.flatMap(g=>[g.mean,g.median]))*1.18);let s=p.s;groups.forEach((g,i)=>{const x=p.l+(p.r-p.l)*(i+.5)/groups.length,bw=Math.min(70,(p.r-p.l)/groups.length*.28);for(const [v,dx,c] of [[g.mean,-bw,BLUE],[g.median,0,ORANGE]])s+=`<rect x="${x+dx}" y="${p.y(v)}" width="${bw-2}" height="${p.b-p.y(v)}" fill="${c}"><title>${g.g}: ${fmt(v)}</title></rect>`;s+=`<text x="${x}" y="${p.b+18}" text-anchor="middle">${g.g}</text><text class="tick" x="${x}" y="${p.b+33}" text-anchor="middle">${g.n} records</text>`});shell('regionchart','Mean and median charges by region; vertical axis is recorded charges',w,h,s)}
function scatter(rows,key,id){const w=550,h=320,a=rows.map(r=>r[key]),min=Math.min(...a),max=Math.max(...a),p=base(w,h,key==='age'?'Age (years)':'BMI (kg/m²)',Math.max(...rows.map(r=>r.charges))*1.1);let s=p.s;rows.forEach(r=>{const x=p.l+5+(p.r-p.l-10)*(r[key]-min)/(max-min||1),y=p.y(r.charges),c=r.smoker==='yes'?ORANGE:BLUE,tip=`${key}=${r[key]}, charges=USD ${fmt(r.charges)}, ${smokingName(r.smoker)}`;s+=r.smoker==='yes'?`<path d="M${x},${y-3}l3,6h-6z" fill="${c}" opacity=".55"><title>${tip}</title></path>`:`<circle cx="${x}" cy="${y}" r="2.5" fill="${c}" opacity=".45"><title>${tip}</title></circle>`});[0,.5,1].forEach(k=>s+=`<text x="${p.l+5+(p.r-p.l-10)*k}" y="${p.b+20}" text-anchor="middle">${(min+(max-min)*k).toFixed(key==='age'?0:1)}</text>`);shell(id,`${key} and recorded charges; circles represent non-smokers and triangles smokers; vertical axis is charges`,w,h,s)}
function comparison(rows,key,categories,id,splitSmoking=false){
 const w=1050,h=340,groups=categories.map(g=>({g,rows:rows.filter(r=>r[key]===g)})).filter(g=>g.rows.length).map(g=>{const z=stats(g.rows);return {...g,...z,series:splitSmoking?SMOKERS.map(sm=>{const part=g.rows.filter(r=>r.smoker===sm);return part.length?{value:stats(part).mean,n:part.length}:null}):[{value:z.mean,n:z.n},{value:z.median,n:z.n}]}});
 const max=Math.max(...groups.flatMap(g=>g.series.filter(Boolean).map(z=>z.value))),p=base(w,h,key==='children'?'Covered dependants':key==='sex'?'Source sex label':'Smoking status',max*1.3);let out=p.s;
 groups.forEach((g,i)=>{const x=p.l+(p.r-p.l)*(i+.5)/groups.length,bw=Math.min(100,(p.r-p.l)/groups.length*.35);g.series.forEach((z,j)=>{if(!z)return;const bx=x+(j-1)*bw,c=j?ORANGE:BLUE;out+=`<rect x="${bx}" y="${p.y(z.value)}" width="${bw-3}" height="${p.b-p.y(z.value)}" fill="${c}"><title>${g.g}: ${splitSmoking?smokingName(SMOKERS[j]):j?'median':'mean'}: $${fmt(z.value)}</title></rect><text class="tick" x="${bx+(bw-3)/2}" y="${p.y(z.value)-8}" text-anchor="middle">${fmt(z.value)}</text>`;if(splitSmoking)out+=`<text class="tick" x="${bx+(bw-3)/2}" y="${p.y(z.value)-23}" text-anchor="middle">${z.n} records</text>`});out+=`<text x="${x}" y="${p.b+19}" text-anchor="middle">${key==='smoker'?smokingName(g.g):g.g}</text>${splitSmoking?'':`<text class="tick" x="${x}" y="${p.b+34}" text-anchor="middle">${g.n} records</text>`}`});shell(id,key==='sex'?'Mean charges by sex and smoking status':key==='smoker'?'Mean and median charges by smoking status':'Mean and median charges by dependant count',w,h,out)
}

function correlation(rows,key){
 if(rows.length<3)return null;
 const x=rows.map(r=>r[key]),y=rows.map(r=>r.charges),mx=mean(x),my=mean(y);
 const xx=x.reduce((s,v)=>s+(v-mx)**2,0),yy=y.reduce((s,v)=>s+(v-my)**2,0);
 if(!xx||!yy)return null;
 return x.reduce((s,v,i)=>s+(v-mx)*(y[i]-my),0)/Math.sqrt(xx*yy);
}
function explainCharts(rows){
 const put=(id,text)=>document.getElementById(id+'-explanation').textContent=text;
 const overall=stats(rows),no=rows.filter(r=>r.smoker==='no'),yes=rows.filter(r=>r.smoker==='yes');
 if(no.length&&yes.length){
  const a=stats(no),b=stats(yes),gap=b.mean-a.mean;
  put('smokingcomparison',`The ${gap>=0?'smoking':'non-smoking'} group has higher average charges, with a gap of $${fmt(Math.abs(gap))}. ${a.mean>0?'Smokers’ mean charges are '+(b.mean/a.mean).toFixed(2)+' times those of non-smokers. ':''}This is an observed group difference, not an estimate of what smoking adds to an individual's costs.`);
  put('box',`The boxes show the middle half of each group's charges. ${b.median>a.median?'The higher median for smokers shows that the difference extends to typical records, rather than only a few very high charges.':b.median<a.median?'The median is higher among non-smokers in this selection, so the middle of each distribution adds context beyond the averages.':'The medians coincide in this selection; the width of each distribution still shows how much individual charges vary.'}`);
 }else{
  const label=yes.length?'smokers':'non-smokers';
  put('smokingcomparison',`Only ${label} are selected. Select both smoking groups to compare their charges.`);
  put('box','The box shows how much charges vary within the selected group; the centre line marks the median.');
 }
 const difference=overall.mean-overall.median;
 put('hist',difference>0?'Higher charges pull the mean above the median. The average therefore exceeds the charge of the middle record, so the median is useful when describing a typical record.':difference<0?'The mean falls below the median. The distribution adds context that a single average would miss.':'The mean and median coincide here; the distribution shows the variation around them.');
 const rg=REGIONS.map(g=>({g,part:rows.filter(r=>r.region===g)})).filter(g=>g.part.length).map(g=>({...g,...stats(g.part)}));
 const topMean=[...rg].sort((a,b)=>b.mean-a.mean)[0],topMedian=[...rg].sort((a,b)=>b.median-a.median)[0];
 const title=s=>s.charAt(0).toUpperCase()+s.slice(1);
 put('regionchart',rg.length>1?`${title(topMean.g)} has the highest mean; ${topMedian.g} has the highest median. ${topMean.g===topMedian.g?'Both measures rank the same region first.':'Different rankings show that the region with the largest average is not necessarily the one with the largest typical charge.'} Population mix can influence these comparisons.`:`Only ${topMean.g} is selected. Add other regions to make a geographic comparison.`);
 for(const [key,id] of [['age','agechart'],['bmi','bmichart']]){
  const r=correlation(rows,key),label=key==='age'?'age':'BMI';
  let text=r===null?`There is not enough variation or enough records to summarise the ${label}–charge relationship.`:Math.abs(r)<.15?`${key==='age'?'Age':'BMI'} shows little overall linear relationship with charges (correlation ${r.toFixed(2)}).`:`${r>0?'Higher':'Lower'} ${label} tends to accompany higher charges (correlation ${r.toFixed(2)}).`;
  const rn=correlation(no,key),ry=correlation(yes,key);
  if(rn!==null&&ry!==null){text+=` The correlation is ${rn.toFixed(2)} among non-smokers and ${ry.toFixed(2)} among smokers. `;text+=Math.abs(rn-ry)>.25?'Separating the groups reveals a pattern that the overall result can hide.':'The markers show how the pattern varies within each smoking group.';}
  else text+=' The spread shows that this variable alone does not explain individual charges.';
  put(id,text);
 }
 const comparisons=[];
 for(const sm of SMOKERS){const f=rows.filter(r=>r.sex==='female'&&r.smoker===sm),m=rows.filter(r=>r.sex==='male'&&r.smoker===sm);if(f.length&&m.length){const d=stats(f).mean-stats(m).mean;comparisons.push({sm,d});}}
 let text='';
 if(comparisons.length){text=comparisons.map(c=>`Among ${c.sm==='yes'?'smokers':'non-smokers'}, ${c.d>0?'female-labelled records have higher average charges than male-labelled records':c.d<0?'male-labelled records have higher average charges than female-labelled records':'both sex groups have the same average charges'}.`).join(' ');if(comparisons.length===2&&comparisons[0].d*comparisons[1].d<0)text+=' The direction reverses between smoking groups, so one overall sex comparison would hide an important difference.';else text+=' Comparing within smoking groups helps separate these patterns from differences in smoking-group mix.';}
 else text='The selection does not contain both sex labels within a smoking group. Widen the filters to compare them.';
 put('sexcomparison',text);
 const cg=[0,1,2,3,4,5].map(g=>({g,part:rows.filter(r=>r.children===g)})).filter(g=>g.part.length).map(g=>({...g,...stats(g.part)}));
 if(cg.length>1){const rising=cg.slice(1).every((g,i)=>g.mean>=cg[i].mean),small=cg.filter(g=>g.n<30);put('childrencomparison',(rising?'Means increase across the selected categories, but this does not establish that each extra dependant raises charges.':'Average charges do not rise consistently with dependant count, so there is no simple “more dependants, higher charges” pattern.')+(small.length?' The smaller groups shown in the chart should be interpreted cautiously.':''));}else put('childrencomparison',`Only the ${cg[0].g}-dependant category appears. Widen the filters to compare dependant counts.`);
 put('groups','Compare regions within each smoking group to see whether the overall regional pattern remains. These comparisons still do not control for age, BMI or clinical needs.');
}

function render(){const rs=selected('regions'),ss=selected('smokers'),bs=selected('bands'),rows=allRows.filter(r=>rs.includes(r.region)&&ss.includes(r.smoker)&&bs.includes(r.age_band));document.getElementById('results').hidden=!rows.length;document.getElementById('empty').hidden=!!rows.length;if(!rows.length)return;const s=stats(rows);document.getElementById('count').textContent=s.n.toLocaleString('en-GB');document.getElementById('mean').textContent=fmt(s.mean);document.getElementById('median').textContent=fmt(s.median);document.getElementById('warning').hidden=s.n>=30;comparison(rows,'smoker',SMOKERS,'smokingcomparison');comparison(rows,'sex',['female','male'],'sexcomparison',true);comparison(rows,'children',[0,1,2,3,4,5],'childrencomparison');histogram(rows);boxplot(rows);regions(rows);scatter(rows,'age','agechart');scatter(rows,'bmi','bmichart');let body='';for(const region of REGIONS)for(const smoker of SMOKERS){const g=rows.filter(r=>r.region===region&&r.smoker===smoker);if(!g.length)continue;const z=stats(g);body+=`<tr><td>${region}</td><td>${smokingName(smoker)}</td><td>${z.n}</td><td>${fmt(z.mean)}</td><td>${fmt(z.median)}</td><td>${Number.isNaN(z.sd)?'—':fmt(z.sd)}</td></tr>`}document.getElementById('groups').innerHTML=body;explainCharts(rows)}
fetch('data.json').then(r=>{if(!r.ok)throw Error('Dataset download failed.');return r.json()}).then(rows=>{if(rows.length!==1338||rows.some(r=>!Number.isFinite(r.charges)))throw Error('Dataset validation failed.');allRows=rows;render()}).catch(err=>{document.getElementById('results').hidden=true;const el=document.getElementById('error');el.hidden=false;el.textContent='The dataset could not be loaded. '+err.message});
