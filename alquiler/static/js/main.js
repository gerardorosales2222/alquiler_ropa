document.addEventListener('DOMContentLoaded', function() {
    var rows = document.querySelectorAll('#mi_tabla tbody tr');
    rows.forEach(function(row) {
        var disponible = row.cells[9].textContent.trim().toLowerCase();
        if (disponible === 'no') {
            row.classList.add('table-secondary');
        }
    });
});
