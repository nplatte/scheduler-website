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