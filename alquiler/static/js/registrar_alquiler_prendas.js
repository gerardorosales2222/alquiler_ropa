document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('searchPreInput');
    const select = document.getElementById('prendas');
    const prendas = Array.from(select.options).map(option => ({ value: option.value, text: option.text }));

    input.addEventListener('input', () => {
        const query = input.value.toLowerCase();
        select.innerHTML = '';

        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = '--Seleccione una prenda--';
        select.appendChild(defaultOption);

        prendas.forEach(prenda => {
            if (prenda.text.toLowerCase().includes(query)) {
                const option = document.createElement('option');
                option.value = prenda.value;
                option.textContent = prenda.text;
                select.appendChild(option);
            }
        });
    });
});