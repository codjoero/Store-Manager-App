//Declarations
const usersUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/users'
const msg = document.querySelector('span.msg')
const updateMsg = document.getElementById('updateMsg')
const errMsg = document.querySelector('span.errMsg')
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")
const mytableBody = document.querySelector('#mytable > tbody');

// Listeners
document.getElementById('addUser').addEventListener
('submit', addUser)
document.getElementById('updateUser').addEventListener
('submit', updateUser)

//Fetch-api functions
function addUser(e){
    e.preventDefault();

    let name = document.getElementById('name').value;
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirm').value;
    let role = document.getElementById('role').value;

    try {
        if (password != confirmPassword) {
            throw 'Passwords not matching!'
        }
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
        .then(handleResponse)
        .then((data) => {
            msg.innerText = data['message'];
            location.reload(true);
        })
        .catch(err => {
            msg.innerHTML = err['message'];
            if (err['msg'] === 'Token has expired') {
                window.location = "/UI/templates/index.html";
            }
            console.log(err)
        })
    } catch (err) {
        msg.innerHTML = err
    }
}

function updateUser(e){
    e.preventDefault();

    const updateUserUrl = `https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/users/${user_id}`
    let name = document.getElementById('updateName').value;
    let username = document.getElementById('updateUsername').value;
    let password = document.getElementById('updatePassword').value;
    let confirmPassword = document.getElementById('updateConfirm').value;
    let role = document.getElementById('role').value;

    try {
        if (password != confirmPassword) {
            throw 'Passwords not matching!'
        }
        fetch(updateUserUrl, {
            method: 'PUT',
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
        .then(handleResponse)
        .then((data) => {
            updateMsg.innerText = data['message'];
            location.reload(true);
        })
        .catch(err => {
            updateMsg.innerHTML = err['message'];
            if (err['msg'] === 'Token has expired') {
                window.location = "/UI/templates/index.html";
            }
            console.log(err);
        })
    } catch (err) {
        updateMsg.innerHTML = err
    }
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
    loadTable();
    style();
    }
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
    .then(handleResponse)
    .then((data) => {
        populateTable(data['users']);
    })
    .catch(err => {
        if (err['msg'] === 'Token has expired' ||
            err['message'] === 'Invalid Authentication, Please Login!') {
            window.location = "/UI/templates/index.html";
        }
        console.log(err)
    })
}

function style() {
    let paragraph = document.querySelector("span.loggedin");
    paragraph.innerHTML += loggedUser;
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
    var edit = '<i class="fa fa-edit" onclick="editRow(this)"></i>'
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

//Edit table row
function editRow(call) {
    var table = document.getElementById('mytable')
    var userForm = document.forms['updateUser']
    var name = userForm.elements[0]
    var username = userForm.elements[1]
    var data = [];
    var i = call.parentNode.parentNode.rowIndex;
    user_id = table.rows[i].cells[1].innerHTML
    for (var c = 2; c < table.rows[i].cells.length - 3; c++){
        content = table.rows[i].cells[c].innerHTML;
        data.push(content)
    }
    name.value = data[0];
    username.value = data[1];
    $('form').animate({height: "toggle", opacity: "toggle"}, 'slow');
}

//Delete table row
function deleteRow(call) {
    var i = call.parentNode.parentNode.rowIndex;
    document.getElementById("mytable").deleteRow(i);
}