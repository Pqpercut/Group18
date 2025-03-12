        // Simulated backend response (example data)
        const notifications = [
            { message: "Stock for Gotham Kitty is running low", date: "02/02/2025", priority: "!!", read: false },
            { message: "An order has been created for _______", date: "02/02/2025", priority: "!", read: false },
            { message: "Stock for ___ small has ran out", date: "02/02/2025", priority: "!!", read: true },
            { message: "User has a problem with a product", date: "01/02/2025", priority: "!!!", read: false }
        ];

        function loadNotifications() {
            const notificationsList = document.getElementById("notificationsList");
            notificationsList.innerHTML = ""; // Clear existing notifications

            notifications.forEach(notification => {
                const row = document.createElement("tr");
                row.classList.add(notification.read ? "read" : "unread");
                
                row.innerHTML = `
                    <td class="notification-message">${notification.read ? notification.message : `<strong>${notification.message}</strong>`}</td>
                    <td>${notification.date}</td>
                    <td class="priority">${notification.priority}</td>
                `;
                
                notificationsList.appendChild(row);
            });
        }

        // Load notifications dynamically on page load
        loadNotifications();

        function openPopup() {
            document.getElementById("notificationPopup").style.display = "flex";
        }

        function closePopup() {
            document.getElementById("notificationPopup").style.display = "none";
        }

        document.addEventListener("DOMContentLoaded", () => {
            const sendNotificationButton = document.querySelector(".send-notification");
            const popup = document.getElementById("notificationPopup");
            const closePopupButton = document.querySelector(".popup .close");
        

            // Open Popup on Button Click
            sendNotificationButton.addEventListener("click", () => {
                console.log("Opening popup...");
                popup.style.display = "flex"; // Show popup
            });
        
            // Close Popup on X Button Click
            closePopupButton.addEventListener("click", () => {
                console.log("Closing popup...");
                popup.style.display = "none"; // Hide popup
            });
        
            // Close Popup if Clicking Outside of Popup Content
            popup.addEventListener("click", (event) => {
                if (event.target === popup) {
                    console.log("Closing popup by clicking outside...");
                    popup.style.display = "none";
                }
            });
        });