//Declarations
const productsUrl = 'https://thecodestoremanager-api-heroku.herokuapp.com/api/v1/products'
const token = localStorage.getItem("token");
const loggedUser = localStorage.getItem("loggedUser")
const stockBody = document.querySelector('#prodStock > tbody');
var heading = document.querySelector('#thelist')

// Listeners
var category = document.getElementsByClassName("prodCategory");
Array.from(category).forEach(function(element) {
    element.addEventListener('click', categoryCall);
});

//On window load
window.onload=function(){
    getProducts();
    style();
}
function getProducts() {
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
        products = data['products'];
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

//Collect category name
function categoryCall(call) {
    data = this.id
    heading.innerHTML = data
    let categoryProducts = []
    products.forEach(function(product) {
        if (product.category == data) {
            categoryProducts.push(product)
        }
    });
    categoryData(categoryProducts)
}

//Add row elements to products table
function categoryData(data) {
    clearTable(stockBody)
    data.forEach(function(product){
        var row = $('<tr />')
        $('#prodStock').append(row);
        row.append($('<td>' + product.prod_name + '</td>'));
        row.append($('<td>' + product.price + '</td>'));
    })
}

//Clear all table rows
function clearTable(tableBody) {
    while (tableBody.firstChild) {
        tableBody.removeChild(tableBody.firstChild);
    }
}