/********************************
Developer: Azaan Mudassar
University ID: 230098501
********************************/


const images = [
    "https://via.placeholder.com/600x400/FFFFFF",
    "https://via.placeholder.com/140x140/FFFFFF",
    "https://via.placeholder.com/140x140/FFFFFF",
    "https://via.placeholder.com/140x140/FFFFFF"
];

let currentIndex = 0; // Current image index

// Function to update the main image
function updateMainImage() {
    const mainImage = document.getElementById("main-image");
    mainImage.src = images[currentIndex];
    mainImage.alt = `Thumbnail ${currentIndex + 1}`;
}

// Function to go to the next image
function nextImage() {
    currentIndex = (currentIndex + 1) % images.length; // Loop back to the first image
    updateMainImage();
}

// Function to go to the previous image
function previousImage() {
    currentIndex = (currentIndex - 1 + images.length) % images.length; // Loop back to the last image
    updateMainImage();
}

// Function to change the main image when a thumbnail is clicked
function changeMainImage(index) {
    currentIndex = index; // Update current index
    updateMainImage();
}

// Quantity adjustment logic
document.getElementById("increase").addEventListener("click", () => {
    const quantityInput = document.getElementById("quantity-input");
    let currentValue = parseInt(quantityInput.value, 10); // Get the current value as an integer
    if (currentValue < parseInt(quantityInput.max, 10)) {
        quantityInput.value = currentValue + 1; // Increment the value
    }
});

document.getElementById("decrease").addEventListener("click", () => {
    const quantityInput = document.getElementById("quantity-input");
    let currentValue = parseInt(quantityInput.value, 10); // Get the current value as an integer
    if (currentValue > parseInt(quantityInput.min, 10)) {
        quantityInput.value = currentValue - 1; // Decrement the value
    }
});
