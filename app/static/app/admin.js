import CodeMirror from "codemirror"
import "codemirror/lib/codemirror.css"

// import "codemirror/keymap/vim.js"
import "codemirror/mode/gfm/gfm.js"

document.addEventListener("DOMContentLoaded", function () {
  let areas = Array.from(document.querySelectorAll("textarea"))
  areas.forEach((element) => {
    CodeMirror.fromTextArea(element, {
      // keyMap: "vim",
      // lineNumbers: true,
      lineWrapping: true,
      mode: "gfm",
      viewportMargin: Infinity,
    })
  })
})
