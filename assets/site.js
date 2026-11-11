document.body.classList.remove('no-js');
var tr=document.getElementById('rTrack');if(tr){function step(d){var c=tr.querySelector('.rcard');tr.scrollBy({left:d*(c.offsetWidth+18)*(innerWidth>900?2:1),behavior:'smooth'})}
document.getElementById('rPrev').onclick=function(){step(-1)};document.getElementById('rNext').onclick=function(){step(1)};}
document.getElementById('yr').textContent=new Date().getFullYear();
var nav=document.getElementById('nav');
function onScroll(){nav.classList.toggle('solid',window.scrollY>40)}
onScroll();addEventListener('scroll',onScroll,{passive:true});
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
  document.querySelectorAll('.rv').forEach(function(el,i){el.style.transitionDelay=(i%3)*80+'ms';io.observe(el)});
  var bar=document.getElementById('bar'),cta=document.getElementById('heroCta'),contact=document.getElementById('contact');
  var vis={cta:true,contact:false};
  function upd(){bar.classList.toggle('show',!vis.cta&&!vis.contact)}
  new IntersectionObserver(function(e){vis.cta=e[0].isIntersecting;upd()}).observe(cta);
  new IntersectionObserver(function(e){vis.contact=e[0].isIntersecting;upd()},{threshold:.25}).observe(contact);
}else{document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')})}
function linkInfo(a){var sec=a.closest('[id]'),h=a.querySelector('h3,h4,small');return{link_location:sec?sec.id:'page',link_label:h?h.textContent:a.textContent.trim().replace(/\s+/g,' ')}}
function track(name,data){if(typeof gtag=='function')gtag('event',name,data)}
document.addEventListener('click',function(e){
  var a=e.target.closest('a[href*="wa.me"],a[href^="tel:"]');if(!a)return;
  track(a.href.indexOf('wa.me')>-1?'whatsapp_click':'call_click',linkInfo(a));
});

/* After hours (10 pm - 7 am IST): show business hours before opening WhatsApp. Add ?afterhours=1 to the URL to test. */
(function(){
  var dlg=document.getElementById('ahDialog');if(!dlg||typeof dlg.showModal!='function')return;
  var QUIET_FROM=22*60,QUIET_TO=7*60,pending=null;
  function istMinutes(){var d=new Date();return(d.getUTCHours()*60+d.getUTCMinutes()+330)%1440}
  function istTime(){var m=istMinutes();return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0')}
  function isAfterHours(){if(/[?&]afterhours=1\b/.test(location.search))return true;var m=istMinutes();return m>=QUIET_FROM||m<QUIET_TO}
  // Called when a visitor decides not to message after hours. Hook the admin-panel API in here later.
  function recordEnquiry(info){track('after_hours_enquiry',Object.assign({ist_time:istTime()},info))}
  function channel(a){return a.href.indexOf('tel:')===0?'call':'whatsapp'}
  document.addEventListener('click',function(e){
    var a=e.target.closest('a[href*="wa.me"],a[href^="tel:"]');if(!a||!isAfterHours())return;
    var call=a.href.indexOf('tel:')===0;
    document.getElementById('ahMsg').textContent=call?'We may not be able to answer right now. We’ll get back to you as soon as we can.':'You can still send your message now. We’ll reply as soon as we can.';
    document.getElementById('ahSend').textContent=call?'Call anyway':'Send on WhatsApp anyway';
    document.getElementById('ahIcon').setAttribute('href',call?'#i-phone':'#i-wa');
    e.preventDefault();e.stopPropagation();
    pending=a;
    dlg.showModal();
  },true);
  function finish(choice){
    if(!pending)return;var a=pending,info=Object.assign({channel:channel(a)},linkInfo(a));pending=null;dlg.close();
    if(choice==='send'){
      track(info.channel==='call'?'call_click':'whatsapp_click',Object.assign({after_hours:true},info));
      if(a.target==='_blank')window.open(a.href,'_blank','noopener');else location.href=a.href;
    }else recordEnquiry(info);
  }
  dlg.addEventListener('click',function(e){var b=e.target.closest('[data-ah]');if(b)finish(b.getAttribute('data-ah'));else if(e.target===dlg)finish('later')});
  dlg.addEventListener('cancel',function(e){e.preventDefault();finish('later')});
})();

/* FAQ accordion: only one answer open at a time (fallback for browsers without <details name>) */
document.querySelectorAll('.faq').forEach(function(list){
  list.addEventListener('toggle',function(e){
    var d=e.target;if(!d.open)return;
    list.querySelectorAll('details[open]').forEach(function(o){if(o!==d)o.open=false});
  },true);
});
