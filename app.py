from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
import requests
import re

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Api
api_products = 'https://fakestoreapi.com/products'
api_categories = 'https://fakestoreapi.com/products/categories'


@app.route('/', methods=["GET", "POST"])
def index():
    try:
        # Make a GET request to the API
        response = requests.get(api_products)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON data from the response
            products = response.json()

            # Extract the first three products
            selected_products = products[:3]

            # Get the total quantity from session
            total_quantity = session.get('total_quantity', 0)

            # Render the index template
            return render_template('index.html', products=selected_products, total_quantity=total_quantity)

        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_product_details(product_id):
    product_api_url = f'https://fakestoreapi.com/products/{product_id}'

    # Make a GET request to the API
    response = requests.get(product_api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the product details in JSON format from the response
        return response.json()
    else:
        return None


@app.route('/shop', methods=["GET", "POST"])
def shop():
    try:
        # Make GET requests to the APIs
        response_products = requests.get(api_products)
        response_categories = requests.get(api_categories)

        # Check if the requests were successful
        if response_products.status_code == 200 and response_categories.status_code == 200:
            # Parse the JSON data from the responses
            products = response_products.json()
            categories = response_categories.json()

            # Get the total quantity from session
            total_quantity = session.get('total_quantity', 0)

            # Render the shop template
            return render_template('shop.html', products=products, categories=categories, total_quantity=total_quantity)

        else:
            return f"Error: {response_products.status_code} or {response_categories.status_code}"

    except Exception as e:
        # Log the error for debugging purposes
        app.logger.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Get the JSON data from the request
    data = request.get_json()
    product_id = data.get('product_id')
    # Get product details based on the provided product ID
    selected_product = get_product_details(product_id)

    # Check if the selected product exists
    if selected_product:
        # Get the cart array from the session
        cart = session.get('cart', [])

        # Check if the product is already in the cart
        existing_product = next((item for item in cart if str(item['id']) == product_id), None)

        # Increment the existing product quantity
        if existing_product:
            existing_product['quantity'] += 1
            quantity = existing_product['quantity']
            price = existing_product['price']
        # Else initialize the quantity to 1
        else:
            selected_product['quantity'] = 1
            cart.append(selected_product)
            quantity = 1
            price = selected_product['price']

        # Update the session cart
        session['cart'] = cart

        # Calculate the total price and quantity for all products in the cart
        total = round(sum(product['quantity'] * product['price'] for product in cart), 2)
        total_quantity = sum(product['quantity'] for product in cart)

        # Update the session total_quantity
        session['total_quantity'] = total_quantity

        # Return success message and updated cart details
        return jsonify({
            'message': 'Product added to cart successfully',
            'status': 'success',
            'quantity': quantity,
            'price': price,
            'total': total,
            'total_quantity': total_quantity,
        })

    # Return error message for product not found
    return jsonify({'message': 'Product not found', 'status': 'error'})


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    # Get the cart array from the session
    cart = session.get('cart', [])

    # Find the index of the product to remove
    index_to_remove = next((index for index, item in enumerate(cart) if item['id'] == product_id), None)

    if index_to_remove is not None:
        # Remove the product from the cart
        removed_product = cart.pop(index_to_remove)

        # Update the session with the modified cart
        session['cart'] = cart

        # Calculate the total price and quantity for all products in the cart
        total = round(sum(product['quantity'] * product['price'] for product in cart), 2)
        total_quantity = sum(product['quantity'] for product in cart)

        # Update the session total_quantity
        session['total_quantity'] = total_quantity

        # Return success message and updated cart details
        return jsonify({
            'message': 'Product removed from cart successfully',
            'status': 'success',
            'removed_product': removed_product,
            'total': total,
            'total_quantity': total_quantity,
        })
    else:
        # Return error message for product not found in the cart
        return jsonify({'message': 'Product not found in the cart', 'status': 'error'})


@app.route('/decrease_quantity/<int:product_id>', methods=['POST'])
def decrease_quantity(product_id):
    # Get the cart array from the session
    cart = session.get('cart', [])

    # Find the index of the product to decrease the quantity
    index_to_decrease = next((index for index, item in enumerate(cart) if item['id'] == product_id), None)

    if index_to_decrease is not None:
        # Decrease the quantity of the product in the cart
        cart[index_to_decrease]['quantity'] -= 1

        # Update the session cart
        session['cart'] = cart

        # Calculate the total price and quantity for all products in the cart
        total = round(sum(product['quantity'] * product['price'] for product in cart), 2)
        total_quantity = sum(product['quantity'] for product in cart)

        # Update the session total_quantity
        session['total_quantity'] = total_quantity

        # Return success message and updated cart details
        return jsonify({
            'message': 'Quantity decreased successfully',
            'status': 'success',
            'quantity': cart[index_to_decrease]['quantity'],
            'price': cart[index_to_decrease]['price'],
            'total': total,
            'total_quantity': total_quantity,
        })
    else:
        # Return error message for product not found in the cart
        return jsonify({'message': 'Product not found in the cart', 'status': 'error'})


@app.route('/about', methods=["GET", "POST"])
def about():
    # Get the total quantity from session
    total_quantity = session.get('total_quantity', 0)

    # Render the about template
    return render_template('about.html', total_quantity=total_quantity)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    # Get the total quantity from session
    total_quantity = session.get('total_quantity', 0)

    if request.method == "POST":
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validate form data
        if not name or not email or not message:
            alert_message = "Please fill in all fields"
            return render_template('contact.html', alert_message=alert_message, total_quantity=total_quantity)

        # Validate name
        if not re.match("^[A-Za-z]+$", name):
            alert_message = "Please enter a valid name."
            return render_template('contact.html', alert_message=alert_message, total_quantity=total_quantity)

        # Validate email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            alert_message = "Please enter a valid email address."
            return render_template('contact.html', alert_message=alert_message, total_quantity=total_quantity)

         # Redirect to a success page with a thank you message
        return redirect(url_for('success', alert_message='Thanks for your feedback!'))

    # Render the contact page
    return render_template('contact.html', total_quantity=total_quantity)


@app.route('/cart', methods=["GET", "POST"])
def cart():
    # Get the cart array from the session
    cart = session.get('cart', [])

    # Calculate the total price and quantity for all products in the cart
    total = round(sum(product['quantity'] * product['price'] for product in cart), 2)
    total_quantity = session.get('total_quantity', 0)

    # Render the cart template
    return render_template('cart.html', cart=cart, total=total, total_quantity=total_quantity)


@app.route('/product/<int:product_id>', methods=["GET", "POST"])
def product(product_id):
    # Make an API request to fetch product data
    api_url = f'https://fakestoreapi.com/products/{product_id}'
    response = requests.get(api_url)

    # Check if the requests were successful
    if response.status_code == 200:
        # Parse the JSON response
        product_data = response.json()

        # Get the total quantity from session
        total_quantity = session.get('total_quantity', 0)

        # Render the product template
        return render_template('product.html', product=product_data, total_quantity=total_quantity)
    else:
        return f"Error: {response.status_code}"


@app.route('/success')
def success():
    # Get the total quantity from session
    total_quantity = session.get('total_quantity', 0)
     # Get the alert message
    alert_message = request.args.get('alert_message', None)
    # Render the success template
    return render_template('success.html', alert_message=alert_message, total_quantity=total_quantity)


@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    # Get the total quantity and cart from session
    total_quantity = session.get('total_quantity', 0)
    cart = session.get('cart', [])

    # Calculate the total price of items in the cart
    total = round(sum(product['quantity'] * product['price'] for product in cart), 2)

    # Check if the cart is empty
    cart_empty = total_quantity == 0

    # If the cart is empty, render the cart template
    if cart_empty:
        return render_template('cart.html', total_quantity=total_quantity, cart=cart, total=total)

    if request.method == "POST":
        # Retrieve form data
        name = request.form.get('name')
        address = request.form.get('address')
        card_number = request.form.get('card_number')
        card_name = request.form.get('card_name')
        expiration_date = request.form.get('expiration_date')
        cvv = request.form.get('cvv')

        # Validate form data
        if not name or not address or not card_number or not card_name or not expiration_date or not cvv:
            alert_message = "Please fill in all fields"
            return render_template('checkout.html', alert_message=alert_message, total_quantity=total_quantity)

        # Define regex patterns for form field validation
        name_pattern = "^[A-Za-z ]+$"
        address_pattern = "^[A-Za-z0-9 .,-]+$"
        credit_number_pattern = "^[0-9]{4}( ?[0-9]{4}){3}$"
        expiration_date_pattern = "^(0[1-9]|1[0-2])\/[0-9]{4}$"
        cvv_pattern = "^[0-9]{3,4}$"

        # Validate name and card_name
        if not re.match(name_pattern, name) or not re.match(name_pattern, card_name):
            alert_message = "Please enter a valid name."
            return render_template('checkout.html', alert_message=alert_message, total_quantity=total_quantity)

        # Validate address
        if not re.match(address_pattern, name):
            alert_message = "Please enter a valid address."
            return render_template('checkout.html', alert_message=alert_message, total_quantity=total_quantity)

        # Validate credit number
        if not re.match(credit_number_pattern, card_number):
            alert_message = "Please enter a valid 16-digit credit card number."
            return render_template('checkout.html', alert_message=alert_message, total_quantity=total_quantity)

        # Validate expiration date
        if not re.match(expiration_date_pattern, expiration_date):
            alert_message = "Please enter a valid expiration date in MM/YYYY format."
            return render_template('checkout.html', alert_message=alert_message, total_quantity=total_quantity)

        # Validate cvv
        if not re.match(cvv_pattern, cvv):
            alert_message = "Please enter a valid 3 or 4-digit CVV."
            return render_template('checkout.html', alert_message=alert_message, total_quantity=total_quantity)

        # Clear the cart and total_quantity from the session
        session.pop('cart', None)
        session.pop('total_quantity', 0)

        # Redirect to the success page
        return redirect(url_for('success', alert_message='Thank you for your purchase!'))

    # Render the checkout template
    return render_template('checkout.html', total_quantity=total_quantity)
