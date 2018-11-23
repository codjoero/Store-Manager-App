//Declarations
const productsUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products'
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")
const mytableBody = document.querySelector('#mytable > tbody');

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
    fetch(productsUrl, {
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
        populateTable(data['products']);
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

//Add products to table
function populateTable(products) {
    //clear out HTML data
    while (mytableBody.firstChild) {
        mytableBody.removeChild(mytableBody.firstChild);
    }
    //Populate table
    products.forEach((product) => {
        drawTable(product);
    })
}

function drawTable(product) {
    var row = $('<tr />')
    var addDate = shortDate(product.added_on)
    $('#mytable').append(row);
    row.append($('<td>' + product.prod_name + '</td>'));
    row.append($('<td>' + product.prod_id + '</td>'));
    row.append($('<td>' + product.category + '</td>'));
    row.append($('<td>' + product.stock + '</td>'));
    row.append($('<td>' + 10 + '</td>'));
    row.append($('<td>' + product.price + '</td>'));
    row.append($('<td>' + addDate + '</td>'));
}

function shortDate(date) {
    var length = 16;
    return date.substring(0, length);
}