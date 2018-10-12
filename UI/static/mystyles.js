/* Array for username/password */
var _CONFIG = {
    "user": {
        "Password": "andela",
        "Redirect": "../templates/dashboard.html"
    },
    "admin": {
        "Password": "bootcamp",
        "Redirect": "../templates/index.html"
    }
}

function checkLogin() {
    var login = document.getElementById("login").value;
    var pass = document.getElementById("password").value;
    if ( _CONFIG[login] !== undefined && _CONFIG[login]["Password"] == pass) {
        window.location.replace(_CONFIG[login]["Redirect"]);
    }
}

function logout(){
    window.location.replace("/UI/templates/index.html");
}

function dashboard(){
    window.location.replace("/UI/templates/dashboard.html");
};