//Declarations
const productsUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products'
const msg = document.querySelector('span.msg')
const token = localStorage.getItem("token");
const adminLoggedin = localStorage.getItem("adminLoggedin");
const mytableBody = document.querySelector('#mytable > tbody');

// Listeners
document.getElementById('addProduct').addEventListener
('submit', addProduct)

//Fetch-api functions
function addProduct(e){
    e.preventDefault();

    let prodName = document.getElementById('prodName').value;
    let category = document.getElementById('category').value;
    let stock = document.getElementById('stock').value;
    let price = document.getElementById('price').value;
    let product = {
        prod_name:prodName,
		category:category,
		stock:parseInt(stock, 10),
		price:parseInt(price, 10)
    };
    fetch(productsUrl, {
        method: 'POST',
        mode: "cors",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-type': 'application/json',
            'Authorization': 'Bearer '+ token 
        },
        body:JSON.stringify(product)
    })
    .then(handleResponse)
    .then((data) => {
        msg.innerText = data['message'];
        loadTable();
    })
    .catch(err => {
        msg.innerHTML = err['message'] + '<br>';
        if (err['msg'] === 'Token has expired') {
            window.location = "/UI/templates/index.html";
        }
        console.log(err)
    })
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

//Add users to table
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
    var edit = '<i class="fa fa-edit" onclick="editRow(this)"></i>'
    var del = '<i class="fa fa-close" onclick="deleteRow(this)"></i>'
    var addDate = shortDate(product.added_on)
    $('#mytable').append(row);
    row.append($('<td>' + product.prod_name + '</td>'));
    row.append($('<td>' + product.prod_id + '</td>'));
    row.append($('<td>' + product.category + '</td>'));
    row.append($('<td>' + product.stock + '</td>'));
    row.append($('<td>' + 10 + '</td>'));
    row.append($('<td>' + product.price + '</td>'));
    row.append($('<td>' + addDate + '</td>'));
    row.append($('<td class="txtright">' + edit + '</td>'));
    row.append($('<td class="txtdel">' + del + '</td>'));
}

function shortDate(date) {
    var length = 16;
    return date.substring(0, length);
}

//Delete table row
function deleteRow(call) {
    var i = call.parentNode.parentNode.rowIndex;
    document.getElementById("mytable").deleteRow(i);
}