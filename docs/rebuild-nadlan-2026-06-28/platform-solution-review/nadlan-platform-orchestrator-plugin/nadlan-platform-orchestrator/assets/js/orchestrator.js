(function(){
  function loadTour(btn){
    var url = btn.getAttribute('data-nlpo-tour-url');
    if(!url) return;
    var box = btn.closest('[data-nlpo-interior]');
    var stage = box && box.querySelector('[data-nlpo-interior-stage]');
    if(!stage) return;
    var iframe = document.createElement('iframe');
    iframe.loading = 'lazy';
    iframe.allow = 'fullscreen; xr-spatial-tracking; gyroscope; accelerometer';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    iframe.src = url;
    stage.innerHTML = '';
    stage.appendChild(iframe);
  }
  document.addEventListener('click', function(e){
    var btn = e.target.closest('[data-nlpo-tour-url]');
    if(btn) loadTour(btn);
  });
})();
