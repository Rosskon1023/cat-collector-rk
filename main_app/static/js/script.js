// Date Picker Animations

const dateEl = document.getElementById('id_date');

M.Datepicker.init(dateEl, {
    format: 'yyyy-mm-dd',
    defaultDate: new Date(),
    setDefaultDate: true,
    autoClose: true
})

// Select Widget Animations

const selectEl = document.getElementById('id_meal');

M.FormSelect.init(selectEl);

