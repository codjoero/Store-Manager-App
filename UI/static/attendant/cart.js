//Declarations
const productsUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products'
const salesUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/sales'
const msg = document.querySelector('span.msg')
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")
const stockTableBody = document.querySelector('#stockTable > tbody');
const saleBody = document.querySelector('#sale > tbody');

// Listeners
document.getElementById('makeSale').addEventListener
('click', makeSale)

//Fetch-api functions
function makeSale(){
    saleItems = soldItems();
    if (Array.isArray(saleItems) && saleItems.length === 0) {
        msg.style.fontWeight = 'bold';
        msg.innerText = "Please Add a Sale from Items!";
    } else {
        console.log(saleItems)
        
        fetch(salesUrl, {
            method: 'POST',
            mode: "cors",
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-type': 'application/json',
                'Authorization': 'Bearer '+ token 
            },
            body:JSON.stringify({"products": saleItems})
        })
        .then(handleResponse)
        .then((data) => {
            msg.innerText = data['message'];
        })
        .catch(err => {
            msg.innerHTML = err['message'] + '<br>';
            if (err['msg'] === 'Token has expired') {
                window.location = "/UI/templates/index.html";
            }
            console.log(err)
        })
    }
}

//Collect row elements from sales table
function soldItems() {
    var table = document.getElementById('sale')
    var rows = table.rows
    var data = [];
    for (var r = 2; r < rows.length; r++) {
        var row = rows[r]
        var product ={
            prod_name: row.cells[0].innerHTML,
            quantity: parseInt(row.cells[1].innerHTML)
        }
        data.push(product)
    }
    return data;
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
    clearTable(stockTableBody)
    clearTable(saleBody)
    
    //Populate table
    products.forEach((product) => {
        drawTable(product);
    })
}

function drawTable(product) {
    var row = $('<tr onclick="saleProduct(this)" />')
    $('#stockTable').append(row);
    row.append($('<td>' + product.prod_name + '</td>'));
    row.append($('<td>' + product.prod_id + '</td>'));
    row.append($('<td>' + product.category + '</td>'));
    row.append($('<td>' + product.stock + '</td>'));
    row.append($('<td>' + product.price + '</td>'));
}

//Collect row elements from Inventory table
function saleProduct(call) {
    var table = document.getElementById('stockTable')
    var data = [];
    var i = call.rowIndex;
    for (var c = 0; c < table.rows[i].cells.length; c++){
        content = table.rows[i].cells[c].innerHTML;
        data.push(content)
    }
    saleData(data);
}

//Add row elements to Sales table
function saleData(data) {
    var table = document.getElementById('sale');
    var rows = table.rows
    var prodNames = [];
    var totalSale = 0;
    for (var r = 1; r < rows.length; r++) {
        var row = rows[r]
        let prodName = row.cells[0].innerHTML;
        prodNames.push(prodName)
    }
    if (prodNames.includes(data[0])) {
        let prodQnty = parseInt(row.cells[1].innerHTML);
        let price = parseInt(row.cells[2].innerHTML);
        prodQnty += 1;
        totalPrice = prodQnty * price;
        row.cells[1].innerHTML = prodQnty;
        row.cells[2].innerHTML = totalPrice;
    } else {
        var row = $('<tr />')
        $('#sale').append(row);
        row.append($('<td>' + data[0] + '</td>'));
        row.append($('<td>' + 1 + '</td>'));
        row.append($('<td>' + data[4] + '</td>'));
    }
    saleAddup(rows, totalSale);
}
//Compound the sale totals
function saleAddup(rows, totalSale) {
    for (var r = 2; r < rows.length; r++) {
        var row = rows[r]
        let price = parseInt(row.cells[2].innerHTML);
        totalSale += price
    }
    totalsCell = rows[1].cells[2];
    totalsCell.innerHTML = totalSale
}

//Clear all table rows
function clearTable(tableBody) {
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}