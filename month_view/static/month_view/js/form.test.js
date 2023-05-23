import { IncrementDate } from "./form.mjs";

test('month is icremented up by 1', () =>{
    var test_date = '2023-05-24';
    var recieved_date = IncrementDate(test_date, 1)
    expect(recieved_date).toBe('2023-6-24')
})

test('month is icremented down by 1', () =>{
    var test_date = '2023-05-24';
    var recieved_date = IncrementDate(test_date, -1)
    expect(recieved_date).toBe('2023-4-24')
})

test('year is incremented down by 1', () =>{
    var test_date = '2023-01-24';
    var recieved_date = IncrementDate(test_date, -1)
    expect(recieved_date).toBe('2022-12-24')
})

test('year is incremented up by 1', () =>{
    var test_date = '2022-12-24';
    var recieved_date = IncrementDate(test_date, 1)
    expect(recieved_date).toBe('2023-1-24')
})