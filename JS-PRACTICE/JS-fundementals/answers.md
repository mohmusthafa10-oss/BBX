1. What is a closure and when have you used one?

A closure happens when an inner function remembers and can access variables from its outer function, even after the outer function has finished executing.

I have used closures when implementing debounce, throttle, and once functions. For example, in a debounce function, the returned function remembers the timer variable from the outer function. This allows it to clear the previous timer when the function is called again.

JavaScript is single-threaded, which means it executes one piece of code at a time.

The **event loop** helps JavaScript handle asynchronous tasks without blocking the main thread. First, the synchronous code runs on the call stack.

When JavaScript encounters something asynchronous, like a timer, API request, or Promise, it can be handled outside the main execution flow. Once the operation is ready, its callback is placed in the appropriate queue.

The **event loop** keeps checking whether the call stack is empty. If it is empty, it moves the waiting callback to the call stack so JavaScript can execute it.

So, in simple terms, the event loop helps JavaScript manage synchronous and asynchronous operations efficiently.


In JavaScript, `this` refers to the object that is calling the function. Its value mainly depends on how the function is called.

For example, if we call `user.greet()`, `this` refers to the `user` object.

Arrow functions are different because they don't have their own `this`; they inherit it from the surrounding scope.

So, in short, regular functions get `this` based on how they are called, while arrow functions inherit `this` from their surrounding context.
