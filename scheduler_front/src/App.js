import {MonthInfo, LeftArrow, RightArrow} from './calendar/calendar_overlay.js';
import DayGrid from './calendar/calendar_box.js';
import axios from 'axios';

function Calendar() {
    //calendar box
    //  left arrow right arrow
    //  month info
    //  week day labels
    //  month days
    //    day box
    //      day number
    //      event
    //      a new event button
    const today = new Date();
    const baseURL = "http://localhost:8000/month_view";
    const extension = `${today.getMonth() + 1}-${today.getFullYear()}/api`
    axios.get(`${baseURL}/${extension}`).then(response => {
      console.log(response.data);
    }).catch(error => {
      console.error(error);
    });
    return (
      <div className="calendar">
        <MonthInfo />
        <div>
          <LeftArrow />
          <DayGrid />
          <RightArrow />
        </div>
      </div>
    );
}

export default Calendar;
