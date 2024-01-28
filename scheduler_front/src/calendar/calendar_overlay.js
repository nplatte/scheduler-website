function MonthInfo() {
    return (
        <div className="calendar__descriptions">
            <h3 className="calendar__month">Month Name</h3>
            <h3 className="calendar__year">Year Number</h3>
        </div>
    );
}

function LeftArrow() {
    return (
        <div>
            <button>Left</button>
        </div>
    );
}

function RightArrow() {
    return (
        <div>
            <button>Right</button>
        </div>
    );
}

export {MonthInfo, LeftArrow, RightArrow};