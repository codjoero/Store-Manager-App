const api = new Api();

// Listeners
document.querySelector('.logout').addEventListener('click', logoutUser);

// Fetch-api functions
function logoutUser() {
  api.delete('logout')
    .then(api.handleResponse)
    .then(() => window.location = '../../index.html')
    .catch(err => {
        api.errCheck(err);
        window.location = '../../index.html';
    });
}

// On window load
window.onload = function () {
  api.style();
};
