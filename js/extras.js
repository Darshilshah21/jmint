(function(){
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// scroll progress + cursor glow
var pb=document.createElement('div');pb.className='progress';document.body.appendChild(pb);
window.addEventListener('scroll',function(){var h=document.documentElement;pb.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight||1)*100)+'%';},{passive:true});
var gl=document.createElement('div');gl.className='glow';document.body.appendChild(gl);
window.addEventListener('mousemove',function(e){gl.style.left=e.clientX+'px';gl.style.top=e.clientY+'px';},{passive:true});
// card tilt
if(!reduce&&window.matchMedia('(hover:hover)').matches){document.querySelectorAll('.card,.techcat,.stat').forEach(function(c){
  c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(700px) rotateY('+x*5+'deg) rotateX('+(-y*5)+'deg)';});
  c.addEventListener('mouseleave',function(){c.style.transform='';});});}
// counters
var cn=document.querySelectorAll('[data-count]');
if(cn.length&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;io.unobserve(e.target);
  var el=e.target,to=parseFloat(el.getAttribute('data-count')),pre=el.getAttribute('data-pre')||'',suf=el.getAttribute('data-suf')||'',t0=null;
  function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1400);el.textContent=pre+Math.round(to*(1-Math.pow(1-p,3)))+suf;if(p<1)requestAnimationFrame(f);}requestAnimationFrame(f);});},{threshold:.4});
  cn.forEach(function(el){io.observe(el);});}
// zig-zag train on a responsive track
var sc=document.querySelector('.rail-scene');
if(sc){var cars=[].slice.call(sc.querySelectorAll('.cars>a')),svg=sc.querySelector('svg.track');
  if(reduce){sc.classList.add('static');cars.forEach(function(c){c.style.opacity=1;});}
  else{var W,H,L,path,cw,gap,t=0,paused=false,last=0,sp=70;
    function build(){W=sc.clientWidth;H=sc.clientHeight;cw=W<620?150:196;sc.style.setProperty('--cw',cw+'px');gap=cw+16;
      var seg=Math.max(260,W/3),amp=H*.13,mid=H*.58,d='',x=-60,k=0;
      while(x<W+seg){d+=(k?' L':'M')+x+' '+(mid+(k%2?-amp:amp));x+=seg;k++;}
      svg.setAttribute('viewBox','0 0 '+W+' '+H);
      svg.innerHTML='<path class="sl" d="'+d+'"/><path class="rl" d="'+d+'" transform="translate(0 -7)"/><path class="rl" d="'+d+'" transform="translate(0 7)"/>';
      path=svg.querySelector('.sl');L=path.getTotalLength();}
    function frame(now){var dt=Math.min(.05,(now-last)/1000);last=now;if(!paused)t+=sp*dt;
      var cyc=Math.max(L+gap,cars.length*gap);
      for(var i=0;i<cars.length;i++){var p=(((t-i*gap)%cyc)+cyc)%cyc,c=cars[i];
        if(p>L){c.style.opacity=0;continue;}
        var a=path.getPointAtLength(Math.max(0,p-34)),b=path.getPointAtLength(Math.min(L,p+34)),m=path.getPointAtLength(p),ang=Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI;
        c.style.transform='translate('+(m.x-cw/2)+'px,'+(m.y-35-14)+'px) rotate('+ang+'deg)';c.style.opacity=1;}
      requestAnimationFrame(frame);}
    build();window.addEventListener('resize',build);
    sc.addEventListener('mouseenter',function(){paused=true;});sc.addEventListener('mouseleave',function(){paused=false;});
    sc.addEventListener('touchstart',function(){paused=true;},{passive:true});sc.addEventListener('touchend',function(){setTimeout(function(){paused=false;},1800);});
    requestAnimationFrame(function(n){last=n;frame(n);});}}
// live avatar demo
var demo=document.getElementById('avatar-demo');
if(demo){var says=demo.querySelector('.says'),QA={
 pricing:'Our projects are fixed price. A focused prototype usually starts in the lower budget band, and I can book a call so an engineer can size yours properly.',
 data:'Your documents stay in your own environment. I can answer from your manuals and always show which page an answer came from, and I will say so when I do not know.',
 time:'Most pilots are live in six to twelve weeks. You see a working demo every second week, so nothing is a surprise at the end.',
 human:'Of course. I will pass you to a team member along with a short summary of this chat, so you do not need to repeat yourself.'},timer;
 function speak(k){clearInterval(timer);var s=QA[k],i=0;says.textContent='';demo.classList.add('talking');
  timer=setInterval(function(){says.textContent=s.slice(0,++i);if(i>=s.length){clearInterval(timer);demo.classList.remove('talking');}},28);
  if(demo.querySelector('#voice').checked&&'speechSynthesis' in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(s));}}
 demo.querySelectorAll('[data-q]').forEach(function(b){b.addEventListener('click',function(){speak(b.getAttribute('data-q'));});});}
// ROI calculator
var calc=document.getElementById('roi-calc');
if(calc){var f=function(){var h=+calc.hrs.value,r=+calc.rate.value,p=+calc.pct.value,ppl=+calc.ppl.value;
  calc.querySelector('[for-o=hrs]').textContent=h+' h';calc.querySelector('[for-o=rate]').textContent=r;calc.querySelector('[for-o=pct]').textContent=p+'%';calc.querySelector('[for-o=ppl]').textContent=ppl;
  var yr=h*r*(p/100)*ppl*52,fmt=function(n){return n>=1e5?(n/1e5).toFixed(1)+' lakh':Math.round(n).toLocaleString('en-IN');};
  calc.querySelector('#roi-out').textContent=fmt(yr);calc.querySelector('#roi-hrs').textContent=Math.round(h*(p/100)*ppl*52).toLocaleString('en-IN')+' hours';};
  calc.addEventListener('input',f);f();}
})();
