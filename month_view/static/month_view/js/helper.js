function ShowNewForm(date) {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    date_box.value = date;
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

function HideNewForm() {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'hidden';
}

function HideEditForm() {
    var form = document.getElementById('edit_event_input');
    form.style.visibility = 'hidden';
}

function MouseOverDay(day, day_num) {
    day.style.backgroundColor = '#ADCAF7';
    var btn = document.getElementById('new_event_button_' + day_num);
    btn.style.display = 'inline-block';
}

function MouseOffDay(day, day_num) {
    day.style.backgroundColor = '#C9D9F2';
    var btn = document.getElementById('new_event_button_' + day_num);
    btn.style.display = 'none'
}

function MouseOverNextMonthDay(day, day_num) {
    day.style.backgroundColor = '#c4c6c8';
    var btn = document.getElementById('next_month_new_event_button_' + day_num);
    btn.style.display = 'inline-block';
}

function MouseOffNextMonthDay(day_div, day_num) {
    day_div.style.backgroundColor = '#c4c6c8';
    var btn = document.getElementById('next_month_new_event_button_' + day_num);
    btn.style.display = 'none'
}

function ShowNewNextMonthForm(day, month, year) {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    var date = year + '-' + String(Number(month) + 1) + '-' + day;
    date_box.value = date;
}

function MouseOverLastMonthDay(day, day_num) {
    day.style.backgroundColor = '#c4c6c8';
    var btn = document.getElementById('last_month_new_event_button_' + day_num);
    btn.style.display = 'inline-block';
}

function MouseOffLastMonthDay(day_div, day_num) {
    day_div.style.backgroundColor = '#c4c6c8';
    var btn = document.getElementById('last_month_new_event_button_' + day_num);
    btn.style.display = 'none'
}

function ShowNewLastMonthForm(day, month, year) {
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    var date = year + '-' + String(Number(month) - 1) + '-' + day;
    date_box.value = date;
}