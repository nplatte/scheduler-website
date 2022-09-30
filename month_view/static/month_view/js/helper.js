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
    var num_month = Number(month) + 1;
    var num_year = Number(year);
    const [new_month, new_year] = ValidateMonthYear(num_month, num_year);
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    var date = String(new_year) + '-' + String(new_month) + '-' + day;
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
    var num_month = Number(month) - 1;
    var num_year = Number(year);
    const [new_month, new_year] = ValidateMonthYear(num_month, num_year);
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    var date = String(new_year) + '-' + String(new_month) + '-' + day;
    date_box.value = date;
}

function ValidateMonthYear(month, year) {
    if (month == 0) {
        return [12, year - 1];
    }
    if (month == 13) {
        return [1, year + 1];
    }
    else {
        return [month, year]
    }
}