coordinates = geocode(document.getElementById('address').textContent, function(coordinates){initMap(coordinates)})

//Information Tabs (Information/Map)
//credit: //https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_tabs
function changeTab(evn, selectedTab){
    var i;
    var tab;
    var toolbar;

    tab = document.getElementsByClassName("tab");
    for (i = 0; i < tab.length; i++) {
        tab[i].style.display = "none";
    }
    toolbar = document.getElementsByClassName("toolbar");

    for (i = 0; i < toolbar.length; i++) {
        toolbar[i].className = toolbar[i].className.replace(" active", "");
    }

    document.getElementById(selectedTab).style.display = "block";
    evn.currentTarget.className += " active";
}   

//Displays google map
function initMap(coords){
    var options = {
        zoom:17,
        center:{lat:coords[0], lng:coords[1]}
    }
    var map = new google.maps.Map(document.getElementById('map'),options) ;
    var marker = new google.maps.Marker({
        position:{lat:coords[0], lng:coords[1]},
        map:map //which map you want to add it to
    })
}

//Gets the Geo Coordinates of the property
//credit: https://www.youtube.com/watch?v=pRiQeo17u6c
function geocode(address, callback){
    var location = document.getElementById('address').textContent

    axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
        params:{
            address: location,
            key:'AIzaSyBzJOP-YgBoJTAl5X1zK3NXmE3ynx4NZQY'
        }
    })
    .then(function(response){
        coordinates = [response.data.results[0].geometry.location.lat,response.data.results[0].geometry.location.lng];
        callback(coordinates)
    })
    .catch(function(error){
        console.log(error);
    })   
}