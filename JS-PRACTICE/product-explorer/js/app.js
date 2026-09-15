const productList = document.querySelector(".product-list");
const searchForm = document.querySelector("#products search form");
const searchInput = document.querySelector("#search");
const categorySelect = document.querySelector("#category");
const favouriteSection = document.querySelector("#favourites");
const feedbackForm = document.querySelector(".feedback-form");

const API_URL = "https://dummyjson.com/products";

let lastRequest = loadProducts;


/* =========================
   RENDER PRODUCTS
========================= */

function renderProducts(products) {

    if (products.length === 0) {

        productList.innerHTML = `
            <li class="empty-state">
                <p>No products found.</p>
            </li>
        `;

        return;
    }

    const productsHTML = products.map(product => {

        return `
            <li>
                <article>

                    <img
                        class="product-image"
                        src="${product.thumbnail}"
                        alt="${product.title}"
                        loading="lazy"
                    >

                    <h3 class="product-name">
                        ${product.title}
                    </h3>

                    <p class="description">
                        ${product.description}
                    </p>

                    <p class="price">
                        $${product.price}
                    </p>

                    <button
                        type="button"
                        class="fav-button"
                        data-id="${product.id}"
                        aria-pressed="false"
                    >
                        Add to favourites
                    </button>

                </article>
            </li>
        `;
    }).join("");

    productList.innerHTML = productsHTML;

    addFavouriteEvents();
}


/* =========================
   LOADING STATE
========================= */

function showLoading() {

    productList.innerHTML = `
        <li class="loading-state" aria-live="polite">
            <p>Loading products...</p>
        </li>
    `;
}


/* =========================
   ERROR STATE
========================= */

function showError() {

    productList.innerHTML = `
        <li class="error-state" role="alert">

            <p>
                Failed to load products.
            </p>

            <button
                type="button"
                id="retry-button"
            >
                Try Again
            </button>

        </li>
    `;

    const retryButton =
        document.querySelector("#retry-button");

    retryButton.addEventListener("click", () => {
        lastRequest();
    });
}


/* =========================
   FETCH HELPER
========================= */

function fetchProducts(url, requestFunction) {

    lastRequest = requestFunction;

    showLoading();

    fetch(url)
        .then(response => {

            if (!response.ok) {
                throw new Error("Request failed");
            }

            return response.json();
        })
        .then(data => {

            renderProducts(data.products);
        })
        .catch(() => {

            showError();
        });
}


/* =========================
   LOAD ALL PRODUCTS
========================= */

function loadProducts() {

    const url = `${API_URL}?delay=2000`;

    fetchProducts(
        url,
        loadProducts
    );
}


/* =========================
   SEARCH PRODUCTS
========================= */

searchForm.addEventListener("submit", event => {

    event.preventDefault();

    const searchTerm =
        searchInput.value.trim();

    if (searchTerm === "") {

        loadProducts();

        return;
    }

    const searchURL =
        `${API_URL}/search?q=${encodeURIComponent(searchTerm)}&delay=2000`;

    const searchProducts = () => {

        fetchProducts(
            searchURL,
            searchProducts
        );
    };

    searchProducts();
});


/* =========================
   CATEGORY FILTER
========================= */

categorySelect.addEventListener("change", () => {

    const category =
        categorySelect.value;

    if (category === "all") {

        loadProducts();

        return;
    }

    const categoryURL =
        `${API_URL}/category/${category}?delay=2000`;

    const loadCategory = () => {

        fetchProducts(
            categoryURL,
            loadCategory
        );
    };

    loadCategory();
});


/* =========================
   LOAD CATEGORIES
========================= */

function loadCategories() {

    fetch(`${API_URL}/categories`)
        .then(response => {

            if (!response.ok) {
                throw new Error("Failed to load categories");
            }

            return response.json();
        })
        .then(categories => {

            categorySelect.innerHTML = `
                <option value="all">
                    All Categories
                </option>
            `;

            categories.forEach(category => {

                const option =
                    document.createElement("option");

                option.value = category.slug;
                option.textContent = category.name;

                categorySelect.appendChild(option);
            });
        })
        .catch(() => {

            /*
             * If categories fail, keep the
             * original "All Categories" option.
             */
            categorySelect.innerHTML = `
                <option value="all">
                    All Categories
                </option>
            `;
        });
}


/* =========================
   GET FAVOURITE IDS
========================= */

function getFavouriteIds() {

    return JSON.parse(
        localStorage.getItem("favourites")
    ) || [];
}


/* =========================
   SAVE FAVOURITE IDS
========================= */

function saveFavouriteIds(favourites) {

    localStorage.setItem(
        "favourites",
        JSON.stringify(favourites)
    );
}


/* =========================
   ADD TO FAVOURITES
========================= */

function addFavouriteEvents() {

    const favouriteButtons =
        document.querySelectorAll(".fav-button");

    favouriteButtons.forEach(button => {

        const productId =
            Number(button.dataset.id);

        const favourites =
            getFavouriteIds();

        if (favourites.includes(productId)) {

            button.textContent =
                "❤️ Added to favourites";

            button.setAttribute(
                "aria-pressed",
                "true"
            );
        }

        button.addEventListener("click", () => {

            let favourites =
                getFavouriteIds();

            if (!favourites.includes(productId)) {

                favourites.push(productId);

                saveFavouriteIds(favourites);

                button.textContent =
                    "❤️ Added to favourites";

                button.setAttribute(
                    "aria-pressed",
                    "true"
                );

                displayFavourites();
            }
        });
    });
}


