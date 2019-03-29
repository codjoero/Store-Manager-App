const api = new Api();

// Declarations
const msg = document.querySelector('span.msg');
const topMsg = document.getElementById('topMsg');
const stockTableBody = document.querySelector('#stockTable > tbody');
const saleBody = document.querySelector('#sale > tbody');
const modal = document.getElementById('confirm-modal');
const modalConfirm = document.getElementById('modal-yes');
const modalDecline = document.getElementById('modal-no');

// Listeners
document.getElementById('makeSale').addEventListener('click', makeSale);
document.getElementById('cancelSale').addEventListener('click', cancelSale);

// Fetch-api functions
function makeSale() {
  const saleItems = soldItems();
  if (Array.isArray(saleItems) && saleItems.length === 0) {
    msg.style.fontWeight = 'bold';
    msg.innerText = 'Please Add a Sale from Items!';
  } else {
    modal.style.display = 'block';
    modalConfirm.onclick = () => {
      modal.style.display = 'none';
      api.post('sales', { products: saleItems })
        .then(api.handleResponse)
        .then((data) => {
          msg.innerText = data.message;
          api.clearTable(saleBody);
        })
        .catch((err) => {
          msg.innerHTML = `${err.message}<br>`;
          api.errCheck(err);
          console.log(err);
        });
    };
    modalDecline.onclick = () => {
      modal.style.display = 'none';
    };
    window.onclick = (event) => {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    };
  }
}

function cancelSale() {
  api.clearTable(saleBody);
}

// Collect row elements from sales table
function soldItems() {
  const table = document.getElementById('sale');
  const rows = table.rows;
  const data = [];
  for (let r = 2; r < rows.length; r++) {
    const row = rows[r];
    const product = {
      prod_name: row.cells[0].innerHTML,
      quantity: parseInt(row.cells[1].innerHTML),
    };
    data.push(product);
  }
  return data;
}

// On window load
window.onload = function () {
  loadTable();
  api.style();
};
function loadTable() {
  api.get('products')
    .then(api.handleResponse)
    .then(data => populateTable(data.products))
    .catch((err) => {
      api.errCheck(err);
      console.log(err);
      topMsg.innerText = err.message;
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
  const row = $('<tr onclick="saleProduct(this)" />');
  $('#stockTable').append(row);
  row.append($(`<td>${product.prod_name}</td>`));
  row.append($(`<td>${product.prod_id}</td>`));
  row.append($(`<td>${product.category}</td>`));
  row.append($(`<td>${product.stock}</td>`));
  row.append($(`<td>${product.price}</td>`));
}

// Collect row elements from Inventory table
function saleProduct(call) {
  const table = document.getElementById('stockTable');
  const data = [];
  const i = call.rowIndex;
  for (let c = 0; c < table.rows[i].cells.length; c++) {
    content = table.rows[i].cells[c].innerHTML;
    data.push(content);
  }
  saleData(data);
}

// Add row elements to Sales table
function saleData(data) {
  const table = document.getElementById('sale');
  const rows = table.rows;
  const prodNames = [];
  const totalSale = 0;
  for (let r = 1; r < rows.length; r++) {
    var row = rows[r];
    const prodName = row.cells[0].innerHTML;
    prodNames.push(prodName);
  }
  if (prodNames.includes(data[0])) {
    let prodQnty = parseInt(row.cells[1].innerHTML);
    const price = parseInt(row.cells[2].innerHTML);
    prodQnty += 1;
    totalPrice = prodQnty * price;
    row.cells[1].innerHTML = prodQnty;
    row.cells[2].innerHTML = totalPrice;
  } else {
    var row = $('<tr />');
    $('#sale').append(row);
    row.append($(`<td>${data[0]}</td>`));
    row.append($(`<td>${1}</td>`));
    row.append($(`<td>${data[4]}</td>`));
  }
  saleAddup(rows, totalSale);
}
// Compound the sale totals
function saleAddup(rows, totalSale) {
  for (let r = 2; r < rows.length; r++) {
    const row = rows[r];
    const price = parseInt(row.cells[2].innerHTML);
    totalSale += price;
  }
  totalsCell = rows[1].cells[2];
  totalsCell.innerHTML = totalSale;
}

// Onchange
function filterCategories() {
  const regx = new RegExp($('#toFilter').val());
  if (regx === '/all/') { removeFilter(); } else {
    $('.content').hide();
    $('.content').filter(function () {
      return regx.test($(this).text());
    }).show();
  }
}

function removeFilter() {
  $('.toFilter').val('');
  $('.content').show();
}
