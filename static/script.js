// Dark Mode Toggle Logic
const darkModeToggle = document.getElementById("darkModeToggle");
const body = document.body;
const moonIcon = document.getElementById("moonIcon");
const sunIcon = document.getElementById("sunIcon");

// Check if dark mode preference is stored in localStorage
if (localStorage.getItem("darkMode") === "enabled") {
    body.classList.add("dark");
    moonIcon.style.display = "none";
    sunIcon.style.display = "block";
}

// Toggle dark mode when the button is clicked
darkModeToggle.addEventListener("click", () => {
    body.classList.toggle("dark");

    // Update the icon visibility
    if (body.classList.contains("dark")) {
        moonIcon.style.display = "none";
        sunIcon.style.display = "block";
        localStorage.setItem("darkMode", "enabled"); 
    } else {
        moonIcon.style.display = "block";
        sunIcon.style.display = "none";
        localStorage.setItem("darkMode", "disabled"); 
    }
});
