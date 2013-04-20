var currPosition;
navigator.geolocation.getCurrentPosition(function(position) {
    updatePosition(position);
    setInterval(function(){
        var lat = currPosition.coords.latitude;
        var lng = currPosition.coords.longitude;
        jQuery.ajax({
            type: "POST", 
            url:  "/updatelocation", 
            data: 'lat='+lat+'&long='+lng, 
            cache: false
        });
    }, 1000);
}, errorCallback, {timeout:10000}); 

var watchID = navigator.geolocation.watchPosition(function(position) {
    updatePosition(position);
});

function updatePosition( position ){
    currPosition = position;
}

function errorCallback(error) {
    var msg = "Can't get your location. Error = ";
    if (error.code == 1)
        msg += "PERMISSION_DENIED";
    else if (error.code == 2)
        msg += "POSITION_UNAVAILABLE";
    else if (error.code == 3)
        msg += "TIMEOUT";
    msg += ", msg = "+error.message;

    alert(msg);
}