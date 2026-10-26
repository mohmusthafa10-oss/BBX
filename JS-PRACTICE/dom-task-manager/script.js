
const API_URL = "https://jsonplaceholder.typicode.com/todos";

const taskForm = document.getElementById("task-form");
const taskTitle = document.getElementById("task-title");
const searchInput = document.getElementById("search-input");
const taskList = document.getElementById("task-list");
const loadingMessage = document.getElementById("loading-message");
const emptyMessage = document.getElementById("empty-message");
const errorMessage = document.getElementById("error-message");
const benchmarkLoop = document.getElementById("benchmark-loop");
const benchmarkFragment = document.getElementById("benchmark-fragment");
const benchmarkResult = document.getElementById("benchmark-result");
const benchmarkContainer = document.getElementById("benchmark-container");

// Add ?staleDemo=1 to the URL to demonstrate the search race condition.
const staleDemo = new URLSearchParams(location.search).has("staleDemo");

let tasks = [];
let searchTimer;
let searchController;
let searchVersion = 0;

// --------------------------------------------------
// 1. UI messages
// --------------------------------------------------

function showLoading(show) {
    loadingMessage.hidden = !show;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = !message;
}

function updateEmptyState() {
    emptyMessage.hidden = tasks.length !== 0;
}

// --------------------------------------------------
// 2. API helper: check res.ok explicitly
// --------------------------------------------------

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    if (!response.ok) {
        throw new Error(`Request failed: HTTP ${response.status}`);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

// --------------------------------------------------
// 3. Render tasks safely
// --------------------------------------------------

function renderTasks() {
    taskList.replaceChildren();

    tasks.forEach(task => {
        const item = document.createElement("li");
        item.className = "task-item";
        item.dataset.id = task.id;

        if (task.completed) {
            item.classList.add("completed");
        }

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.completed;
        checkbox.className = "complete-checkbox";
        checkbox.setAttribute("aria-label", "Mark task complete");

        const title = document.createElement("span");
        title.className = "task-title";

        // SECURITY: use textContent, never innerHTML for user input.
        title.textContent = task.title;

        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.className = "edit-button";
        editButton.textContent = "Edit";

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.className = "delete-button";
        deleteButton.textContent = "Delete";

        item.append(checkbox, title, editButton, deleteButton);
        taskList.appendChild(item);
    });

    updateEmptyState();
}

// --------------------------------------------------
// 4. Load tasks from the real API
// --------------------------------------------------

async function loadTasks() {
    showLoading(true);
    showError("");

    try {
        const data = await apiRequest(`${API_URL}?_limit=10`);

        tasks = data.map(task => ({
            id: task.id,
            title: task.title,
            completed: task.completed
        }));

        renderTasks();
    } catch (error) {
        showError(`Could not load tasks. ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// --------------------------------------------------
// 5. Add tasks with optimistic updates
// --------------------------------------------------

taskForm.addEventListener("submit", async event => {
    event.preventDefault();

    const title = taskTitle.value.trim();

    if (!title) {
        showError("Please enter a task title.");
        return;
    }

    const temporaryId = `temp-${Date.now()}`;
    const newTask = {
        id: temporaryId,
        title,
        completed: false
    };

    // Optimistic update: show the task immediately.
    tasks.unshift(newTask);
    renderTasks();
    taskForm.reset();
    showError("");

    try {
        const savedTask = await apiRequest(API_URL, {
            method: "POST",
            body: JSON.stringify({
                title,
                completed: false,
                userId: 1
            })
        });

        tasks = tasks.map(task =>
            task.id === temporaryId
                ? { ...newTask, id: savedTask.id }
                : task
        );

        renderTasks();
    } catch (error) {
        // Rollback if the API request fails.
        tasks = tasks.filter(task => task.id !== temporaryId);
        renderTasks();
        showError(`Could not save task. ${error.message}`);
    }
});

// --------------------------------------------------
// 6. Event delegation: ONE click listener on the list
// --------------------------------------------------

taskList.addEventListener("click", handleTaskClick);

async function handleTaskClick(event) {
    const button = event.target.closest("button");

    if (!button || !taskList.contains(button)) {
        return;
    }

    const item = button.closest(".task-item");
    const id = item.dataset.id;
    const task = tasks.find(task => String(task.id) === id);

    if (!task) return;

    if (button.classList.contains("edit-button")) {
        await editTask(task);
    }

    if (button.classList.contains("delete-button")) {
        await deleteTask(task);
    }
}

// --------------------------------------------------
// 7. Edit task with rollback
// --------------------------------------------------

async function editTask(task) {
    const newTitle = prompt("Edit task title:", task.title);

    if (newTitle === null) return;

    const title = newTitle.trim();

    if (!title) {
        showError("Task title cannot be empty.");
        return;
    }

    const oldTitle = task.title;

    task.title = title;
    renderTasks();
    showError("");

    try {
        await apiRequest(`${API_URL}/${task.id}`, {
            method: "PUT",
            body: JSON.stringify({
                ...task,
                title,
                userId: 1
            })
        });
    } catch (error) {
        task.title = oldTitle;
        renderTasks();
        showError(`Edit failed; previous title restored. ${error.message}`);
    }
}

// --------------------------------------------------
// 8. Delete task with rollback
// --------------------------------------------------

async function deleteTask(task) {
    const originalIndex = tasks.findIndex(
        item => String(item.id) === String(task.id)
    );

    // Optimistic delete.
    tasks = tasks.filter(
        item => String(item.id) !== String(task.id)
    );

    renderTasks();
    showError("");

    try {
        await apiRequest(`${API_URL}/${task.id}`, {
            method: "DELETE"
        });
    } catch (error) {
        // Restore the task at its previous position.
        tasks.splice(originalIndex, 0, task);
        renderTasks();
        showError(`Delete failed; task restored. ${error.message}`);
    }
}

// --------------------------------------------------
// 9. Toggle completion with rollback
// --------------------------------------------------

taskList.addEventListener("change", handleTaskChange);

async function handleTaskChange(event) {
    if (!event.target.matches(".complete-checkbox")) return;

    const item = event.target.closest(".task-item");
    const id = item.dataset.id;

    const task = tasks.find(task => String(task.id) === id);

    if (!task) return;

    const oldCompleted = task.completed;
    const newCompleted = event.target.checked;

    // Optimistic update.
    task.completed = newCompleted;
    renderTasks();
    showError("");

    try {
        await apiRequest(`${API_URL}/${task.id}`, {
            method: "PATCH",
            body: JSON.stringify({
                completed: newCompleted
            })
        });
    } catch (error) {
        task.completed = oldCompleted;
        renderTasks();
        showError(`Update failed; completion restored. ${error.message}`);
    }
}

// --------------------------------------------------
// 10. Search with 300ms debounce and AbortController
// --------------------------------------------------

searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);

    // Fixed mode: cancel the previous request.
    if (!staleDemo && searchController) {
        searchController.abort();
    }

    const version = ++searchVersion;

    searchTimer = setTimeout(() => {
        searchTasks(searchInput.value.trim(), version);
    }, 300);
});

async function searchTasks(query, version) {
    if (!query) {
        if (searchController) searchController.abort();

        showLoading(true);

        try {
            const data = await apiRequest(`${API_URL}?_limit=10`);

            if (!staleDemo && version !== searchVersion) return;

            tasks = data.map(task => ({
                id: task.id,
                title: task.title,
                completed: task.completed
            }));

            renderTasks();
            showError("");
        } catch (error) {
            if (error.name !== "AbortError") {
                showError(`Search failed. ${error.message}`);
            }
        } finally {
            showLoading(false);
        }

        return;
    }

    const controller = new AbortController();
    searchController = controller;

    showLoading(true);
    showError("");

    try {
        const data = await apiRequest(
            `${API_URL}?title_like=${encodeURIComponent(query)}&_limit=10`,
            { signal: controller.signal }
        );

        // Ignore stale responses in the fixed version.
        if (!staleDemo && version !== searchVersion) return;

        tasks = data.map(task => ({
            id: task.id,
            title: task.title,
            completed: task.completed
        }));

        renderTasks();
    } catch (error) {
        if (error.name !== "AbortError") {
            showError(`Search failed. ${error.message}`);
        }
    } finally {
        if (version === searchVersion) {
            showLoading(false);
        }
    }
}

// --------------------------------------------------
// 11. Throttled scroll handler
// --------------------------------------------------

function throttle(callback, delay) {
    let lastRun = 0;

    return function (...args) {
        const now = Date.now();

        if (now - lastRun >= delay) {
            lastRun = now;
            callback.apply(this, args);
        }
    };
}

// Scroll events fire frequently. Throttle limits execution
// to once per interval; debounce would wait until scrolling stops.
window.addEventListener("scroll", throttle(() => {
    document.body.dataset.scrollPosition = window.scrollY;
}, 200), { passive: true });

// --------------------------------------------------
// 12. Performance test: 5,000 items
// --------------------------------------------------

function createBenchmarkItem(index) {
    const item = document.createElement("div");
    item.className = "benchmark-item";
    item.textContent = `Task ${index + 1}`;
    return item;
}

function runLoopBenchmark() {
    benchmarkContainer.replaceChildren();

    const start = performance.now();

    for (let i = 0; i < 5000; i++) {
        benchmarkContainer.appendChild(createBenchmarkItem(i));
    }

    const duration = performance.now() - start;

    benchmarkResult.textContent =
        `Normal loop: ${duration.toFixed(2)} ms`;
}

function runFragmentBenchmark() {
    benchmarkContainer.replaceChildren();

    const start = performance.now();
    const fragment = document.createDocumentFragment();

    for (let i = 0; i < 5000; i++) {
        fragment.appendChild(createBenchmarkItem(i));
    }

    benchmarkContainer.appendChild(fragment);

    const duration = performance.now() - start;

    benchmarkResult.textContent =
        `DocumentFragment: ${duration.toFixed(2)} ms`;
}

benchmarkLoop.addEventListener("click", runLoopBenchmark);
benchmarkFragment.addEventListener("click", runFragmentBenchmark);

// --------------------------------------------------
// 13. Start application
// --------------------------------------------------

loadTasks();
