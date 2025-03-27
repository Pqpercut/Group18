       // Example notifications array (backend will provide this data)
       const notifications = [
        { title: "YOUR ORDER 12345 HAS BEEN SHIPPED", order: "# Order Number 12345", date: "02/01/2025" },
        { title: "YOUR ORDER 67890 HAS BEEN SHIPPED", order: "# Order Number 67890", date: "03/01/2025" },
        { title: "YOUR ORDER 11223 HAS BEEN SHIPPED", order: "# Order Number 11223", date: "04/01/2025" }
    ];

    function loadNotifications() {
        const notificationList = document.getElementById("notificationList");
        notificationList.innerHTML = ""; // Clear existing notifications

        notifications.forEach(notification => {
            const notificationItem = document.createElement("div");
            notificationItem.classList.add("notification-item");
            
            notificationItem.innerHTML = `
                <div class="notification-content">
                    <strong>${notification.title}</strong>
                    <div class="notification-order">${notification.order}</div>
                </div>
                <div class="notification-date">${notification.date}</div>
            `;
            
            notificationList.appendChild(notificationItem);
        });
    }

    // Load notifications dynamically
    loadNotifications();