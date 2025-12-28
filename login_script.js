function login() {
    const email = document.getElementById("email").value;       // lowercase .value
    const password = document.getElementById("password").value; // lowercase .value

    if(email && password) {
        localStorage.setItem("isLoggedIn", "true"); // must match what you check later
        window.location.href = "index.html";
    } else {
        alert("Please enter email and password");
    }
}
