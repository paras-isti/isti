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

document.addEventListener("DOMContentLoaded", function () {
    let obstructionAlertShown = false;
    let alertSound = document.getElementById("alert-sound");
    let alertBox = document.getElementById("alert-box"); // Ensure element is selected after DOM loads
    let soundEnabled = false; // Initially, sound is disabled

    function enableSound() {
        soundEnabled = true;
        alert("🔊 Sound Alerts Enabled!");
    }

    function checkForAlert() {
        fetch('/alert-status')
            .then(response => response.json())
            .then(data => {
                if (data.obstruction) {
                    alertBox.classList.remove('hidden'); // Show alert
                    if (!obstructionAlertShown && soundEnabled) {
                        alertSound.play();
                    }
                    obstructionAlertShown = true;
                } else {
                    alertBox.classList.add('hidden'); // Hide alert
                    obstructionAlertShown = false;
                    alertSound.pause();
                    alertSound.currentTime = 0;
                }
            })
            .catch(error => {
                console.error("Error fetching alert status:", error);
            });
    }

    setInterval(checkForAlert, 2000); // Check every 2 seconds
});
