function clickFunction() {
    var date_from_par = $('#inputDateFrom').val();
    var date_till_par = $('#inputDateTill').val();
    var mag_par = $('#inputMag').val();
    var place_par = $('#inputPlace').val();

    if (place_par.length == 0) {
        place_par = '';
    }


    $.ajax({
        url: 'search',
        data: {
            'date_from': date_from_par,
            'date_till': date_till_par,
            'mag': mag_par,
            'region': place_par
        },
        success: function (response) {

            
            var $table = $('#eathquakeDataTable');
            var $bodyContent = $(response).find('tbody').children();

            $table.find('tbody').empty().append($bodyContent);
            $table.trigger('reflow');
            

           
            

            /*

            var $table = $('#eathquakeDataTable');
            var $bodyContent = $(response).find('table');          
            
            console.log($bodyContent);


            $table.empty().html($bodyContent);

            var $main_form = $('#main_form');
            var $content = $(response).find('div').children();

            console.log($content);
            
            $main_form.find('div').empty().html($content);
            //$main_form.trigger('refresh');
            */
        }
    });

    $.ajax({
        url: 'api/quakelist',
        data: {
            'date_from': date_from_par,
            'date_till': date_till_par,
            'mag': mag_par,
            'region': place_par
        },
        success: function (response) {
            //console.log(response);

            var geo_features = new Array(response.length);

            for (var i = 0; i < response.length; i++) {
                var coordinates = [parseFloat(response[i].lat), parseFloat(response[i].lng)];
                var magnitude = parseFloat(response[i].mag) * 1.5;

                geo_features[i] = new ol.Feature({
                    geometry: new ol.geom.Point(ol.proj.fromLonLat(coordinates)),
                    Place: response[i].region,
                    Mag: parseFloat(response[i].mag),
                    Details: response[i].url,
                    Time: moment(response[i].eathquake_time).format('LLLL'),
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

            var source = new ol.source.Vector({
                features: geo_features
            });

            var sourceVectorLayer = new ol.layer.Vector({
                source: source,
            });

            //------ Delete privious layers ------------------------
            var mapLayers = map.getLayers().getArray();

            if (mapLayers.length > 1) {
                for (i = 0; i < mapLayers.length; i++) {
                    if (mapLayers[i].type != 'TILE') {
                        map.removeLayer(mapLayers[i]);
                    }
                }

            }

            //-------- Add new layer --------------------------------
            map.addLayer(sourceVectorLayer);            
        }
    });
}