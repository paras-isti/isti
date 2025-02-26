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
    let alertBox = document.getElementById("alert-box");
    let soundEnabled = false; 

    // ✅ Make enableSound globally accessible
    window.enableSound = function () {
        soundEnabled = true;
        alert("🔊 Sound Alerts Enabled!");
    };

    function checkForAlert() {
        fetch('/alert-status')
            .then(response => response.json())
            .then(data => {
                if (data.obstruction) {
                    alertBox.classList.remove('hidden');
                    if (!obstructionAlertShown && soundEnabled) {
                        alertSound.play();
                    }
                    obstructionAlertShown = true;
                } else {
                    alertBox.classList.add('hidden');
                    obstructionAlertShown = false;
                    alertSound.pause();
                    alertSound.currentTime = 0;
                }
            })
            .catch(error => {
                console.error("Error fetching alert status:", error);
            });
    }

    setInterval(checkForAlert, 2000);
});
