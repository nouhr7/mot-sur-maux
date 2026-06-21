/*
 * Visual editor for the team's article form.
 * Quill renders a friendly toolbar; on submit we copy its HTML into the
 * hidden <textarea name="content"> so Django receives and sanitises it.
 */
(function () {
  "use strict";

  var holder = document.getElementById("editor");
  var source = document.getElementById("id_content");
  if (!holder || !source || typeof Quill === "undefined") {
    return;
  }

  var quill = new Quill(holder, {
    theme: "snow",
    placeholder: "Écrivez votre article ici… Prenez le temps, les mots viendront.",
    modules: {
      toolbar: [
        [{ header: [2, 3, false] }],
        ["bold", "italic", "underline"],
        [{ list: "ordered" }, { list: "bullet" }],
        ["blockquote", "link"],
        ["clean"],
      ],
    },
  });

  // Load any existing content (editing an article, or a pre-filled submission).
  var initial = source.value.trim();
  if (initial) {
    quill.clipboard.dangerouslyPasteHTML(initial);
  }

  // Keep the hidden field in sync so the value is always current on submit.
  function sync() {
    source.value = quill.getText().trim().length ? quill.root.innerHTML : "";
  }
  quill.on("text-change", sync);

  var form = holder.closest("form");
  if (form) {
    form.addEventListener("submit", sync);
  }
})();
