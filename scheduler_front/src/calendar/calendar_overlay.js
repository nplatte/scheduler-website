function MonthInfo() {
    return (
        <div className="calendar__descriptions">
            <h3 className="calendar__month">Month Name</h3>
            <h3 className="calendar__year">Year Number</h3>
        </div>
    );
}

function LeftArrow() {

    function  handleClick() {
        console.log("left clicked");
    }

    return (
        <div>
            <button onClick={handleClick}>Left</button>
        </div>
    );
}

function RightArrow() {

    function handleClick() {
        console.log("right clicked");
    }

    return (
        <div>
            <button onClick={handleClick}>Right</button>
        </div>
    );
}

export {MonthInfo, LeftArrow, RightArrow};