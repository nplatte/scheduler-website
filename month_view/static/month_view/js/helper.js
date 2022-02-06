function ToggleForm(date) {
    var form = document.getElementById('event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    date_box.value = date;
}