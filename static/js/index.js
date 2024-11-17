// to enable or disable inputs based on checkbox selection
function toggleInputs(checkbox) {
    const row = checkbox.closest('tr');
    const qtyInput = row.querySelector('input[name="qty[]"]');
    const rateInput = row.querySelector('input[name="rate[]"]');
    qtyInput.disabled = !checkbox.checked;
    rateInput.disabled = !checkbox.checked;
}

// to calculate total amount dynamically
function calculateAmount(row) {
    const qty = row.querySelector('input[name="qty[]"]').value;
    const rate = row.querySelector('input[name="rate[]"]').value;
    const totalAmount = row.querySelector('.amount');
    if (qty && rate) {
        totalAmount.textContent = (qty * rate).toFixed(2);
    } else {
        totalAmount.textContent = '0.00';
    }
}

// to filter items
function filterItems() {
    const filterMode = document.getElementById("filter-mode").value;
    const table = document.getElementById("items-table");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const checkbox = rows[i].querySelector('input[type="checkbox"]');
        const isChecked = checkbox.checked;

        if (filterMode === "all") {
            rows[i].style.display = "";
        } else if (filterMode === "selected") {
            rows[i].style.display = isChecked ? "" : "none";
        } else if (filterMode === "not_selected") {
            rows[i].style.display = !isChecked ? "" : "none";
        }
    }
}

//to filter the row based on search
function filterTable() {
    const input = document.getElementById("filter-input");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("items-table");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let match = false;

        for (let j = 0; j < cells.length; j++) {
            if (cells[j]) {
                const textValue = cells[j].textContent || cells[j].innerText;
                if (textValue.toLowerCase().includes(filter)) {
                    match = true;
                    break;
                }
            }
        }
        rows[i].style.display = match ? "" : "none";
    }
}

// timeout for flash message
setTimeout(function () {
    var flashMessages = document.querySelectorAll(".message");
    flashMessages.forEach(function (message) {
        message.style.display = "none";
    });
}, 2000); 