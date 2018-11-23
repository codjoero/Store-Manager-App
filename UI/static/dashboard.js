//Declarations
const logoutUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/logout'
const msg = document.querySelector('span.msg')
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")

//Listeners
document.querySelector('.logout').addEventListener
('click', logoutUser)

//Fetch-api functions
function logoutUser(){
    fetch(logoutUrl, {
        method: 'DELETE',
        mode: "cors",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer '+ token 
        }
    })
    .then(handleResponse)
    .then((data) => {
        window.location = "/UI/templates/index.html";
    })
    .catch(err => {
        if (err['msg'] === 'Token has expired') {
            window.location = "/UI/templates/index.html";
        }
        window.location = "/UI/templates/index.html";
    })
}

//Handle response
function handleResponse(response) {
    return response.json()
    .then(json => {
        if (response.ok) {
            return json
        } else {
            return Promise.reject(json)
        }
    })
}

//On window load
window.onload=function(){
    style();
    }
function style() {
    let paragraph = document.querySelector("span.loggedin");
    paragraph.innerHTML += loggedUser;
}
