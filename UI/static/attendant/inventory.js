const api = new Api;

//Declarations
const mytableBody = document.querySelector('#mytable > tbody');

//On window load
window.onload=function(){
    loadTable();
    api.style();
    };
function loadTable() {
    api.get('products')
    .then(api.handleResponse)
    .then((data) => {
        populateTable(data['products']);
    })
    .catch(err => {
        api.errCheck(err);
        console.log(err);
    });
}

//Add products to table
function populateTable(products) {
    api.clearTable(mytableBody);
    //Populate table
    products.forEach((product) => {
        drawTable(product);
    });
}

function drawTable(product) {
    var row = $('<tr />');
    var addDate = api.shortDate(product.added_on);
    $('#mytable').append(row);
    row.append($('<td>' + product.prod_name + '</td>'));
    row.append($('<td>' + product.prod_id + '</td>'));
    row.append($('<td>' + product.category + '</td>'));
    row.append($('<td>' + product.stock + '</td>'));
    row.append($('<td>' + 10 + '</td>'));
    row.append($('<td>' + product.price + '</td>'));
    row.append($('<td>' + addDate + '</td>'));
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