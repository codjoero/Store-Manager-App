//Declarations
const usersUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/users'
const msg = document.querySelector('span.msg')
const errMsg = document.querySelector('span.errMsg')
const token = localStorage.getItem("token");
const adminLoggedin = localStorage.getItem("adminLoggedin");

const mytableBody = document.querySelector('#mytable > tbody');

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
        location.reload(true);
    })
    .catch(err => console.log(err))
}

//On window load
function loadTable() {
    fetch(usersUrl, {
        method: 'GET',
        mode: "cors",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json',
            'Authorization': 'Bearer '+ token 
        },
    })
    .then(errHandler)
    .then((res) => res.json())
    .then((data) => {
        populateTable(data['users']);
    })
    .catch(err => console.log(err))
}

//Add users to table
function populateTable(users) {
    //clear out HTML data
    while (mytableBody.firstChild) {
        mytableBody.removeChild(mytableBody.firstChild);
    }
    //Populate table
    users.forEach((user) => {
        drawTable(user);
    })
}

function drawTable(user) {
    var row = $('<tr />')
    var select = '<input type="checkbox">'
    var edit = '<i class="fa fa-edit" onclick="editRow()"></i>'
    var del = '<i class="fa fa-close" onclick="deleteRow(this)"></i>'
    $('#mytable').append(row);
    row.append($('<td>' + select + '</td>'));
    row.append($('<td>' + user.user_id + '</td>'));
    row.append($('<td>' + user.name + '</td>'));
    row.append($('<td>' + user.username + '</td>'));
    row.append($('<td>' + user.role + '</td>'));
    row.append($('<td class="txtright">' + edit + '</td>'));
    row.append($('<td class="txtdel">' + del + '</td>'));
}

//Delete table row
function deleteRow(call) {
    var i = call.parentNode.parentNode.rowIndex;
    document.getElementById("mytable").deleteRow(i);
}

//Edit table row
function editRow(call) {
    $('form').animate({height: "toggle", opacity: "toggle"}, 'slow');
}