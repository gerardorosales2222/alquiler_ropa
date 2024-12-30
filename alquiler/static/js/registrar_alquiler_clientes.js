document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('searchInput');
    const select = document.getElementById('clientes');
    const clientes = Array.from(select.options).map(option => ({ value: option.value, text: option.text }));

    input.addEventListener('input', () => {
        const query = input.value.toLowerCase();
        select.innerHTML = '';

        const defaultOption = document.createElement('option');
        defaultOption.value = '';
    // defaultOption.textContent = '--Seleccione un cliente--';
        select.appendChild(defaultOption);

        clientes.forEach(cliente => {
            if (cliente.text.toLowerCase().includes(query)) {
                const option = document.createElement('option');
                option.value = cliente.value;
                option.textContent = cliente.text;
                select.appendChild(option);
            }
        });
    });
});