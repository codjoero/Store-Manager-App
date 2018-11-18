//Declarations
const usersUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/users'
const msg = document.querySelector('span.msg')
const errMsg = document.querySelector('span.errMsg')
const token = localStorage.getItem("token");
const adminLoggedin = localStorage.getItem("adminLoggedin");

// Listeners
document.getElementById('addUser').addEventListener
('submit', addUser)

const errHandler = (response) => {
    if (!response.ok){
        console.log(response)
    }
    return response
}

//Fetch-api functions
function addUser(e){
    e.preventDefault();

    let name = document.getElementById('name').value;
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let role = document.getElementById('role').value;

    fetch(usersUrl, {
        method: 'POST',
        mode: "cors",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json',
            'Authorization': 'Bearer '+ token 
        },
        body:JSON.stringify({
            name:name, username:username, password:password, role:role
        })
    })
    .then(errHandler)
    .then((res) => res.json())
    .then((data) => {
        msg.innerText = data['message'];
        console.log(data)
    })
    .catch(err => console.log(err))
}

//Normal call functions
function deleteRow(call) {
    var i = call.parentNode.parentNode.rowIndex;
    document.getElementById("mytable").deleteRow(i);
}