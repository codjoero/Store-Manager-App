const registerUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/register'
const loginUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/login'
const msg = document.querySelector('span.msg')
const errMsg = document.querySelector('span.errMsg')

// Listeners
document.getElementById('addUser').addEventListener
('submit', addAdmin)
document.getElementById('loginUser').addEventListener
('submit', loginUser)

const errHandler = (response) => {
    if (!response.ok){
        console.log(response)
    }
    return response
}

function addAdmin(e){
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
        fetch(registerUrl, {
            method: 'POST',
            mode: "cors",
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-type': 'application/json'
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
    } catch (err) {
        msg.innerHTML = err
    }
}

function loginUser(e){
    e.preventDefault();

    let username = document.getElementById('loginUsername').value;
    let password = document.getElementById('loginPassword').value;

    fetch(loginUrl, {
        method: 'POST',
        mode: "cors",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json'
        },
        body:JSON.stringify({
            username:username, password:password,
        })
    })
    .then(errHandler)
    .then((res) => res.json())
    .then((data) => {
        errMsg.innerText = data['message'];
        console.log(data)

        if (data['user']['role'] === 'admin' && typeof data['token'] !== null){
            localStorage.setItem("token", data['token'])
            localStorage.setItem("adminLoggedin", true)
            window.location = "/UI/templates/admin/dashboard.html";
        }
        else if (data['user']['role'] === 'attendant' && typeof data['user']['token'] !== null){
            localStorage.setItem("token", data['user']['token'])
            localStorage.setItem("attendantLoggedin", true)
            window.location = "/UI/templates/attendant/dashboard.html";
        }
    })
    .catch(err => console.log(err))
}