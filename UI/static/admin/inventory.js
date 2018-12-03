const api = new Api();

// Declarations
const msg = document.querySelector('span.msg');
const topMsg = document.getElementById('topMsg');
const mytableBody = document.querySelector('#mytable > tbody');

// Listeners
document.getElementById('addProduct').addEventListener('submit', addProduct);
document.getElementById('updateProduct').addEventListener('submit', updateProduct);

// Fetch-api functions
function addProduct (e) {
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

    api.post('products', product)
    .then(api.handleResponse)
    .then((data) => {
        msg.innerText = data['message'];
        location.reload(true);
    })
    .catch(err => {
        msg.innerHTML = err['message'] + '<br>';
        api.errCheck(err);
        console.log(err);
    });
}

function updateProduct(e){
    e.preventDefault();

    let prodName = document.getElementById('uProdName').value;
    let category = document.getElementById('uCategory').value;
    let stock = document.getElementById('uStock').value;
    let price = document.getElementById('uPrice').value;
    let product = {
        prod_name: prodName,
		category: category,
		stock: parseInt(stock, 10),
        price: parseInt(price, 10)
    };

    api.put(`products/${prod_id}`, product)
    .then(api.handleResponse)
    .then(() => location.reload(true))
    .catch(err => {
        updateMsg.innerHTML = err['message'];
        api.errCheck(err);
        console.log(err);
    });
}

function deleteProduct(_id){
    api.delete(`products/${_id}`)
    .then(api.handleResponse)
    .then((data) => {
        msg.innerText = data['message'];
    })
    .catch(err => {
        msg.innerHTML = err['message'] + '<br>';
        api.errCheck(err);
        console.log(err);
    });
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
    api.clearTable(mytableBody);
    // Populate table
    products.forEach(product => drawTable(product));
}

function drawTable(product) {
    var row = $('<tr class="content" />');
    var edit = '<i class="fa fa-edit" onclick="editRow(this)"></i>';
    var del = '<i class="fa fa-close" onclick="deleteRow(this)"></i>';
    var addDate = api.shortDate(product.added_on);
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

// Edit table row
function editRow(call) {
    var table = document.getElementById('mytable');
    var prodForm = document.forms['updateProduct'];
    var prodName = prodForm.elements[0];
    var category = prodForm.elements[1];
    var stock = prodForm.elements[2];
    var price = prodForm.elements[3];
    var data = [];
    var i = call.parentNode.parentNode.rowIndex;
    prod_id = table.rows[i].cells[1].innerHTML;
    for (var c = 0; c < table.rows[i].cells.length - 1; c++){
        content = table.rows[i].cells[c].innerHTML;
        data.push(content);
    }
    prodName.value = data[0];
    category.value = data[2];
    stock.value = data[3];
    price.value = data[5];
    $('form').animate({height: 'toggle', opacity: 'toggle'}, 'slow');
}

// Delete table row
function deleteRow(call) {
    var table = document.getElementById('mytable');
    var i = call.parentNode.parentNode.rowIndex;
    deleteProd_id = table.rows[i].cells[1].innerHTML;
    deleteProduct(deleteProd_id);
    document.getElementById('mytable').deleteRow(i);
}

//Onchange
function filterCategories(){  
    var regx = new RegExp($('#toFilter').val());
    if(regx =='/all/'){removeFilter();}else{
        console.log($('.content'));
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