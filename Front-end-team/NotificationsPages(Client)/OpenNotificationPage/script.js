        //  (example data)
        const notificationData = {
            title: "Your order for _______ has been shipped",
            orderNumber: "CAT12345MEOW",
            date: "02/01/2025",
            statusMessage: "Your order for x has been shipped! You can check the delivery status of your order through the courier website <a href='#'>evri.com</a>",
            product: "Gotham Kitty Small x1",
            deliveryDetails: "Cat Ahmed<br>123 Aston Street<br>B11 1AB<br>Birmingham<br>West Meowdlands",
            additionalInfo: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        };

        function loadNotificationDetails() {
            const notificationDetails = document.getElementById("notificationDetails");
            
            notificationDetails.innerHTML = `
                <div class="notification-header">
                    <strong>${notificationData.title}</strong>
                    <span class="date">${notificationData.date}</span>
                </div>
                <p class="order-number">Order number: <strong>${notificationData.orderNumber}</strong></p>
                <hr>
                <p>${notificationData.statusMessage}</p>
                <p><strong>${notificationData.product}</strong></p>
                <p><strong>Delivery Details:</strong><br>${notificationData.deliveryDetails}</p>
                <p>${notificationData.additionalInfo}</p>
                <hr>
                <button class="view-order-btn">View Order</button>
            `;
        }

        loadNotificationDetails();