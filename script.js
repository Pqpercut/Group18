/**********************
Developer: Khalid Abukar
University ID: 230129012
**********************/

// references to relevant elements
const wishlistList = document.getElementById('wishlistList');
const newWishlistBtn = document.getElementById('newWishlistBtn');
const wishlistTitle = document.getElementById('wishlistTitle');

// Modal elements
const modal = document.getElementById('modal');
const closeModal = document.querySelector('.close');
const createWishlistBtn = document.getElementById('createWishlistBtn');
const newWishlistNameInput = document.getElementById('newWishlistName');
// NEW ITEM LINK reference (for the header "NEW" link)
const newItemLink = document.getElementById('newItemLink');

// references for the Edit Wishlist functionality
const editWishlistLink = document.getElementById('editWishlistLink');
const editModal = document.getElementById('editModal');
const editClose = document.querySelector('.edit-close');
const editWishlistNameInput = document.getElementById('editWishlistName');
const saveWishlistBtn = document.getElementById('saveWishlistBtn');


//references for the Delete Wishlist functionality
const deleteWishlistLink = document.getElementById('deleteWishlistLink');
const deleteModal = document.getElementById('deleteModal');
const deleteClose = document.querySelector('.delete-close');
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

// Open the modal when "New Wishlist" button is clicked
newWishlistBtn.addEventListener('click', () => {
  newWishlistNameInput.value = ""; // clear any previous input
  modal.style.display = 'block';
});

// Close the modal when the close span is clicked
closeModal.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Also close modal if user clicks outside the modal-content area
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

// When the Create button is pressed inside the modal:
createWishlistBtn.addEventListener('click', () => {
  const wishlistName = newWishlistNameInput.value.trim();
  if (wishlistName) {
    // Create a new <li><a> entry for the new wishlist
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#';
    a.textContent = wishlistName;
    a.dataset.wishlist = wishlistName;
    a.dataset.new = "true";

    // When user clicks this new link, set it active
    a.addEventListener('click', (e) => {
      e.preventDefault();
      setActiveWishlist(a);
    });

    li.appendChild(a);
    wishlistList.appendChild(li);

    // Immediately switch to the new wishlist in the main area
    setActiveWishlist(a);
    
    // Close the modal
    modal.style.display = 'none';
  }
});


// Attach a click listener on the document (or a parent container)
document.addEventListener('click', function(e) {
  // Check if the clicked element has the class 'remove-btn'
  if (e.target && e.target.classList.contains('remove-btn')) {
    e.preventDefault();
    const wishlistItem = e.target.closest('.wishlist-item');
    if (wishlistItem) {
      wishlistItem.remove();
    }
  }
});

// When the Edit button is clicked, open the edit modal and pre-fill the input
editWishlistLink.addEventListener('click', (e) => {
  e.preventDefault();
  // Pre-fill with the current wishlist title
  editWishlistNameInput.value = wishlistTitle.textContent;
  editModal.style.display = 'block';
});

// Close the edit modal when the user clicks the close icon
editClose.addEventListener('click', () => {
  editModal.style.display = 'none';
});

// Also close the modal if the user clicks outside the modal content
window.addEventListener('click', (e) => {
  if (e.target === editModal) {
    editModal.style.display = 'none';
  }
});

// When the user clicks Save in the edit modal:
saveWishlistBtn.addEventListener('click', () => {
  const newName = editWishlistNameInput.value.trim();
  if (newName) {
    // Update the header title
    wishlistTitle.textContent = newName;
    
    // Also update the active link in the sidebar
    const activeLink = document.querySelector('#wishlistList a.active');
    if (activeLink) {
      activeLink.textContent = newName;
      activeLink.dataset.wishlist = newName;
    }
    // Close the modal
    editModal.style.display = 'none';
  }
});

// Open the delete modal when the Delete button is clicked
deleteWishlistLink.addEventListener('click', (e) => {
  e.preventDefault();
  deleteModal.style.display = 'block';
});

// Close the delete modal when the user clicks the close icon
deleteClose.addEventListener('click', () => {
  deleteModal.style.display = 'none';
});

// Close the delete modal if the user clicks outside the modal content
window.addEventListener('click', (e) => {
  if (e.target === deleteModal) {
    deleteModal.style.display = 'none';
  }
});

// Cancel deletion when the Cancel button is clicked
cancelDeleteBtn.addEventListener('click', () => {
  deleteModal.style.display = 'none';
});

// Confirm deletion when the Yes, Delete button is clicked
confirmDeleteBtn.addEventListener('click', () => {
  // Find the currently active wishlist link in the sidebar
  const activeLink = document.querySelector('#wishlistList a.active');
  if (activeLink) {
    // Remove its parent <li> from the wishlist list
    activeLink.parentElement.remove();
    
    // Optionally update the header title and product container
    // If there is another wishlist, set it active. Otherwise, clear the main area.
    const remainingLinks = document.querySelectorAll('#wishlistList a');
    if (remainingLinks.length > 0) {
      // Activate the first one (or you can choose another logic)
      setActiveWishlist(remainingLinks[0]);
    } else {
      wishlistTitle.textContent = "No Wishlist Selected";
      const productContainer = document.getElementById('productContainer');
      if (productContainer) {
        productContainer.innerHTML = '<p id="emptyMessage">Your wishlist is empty. Add some products!</p>';
      }
    }
  }
  // Close the modal after deletion
  deleteModal.style.display = 'none';
});


// Helper function to mark a wishlist as active and update the title
function setActiveWishlist(linkElement) {
  // Remove "active" class from all existing wishlist links
  const allLinks = wishlistList.querySelectorAll('a');
  allLinks.forEach(link => link.classList.remove('active'));

  // Add "active" class to the clicked link
  linkElement.classList.add('active');

  // Update the main title to match
  wishlistTitle.textContent = linkElement.dataset.wishlist;

  // If this wishlist is new (has no products), clear the product container
  if (linkElement.dataset.new === "true") {
    productContainer.innerHTML = '<p id="emptyMessage">Your wishlist is empty. Add some products!</p>';
    
  } else {
    
  }
}
// Function to open the modal for creating a new wishlist
function openNewWishlistModal(e) {
  e.preventDefault();
  newWishlistNameInput.value = ""; // clear any previous input
  modal.style.display = 'block';
}


newWishlistBtn.addEventListener('click', openNewWishlistModal);
newItemLink.addEventListener('click', openNewWishlistModal);