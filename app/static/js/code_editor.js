document.addEventListener("DOMContentLoaded", function() {
    const textarea = document.getElementById("answer");
    const languageSelect = document.getElementById("language");
    const themeToggle = document.getElementById("theme-toggle");

    // check localStorage for saved theme
    let savedTheme = localStorage.getItem("editorTheme") || "monokai";

    // pick initial mode
    let mode = languageSelect.value === "sql" ? "text/x-sql" : "python";

    let currentTheme = savedTheme;

    const editor = CodeMirror.fromTextArea(textarea, {
        lineNumbers: true,
        mode: mode,
        theme: currentTheme,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        viewportMargin: Infinity,
        extraKeys: {
            "Tab": function(cm) {
                if (cm.somethingSelected()) {
                    cm.indentSelection("add");
                } else {
                    cm.replaceSelection("    ", "end");
                }
            }
        }
    });

    editor.setSize("100%", "500px"); // larger default height

    // update mode if language changes
    languageSelect.addEventListener("change", function() {
        const newMode = this.value === "sql" ? "text/x-sql" : "python";
        editor.setOption("mode", newMode);
    });

    // toggle theme and persist
    themeToggle.addEventListener("click", function() {
        if (currentTheme === "monokai") {
            currentTheme = "default";
        } else {
            currentTheme = "monokai";
        }
        editor.setOption("theme", currentTheme);
        localStorage.setItem("editorTheme", currentTheme); // persist
    });
});
