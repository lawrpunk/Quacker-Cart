document.addEventListener("scroll", handleScroll);
document.addEventListener('DOMContentLoaded', handleCategory);
document.getElementById('searchInput').addEventListener('input', searchProduct);

// Add selected product in cart
function addToCart(productId) {
    // Use AJAX to send the product ID to the server
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);

            // Update the cart badge
            updateCartBadge(data.total_quantity);
            localStorage.setItem('cartQuantity', data.total_quantity);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Update the cart badge
function updateCartBadge(quantity) {
    const cartBadge = document.querySelector(".cart-badge");
    const cartBadgeMobile = document.querySelector(".cart-badge-mobile");
    cartBadge.textContent = quantity;
    cartBadgeMobile.textContent = quantity;
}

// Increase the quantity of the seleceted product
function increaseQuantity(productId) {
    // Use AJAX to send the product ID to the server for increasing the quantity
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data && data.quantity !== undefined && data.price !== undefined) {
            console.log(data.message);

            const totalPrice = (data.quantity * data.price).toFixed(2);
            const quantityElement = document.getElementById(`quantity-${productId}`);
            const quantityMobileElement = document.getElementById(`mobile-quantity-${productId}`);
            const totalElement = document.getElementById(`total-${productId}`);
            const totalPirce = document.getElementById('cart-total');

            // Update the displayed quantity, total and cart badge on the page
            if (quantityElement && totalElement && quantityMobileElement) {
                quantityElement.textContent = data.quantity;
                quantityMobileElement.textContent = data.quantity;
                totalElement.textContent = `$${totalPrice}`;
                totalPirce.textContent = `$${data.total}`;
                updateCartBadge(data.total_quantity);
                localStorage.setItem('cartQuantity', data.total_quantity);
            }

        } else {
            console.error('Invalid server response:', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Decrease the quantity of the selected product
function decreaseQuantity(productId) {
    // Use AJAX to send the product ID to the server for decreasing the quantity
    fetch(`/decrease_quantity/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);

        const totalPrice = (data.quantity * data.price).toFixed(2);
        const quantityElement = document.getElementById(`quantity-${productId}`);
        const quantityMobileElement = document.getElementById(`mobile-quantity-${productId}`);
        const totalElement = document.getElementById(`total-${productId}`);
        const totalPirce = document.getElementById('cart-total');

        // Update the displayed quantity, total and cart badge on the page
        if (quantityElement && totalElement && quantityMobileElement) {
            quantityElement.textContent = data.quantity;
            quantityMobileElement.textContent = data.quantity;
            totalElement.textContent = `$${totalPrice}`;
            totalPirce.textContent = `$${data.total}`;
            updateCartBadge(data.total_quantity);
            localStorage.setItem('cartQuantity', data.total_quantity);
        }

        if (data.quantity === 0) {
            removeFromCart(productId)
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Remove selected product from the cart
function removeFromCart(productId) {
    // Use AJAX to send the product ID to the server to remove the selected product
    fetch(`/remove_from_cart/${productId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);

        // Remove the row from the table
        const tableRow = document.getElementById(`product-row-${productId}`);
            if (tableRow) {
                tableRow.remove();
            }

        // Update the total price
        const totalElement = document.getElementById('cart-total');
            if (totalElement) {
                totalElement.textContent = `$${data.total}`;
            }

            // Update the cart badge
            updateCartBadge(data.total_quantity);
            localStorage.setItem('cartQuantity', data.total_quantity);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Change the background color of navbar when scrolled
function handleScroll() {
    const navbar = document.querySelector(".navbar");
    const navbarLinks = document.querySelectorAll(".nav-link")

    navbar.classList.toggle("navbar-scrolled", window.scrollY > 0);

    navbarLinks.forEach(link => {
        link.classList.toggle("navbar-link-scrolled", window.scrollY > 0);
    });
}

// Update the shop UI according to the selected cateogry
function handleCategory() {
    const checkboxes = document.querySelectorAll(".category-checkbox");
    const categoryHeading = document.querySelector(".products-category-heading");
    const selectedCategories = [];
    let selectedCategoriesText = "";

    // Update the UI by selected category
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const selectedCategory = this.id;

            if (!this.checked) {
                // Remove unselected category from the array
                const index = selectedCategories.indexOf(selectedCategory);
                if (index !== -1) {
                    selectedCategories.splice(index, 1);
                }
            } else {
                // Add selected category to the array
                selectedCategories.push(selectedCategory);
            }

            // If no categories are selected, show all product cards
            if (selectedCategories.length === 0) {
                const allProductCards = document.querySelectorAll(".product-card");
                allProductCards.forEach(function (card) {
                    card.style.display = "block";
                    categoryHeading.textContent = "Featured Products";
                });
                return;
            }

            // Hide all product cards
            const productCards = document.querySelectorAll(".product-card");
            productCards.forEach(function (card) {
                card.style.display = "none";
            });

            selectedCategoriesText = "";

            // Show product cards belonging to the selected categories
            selectedCategories.forEach(function (category) {
                const selectedProductCards = document.querySelectorAll('.product-card[data-category="' + category + '"]');
                selectedProductCards.forEach(function (card) {
                    card.style.display = "block";
                });

                const capitalized = category.charAt(0).toUpperCase() + category.slice(1);
                selectedCategoriesText += `${capitalized} - `;
            });

            selectedCategoriesText = selectedCategoriesText.slice(0, -2);
            categoryHeading.textContent = selectedCategoriesText;
        });
    });
}

// Show products through price range
function selectCustomPriceRange() {
    const productCards = document.querySelectorAll(".product-card");
    const productCardsPrice = document.querySelectorAll(".card-price");

    // Get the values from the user
    const minPrice = parseFloat(document.querySelector("#minPrice").value);
    const maxPrice = parseFloat(document.querySelector("#maxPrice").value);

    // Hide all product cards
    productCards.forEach(function (card) {
        card.style.display = "none";
    })

    // Show product cards belonging to the selected price range
    productCardsPrice.forEach((cardPrice) => {
        const price = parseFloat(cardPrice.textContent.replace(/[^\d.]/g, ''));
        if (price >= minPrice && price <= maxPrice) {
            const selectedProductCards = document.querySelectorAll('.product-card[data-price="' + price + '"]');
            selectedProductCards.forEach(function (card) {
                card.style.display = "block";
            });
        }
    });
}

// Reload the page
function resetPage() {
    location.reload();
}


// Search for products
function searchProduct() {
    const productCards = document.querySelectorAll(".product-card");
    const searchInput = event.target.value.toLowerCase();
    const productsTitle = document.querySelectorAll('.product-title');

    // Hide all product cards
    productCards.forEach(function (card) {
        card.style.display = "none";
    })

    // Display the searched products
    productsTitle.forEach((title) => {
        const titleText = title.textContent;

        if (titleText.toLowerCase().includes(searchInput)) {
            const selectedProductCards = document.querySelectorAll('.product-card[data-title="' + titleText + '"]');
            selectedProductCards.forEach((card) => {
                card.style.display = "block";
            })
        }
    })
}

