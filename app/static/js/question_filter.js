document.addEventListener("DOMContentLoaded", function() {
    const categoryButtons = document.querySelectorAll(".question-filters .category-list button");
    const difficultySelect = document.getElementById("difficulty-filter");
    const rows = document.querySelectorAll(".questions-table tbody tr");

    function filterQuestions() {
        const selectedCategory = document.querySelector(".question-filters .category-list button.active")?.dataset.category || "All";
        const selectedDifficulty = difficultySelect.value;

        rows.forEach(row => {
            const rowCategory = row.dataset.category;
            const rowDifficulty = row.dataset.difficulty;

            const categoryMatch =
                selectedCategory === "All" ||
                (selectedCategory === "Data Science" &&
                    (rowCategory === "Computer Science" || rowCategory === "Databases")) ||
                rowCategory === selectedCategory;

            const difficultyMatch =
                selectedDifficulty === "All" || rowDifficulty === selectedDifficulty;

            if (categoryMatch && difficultyMatch) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    // highlight active category
    categoryButtons.forEach(button => {
        button.addEventListener("click", function() {
            categoryButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
            filterQuestions();
        });
    });

    // difficulty change
    difficultySelect.addEventListener("change", function() {
        filterQuestions();
    });
});
