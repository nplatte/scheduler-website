function ShowNewForm(date) {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    date_box.value = date;
}

function HideNewForm() {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'hidden';
}

function ToggleNewEventFormVisibility(date) {
    var form = document.getElementById('new_event_input');
    if (form.style.visibility = 'visible') {
        form.style.visibility = 'hidden';
    } else {
        form.style.visibility = 'visible';
        var date_box = document.getElementById('new_event_date');
        date_box.value = date;
    }
}