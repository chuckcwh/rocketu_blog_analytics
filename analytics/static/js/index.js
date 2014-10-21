$(document).ready(function(){

    function initialize(data) {
        var mapOptions = {
            center: { lat: 37.7833, lng: -122.4167},
            zoom: 11
        };
        var map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

        for (i = 0; i < data.length; i++) {
            new google.maps.Marker({
                position: new google.maps.LatLng(data[i][0], data[i][1]),
                map: map,
                title: "Hello World!"
            });
        }
    }



    url_path = $('#url').text();
    $.ajax({
        url : '/analytics/page_map_ajax/',
        type: "POST",
        dataType: "json",
        data: JSON.stringify(url_path),
        success: function(data){
            google.maps.event.addDomListener(window, 'load', initialize(data));
        }
    });



});
