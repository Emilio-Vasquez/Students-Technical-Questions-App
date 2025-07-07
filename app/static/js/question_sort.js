document.addEventListener("DOMContentLoaded", function() {
    const sortableHeaders = document.querySelectorAll(".sortable");

    sortableHeaders.forEach(header => {
        let sortDirection = null; // null, 'asc', or 'desc'

        header.addEventListener("click", function() {
            const column = header.dataset.column;
            const icon = header.querySelector(".sort-icons");

            // toggle direction
            if (sortDirection === null || sortDirection === "desc") {
                sortDirection = "asc";
                icon.classList.add("active-asc");
                icon.classList.remove("active-desc");
            } else {
                sortDirection = "desc";
                icon.classList.add("active-desc");
                icon.classList.remove("active-asc");
            }

            // sort table rows
            const tbody = document.querySelector(".questions-table tbody");
            const rows = Array.from(tbody.querySelectorAll("tr"));
            rows.sort((a, b) => {
                let aVal, bVal;
                if (column === "title") {
                    aVal = a.children[0].innerText.toLowerCase();
                    bVal = b.children[0].innerText.toLowerCase();
                } else if (column === "difficulty") {
                    aVal = a.children[3].innerText.toLowerCase();
                    bVal = b.children[3].innerText.toLowerCase();
                }
                if (sortDirection === "asc") {
                    return aVal.localeCompare(bVal);
                } else {
                    return bVal.localeCompare(aVal);
                }
            });
            // re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });
});
