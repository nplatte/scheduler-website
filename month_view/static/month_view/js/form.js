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