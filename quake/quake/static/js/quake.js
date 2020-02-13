$(document).ready(
    function () {


        document.getElementById("clickBtn").onclick = function () {
            clickFunction();
        };

        var json_object = JSON.parse(json_list.replace(/&quot;/g, '"'));
        var geo_features = new Array(json_object.length);


        for (var i = 0; i < json_object.length; i++) {
            var coordinates = [parseFloat(json_object[i].lat), parseFloat(json_object[i].lng)];
            var magnitude = parseFloat(json_object[i].mag) * 1.5;

            geo_features[i] = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat(coordinates)),
                Place: json_object[i].region,
                Mag: parseFloat(json_object[i].mag),
                Details: json_object[i].url,
                Time: moment(json_object[i].eathquake_time).format('LLLL'),
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
            source: source
            //name: 'search_layer'
        });

        map.addLayer(sourceVectorLayer);

        /*
                // Toggle the side navigation
                $("#sidebarToggle, #sidebarToggleTop").on('click', function (e) {
                    $("body").toggleClass("sidebar-toggled");
                    $(".sidebar").toggleClass("toggled");
                    if ($(".sidebar").hasClass("toggled")) {
                        $('.sidebar .collapse').collapse('hide');
                    }
                });

                // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
                $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function (e) {
                    if ($(window).width() > 768) {
                        var e0 = e.originalEvent,
                            delta = e0.wheelDelta || -e0.detail;
                        this.scrollTop += (delta < 0 ? 1 : -1) * 30;
                        e.preventDefault();
                    }
                });
        */
    });