document.addEventListener('DOMContentLoaded', () => {
    const searchIcon = document.querySelector('.searchIcon');
    const searchPopup = document.getElementById('searchPopup');
    const closeSearchIcon = document.getElementById('closeSearch');
    const searchBox = document.getElementById('searchBox');
    const searchResults = document.getElementById('searchList');
    const trendingSection = document.getElementById('trendingSection');
    const trendingTitle = document.getElementById('trendingTitle');
    const featuredProduct = document.querySelector('.featured-product');
    const featuredImage = document.querySelector('.featured-product img');
    const overlay = document.getElementById('searchOverlay');

    // Open search popup
    searchIcon.addEventListener('click', () => {
        searchPopup.style.display = 'block';
        overlay.style.display = 'block';
        searchBox.focus();
    });

    // Close search popup
    closeSearchIcon.addEventListener('click', () => {
        searchPopup.style.display = 'none';
        overlay.style.display = 'none';
        searchBox.value = ''; // Clear search input
        trendingTitle.textContent = 'Trending'; // Reset title
        resetTrending();
    });

    // Close popup when clicking outside overlay
    overlay.addEventListener('click', () => {
        searchPopup.style.display = 'none';
        overlay.style.display = 'none';
        searchInput.value = ''; // Clear search input
        trendingTitle.textContent = 'Trending'; // Reset title
        resetTrending();
    });

    // Live search function
    searchInput.addEventListener('input', () => {
        const filter = searchInput.value.toLowerCase();
        if (filter.length > 0) {
            trendingTitle.textContent = 'Results'; // Change title to Results
            searchResults.innerHTML = ''; // Clear previous results

            // Placeholder for backend data (example)
            const dummyResults = ["Fancy Cat Hat", "Winter Kitty Beanie", "Luxury Feline Fedora", "Playful Kitten Cap"];
            
            dummyResults.forEach(result => {
                if (result.toLowerCase().includes(filter)) {
                    const li = document.createElement('li');
                    li.textContent = result;
                    searchResults.appendChild(li);
                }
            });
        } else {
            trendingTitle.textContent = 'Trending'; // Reset title
            resetTrending();
        }
    });

    // Function to reset trending list
    function resetTrending() {
        searchResults.innerHTML = `
            <li>Top Cat Hats</li>
            <li>Winter Warmers</li>
            <li>Luxury Feline Collection</li>
            <li>Best Sellers</li>
        `;
    }


});
