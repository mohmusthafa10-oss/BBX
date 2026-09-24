function myMap(arr, callback) {
    const result = [];

    for (let i = 0; i < arr.length; i++) {
        result.push(callback(arr[i], i, arr));
    }

    return result;
}

function myFilter(arr, callback) {
    const result = [];

    for (let i = 0; i < arr.length; i++) {
        if (callback(arr[i], i, arr)) {
            result.push(arr[i]);
        }
    }

    return result;
}


function myReduce(arr, callback, initialValue) {
    let accumulator;
    let startIndex;

    if (initialValue !== undefined) {
        accumulator = initialValue;
        startIndex = 0;
    } else {
        accumulator = arr[0];
        startIndex = 1;
    }

    for (let i = startIndex; i < arr.length; i++) {
        accumulator = callback(accumulator, arr[i], i, arr);
    }

    return accumulator;
}


function debounce(fn, ms) {
    let timer;

    return function (...args) {
        clearTimeout(timer);

        timer = setTimeout(() => {
            fn(...args);
        }, ms);
    };
}

/*
Debounce:
- Waits until the calls STOP for the specified time.
- Useful when you only want the final action.

Example:
Search box:
User types: h -> he -> hel -> hell -> hello
The function runs only after the user stops typing.

Throttle:
- Limits how often a function can run.
- Useful when an event happens continuously.

Example:
Scroll event:
Instead of running the function hundreds of times,
run it at most once every specified interval.
*/



function throttle(fn, ms) {
    let lastTime = 0;

    return function (...args) {
        const currentTime = Date.now();

        if (currentTime - lastTime >= ms) {
            lastTime = currentTime;
            fn(...args);
        }
    };
}


function deepClone(obj) {

    
    if (obj === null || typeof obj !== "object") {
        return obj;
    }

    
    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }

    
    if (Array.isArray(obj)) {
        const result = [];

        for (let i = 0; i < obj.length; i++) {
            result.push(deepClone(obj[i]));
        }

        return result;
    }


    const result = {};

    for (const key in obj) {
        result[key] = deepClone(obj[key]);
    }

    return result;
}


/*
JSON.parse(JSON.stringify(x)) loses or changes several things:

1. Date
   Date becomes a string.

2. undefined
   Object properties containing undefined are removed.

3. Functions
   Functions are removed.

4. Symbol
   Symbol properties are lost.

5. NaN / Infinity
   They become null.

6. RegExp
   Regular expressions are not preserved correctly.

7. Map / Set
   Their contents are not preserved as Map/Set objects.

8. Circular references
   JSON.stringify() throws an error.

So JSON cloning is only suitable for simple JSON-compatible data.
*/



function once(fn) {
    let hasRun = false;
    let result;

    return function (...args) {

        if (!hasRun) {
            hasRun = true;
            result = fn(...args);
        }

        return result;
    };
}



export {
    myMap,
    myFilter,
    myReduce,
    debounce,
    throttle,
    deepClone,
    once
};