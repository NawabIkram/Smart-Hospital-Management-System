function confirmDelete() {
    return confirm("Are you sure you want to delete this record? Related foreign key records may block deletion.");
}

document.addEventListener("mousemove", function (event) {
    const cards = document.querySelectorAll(".tilt-card");
    const x = (event.clientX / window.innerWidth - 0.5) * 4;
    const y = (event.clientY / window.innerHeight - 0.5) * -4;

    cards.forEach(card => {
        if (!card.matches(":hover")) {
            card.style.transform = `rotateX(${y}deg) rotateY(${x}deg)`;
        }
    });
});

document.addEventListener("mouseleave", function () {
    document.querySelectorAll(".tilt-card").forEach(card => {
        card.style.transform = "";
    });
});
