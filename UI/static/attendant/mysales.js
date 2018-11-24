//Declarations
const salesUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/sales'
const msg = document.querySelector('span.msg')
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")
const stockTableBody = document.querySelector('#stockTable > tbody');
const saleBody = document.querySelector('#sale > tbody');

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
    fetch(salesUrl, {
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
        saleRecords = data['Sale Records']
        populateTable(saleRecords);
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

//Add Sales to table
function populateTable(records) {
    //clear out HTML data
    clearTable(stockTableBody)
    clearTable(saleBody)

    //Populate table
    records.forEach((record) => {
        drawTable(record);
    })
}

function drawTable(record) {
    var row = $('<tr onclick="saleProduct(this)" />')
    var addDate = shortDate(record.sale_date)
    $('#stockTable').append(row);
    row.append($('<td>' + record.sale_id + '</td>'));
    row.append($('<td>' + record.products.length + '</td>'));
    row.append($('<td>' + record.sold_by + '</td>'));
    row.append($('<td>' + addDate + '</td>'));
    row.append($('<td>' + record.total_sale + '</td>'));
}

function shortDate(date) {
    var length = 16;
    return date.substring(0, length);
}

//Collect row elements from Sales table
function saleProduct(call) {
    let table = document.getElementById('stockTable')
    let i = call.rowIndex;
    let row = table.rows[i];
    let sale_id = row.cells[0].innerHTML;

    clearTable(saleBody)
    saleRecords.forEach((record) => {
        if (record['sale_id'] == sale_id) {
            saleData(record['products'], record['total_sale'])
        }
    })
}

//Add row elements to products table
function saleData(products, totals) {
    var table = document.getElementById('sale');
    var rows = table.rows
    var totalSale = rows[1].cells[2];
    products.forEach(product => {
        var row = $('<tr />')
        $('#sale').append(row);
        row.append($('<td>' + product.prod_name + '</td>'));
        row.append($('<td>' + product.quantity + '</td>'));
        row.append($('<td>' + product.price + '</td>'));
    })
    totalSale.innerHTML = totals
}

//Clear all table rows
function clearTable(tableBody) {
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}