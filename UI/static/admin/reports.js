/* eslint-disable no-undef */
const api = new Api;

//Declarations
const topMsg = document.getElementById('topMsg');
const stockTableBody = document.querySelector('#stockTable > tbody');
const saleBody = document.querySelector('#sale > tbody');

//On window load
window.onload=function(){
    loadTable();
    api.style();
    };
function loadTable() {
    api.get('sales')
    .then(api.handleResponse)
    .then((data) => {
        saleRecords = data['Sale Records'];
        populateTable(saleRecords);
    })
    .catch(err => {
        api.errCheck(err);
        console.log(err);
        topMsg.innerText = err['message'];
    });
}

//Add Sales to table
function populateTable(records) {
    api.clearTable(stockTableBody);
    api.clearTable(saleBody);

    //Populate table
    records.forEach((record) => {
        drawTable(record);
    });
}

function drawTable(record) {
    var row = $('<tr onclick="saleProduct(this)" />');
    var addDate = api.shortDate(record.sale_date);
    $('#stockTable').append(row);
    row.append($('<td>' + record.sale_id + '</td>'));
    row.append($('<td>' + record.products.length + '</td>'));
    row.append($('<td>' + record.sold_by + '</td>'));
    row.append($('<td>' + addDate + '</td>'));
    row.append($('<td>' + record.total_sale + '</td>'));
}

//Collect row elements from Sales table
function saleProduct(call) {
    let table = document.getElementById('stockTable');
    let i = call.rowIndex;
    let row = table.rows[i];
    let sale_id = row.cells[0].innerHTML;

    api.clearTable(saleBody);
    saleRecords.forEach((record) => {
        if (record['sale_id'] == sale_id) {
            saleData(record['products'], record['total_sale']);
        }
    });
}

//Add row elements to products table
function saleData(products, totals) {
    var table = document.getElementById('sale');
    var rows = table.rows;
    var totalSale = rows[1].cells[2];
    products.forEach(product => {
        var row = $('<tr />');
        $('#sale').append(row);
        row.append($('<td>' + product.prod_name + '</td>'));
        row.append($('<td>' + product.quantity + '</td>'));
        row.append($('<td>' + product.price + '</td>'));
    });
    totalSale.innerHTML = totals;
}