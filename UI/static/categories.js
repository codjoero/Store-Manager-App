//Declarations
const loggedUser = localStorage.getItem("loggedUser")


//On window load
window.onload=function(){
    style();
}
function style() {
    let paragraph = document.querySelector("span.loggedin");
    paragraph.innerHTML += loggedUser;
}