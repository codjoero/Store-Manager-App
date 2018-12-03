/* eslint-disable no-undef */
// Declarations
const api = new Api();
const msg = document.querySelector('span.msg');
const errMsg = document.querySelector('span.errMsg');
loader = document.getElementsByClassName('progress-bar');
showLoader = loader[0];

// Listeners
document.getElementById('addUser').addEventListener('submit', addAdmin);
document.getElementById('loginUser').addEventListener('submit', loginUser);

// Fetch-api functions
function addAdmin(e){
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
        showLoader.style.display = 'block';
        api.post('register', user)
        .then(api.handleResponse)
        .then((data) => {
            msg.innerText = data['message'];
            console.log(data);
        })
        .catch(err => {
            showLoader.style.display = 'none';
            msg.innerText = err['message'];
            console.log(err);
        });
    } catch (err) {
        showLoader.style.display = 'none';
        msg.innerHTML = err;
    }
}

function loginUser(e){
    e.preventDefault();

    let username = document.getElementById('loginUsername').value;
    let password = document.getElementById('loginPassword').value;
    let user = {
        username: username,
        password: password
    };
    showLoader.style.display = 'block';
    api.post('login', user)
    .then(api.handleResponse)
    .then((data) => {
        errMsg.innerText = data['message'];
        console.log(data);

        if (data['user']['role'] === 'admin' && typeof data['token'] !== null){
            localStorage.setItem('token', data['token']);
            localStorage.setItem('loggedUser', data['user']['username']);
            window.location = 'UI/templates/admin/dashboard.html';
        }
        else if (data['user']['role'] === 'attendant' && typeof data['token'] !== null){
            localStorage.setItem('token', data['token']);
            localStorage.setItem('loggedUser', data['user']['username']);
            window.location = 'UI/templates/attendant/dashboard.html';
        }
    })
    .catch(err => {
        showLoader.style.display = 'none';
        errMsg.innerText = err['message'];
        console.log(err);
    });
}