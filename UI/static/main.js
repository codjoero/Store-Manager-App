/* eslint-disable valid-typeof */
/* eslint-disable prefer-destructuring */
/* eslint-disable no-use-before-define */
/* eslint-disable no-throw-literal */
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
function addAdmin(e) {
  e.preventDefault();

  const name = document.getElementById('name').value;
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm').value;
  const role = document.getElementById('role').value;
  const user = {
    name,
    username,
    password,
    role,
  };
  try {
    if (password !== confirmPassword) {
      throw 'Passwords not matching!';
    }
    showLoader.style.display = 'block';
    api.post('register', user)
      .then(api.handleResponse)
      .then((data) => {
        msg.innerText = data.message;
        console.log(data);
      })
      .catch((err) => {
        showLoader.style.display = 'none';
        msg.innerText = err.message;
        console.log(err);
      });
  } catch (err) {
    showLoader.style.display = 'none';
    msg.innerHTML = err;
  }
}

function loginUser(e) {
  e.preventDefault();

  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;
  const user = {
    username,
    password,
  };
  showLoader.style.display = 'block';
  api.post('login', user)
    .then(api.handleResponse)
    .then((data) => {
      errMsg.innerText = data.message;
      console.log(data);

      if (data.user.role === 'admin' && typeof data.token !== null) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('loggedUser', data.user.username);
        window.location = '/UI/templates/admin/dashboard.html';
      } else if (data.user.role === 'attendant' && typeof data.token !== null) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('loggedUser', data.user.username);
        window.location = '/UI/templates/attendant/dashboard.html';
      }
    })
    .catch((err) => {
      showLoader.style.display = 'none';
      errMsg.innerText = err.message;
      console.log(err);
    });
}
