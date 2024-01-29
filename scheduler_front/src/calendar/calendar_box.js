

function DayGrid() {
    return(
        <div className="calender__days">
        <DayName name="Sunday" />
        <DayName name="Monday" />
        <DayName name="Tueday" />
        <DayName name="Wednesday" />
        <DayName name="Thursday" />
        <DayName name="Friday" />
        <DayName name="Saturday" />
        </div>
    );
}

function DayName({name}) {
    return (
        <h3 className="day_name">{name}</h3>
    );
}

export default DayGrid;