/*eslint no-unused-vars: ["error", { "vars": "local" }]*/
/* global $, $$ */  /* Bliss */
// var $ = require('jquery');
// require('foundation-sites');
// require('jquery');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.core');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.util.triggers');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.util.mediaQuery');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.util.keyboard');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.util.box');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.util.nest');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.responsiveToggle');
// require('imports?jQuery=jquery!foundation-sites/js/foundation.sticky');

import 'blissfuljs';
// import debounce from 'lodash/debounce';
// import {SwipeDetector} from './swipedetector';
// import smoothScroll from 'smoothscroll';


document.addEventListener('DOMContentLoaded', function initializeFooter() {
  /*
  $('footer .lid').addEventListener(
    'click', () => document.body.classList.toggle('footer-open'));
  */
});


/*
let pos = 0,
  slideCount;

document.addEventListener('DOMContentLoaded', () => { slideCount = $$('.slide').length; });

function slideBy(delta) {
  pos += delta;
  pos = Math.max(0, Math.min(slideCount - 1, pos));

  let slides = $('.slides');
  slides.style.webkitTransform = slides.style.mozTransform = slides.style.transform = `translate3d(0, -${pos*100}vh, 0)`;
}

const mouseWheelHandler = debounce((e) => {
  slideBy(Math.sign(-e.wheelDelta || e.deltaY || e.detail || 0));
}, 50);

document.addEventListener('DOMContentLoaded', () => {
  let slides = $('.slides');
  slides.addEventListener('wheel', mouseWheelHandler);
  slides.addEventListener('mousewheel', mouseWheelHandler);
  slides.addEventListener('onmousewheel', mouseWheelHandler);

  let detector = new SwipeDetector(slides);
  detector.emitter.on('up', () => slideBy(1));
  detector.emitter.on('down', () => slideBy(-1));
});
*/

/*
const snapToClosestSlide = debounce(function snapToClosestSlide() {
  let index = Math.floor(.5 + window.pageYOffset / $('.slide').scrollHeight);
  let slides = $$('.slide');

  // To last slide iff index invalid.
  smoothScroll(slides[index] || slides[slides.length - 1], 300);
}, 200);

window.addEventListener('resize', snapToClosestSlide);
window.addEventListener('scroll', (e) => { console.log(e, 'onscroll'); cancelSmoothScroll = true; snapToClosestSlide() });
document.addEventListener('DOMContentLoaded', snapToClosestSlide);




// ease in out function thanks to:
// http://blog.greweb.fr/2012/02/bezier-curve-based-easing-functions-from-concept-to-implementation/
function easeInOutCubic(t) {
  return t<.5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1;
}

var requestAnimationFrame = window.requestAnimationFrame ||
  window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame ||
  function(fn){window.setTimeout(fn, 15);};

function smoothScroll(el) {
  let start = window.pageYOffset,
    end = el.getBoundingClientRect().top + start,
    duration = 300,
    clock = Date.now();

  let step = function() {
    let elapsed = Date.now() - clock;

    window.scroll(0, start + (end - start) * easeInOutCubic(elapsed / duration));

    if (elapsed < duration && !cancelSmoothScroll) {
      requestAnimationFrame(step);
    }
  };

  cancelSmoothScroll = false;
  step();
}
let cancelSmoothScroll = false;
*/
