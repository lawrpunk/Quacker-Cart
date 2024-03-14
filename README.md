# Quacker Cart

#### Description

Welcome to Quaker Cart! An easy-to-use online store where you can find great products. The website works well on any device, making it simple for everyone to explore and shop.

## Table of Contents

- [Description](#description)
- [HTML](#html)
- [CSS](#css)
- [JavaScript](#javascript)
- [Flask](#flask)

## Description

In this project, I used Python with the Flask framework for the backend, and HTML, CSS, and JavaScript for the frontend. Additionally, I integrated various tools and APIs, such as the Fake Store API for product data, Font Awesome for icons, and LOGO.com for creating the website's logo. My initial goal was to design a user-friendly interface to ensure accessibility for all users on any device, enabling them to seamlessly purchase products from the site.

## HTML

In the `templates` folder, there are nine HTML files for this project. The crucial file `layout.html` defines the overall structure used by most other files. It employs Jinja templating for dynamic content in the title and main sections, reducing redundancy across files.

`layout.html` centralizes essential elements like links to Bootstrap, Font Awesome, CSS, and JS, avoiding repetition in every file. It features a navigation bar and footer. The `main` section uses Jinja's block feature, allowing other files to add their content without duplicating the navigation bar and other common elements.

## CSS

The primary CSS file `style.css` is in the `static` folder and plays a key role in shaping the website's visual appeal. In this file, I've added the Google font Afacad to enhance the overall typography.

The color scheme of the website is composed of #093D65, #F98E54, #FFFFFF, and #333333, lending an engaging visual experience. To ensure adaptability across various devices, the CSS files include media queries, allowing the design to be responsive and user-friendly on screens of all sizes.

## JavaScript

The `script.js` file, in the `static` folder, adds dynamic behavior and interactivity to the website. It handles various aspects such as updating the cart, adjusting quantities, implementing responsive design features, and enabling user-friendly functionalities like searching for products.

**Event Listeners:**

- `document.addEventListener("scroll", handleScroll);`: Listens for the scroll event to change the background color of the navbar.
- `document.addEventListener('DOMContentLoaded', handleCategory);`: Listens for the DOMContentLoaded event to update the UI based on the selected category.
- `document.getElementById('searchInput').addEventListener('input', searchProduct);`: Listens for the input event on the search input field to dynamically search for products.

**Functions:**

- `addToCart(productId)`: Adds the selected product to the cart using AJAX to communicate with the server.
- `increaseQuantity(productId)`: Increases the quantity of the selected product in the cart using AJAX.
- `decreaseQuantity(productId)`: Decreases the quantity of the selected product in the cart using AJAX. If the quantity becomes zero, it removes the product.
- `removeFromCart(productId)`: Removes the selected product from the cart using AJAX.
- `updateCartBadge(quantity)`: Updates the cart badge displaying the total quantity of items in the cart.
- `handleScroll()`: Changes the background color of the navbar when scrolled.
- `handleCategory()`: Updates the shop UI based on the selected category.
- `selectCustomPriceRange()`: Shows products within a custom price range based on user input.
- `resetPage()`: Reloads the page.
- `searchProduct()`: Filters and displays products based on user input in the search bar.

## Flask

**File Name:** `app.py`

**Description:** The `app.py` file is the main Flask application responsible for handling various routes and functionalities of the e-commerce website. The file serves as the backbone of the web application, defining routes, handling data from external APIs, and ensuring smooth interactions between the user and the server.

**Flask Setup:**

- Configuration of the Flask application, setting up the session to use the filesystem for storage.

**API:**

- Definition of API (api_products and api_categories) for fetching product and category data from [Fake Store API](https://fakestoreapi.com).

**Routes:**

- `/` (index): Displays a selection of products on the home page.
- `/shop`: Renders the shop page with all available products and categories.
- `/add_to_cart`: Handles AJAX requests to add products to the shopping cart.
- `/remove_from_cart`: Handles AJAX requests to remove products from the shopping cart.
- `/decrease_quantity`: Handles AJAX requests to decrease the quantity of products in the cart.
- `/about` and `/contact`: Display static content on the about and contact pages.
- `/cart`: Renders the shopping cart page with added products.
- `/product/<int:product_id>`: Displays details of a specific product.
- `/success`: Displays a success page.
- `/checkout`: Manages the checkout process, handling form submissions for user details and payment.

**Functions:**

- `get_product_details(product_id)`: A utility function to fetch details of a specific product from the API.

## Acknowledgments

- API: [Fake Store API](https://fakestoreapi.com/)
- Icons: [Font Awesome](https://fontawesome.com/)
- Logo: [LOGO.com](https://app.logo.com)
- Bootstrap: [Bootstrap](https://getbootstrap.com/)
