import {MonthInfo, LeftArrow, RightArrow} from './calendar/calendar_overlay.js';
import DayGrid from './calendar/calendar_box.js';


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
