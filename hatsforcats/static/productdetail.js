/********************************
Developer: Azaan Mudassar
University ID: 230098501
********************************/

console.log("loaded!");

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


//func for adding to basket 
document.addEventListener('DOMContentLoaded', () => {
    //get all the relevant btns 
    const colourBtn = document.querySelectorAll('.color-circle');
    const sizeBtn = document.querySelectorAll('.size-circle');
    const basketAddBtn = document.querySelector('.cartbutton');
    const quantityBtns = document.querySelectorAll('.quantity-btn');

    let selected_colour = null;
    let selected_size = null;

    function validateSelections() {
        const colourSelected = !!selected_colour;
        const sizeSelected = !!selected_size;

        //disable the basket btn
        basketAddBtn.disabled = !(colourSelected && sizeSelected);
        quantityBtns.forEach(control => control.disabled = !(colourSelected && sizeSelected));
    }

    //listeners for colours
    colourBtn.forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault(); 
            selected_colour = button.getAttribute('data-colour'); //gets selected colour
            validateSelections();
        });
    });

    //listeners for size
    sizeBtn.forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault(); 
            selected_size = button.getAttribute('data-size'); //gets selected size
            validateSelections();
        });
    });

    validateSelections();

});