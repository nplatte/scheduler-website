function ToggleNewForm(date) {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    date_box.value = date;
}

function ToggleEditForm(title){
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var title_box = document.getElementById('edit_event_name');
    title_box.value = title;    
}