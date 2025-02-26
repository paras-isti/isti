function toggleMenu() {
    var nav = document.getElementById("nav-menu");
    if (nav.style.display === "block") {
        nav.style.display = "none";
    } else {
        nav.style.display = "block";
    }
}

function closeNote() {
    document.querySelector(".sticky-note").style.display = "none";
}