/* =========================
   DISPLAY FAVOURITES
========================= */

function displayFavourites() {

    const favouriteIds =
        getFavouriteIds();

    if (favouriteIds.length === 0) {

        favouriteSection.innerHTML = `
            <h2>My Favourites</h2>

            <p>
                No favourite products yet.
            </p>
        `;

        return;
    }

    favouriteSection.innerHTML = `
        <h2>My Favourites</h2>

        <p aria-live="polite">
            Loading your favourite products...
        </p>
    `;

    /*
     * limit=0 gets all products so a favourite
     * is not limited to the first 30 products.
     */

    fetch(`${API_URL}?limit=0`)
        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "Failed to load favourites"
                );
            }

            return response.json();
        })
        .then(data => {

            const favouriteProducts =
                data.products.filter(product =>
                    favouriteIds.includes(product.id)
                );

            if (favouriteProducts.length === 0) {

                favouriteSection.innerHTML = `
                    <h2>My Favourites</h2>

                    <p>
                        No favourite products found.
                    </p>
                `;

                return;
            }

            const favouriteHTML =
                favouriteProducts.map(product => {

                    return `
                        <article>

                            <img
                                class="product-image"
                                src="${product.thumbnail}"
                                alt="${product.title}"
                                loading="lazy"
                            >

                            <h3 class="product-name">
                                ${product.title}
                            </h3>

                            <p class="description">
                                ${product.description}
                            </p>

                            <p class="price">
                                $${product.price}
                            </p>

                            <button
                                type="button"
                                class="remove-fav"
                                data-id="${product.id}"
                            >
                                ❌ Remove
                            </button>

                        </article>
                    `;

                }).join("");

            favouriteSection.innerHTML = `
                <h2>My Favourites</h2>

                <div class="favourite-list">
                    ${favouriteHTML}
                </div>
            `;

            addRemoveFavouriteEvents();
        })
        .catch(() => {

            favouriteSection.innerHTML = `
                <h2>My Favourites</h2>

                <p role="alert">
                    Unable to load favourites.
                </p>
            `;
        });
}


/* =========================
   REMOVE FAVOURITE
========================= */

function addRemoveFavouriteEvents() {

    const removeButtons =
        document.querySelectorAll(".remove-fav");

    removeButtons.forEach(button => {

        button.addEventListener("click", () => {

            const productId =
                Number(button.dataset.id);

            let favourites =
                getFavouriteIds();

            favourites =
                favourites.filter(
                    id => id !== productId
                );

            saveFavouriteIds(favourites);

            displayFavourites();

            /*
             * Refresh product buttons so the
             * removed item can be added again.
             */

            const currentProductButtons =
                document.querySelectorAll(".fav-button");

            currentProductButtons.forEach(favButton => {

                if (
                    Number(favButton.dataset.id)
                    === productId
                ) {

                    favButton.textContent =
                        "❤️ Add to favourites";

                    favButton.setAttribute(
                        "aria-pressed",
                        "false"
                    );
                }
            });
        });
    });
}


/* =========================
   FEEDBACK FORM
========================= */

feedbackForm.addEventListener(
    "submit",
    event => {

        event.preventDefault();

        const name =
            document.querySelector("#name");

        const email =
            document.querySelector("#email");

        const rating =
            document.querySelector("#rating");

        const message =
            document.querySelector("#msg");


        /*
         * Remove previous error
         */

        const oldError =
            document.querySelector(
                ".feedback-error"
            );

        if (oldError) {
            oldError.remove();
        }


        /*
         * Validate fields
         */

        if (
            name.value.trim() === "" ||
            email.value.trim() === "" ||
            message.value.trim() === ""
        ) {

            showFormError();

            return;
        }


        /*
         * Validate email
         */

        if (!email.checkValidity()) {

            showEmailError();

            return;
        }


        /*
         * Success state
         */

        feedbackForm.innerHTML = `
            <p
                class="feedback-success"
                role="status"
                tabindex="-1"
            >
                ✅ Thank you for your feedback!
            </p>

            <p>
                Your ${rating.value}-star rating
                has been submitted.
            </p>
        `;

        const successMessage =
            document.querySelector(
                ".feedback-success"
            );

        successMessage.focus();
    }
);


/* =========================
   FORM ERROR
========================= */

function showFormError() {

    const errorMessage =
        document.createElement("p");

    errorMessage.className =
        "feedback-error";

    errorMessage.textContent =
        "❌ Please fill in all required fields.";

    errorMessage.setAttribute(
        "role",
        "alert"
    );

    feedbackForm.prepend(errorMessage);


    /*
     * Find first empty field
     */

    const fields = [
        document.querySelector("#name"),
        document.querySelector("#email"),
        document.querySelector("#msg")
    ];

    const emptyField =
        fields.find(
            field => field.value.trim() === ""
        );

    if (emptyField) {
        emptyField.focus();
    }
}


/* =========================
   EMAIL ERROR
========================= */

function showEmailError() {

    const errorMessage =
        document.createElement("p");

    errorMessage.className =
        "feedback-error";

    errorMessage.textContent =
        "❌ Please enter a valid email address.";

    errorMessage.setAttribute(
        "role",
        "alert"
    );

    feedbackForm.prepend(errorMessage);

    document
        .querySelector("#email")
        .focus();
}


/* =========================
   START APPLICATION
========================= */

loadProducts();

loadCategories();

displayFavourites();