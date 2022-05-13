



function test(){

var crypto_selectionner = document.getElementById("crypto_selectionner");


var show_price = document.getElementById("show_price");
var index = tableau_json.findIndex(x => x == crypto_selectionner.value);

show_price.value = tableau_prix_json[index];

}

