const api = new Api();

// Declarations
const msg = document.querySelector('span.msg');
const topMsg = document.getElementById('topMsg');
const updateMsg = document.getElementById('updateMsg');
const mytableBody = document.querySelector('#mytable > tbody');
const modal = document.getElementById('confirm-modal');
const modalConfirm = document.getElementById('modal-yes');
const modalDecline = document.getElementById('modal-no');

// Listeners
document.getElementById('addUser').addEventListener('submit', addUser);
document.getElementById('updateUser').addEventListener('submit', updateUser);

// Fetch-api functions
function addUser(e) {
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
    if (password != confirmPassword) {
      throw 'Passwords not matching!';
    }
    api.post('users', user)
      .then(api.handleResponse)
      .then((data) => {
        msg.innerText = data.message;
        location.reload(true);
      })
      .catch((err) => {
        msg.innerHTML = err.message;
        api.errCheck(err);
        console.log(err);
      });
  } catch (err) {
    msg.innerHTML = err;
  }
}

function updateUser(e) {
  e.preventDefault();

  const name = document.getElementById('updateName').value;
  const username = document.getElementById('updateUsername').value;
  const password = document.getElementById('updatePassword').value;
  const confirmPassword = document.getElementById('updateConfirm').value;
  const role = document.getElementById('role').value;
  const user = {
    name,
    username,
    password,
    role,
  };

  try {
    if (password != confirmPassword) {
      throw 'Passwords not matching!';
    }
    api.put(`users/${user_id}`, user)
      .then(api.handleResponse)
      .then((data) => {
        updateMsg.innerText = data.message;
        location.reload(true);
      })
      .catch((err) => {
        updateMsg.innerHTML = err.message;
        api.errCheck(err);
        console.log(err);
      });
  } catch (err) {
    updateMsg.innerHTML = err;
  }
}

function deleteUser(_id) {
  api.delete(`users/${_id}`)
    .then(api.handleResponse)
    .then((data) => {
      topMsg.innerText = data.message;
    })
    .catch((err) => {
      topMsg.innerHTML = err.message;
      api.errCheck(err);
      console.log(err);
    });
}

// On window load
window.onload = function () {
  loadTable();
  api.style();
};
function loadTable() {
  api.get('users')
    .then(api.handleResponse)
    .then(data => populateTable(data.users))
    .catch((err) => {
      api.errCheck(err);
      console.log(err);
    });
}

// Add users to table
function populateTable(users) {
  api.clearTable(mytableBody);
  // Populate table
  users.forEach((user) => {
    drawTable(user);
  });
}

function drawTable(user) {
  let row = $('<tr />');
  let select = '<input type="checkbox">';
  let edit = '<i class="fa fa-edit" onclick="editRow(this)"></i>';
  let del = '<i class="fa fa-close" onclick="delRow(this)"></i>';
  $('#mytable').append(row);
  row.append($(`<td>${  select  }</td>`));
  row.append($(`<td>${  user.user_id  }</td>`));
  row.append($(`<td>${  user.name  }</td>`));
  row.append($(`<td>${  user.username  }</td>`));
  row.append($(`<td>${  user.role  }</td>`));
  row.append($(`<td class="txtright">${  edit  }</td>`));
  row.append($(`<td class="txtdel">${  del  }</td>`));
}

// Edit table row
function editRow(call) {
  let table = document.getElementById('mytable');
  let userForm = document.forms.updateUser;
  let name = userForm.elements[0];
  let username = userForm.elements[1];
  let data = [];
  let i = call.parentNode.parentNode.rowIndex;
  user_id = table.rows[i].cells[1].innerHTML;
  for (let c = 2; c < table.rows[i].cells.length - 3; c++) {
    content = table.rows[i].cells[c].innerHTML;
    data.push(content);
  }
  name.value = data[0];
  username.value = data[1];
  $('form').animate({ height: 'toggle', opacity: 'toggle' }, 'slow');
}

// Delete table row
function delRow(call) {
  modal.style.display = 'block';
  modalConfirm.onclick = () => {
    modal.style.display = 'none';
    let table = document.getElementById('mytable');
    let i = call.parentNode.parentNode.rowIndex;
    deleteUser_id = table.rows[i].cells[1].innerHTML;
    deleteUser(deleteUser_id);
    document.getElementById('mytable').deleteRow(i);
  };
  modalDecline.onclick = () => {
    modal.style.display = 'none';
  };
  window.onclick = (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };
}
