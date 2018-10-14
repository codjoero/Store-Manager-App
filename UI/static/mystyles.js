// Array for username/password 
var _CONFIG = {
    "user": {
        "Password": "andela",
        "Redirect": "../templates/user/dashboard.html"
    },
    "admin": {
        "Password": "andela",
        "Redirect": "../templates/admin/dashboard.html"
    }
}

function checkLogin() {
    var login = document.getElementById("login").value;
    var pass = document.getElementById("password").value;
    var text;
    if ( _CONFIG[login] !== undefined && _CONFIG[login]["Password"] == pass) {
        window.location.replace(_CONFIG[login]["Redirect"]);
    }
    else {
        text = "wrong input";
        document.getElementById("checker").innerHTML = text;
    }
    
};

function deleteRow(call) {
    var i = call.parentNode.parentNode.rowIndex;
    document.getElementById("mytable").deleteRow(i);
}