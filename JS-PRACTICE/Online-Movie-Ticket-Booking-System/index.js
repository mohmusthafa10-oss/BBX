alert("Welcome to the Booking System!");
let name = prompt("Enter your name:");
let movie = prompt("Enter the movie name:");
alert(`Hello ${name}, you are booking tickets for ${movie}.`);
alert("One ticket costs ₹200 for regular, ₹300 for premium, and ₹500 for VIP seats.");
let tickets = prompt("Enter the number of tickets:");

if (tickets < 1) {
    alert("Invalid Number of Tickets")
}

if (tickets > 6) {
    alert("Maximum 6 Tickets Allowed")
}

let seatType = prompt("Enter the seat type (regular/premium/vip):");

function discount() {

    if (tickets >= 3) {
        return 0.1; // 10% discount
    }
    return 0;
}

function calculateTotal() {

    let ticketPrice = 0;

    if (seatType === "regular") {
        ticketPrice = tickets * 200;
    } else if (seatType === "premium") {
        ticketPrice = tickets * 300;
    } else if (seatType === "vip") {
        ticketPrice = tickets * 500;
    }
    return ticketPrice;
}

let total = calculateTotal() - (calculateTotal() * discount() + 50);

function bookTickets() {

    if (confirmed) {
        let i = 3;
        while (i > 0) {
            console.log(`Booking starts in ${i}`);
            i--;
        }
        alert("Tickets booked successfully!");
    }
    else {
        alert("Tickets cancelled !!");
    }
}


let confirmed = confirm(`Total cost for ${tickets} ${seatType} tickets: ₹${total}`);

bookTickets();

console.log(`Movie: ${movie}, Tickets: ${tickets}, Seat Type: ${seatType}`);
// document.write(`<p>Movie: ${movie} <br> Tickets: ${tickets} <br> Seat Type: ${seatType} <br> Total Cost: ₹${calculateTotal() - (calculateTotal() * discount())}</p>`);

let avgCost = total / tickets;
console.log(`Avg Ticket cost : ${avgCost}`);

let catogery=" ";
if (total >= 2000) {
    category="Premium Booking";
    console.log("Booking Category : Premium Booking ");
}
else if ((total >= 1000) && (total < 1999)) {
    console.log("Booking Category : Standard Booking ");
    category="Standard Booking";
}
else {
    console.log("Booking Category : Budget Booking ");
    category="Budget Booking";
}

switch (seatType) {

    case "regular":
        console.log("You have selected a Regular seat. Enjoy your experience!");
        break;
    case "premium":
        console.log("You have selected a Premium seat. Includes extra legroom!");
        break;
    case "vip":
        console.log("You have selected a VIP seat. Exclusive lounge access included!");
        break;
    default:
        console.log("Invalid Seat Type. Please choose Regular, Premium, or VIP.");
}

for (let i = 1; i <= tickets; i++) {
    console.log(`Ticket ${i} Ready`);
    if(i==5){
        break;
    }
}

let doWhile = 1

do {
    console.log("Preparing your Tickets...");
    doWhile++;
}
while (doWhile < 1);


for (let i = 1; i <= 3; i++) {

    let row = String.fromCharCode(64 + i);
    let seats = "";

    for (let j = 1; j <= 5; j++) {

        if (row == "A" && j == 3) {
            continue;
        }
        seats += `${row}${j} `;
    }
    console.log(`Row ${row} : ${seats}`);
}

document.write(`<h2>Movie       : ${movie}</h2>`);
document.write(`<p>Name                : ${name}</p>`);
document.write(`<p>Seat Type           : ${seatType}</p>`);
document.write(`<p>No of Tickets       : ${tickets}</p>`);
document.write(`<p>Tickect cost        : ₹${calculateTotal()}</p>`);
document.write(`<p>Discount            : ₹${discount()}</p>`);
document.write(`<p>Convenience Fee     : ₹50</p>`);
document.write(`<p>Total cost          : ${total}</p>`);
document.write(`<p>Avg Tickets rs      : ${avgCost}</p>`);
document.write(`<p>Booking Category    : ${catogery}</p>`);

if(confirmed==true){
    document.write(`<p>Booking status      : Completed</p>`);
}
