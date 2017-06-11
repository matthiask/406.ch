import './main.scss';

import 'blissfuljs';
const {$, $$} = window;

import {EditorState} from 'prosemirror-state';
import {EditorView} from 'prosemirror-view';
import {schema} from 'prosemirror-schema-basic';
import {DOMParser} from 'prosemirror-model';
// import {keymap} from 'prosemirror-keymap';
// import {baseKeymap} from 'prosemirror-commands';
// import {history} from 'prosemirror-history';
import {exampleSetup} from 'prosemirror-example-setup';
import debounce from 'lodash.debounce';

import 'prosemirror-example-setup/style/style.css';
import 'prosemirror-view/style/prosemirror.css';
import 'prosemirror-menu/style/menu.css';


document.addEventListener('DOMContentLoaded', function() {
  $$('.content').forEach((element) => {

    let editor = $.before($.create('div', {
      className: 'editor',
    }), element);

    const state = EditorState.create({
      doc: DOMParser.fromSchema(schema).parse(element),
      plugins: exampleSetup({
        schema: schema,
        menuBar: true,
        floatingMenu: true,
      }),
    });
    const view = new EditorView(editor, {
      state: state,
      dispatchTransaction(tr) {
        view.updateState(view.state.apply(tr));
        postBack();
      },
    });

    /*
    import {DOMSerializer} from 'prosemirror-model';

    const xs = new XMLSerializer(),
      ds = DOMSerializer.fromSchema(schema);

    window.serialize = function() {
      let html = xs.serializeToString(ds.serializeFragment(state.doc.content));
      window.console.log(html);
    };
    */

    window.serialize = function() {
      window.console.log($('.editor [contenteditable]').innerHTML);
    };

    const postBack = debounce(function() {
      let fd = new FormData();
      fd.append('content', $('.editor [contenteditable]').innerHTML);
      fetch('.', {
        credentials: 'include',
        method: 'POST',
        body: fd,
        headers: {
          'X-CSRFToken': document.cookie.match(/csrftoken=(.+)\b/)[1],
        },
      });
    }, 2000, {maxWait: 10000});

  });

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
