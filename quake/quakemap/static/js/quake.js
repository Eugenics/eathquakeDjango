$(document).ready(
    function () {

        document.getElementById("clickBtn").onclick = function() {clickFunction();};

        //console.log(json_text.replace(/&quot;/g,'"'));       
        var json_object = JSON.parse(json_text.replace(/&quot;/g, '"'));

        var geo_features = new Array(json_object.points.length);


        for (var i = 0; i < json_object.points.length; i++) {
            var coordinates = [json_object.points[i].Lat, json_object.points[i].Lng];
            var magnitude = json_object.points[i].Mag * 1.5;

            geo_features[i] = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat(coordinates)),
                Place: json_object.points[i].Place,
                Mag: json_object.points[i].Mag,
                Details: json_object.points[i].url,
                Time: moment(json_object.points[i].Time).format('LLLL'),
                Coordinates: coordinates                
            });
            geo_features[i].setStyle(
                new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: magnitude,
                        stroke: new ol.style.Stroke({
                            color: 'red',
                            width: 2
                        }),
                        fill: new ol.style.Fill({
                            color: 'white'
                        })
                    })
                })
            );
        }

        //console.log(geo_features);

        var source = new ol.source.Vector({
            features: geo_features
        });

        var sourceVectorLayer = new ol.layer.Vector({
            source: source,
        });

        map.addLayer(sourceVectorLayer);
    }
);