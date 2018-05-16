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

    //https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_tabs
}   

// google maps javascript
function initMap(){
    var options = {
        zoom:13,
        center:{lat:53.0328, lng:-7.2988}
    }
    var map = new google.maps.Map(document.getElementById('map'),options) ;
    
    var marker = new google.maps.Marker({
        /*pos of marker*/
        position:{lat:53.0328, lng:-7.2988},
        map:map //which map you want to add it to
    })

}

//call function
geocode();

function geocode(){
//call geocode.
    var location = '22 main st boston ma';
    axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
        params:{
            address:location,
            key:'AIzaSyBzJOP-YgBoJTAl5X1zK3NXmE3ynx4NZQY'
        }
    })
    .then(function(response){
        // Log full response
        console.log(response);
        console.log(response.data.results[0].formatted_address)
    })
    .catch(function(error){
        console.log(error);
    })
}


//    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">


//geocode api key : AIzaSyBzJOP-YgBoJTAl5X1zK3NXmE3ynx4NZQY


