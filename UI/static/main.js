const registerUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/register'
const msg = document.querySelector('span.msg')

// Listeners
document.getElementById('addUser').addEventListener
('submit', addAdmin)

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
    let confirm = document.getElementById('confirm').value;
    let role = document.getElementById('role').value;

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
}