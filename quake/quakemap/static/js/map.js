// Create map
var baseLayer = new ol.layer.Tile({
    source: new ol.source.OSM()
});

var map = new ol.Map({
    target: 'map',
    layers: [baseLayer],
    view: new ol.View({
        center: ol.proj.fromLonLat([82.933952, 55.018803]), //Coordinates of New York
        zoom: 3 //Initial Zoom Level
    })
});

// Adding a marker on the map
var marker = new ol.Feature({
    geometry: new ol.geom.Point(
        ol.proj.fromLonLat([82.933952, 55.018803])
    ),  // Coordinates of Novosibirsk
});

var vectorSource = new ol.source.Vector({
    features: [marker]
});

var markerVectorLayer = new ol.layer.Vector({
    source: vectorSource,
});

/*
marker.setStyle(
    new ol.style.Style({
        image: new CircleStyle({
            radius: 5,
            fill: new Fill({
                color: '#ffcd46'
            })            
        })
    })
);
*/

map.addLayer(markerVectorLayer);