/********************************
Developer: Azaan Mudassar
University ID: 230098501
********************************/



const basketIcon = document.getElementById('BasketIcon');
const cartPopup = document.getElementById('BasketPopUp');
const closePopup = document.getElementById('ClosePopUp');
const cartItems = document.getElementById('CartItems');
const totalPrice = document.getElementById('totalPrice');
const itemsHeader = cartPopup.querySelector('.basket-header h2'); // Select the "Items" text

// Sample Data (Replace with dynamic data)
let cart = [
    { id: 1, name: "Product 1", price: 10.99, quantity: 1, color: "Blue", size: "Large", image: "https://via.placeholder.com/192x148/FFFFFF" },
    { id: 2, name: "Product 2", price: 5.49, quantity: 2, color: "Red", size: "Medium", image: "https://via.placeholder.com/192x148/FFFFFF" },
    { id: 3, name: "Product 3", price: 8.99, quantity: 1, color: "Green", size: "Small", image: "https://via.placeholder.com/192x148/FFFFFF" }
];

// Function to calculate total
function calculateTotal() {
    return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function renderCart() {
    cartItems.innerHTML = ''; // Clear existing items
    let total = 0;
    let totalQuantity = 0;

    cart.forEach(item => {
        total += item.price * item.quantity;
        totalQuantity += item.quantity;

        // Create the cart item container
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');

        // Set up the image
        const img = document.createElement('img');
        img.src = item.image;
        img.alt = item.name;
        img.classList.add('cart-item-img');

        // Set up the details container (flexbox for horizontal layout)
        const details = document.createElement('div');
        details.classList.add('cart-item-details');

        // Create the product name and price container
        const namePriceContainer = document.createElement('div');
        namePriceContainer.classList.add('name-price-container');

        // Add product name
        const name = document.createElement('p');
        name.classList.add('product-name');
        name.innerText = item.name;

        // Add price and quantity
        const priceQuantity = document.createElement('p');
        priceQuantity.classList.add('product-price');
        priceQuantity.innerText = `£${item.price.toFixed(2)} x ${item.quantity}`;

        // Append name and price to the name-price container
        namePriceContainer.appendChild(name);
        namePriceContainer.appendChild(priceQuantity);

        // Add additional details dynamically (color and size)
        const color = document.createElement('p');
        color.classList.add('product-color');
        color.innerText = `Color: ${item.color}`;

        const size = document.createElement('p');
        size.classList.add('product-size');
        size.innerText = `Size: ${item.size}`;

        // Append all details to the details container
        details.appendChild(namePriceContainer); // Name and price horizontally
        details.appendChild(color);
        details.appendChild(size);

        // Append image and details to the cart item
        cartItem.appendChild(img);
        cartItem.appendChild(details);

        // Append the cart item to the cart items container
        cartItems.appendChild(cartItem);
    });

    // Update the total price dynamically
    totalPrice.innerText = `£${calculateTotal().toFixed(2)}`;

    // Update the Items text dynamically
    itemsHeader.innerText = `${totalQuantity} Items`;
}


// Toggle Popup Visibility
basketIcon.addEventListener('click', () => {
    cartPopup.style.display = 'flex';
    renderCart();
});

closePopup.addEventListener('click', () => {
    cartPopup.classList.add('slide-up');
    setTimeout(() => {
        cartPopup.style.display = 'none';
        cartPopup.classList.remove('slide-up');
    }, 400);
});

// Example: Updating cart dynamically
function updateCart(productId, quantity) {
    const product = cart.find(item => item.id === productId);
    if (product) {
        product.quantity = quantity; // Update quantity
        renderCart(); // Re-render the cart
    }
}


