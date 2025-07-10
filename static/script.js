 // Optional: change blob colors every few seconds
    const blobs = document.querySelectorAll('.blob');
    setInterval(() => {
      blobs.forEach(b => {
        b.style.background = `hsl(${Math.random()*360}, 70%, 60%)`;
      });
    }, 8000);


    
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("Link copied to clipboard!");
  }).catch(err => {
    console.error('Could not copy text: ', err);
  });
}


function paginateTable(tableId, rowsPerPage = 20) {
      const table = document.getElementById(tableId);
      const tbody = table.querySelector("tbody");
      const rows = Array.from(tbody.querySelectorAll("tr"));
      const totalRows = rows.length;
      const totalPages = Math.ceil(totalRows / rowsPerPage);
      const controls = document.getElementById("paginationControls");

      if (totalPages <= 1) return;

      let currentPage = 1;

      function renderPage(page) {
        tbody.innerHTML = "";
        const start = (page - 1) * rowsPerPage;
        const end = page * rowsPerPage;
        rows.slice(start, end).forEach(row => tbody.appendChild(row));
      }

      function createButtons() {
        controls.innerHTML = "";
        for (let i = 1; i <= totalPages; i++) {
          const btn = document.createElement("button");
          btn.textContent = i;
          btn.className = (i === currentPage) ? "active-page" : "";
          btn.onclick = () => {
            currentPage = i;
            renderPage(i);
            createButtons();
          };
          controls.appendChild(btn);
        }
      }

      renderPage(currentPage);
      createButtons();
    }

    window.onload = function () {
      const table = document.getElementById("genericTable");
      if (table) paginateTable("genericTable", 20);
    };

