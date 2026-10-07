// Part C - Async JavaScript

const urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3"
];


// 1. Sequential requests with await in a loop


async function sequentialFetch(urls) {
    const results = [];

    const start = performance.now();

    for (const url of urls) {
        const response = await fetch(url);

        // await pauses the current async function until the
        // Promise settles. When it is used inside a loop,
        // the next iteration doesn't start until the current
        // request finishes, so the requests execute sequentially.

        const data = await response.json();
        results.push(data);
    }

    const end = performance.now();

    console.log("Sequential results:", results);
    console.log(
        "Sequential time:",
        (end - start).toFixed(2),
        "ms"
    );

    return results;
}


// ============================================================
// 2. Parallel requests with Promise.all
// ============================================================

async function parallelFetch(urls) {

    const start = performance.now();

    // fetch() is called for every URL immediately.The requests are started without waiting for one request to finish before starting the next one.

    const requests = urls.map(url => fetch(url));

    // Promise.all() waits until all requests have completed.Since the requests were already started above, they can run in parallel.

    const responses = await Promise.all(requests);

    const results = [];

    for (const response of responses) {
        const data = await response.json();
        results.push(data);
    }

    const end = performance.now();

    console.log("Parallel results:", results);
    console.log(
        "Parallel time:",
        (end - start).toFixed(2),
        "ms"
    );

    return results;
}


// 3. Promise.allSettled()
// One endpoint returns HTTP 500


const urlsWithError = [
    "https://jsonplaceholder.typicode.com/posts/1",

    // httpstat.us can be used to generate a 500 response.
    "https://httpstat.us/500",

    "https://jsonplaceholder.typicode.com/posts/3"
];


async function allSettledFetch(urls) {

    const start = performance.now();

    const requests = urls.map(url => fetch(url));

    // Promise.allSettled() waits for every Promise to settle.
    // A rejected Promise does not stop the other requests.
    // The result contains either:
    // { status: "fulfilled", value: ... }
    // or
    // { status: "rejected", reason: ... }

    const results = await Promise.allSettled(requests);

    const end = performance.now();

    console.log("AllSettled results:", results);

    console.log(
        "AllSettled time:",
        (end - start).toFixed(2),
        "ms"
    );

    return results;
}


// 4. Promise.all() vs Promise.allSettled()

/*
Promise.all():

- Waits for all Promises if all succeed.
- If one Promise rejects, Promise.all() rejects.
- Useful when every operation must succeed.

Promise.allSettled():

- Waits for every Promise.
- Gives the result of both successful and failed operations.
- Useful when we want to know the result of every operation,
  even if some operations fail.
*/


// 5. Fetch 404 trap

async function fetch404Example() {

    const response = await fetch(
        "https://jsonplaceholder.typicode.com/posts/999999"
    );

    console.log("Status:", response.status);
    console.log("OK:", response.ok);

    // IMPORTANT:
    // fetch() does NOT reject just because the server returns an HTTP error such as 404 or 500.
    //  A 404 still produces a Response object.
    // Therefore, this code reaches the next line instead of automatically entering catch().
}



// 6. Correct fetch error-handling wrapper

async function fetchWithErrorHandling(url) {

    try {

        const response = await fetch(url);

        // fetch() only rejects for network-level failures.
        // HTTP errors such as 404 and 500 normally do not reject the Promise.
        // response.ok is true for successful HTTP status codes in the range 200-299.

        if (!response.ok) {
            throw new Error(
                `HTTP error: ${response.status} ${response.statusText}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error("Request failed:", error.message);

        throw error;
    }
}


// Run the examples

async function main() {

    console.log("========== SEQUENTIAL ==========");
    await sequentialFetch(urls);

    console.log("\n========== PROMISE.ALL ==========");
    await parallelFetch(urls);

    console.log("\n========== ALL.SETTLED ==========");
    await allSettledFetch(urlsWithError);

    console.log("\n========== 404 TRAP ==========");
    await fetch404Example();

    console.log("\n========== ERROR HANDLING ==========");

    try {
        await fetchWithErrorHandling(
            "https://jsonplaceholder.typicode.com/posts/999999"
        );
    } catch (error) {
        console.log("Handled error:", error.message);
    }
}

main();