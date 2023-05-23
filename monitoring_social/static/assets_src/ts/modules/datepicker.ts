import Datepicker from 'vanillajs-datepicker/Datepicker';

function createDatePicker() {
    const dateInputs = document
        .querySelectorAll('input.js_date_picker') as NodeListOf<HTMLInputElement>;
    if (!dateInputs) return;

    dateInputs.forEach(input => {
        const datepicker = new Datepicker(input, {
            format: 'dd.mm.yyyy'
        });
    });
}

createDatePicker();

export {};
