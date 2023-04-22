const menu = document.querySelector('.js_left_menu');
const closeMenu = document.querySelector('.js_close_menu');
console.log(1);
closeMenu.addEventListener('click', el => {
    console.log(2);
    menu.classList.toggle('show')
    closeMenu.classList.toggle('open')
});

const organizationsSelect = document.querySelector<HTMLSelectElement>('.js_organizations_select');

console.log(organizationsSelect);
organizationsSelect.addEventListener('change', e => {
    const target = e.target as HTMLSelectElement;
    if (+target.value == -1) {
        window.location.replace('/monitoring/organization/create')
    }
    const request = new Request(
        target.dataset.url,
        {
            method: 'POST',
            headers: {'X-CSRFToken': target.dataset.token, "X-Requested-With": "XMLHttpRequest"},
            mode: 'same-origin',
            body: JSON.stringify({'organization': target.value})
        }
    );
    fetch(request)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data['success']) {
                window.location.reload();
            }
        });
});
export {};
