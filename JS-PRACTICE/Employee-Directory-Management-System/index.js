let emp=[`Jhon`,`Jacob`,`Tiago`,`Sara`,`Moidu`];
let totalEmp=emp.length;

console.log(totalEmp);
console.log(emp);

emp.push(`Rasheed`);
console.log(emp);

emp.unshift(`Usman`);
console.log(emp);

emp.pop();
console.log(emp);

emp.shift();
console.log(emp);

console.log(emp.indexOf(`Tiago`));

console.log(emp.includes(`Sara`));

let dept=[`HR`,`Accounts`,`Tech`];

let combine=emp.concat(dept);
console.log(combine);


console.log(emp.join(" | "));

console.log(emp.slice(2,4));

emp.splice(3, 0,`Asarpu`);
console.log(emp);

emp.sort();
console.log(emp);

console.log(emp.reverse());

let str=` Muhammed Jacob O `;
console.log(`Employee name ; ${str}`);

let len=str.length;
console.log(`Total no of charecters : ${len}`);

console.log(`Upper case : ${str.toUpperCase()}`);
console.log(`Lower case : ${str.toLowerCase()}`);

console.log(`Remove spaces only from the beginning : ${str.trimStart()}`);
console.log(`Remove spaces only from the end : ${str.trimEnd()}`);
str.trim();
console.log(`Remove spaces only from Both side : ${str}`);


console.log(`character at index 2 : ${str.charAt(2)}`);
console.log(`last character : ${str.charAt(-1)}`);

console.log(`first occurrence of ${"a"} :${str.indexOf('a')}`);
console.log(`last occurrence of ${"a"} :${str.lastIndexOfndexOf('a')}`);

console.log(`first occurrence of ${"a"} :${str.indexOf('a')}`);