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

var element = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');

var popup = new ol.Overlay({
    element: element,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    }
});

closer.onclick = function () {
    popup.setPosition(undefined);
    closer.blur();
    return false;
};

//map.addOverlay(popup);

map.addOverlay(popup);

map.on('click', function (evt) {
    var mapfeature = map.forEachFeatureAtPixel(evt.pixel,
        function (mapfeature) {
            return mapfeature;
        });
    if (mapfeature) {
        var mapfeature_coordinates = mapfeature.getGeometry().getCoordinates();
        var hdms = ol.coordinate.toStringHDMS(mapfeature.get('Coordinates'));
        console.log(mapfeature.get('Details'));
        content.innerHTML = '<h1><a href="' + mapfeature.get('Details') + '">' + mapfeature.get('Place') + '</a></h1>' +
            '<dl><dt>Time</dt><dd><time datetime="' + mapfeature.get('Time') + '">' + mapfeature.get('Time') + '</time></dd>' +
            '<dt>Location</dt><dd><code>' + hdms + '</code></dd>' +
            '<dt>Depth</dt><dd>' + mapfeature.get('Mag') + '</dd></dl>';
        popup.setPosition(mapfeature_coordinates);
    } else {}
});

/*
// change mouse cursor when over marker
map.on('pointermove', function (e) {
    /*if (e.dragging) {
      $(element).popover('destroy');
      return;
    }
    var pixel = map.getEventPixel(e.originalEvent);
    var hit = map.hasFeatureAtPixel(pixel);
    map.getTarget().style.cursor = '';
});
*/

/*
map.on('pointermove', function (e) {
    if (e.dragging) {
        $(element).popover('destroy');
        return;
    }
    var pixel = map.getEventPixel(e.originalEvent);
    var hit = map.hasFeatureAtPixel(pixel);
    map.getTarget().style.cursor = hit ? 'pointer' : '';
});
*/


/*
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


marker.setStyle(
    new ol.style.Style({
        image: new ol.style.Circle({
            radius: 6,
            stroke: new ol.style.Stroke({
                color: 'orange',
                width: 2
            }),
            fill: new ol.style.Fill({
                color: 'white'
            })            
        })
    })
);


map.addLayer(markerVectorLayer);
*/