const api = new Api();

// Declarations
const msg = document.querySelector('span.msg');
const topMsg = document.getElementById('topMsg');
const stockTableBody = document.querySelector('#stockTable > tbody');
const saleBody = document.querySelector('#sale > tbody');

// Listeners
document.getElementById('makeSale').addEventListener('click', makeSale);
document.getElementById('cancelSale').addEventListener('click', cancelSale);

// Fetch-api functions
function makeSale(){
    let saleItems = soldItems();
    if (Array.isArray(saleItems) && saleItems.length === 0) {
        msg.style.fontWeight = 'bold';
        msg.innerText = 'Please Add a Sale from Items!';
    } else {
        api.post('sales', {'products': saleItems})
        .then(api.handleResponse)
        .then(data => {
            msg.innerText = data['message'];
            api.clearTable(saleBody);
        })
        .catch(err => {
            msg.innerHTML = err['message'] + '<br>';
            api.errCheck(err);
            console.log(err);
        });
    }
}

function cancelSale() {
    api.clearTable(saleBody);
}

// Collect row elements from sales table
function soldItems() {
    var table = document.getElementById('sale');
    var rows = table.rows;
    var data = [];
    for (var r = 2; r < rows.length; r++) {
        var row = rows[r];
        var product ={
            prod_name: row.cells[0].innerHTML,
            quantity: parseInt(row.cells[1].innerHTML)
        };
        data.push(product);
    }
    return data;
}

// On window load
window.onload=function(){
    loadTable();
    api.style();
    };
function loadTable() {
    api.get('products')
    .then(api.handleResponse)
    .then(data => populateTable(data['products']))
    .catch(err => {
        api.errCheck(err);
        console.log(err);
        topMsg.innerText = err['message'];
    });
}

// Add products to table
function populateTable(products) {
    // clear out HTML data
    api.clearTable(stockTableBody);
    api.clearTable(saleBody);
    
    // Populate table
    products.forEach((product) => {
        drawTable(product);
    });
}

function drawTable(product) {
    var row = $('<tr onclick="saleProduct(this)" />');
    $('#stockTable').append(row);
    row.append($('<td>' + product.prod_name + '</td>'));
    row.append($('<td>' + product.prod_id + '</td>'));
    row.append($('<td>' + product.category + '</td>'));
    row.append($('<td>' + product.stock + '</td>'));
    row.append($('<td>' + product.price + '</td>'));
}

// Collect row elements from Inventory table
function saleProduct(call) {
    var table = document.getElementById('stockTable');
    var data = [];
    var i = call.rowIndex;
    for (var c = 0; c < table.rows[i].cells.length; c++){
        content = table.rows[i].cells[c].innerHTML;
        data.push(content);
    }
    saleData(data);
}

// Add row elements to Sales table
function saleData(data) {
    var table = document.getElementById('sale');
    var rows = table.rows;
    var prodNames = [];
    var totalSale = 0;
    for (var r = 1; r < rows.length; r++) {
        var row = rows[r];
        let prodName = row.cells[0].innerHTML;
        prodNames.push(prodName);
    }
    if (prodNames.includes(data[0])) {
        let prodQnty = parseInt(row.cells[1].innerHTML);
        let price = parseInt(row.cells[2].innerHTML);
        prodQnty += 1;
        totalPrice = prodQnty * price;
        row.cells[1].innerHTML = prodQnty;
        row.cells[2].innerHTML = totalPrice;
    } else {
        var row = $('<tr />');
        $('#sale').append(row);
        row.append($('<td>' + data[0] + '</td>'));
        row.append($('<td>' + 1 + '</td>'));
        row.append($('<td>' + data[4] + '</td>'));
    }
    saleAddup(rows, totalSale);
}
// Compound the sale totals
function saleAddup(rows, totalSale) {
    for (var r = 2; r < rows.length; r++) {
        var row = rows[r];
        let price = parseInt(row.cells[2].innerHTML);
        totalSale += price;
    }
    totalsCell = rows[1].cells[2];
    totalsCell.innerHTML = totalSale;
}

// Onchange
function filterCategories(){  
    var regx = new RegExp($('#toFilter').val());
    if(regx =='/all/'){removeFilter();}else{
        $('.content').hide();
        $('.content').filter(function() {
        return regx.test($(this).text());
        }).show();
	}
}
	
function removeFilter(){
    $('.toFilter').val('');
    $('.content').show();
}