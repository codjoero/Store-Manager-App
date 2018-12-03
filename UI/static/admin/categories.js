const api = new Api();

//Declarations
const stockBody = document.querySelector('#prodStock > tbody');
var heading = document.querySelector('#thelist');

// Listeners
var category = document.getElementsByClassName('prodCategory');
Array.from(category).forEach(function(element) {
    element.addEventListener('click', categoryCall);
});

//On window load
window.onload=function(){
    getProducts();
    api.style();
};
function getProducts() {
    api.get('products')
    .then(api.handleResponse)
    .then((data) => {
        products = data['products'];
    })
    .catch(err => {
        api.errCheck(err);
        console.log(err);
    });
}

//Collect category name
function categoryCall(call) {
    data = this.id;
    heading.innerHTML = data;
    let categoryProducts = [];
    products.forEach(function(product) {
        if (product.category == data) {
            categoryProducts.push(product);
        }
    });
    categoryData(categoryProducts);
}

//Add row elements to products table
function categoryData(data) {
    api.clearTable(stockBody);
    data.forEach(function(product){
        var row = $('<tr />');
        $('#prodStock').append(row);
        row.append($('<td>' + product.prod_name + '</td>'));
        row.append($('<td>' + product.price + '</td>'));
    });
}