// Array for username/password 
var _CONFIG = {
    "user": {
        "Password": "andela",
        "Redirect": "../templates/dashboard.html"
    },
    "admin": {
        "Password": "bootcamp",
        "Redirect": "../templates/dashboard.html"
    }
}
var loggedin = "";
function checkLogin() {
    var login = document.getElementById("login").value;
    var pass = document.getElementById("password").value;
    if ( _CONFIG[login] !== undefined && _CONFIG[login]["Password"] == pass) {
        window.location.replace(_CONFIG[login]["Redirect"]);
        
        document.getElementById(login).style.display = "block";
    }
};

// if (loggedin == "user"){
//     document.getElementById("user").style.display = "block";
// }
// else {
//     document.getElementById("admin").style.display = "block";
// };

// inventory2 table row delete
function deleteRow(call) {
    var i = call.parentNode.parentNode.rowIndex;
    document.getElementById("mytable").deleteRow(i);
}