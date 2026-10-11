(function(){
  // mobile menu
  var burger=document.querySelector('.burger'),menu=document.querySelector('.menu');
  if(burger){burger.addEventListener('click',function(){
    var o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o);
  });}
  document.querySelectorAll('.has-dd>button').forEach(function(b){
    b.addEventListener('click',function(){
      var li=b.parentElement,o=li.classList.toggle('open');b.setAttribute('aria-expanded',o);
    });
  });
  document.addEventListener('click',function(e){
    document.querySelectorAll('.has-dd.open').forEach(function(li){if(!li.contains(e.target)&&window.innerWidth>820){li.classList.remove('open');}});
  });

  // reveal on scroll
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12});
    rv.forEach(function(el){io.observe(el);});
  }else{rv.forEach(function(el){el.classList.add('in');});}

  // project filters
  var fb=document.querySelectorAll('.filters button');
  fb.forEach(function(b){b.addEventListener('click',function(){
    fb.forEach(function(x){x.classList.remove('on');});b.classList.add('on');
    var f=b.getAttribute('data-f');
    document.querySelectorAll('[data-cat]').forEach(function(p){
      p.style.display=(f==='all'||p.getAttribute('data-cat')===f)?'':'none';
    });
  });});

  // contact form -> opens visitor's email app (static site, no server needed)
  var form=document.getElementById('contact-form');
  if(form){form.addEventListener('submit',function(e){
    e.preventDefault();
    var d=new FormData(form),to=form.getAttribute('data-to');
    var body='Name: '+d.get('name')+'\nEmail: '+d.get('email')+'\nService: '+d.get('service')+'\nBudget: '+d.get('budget')+'\n\n'+d.get('message');
    window.location.href='mailto:'+to+'?subject='+encodeURIComponent('Project enquiry – '+d.get('service'))+'&body='+encodeURIComponent(body);
  });}

  // hero network animation (light, colourful)
  var c=document.getElementById('net');
  if(c&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    var x=c.getContext('2d'),W,H,P=[],cols=['#3b82f6','#7c5cf0','#ec5fa5','#2e8b3d'];
    function size(){W=c.width=c.offsetWidth;H=c.height=c.offsetHeight;
      var n=Math.min(60,Math.round(W*H/22000));P=[];
      for(var i=0;i<n;i++)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.4,vy:(Math.random()-.5)*.4,c:cols[i%4],r:2+Math.random()*2.5});}
    function tick(){
      x.clearRect(0,0,W,H);
      for(var i=0;i<P.length;i++){var p=P[i];p.x+=p.vx;p.y+=p.vy;
        if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;
        for(var j=i+1;j<P.length;j++){var q=P[j],dx=p.x-q.x,dy=p.y-q.y,d=dx*dx+dy*dy;
          if(d<19000){x.strokeStyle='rgba(124,92,240,'+(.22*(1-d/19000))+')';x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);x.stroke();}}
        x.fillStyle=p.c;x.globalAlpha=.6;x.beginPath();x.arc(p.x,p.y,p.r,0,6.283);x.fill();x.globalAlpha=1;}
      requestAnimationFrame(tick);}
    size();tick();window.addEventListener('resize',size);
  }
})();
