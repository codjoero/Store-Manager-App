const api = new Api();

//Declarations
const msg = document.querySelector('span.msg');
const topMsg = document.getElementById('topMsg');
const updateMsg = document.getElementById('updateMsg');
const mytableBody = document.querySelector('#mytable > tbody');

// Listeners
document.getElementById('addUser').addEventListener('submit', addUser);
document.getElementById('updateUser').addEventListener('submit', updateUser);

//Fetch-api functions
function addUser(e){
    e.preventDefault();

    let name = document.getElementById('name').value;
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirm').value;
    let role = document.getElementById('role').value;
    let user = {
        name: name,
		username: username,
		password: password,
		role: role
    };

    try {
        if (password != confirmPassword) {
            throw 'Passwords not matching!';
        }
        api.post('users', user)
        .then(api.handleResponse)
        .then((data) => {
            msg.innerText = data['message'];
            location.reload(true);
        })
        .catch(err => {
            msg.innerHTML = err['message'];
            api.errCheck(err);
            console.log(err);
        });
    } catch (err) {
        msg.innerHTML = err;
    }
}

function updateUser(e){
    e.preventDefault();

    let name = document.getElementById('updateName').value;
    let username = document.getElementById('updateUsername').value;
    let password = document.getElementById('updatePassword').value;
    let confirmPassword = document.getElementById('updateConfirm').value;
    let role = document.getElementById('role').value;
    let user = {
        name: name,
		username: username,
		password: password,
		role: role
    };

    try {
        if (password != confirmPassword) {
            throw 'Passwords not matching!';
        }
        api.put(`users/${user_id}`, user)
        .then(api.handleResponse)
        .then((data) => {
            updateMsg.innerText = data['message'];
            location.reload(true);
        })
        .catch(err => {
            updateMsg.innerHTML = err['message'];
            api.errCheck(err);
            console.log(err);
        });
    } catch (err) {
        updateMsg.innerHTML = err;
    }
}

function deleteUser(_id){
    api.delete(`users/${_id}`)
    .then(api.handleResponse)
    .then((data) => {
        topMsg.innerText = data['message'];
    })
    .catch(err => {
        topMsg.innerHTML = err['message'];
        api.errCheck(err);
        console.log(err);
    });
}

//On window load
window.onload=function(){
    loadTable();
    api.style();
};
function loadTable() {
    api.get('users')
    .then(api.handleResponse)
    .then((data) => populateTable(data['users']))
    .catch(err => {
        api.errCheck(err);
        console.log(err);
    });
}

//Add users to table
function populateTable(users) {
    api.clearTable(mytableBody);
    //Populate table
    users.forEach((user) => {
        drawTable(user);
    });
}

function drawTable(user) {
    var row = $('<tr />');
    var select = '<input type="checkbox">';
    var edit = '<i class="fa fa-edit" onclick="editRow(this)"></i>';
    var del = '<i class="fa fa-close" onclick="delRow(this)"></i>';
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
    var table = document.getElementById('mytable');
    var userForm = document.forms['updateUser'];
    var name = userForm.elements[0];
    var username = userForm.elements[1];
    var data = [];
    var i = call.parentNode.parentNode.rowIndex;
    user_id = table.rows[i].cells[1].innerHTML;
    for (var c = 2; c < table.rows[i].cells.length - 3; c++){
        content = table.rows[i].cells[c].innerHTML;
        data.push(content);
    }
    name.value = data[0];
    username.value = data[1];
    $('form').animate({height: 'toggle', opacity: 'toggle'}, 'slow');
}

//Delete table row
function delRow(call) {
    var table = document.getElementById('mytable');
    var i = call.parentNode.parentNode.rowIndex;
    deleteUser_id = table.rows[i].cells[1].innerHTML;
    deleteUser(deleteUser_id);
    document.getElementById('mytable').deleteRow(i);
}