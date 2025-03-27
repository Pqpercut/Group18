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
let selected_colour = ""
let selected_size = ""
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
	//check if btn is already selected 
	//if selected, remove selection 
	if (selected_colour === col) {
		//console.log('UNSELECT');
		selected_colour = null;
		document.getElementById("hidden-colour").value = null;
		button.classList.remove("active");

		check_selected();

	//else update col to be the same as selection
	} else {
		selected_colour = col;
		//console.log(selected_colour);
		document.getElementById("hidden-colour").value = col;
		colour_persist(button);
	}
	updateSize(selected_colour);
}


//same as colour but with size instead
function sizeSelect(size, button) {
	if (selected_size === size) {
		selected_size = null;
		document.getElementById("hidden-size").value = null;
		button.classList.remove("active");

		check_selected();    
	} else {
		selected_size = size;
		//console.log(selected_size);
		document.getElementById("hidden-size").value = size;
		size_persist(button);
	}
	updateColour(selected_size);
}


//makes the button purp (active class = making btn purple)
function colour_persist(button) {
	//remove active class from all buttons
	const buttons = document.querySelectorAll('.color-circle');
	buttons.forEach(btn => btn.classList.remove('active'));

	//add active class to clicked button
	if (selected_colour) {
		button.classList.add('active');
	}
}

function size_persist(button) {
	//remove active class from all buttons
	const buttons = document.querySelectorAll('.size-circle');
	buttons.forEach(btn => btn.classList.remove('active'));

	//add active class to clicked button
	if (selected_size) {
		button.classList.add('active');
	}
}


//to update the sizes when colour clicked
function updateSize(selected_colour) {
	const sizeButtons = document.querySelectorAll(".size-circle");
	//console.log(selected_colour);

	//console.log(size_list);
	//console.log(available_sizes[selected_colour]);
	sizeButtons.forEach((button) => { //loop through btns
		const size = button.dataset.size;

		//if colour available in that size, make btn active 
		if (available_sizes[selected_colour]?.includes(size) || selected_colour === null) {
			console.log("enabling buttons");
			button.classList.remove("disabled");
			button.disabled = false;
		//else disable it 
		} else {
			console.log("killing buttons");
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

		if (available_colours[selected_size]?.includes(colour) || selected_size === null){
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
		if (
			available_sizes[selected_colour]?.includes(selected_size) &&
			available_colours[selected_size]?.includes(selected_colour)
		) {
			console.log("basket enabled!")
			//console.log(document.getElementById("add-to-cart"));
			//enables basket adding 
			//document.getElementById("decrease").disabled = false;
			//document.getElementById("increase").disabled = false;
			document.getElementById("add-to-cart").removeAttribute('disabled');
		} else {
			document.getElementById("add-to-cart").setAttribute('disabled');
			console.log("basket disabled");
		}

		//console.log(String(selected_colour), String(selected_size));
	} else {
		//keeps the adding to basket disabled
		//document.getElementById("decrease").disabled = true;
		//document.getElementById("increase").disabled = true;
		document.getElementById("add-to-cart").disabled = true;
		console.log("basket disabled");

		//console.log(String(selected_colour), String(selected_size));
	}
}





