function ToggleNewEventFormVisibility(date) {
    var form = document.getElementById('new_event_input');
    if (form.style.visibility == 'visible') {
        form.style.visibility = 'hidden';
    } else {
        form.style.visibility = 'visible';
        var date_box = document.getElementById('new_event_date');
        date_box.value = date;
    }
}

function ShowEditForm(title, date, id){
    var form = document.getElementById('edit_event_input');
    form.style.visibility = 'visible';
    var title_box = document.getElementById('edit_event_title');
    title_box.value = title;
    var date_box = document.getElementById('edit_event_date');
    date_box.value = date;   
    var id_box = document.getElementById('event_id');
    id_box.value = id;   
}

function HideEditForm() {
    var form = document.getElementById('edit_event_input');
    form.style.visibility = 'hidden';
}