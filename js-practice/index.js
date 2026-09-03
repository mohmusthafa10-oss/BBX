let name="John";
let age=20;
let totalMarks=450;
let attendance=90;
let feePaid=true;
let phone="123-456-7890";
let address="abc house, xyz street, city";
let email="john@example.com";
let bonusMarks=50;
let attempt=10;
let course="JavaScript";

console.log("Name: " + name);
console.log("Age: " + age);
console.log("Total Marks: " + totalMarks); 
console.log("Attendance: " + attendance + "%");
console.log("Fee Paid: " + feePaid);
console.log("Phone: " + phone);
console.log("Address: " + address);
console.log("Email: " + email);
console.log("Bonus Marks: " + bonusMarks);
console.log("Attempt: " + attempt);
console.log("Course: " + course);

console.log("Total Score: " + (totalMarks + bonusMarks));
console.log("Avg Score : " + ((totalMarks + bonusMarks) /5));
console.log("Reminder "+ (totalMarks % 5));
console.log("Sqr of age: " + (age * age));

console.log("Increased total mark : " + (totalMarks + 20));
console.log("Decreased Attendance : " + (attendance - 5));
console.log("updated bonus marks : " + (bonusMarks * 2));
console.log("Half of Total Marks : " + (totalMarks / 2));
console.log("remainder of Total Marks when divided by 7 : " + (totalMarks % 7));

console.log("Is Adult: " + (age >= 18));
console.log("Total Marks is greater than 250: " + (totalMarks > 250));
console.log("Attendance Percentage is less than 75: " + (attendance < 75));
console.log("Course is equal to JavaScript: " + (course == "JavaScript"));
console.log("Course is strictly equal to JavaScript: " + (course === "JavaScript"))
console.log("Student Name is not equal to Admin: " + (name != "Admin"));
console.log("Student Name is not strictly equal to Admin: " + (name !== "Admin"));
console.log("the Age is less than 25" + (age < 25));
console.log("Attendance Percentage is less than or equal to 100: " + (attendance <= 100));

console.log("Student is eligible for exam : " +(attendance >= 75));
console.log("Student is eligible for a certificate : "+(totalMarks>250 || attendance>90));
console.log("Is fee paid : "+ (!feePaid));

console.log("Attempt increment : " + (attempt++));
console.log("Attempt decrement : " + (attempt--));

let avgScore = (totalMarks + bonusMarks) / 5;
let isPassed = (avgScore >=50? "Passed" : "Failed");
console.log("Student has " + isPassed + " the exam.");

let isAdult = (age >= 18? "Yes" : "No");
console.log("Is the student an adult? " + isAdult);

document.write("<h1>Student Details</h1>");
document.write("<p>Name: " + name + "</p>");
document.write("<p>Age: " + age + "</p>");
document.write("<p>Total Marks: " + totalMarks + "</p>");
document.write("<p>Attendance: " + attendance + "%</p>");
document.write("<p>Fee Paid: " + feePaid + "</p>");
document.write("<p>Phone: " + phone + "</p>");
document.write("<p>Address: " + address + "</p>");
document.write("<p>Email: " + email + "</p>");
document.write("<p>Bonus Marks: " + bonusMarks + "</p>");
document.write("<p>Attempt: " + attempt + "</p>");
document.write("<p>Course: " + course + "</p>");


