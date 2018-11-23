//Declarations
const productsUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products'
const msg = document.querySelector('span.msg')
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")
const mytableBody = document.querySelector('#mytable > tbody');

// Listeners
document.getElementById('addProduct').addEventListener
('submit', addProduct)
document.getElementById('updateProduct').addEventListener
('submit', updateProduct)

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

function updateProduct(e){
    e.preventDefault();

    const updateProdUrl = `https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products/${prod_id}`
    let prodName = document.getElementById('uProdName').value;
    let category = document.getElementById('uCategory').value;
    let stock = document.getElementById('uStock').value;
    let price = document.getElementById('uPrice').value;
    let product = {
        prod_name: prodName,
		category: category,
		stock: parseInt(stock, 10),
        price: parseInt(price, 10)
    }

    fetch(updateProdUrl, {
        method: 'PUT',
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
        updateMsg.innerText = data['message'];
        location.reload(true)
    })
    .catch(err => {
        updateMsg.innerHTML = err['message'];
        if (err['msg'] === 'Token has expired') {
            window.location = "/UI/templates/index.html";
        }
        console.log(err);
    })
}

function deleteProduct(_id){
    const deleteProdUrl = `https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products/${_id}`
    fetch(deleteProdUrl, {
        method: 'DELETE',
        mode: "cors",
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'Bearer '+ token 
        }
    })
    .then(handleResponse)
    .then((data) => {
        msg.innerText = data['message'];
        // loadTable();
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

//Edit table row
function editRow(call) {
    var table = document.getElementById('mytable')
    var prodForm = document.forms['updateProduct']
    var prodName = prodForm.elements[0]
    var category = prodForm.elements[1]
    var stock = prodForm.elements[2]
    var price = prodForm.elements[3]
    var data = [];
    var i = call.parentNode.parentNode.rowIndex;
    prod_id = table.rows[i].cells[1].innerHTML
    for (var c = 0; c < table.rows[i].cells.length - 1; c++){
        content = table.rows[i].cells[c].innerHTML;
        data.push(content)
    }
    prodName.value = data[0];
    category.value = data[2];
    stock.value = data[3];
    price.value = data[5];
    $('form').animate({height: "toggle", opacity: "toggle"}, 'slow');
}

//Delete table row
function deleteRow(call) {
    var table = document.getElementById('mytable')
    var i = call.parentNode.parentNode.rowIndex;
    deleteProd_id = table.rows[i].cells[1].innerHTML
    deleteProduct(deleteProd_id);
    document.getElementById("mytable").deleteRow(i);
}