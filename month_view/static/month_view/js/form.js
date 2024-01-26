function ToggleNewEventFormVisibility(date) {
    var form = document.getElementById('new_event_input');
    if (form.style.visibility == 'visi') {
        form.style.visibility = 'hidden';
    } else {
        form.style.visibility = 'visible';
        var date_box = document.getElementById('new_event_date');
        date_box.value = date;
    }
}

function ToggleEditEventFormVisibility(title, date, id) {
    var form = document.getElementById('edit_event_input');
    if (form.style.visibility == 'visible'){
        form.style.visibility = 'hidden';
    } else {
        form.style.visibility = 'visible';
        var title_box = document.getElementById('edit_event_title');
        title_box.value = title;
        var date_box = document.getElementById('edit_event_date');
        date_box.value = date;   
        var id_box = document.getElementById('event_id');
        id_box.value = id;
    }}

function ShowNewNextMonthForm(date) {
    date = IncrementDate(date, 1);
    console.log(date)
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    date_box.value = date;
}

function ShowNewLastMonthForm(date) {
    date = IncrementDate(date, -1);
    var form = document.getElementById('new_event_input');
    form.style.visibility = 'visible';
    var date_box = document.getElementById('new_event_date');
    date_box.value = date;
    }

function IncrementDate(date, amount) {
    const split_date = date.split('-');
    var year = Number(split_date[0]);
    var month = Number(split_date[1]);
    const day = Number(split_date[2]);
    month += amount;
    const [new_month, new_year] = ValidateMonthYear(month, year);
    const new_date = String(new_year) + '-' + String(new_month) + '-' + day;
    return new_date
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