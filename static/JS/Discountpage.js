document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("discountPopup");
    const openpopupBtn = document.querySelector(".newdiscount-btn");
    const closepopup = document.querySelector(".close");
    const cancelpopup = document.querySelector(".cancel-btn");
    const saveDiscount = document.getElementById("saveDiscount");

    /*const offers = document.querySelectorAll(".offer");


    let currentIndex = 0;
    
    function changeOffer() {
        offers[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % offers.length;
        offers[currentIndex].classList.add("active");
    }
    
    setInterval(changeOffer, 3000);
    document.getElementById("offerBanner").addEventListener("click", changeOffer);*/
    


    // Open and close popup 
    openpopupBtn.addEventListener("click", () => {
        popup.style.display = "flex";
    });
   
    closepopup.addEventListener("click", () => {
        popup.style.display = "none";
    });

    cancelpopup.addEventListener("click", () => {
        popup.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });

    saveDiscount.addEventListener("click", () => {
        alert("Discount Added Successfully!");
        popup.style.display = "none";
    });
});