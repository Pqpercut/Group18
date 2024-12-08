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


//saki's shi to make the basket adding work
//assigning variables
let selected_colour = null
let selected_size = null
let quantity = 1

//
function colourSelect(col) {
    selected_colour = col;
    //console.log(selected_colour);
    document.getElementById("hidden-colour").value = col;
    check_selected();
}

//
function sizeSelect(size) {
    selected_size = size;
    //console.log(selected_size);
    document.getElementById("hidden-size").value = size;
    check_selected();
}

//quantity
function change_quantity(q) {
    quantity += q
    if (quantity < 1) {
        quantity = 1;
    } else if (quantity > 99) {
        quantity = 99;
    }
}

//check if size n colour selected
function check_selected() {
    if ((selected_colour != null) && (selected_size != null)){
        console.log("basket enabled!")
        //enables basket adding 
        //document.getElementById("decrease").disabled = false;
        //document.getElementById("increase").disabled = false;
        //document.getElementById("add-to-cart").disabled = false;

        console.log(String(selected_colour), String(selected_size));
    } else {
        //keeps the adding to basket disabled
        //document.getElementById("decrease").disabled = true;
        //document.getElementById("increase").disabled = true;
        //document.getElementById("add-to-cart").disabled = true;

        console.log(String(selected_colour), String(selected_size));
    }
}

