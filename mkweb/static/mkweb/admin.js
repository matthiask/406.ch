import CodeMirror from 'codemirror';
import 'codemirror/lib/codemirror.css';

document.addEventListener('DOMContentLoaded', function() {
  let areas = Array.from(document.querySelectorAll('textarea'));
  areas.forEach((element) => {
    CodeMirror.fromTextArea(element, {
      lineNumbers: true,
      lineWrapping: true,
      mode: 'gfm',
    });
  });
});
