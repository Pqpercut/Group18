/********************************
Developer: Azaan Mudassar
University ID: 230098501
********************************/

console.log("loaded!");



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


//available sizes once the colour is clicked
//const available_sizes = document.getElementById("size-data");
//const available_sizes = JSON.parse(size_map.value);
//const available_sizes = JSON.parse(document.getElementById("size-data").value);
console.log(available_sizes);
console.log(available_colours);
size_list = document.getElementById("size_list").value.split(","); //list of all sizes
colour_list = document.getElementById("colour_list").value.split(","); //list of all colours


//
function colourSelect(col, button) {
    // Remove active class from all buttons
    selected_colour = col;
    //console.log(selected_colour);
    document.getElementById("hidden-colour").value = col;
    updateSize(col);
    colour_persist(button);
}


//
function sizeSelect(size, button) {
    selected_size = size;
    //console.log(selected_size);
    document.getElementById("hidden-size").value = size;
    updateColour(size);
    size_persist(button);
}


//makes the button purp
function colour_persist(button) {
    //remove active class from all buttons
    const buttons = document.querySelectorAll('.color-circle');
    buttons.forEach(btn => btn.classList.remove('active'));

    //add active class to clicked button
    button.classList.add('active');
}

function size_persist(button) {
    //remove active class from all buttons
    const buttons = document.querySelectorAll('.size-circle');
    buttons.forEach(btn => btn.classList.remove('active'));

    //add active class to clicked button
    button.classList.add('active');
}


//to update the sizes when colour clicked
function updateSize(selected_colour) {
    const sizeButtons = document.querySelectorAll(".size-circle");
    console.log(selected_colour);

    //console.log(size_list);
    console.log(available_sizes[selected_colour]);
    sizeButtons.forEach((button) => {
        const size = button.dataset.size;

        if (available_sizes[selected_colour]?.includes(size)) {
            button.classList.remove("disabled");
            button.disabled = false;
        } else {
            button.classList.add("disabled");
            button.disabled = true;
        }
    });

    check_selected();
}

//to update the colour when size clicked
function updateColour(selected_size) {
    const colourButtons = document.querySelectorAll(".color-circle");
    //console.log(selected_size);

    colourButtons.forEach((button) => {
        const colour = button.dataset.colour;
        //console.log(colour);

        if (available_colours[selected_size]?.includes(colour)) {
            button.disabled = false;
            button.classList.remove("disabled");
        } else {
            //console.log(selected_size);
            //console.log(colour);
            button.disabled = true;
            button.classList.add("disabled");
        }
    });

    check_selected();
}


//quantity
function change_quantity(q) {
    const q_inp = document.getElementById("quantity-input");
    let quantity = parseInt(q_inp.value) + q;

    if (quantity < 1) {
        quantity = 1;
    } else if (quantity > 99) {
        quantity = 99;
    }

    q_inp.value = quantity;

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

