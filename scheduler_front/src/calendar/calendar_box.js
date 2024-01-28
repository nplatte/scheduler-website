

function DayGrid() {
    return(
        <div>
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
        <h3 class="day_name">{name}</h3>
    );
}

export default DayGrid;