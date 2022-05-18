


 function show(){

    var crypto_selectionner = document.getElementById("crypto_selectionner");
    var show_price = document.getElementById("show_price");
    
    show_price.value=  tableau_prix_json[crypto_selectionner.selectedIndex-1].toFixed(2) ;

 }
