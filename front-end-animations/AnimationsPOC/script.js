document.addEventListener('DOMContentLoaded', () => { 
    const cards = document.querySelectorAll('.card1, .card2, .card3');

    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('card-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        observer.observe(card);
    });
});

document.addEventListener('mousemove', (event) => {
    const catFace = document.querySelector('.cat-face');
    const elements = document.querySelectorAll('.pupil, .mouth, .whiskers');

    const { clientX: mouseX, clientY: mouseY } = event;
    const rect = catFace.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    const deltaX = mouseX - centerX;
    const deltaY = mouseY - centerY;

    const rotateX = (deltaY / rect.height) * 10;
    const rotateY = -(deltaX / rect.width) * 10;

    catFace.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

    elements.forEach(element => {
        const elementRect = element.parentElement.getBoundingClientRect();
        const elementCenterX = elementRect.left + elementRect.width / 2;
        const elementCenterY = elementRect.top + elementRect.height / 2;

        const elementDeltaX = mouseX - elementCenterX;
        const elementDeltaY = mouseY - elementCenterY;

        const angle = Math.atan2(elementDeltaY, elementDeltaX);
        const moveX = Math.cos(angle) * (element.classList.contains('pupil') ? 8 : 4);
        const moveY = Math.sin(angle) * (element.classList.contains('pupil') ? 8 : 2);

        element.style.transform = `translate(${moveX}px, ${moveY}px)`;
    });
});
