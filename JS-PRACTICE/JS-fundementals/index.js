// Part A 

// 1. typeof
console.log(typeof null, typeof undefined, typeof NaN, typeof []);

// Output:
// object undefined number object


// 2. == vs === and NaN
console.log(
    0 == '0',
    0 === '0',
    null == undefined,
    null === undefined,
    NaN == NaN
);

// Output:
// true false true false false


// 3. [] comparison and truthiness
console.log([] == false, [] ? 'truthy' : 'falsy');

// Output:
// true truthy


// 4. var vs let inside setTimeout

for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log('var', i), 0);
}

for (let j = 0; j < 3; j++) {
    setTimeout(() => console.log('let', j), 0);
}

// Output:
// var 3
// var 3
// var 3
// let 0
// let 1
// let 2


// 5. Synchronous code vs Promise vs setTimeout

console.log('A');

setTimeout(() => console.log('B'), 0);

Promise.resolve().then(() => console.log('C'));

console.log('D');

// Output:
// A
// D
// C
// B


// 6. const with arrays

const arr = [1, 2, 3];

arr.push(4);

console.log(arr);

// Output:
// [1, 2, 3, 4]

// Why is this allowed?
// const prevents reassignment of the variable,
// but it does not make the array itself immutable.


// 7. Shallow copy

const a = { x: { y: 1 } };

const b = { ...a };

b.x.y = 99;

console.log(a.x.y);

// Output:
// 99

// Why?
// Spread creates a shallow copy.
// The nested object x is still shared by both a and b.


// 8. Array sort()

console.log(
    [10, 9, 1].sort(),
    [10, 9, 1].sort((p, q) => p - q)
);

// Output:
// [1, 10, 9] [1, 9, 10]

// Why?
// Default sort() converts elements to strings and sorts lexicographically.
// p - q provides numeric sorting.


// 9. Regular method vs arrow function and this

const o = {
    n: 'x',

    reg() {
        return this.n;
    },

    arrow: () => this?.n
};

console.log(o.reg(), o.arrow());

// Output:
// x undefined

// Why?
// reg() gets this from the object that calls it.
// Arrow functions do not have their own this;
// they inherit this from the surrounding scope.


// 10. map() vs forEach()

console.log(
    [1, 2, 3].map(n => n * 2),
    [1, 2, 3].forEach(n => n * 2)
);

// Output:
// [2, 4, 6] undefined

// Why?
// map() creates and returns a new array.
// forEach() executes the callback but returns undefined.