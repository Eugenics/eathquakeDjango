function clickFunction() {
    console.log('aaaa');

    var animeLayer = new ol.layer.Vector();

    var client = new XMLHttpRequest();
    client.open('GET', 'srch');
    client.onload = function(){
        var result = client.responseText;
        var feature = [];

        console.log(result);
    };

    client.send();
}