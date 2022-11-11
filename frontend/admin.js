import { EditorView, minimalSetup } from "codemirror"
import { lineNumbers } from "@codemirror/view"
import { markdown, markdownLanguage } from "@codemirror/lang-markdown"

import "./admin.css"

import { onReady } from "./utils.js"

onReady(() => {
  function editorFromTextArea(textarea, extensions) {
    const view = new EditorView({
      doc: textarea.value,
      extensions,
      lineWrapping: true,
    })
    textarea.after(view.dom)
    textarea.style.display = "none"
    if (textarea.form)
      textarea.form.addEventListener("submit", () => {
        textarea.value = view.state.doc.toString()
      })
    return view
  }

  const areas = Array.from(document.querySelectorAll("#id_content"))
  if (!areas.length) return

  const extensions = [
    minimalSetup,
    lineNumbers(),
    markdown({ base: markdownLanguage }),
    EditorView.lineWrapping,
  ]
  areas.forEach((element) => {
    editorFromTextArea(element, extensions)
  })
})
