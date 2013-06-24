<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <link href="https://developers.google.com/maps/documentation/javascript/examples/default.css"
        rel="stylesheet">
    <title>Places search box</title>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=places"></script>
    <script>
      var map;
      var markers = [];
      var marker = [];
      var infowindow = new google.maps.InfoWindow({size: new google.maps.Size(150,50)});
      var odessa = new google.maps.LatLng(31.848253,-102.367687);

      function initialize() { //create map element
        map = new google.maps.Map(document.getElementById('map-canvas'), {
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          zoom: 12,
          center: odessa,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });

        var input = (document.getElementById('target'));
        var searchBox = new google.maps.places.SearchBox(input);
        service = new google.maps.places.PlacesService(map);

	//Create a searchbox listener 
        google.maps.event.addListener(searchBox, 'places_changed', function() {
          var places = searchBox.getPlaces();

          for (var i = 0, marker; marker = markers[i]; i++) { //erase previous markers
            marker.setMap(null);
          }

          markers = [];
          var bounds = new google.maps.LatLngBounds();
          for (var i = 0, place; place = places[i]; i++) {  //create markers for current
	    createMarker(place);			    //search
            bounds.extend(place.geometry.location);
          }
          map.fitBounds(bounds);
        }); //end searchBox listener

        google.maps.event.addListener(map, 'bounds_changed', function() { //reset map bounds
          var bounds = map.getBounds();					  //according to search
          searchBox.setBounds(bounds);
        });
      }  //end initialize()

      function createMarker(place) { 			//create markers and infowindows
        var placeLoc = place.geometry.location;
        var marker = new google.maps.Marker({
          map: map,
          position: place.geometry.location
        });

        var request = {
          reference: place.reference
        };
							//create listener for opening infowindow
        google.maps.event.addListener(marker, 'click', function() {
          service.getDetails(request, function(place, status){
            if (status == google.maps.places.PlacesServiceStatus.OK) {
              var contentStr = "<h5>"+place.name+"</h5>"+place.formatted_address;
	      if (!!place.formatted_phone_number) contentStr += "<br>"+place.formatted_phone_number+"<br>";
              contentStr += "<a href='../sendmail.php?name=" + place.name + "&address=" 
			 + place.formatted_address + "&phone=" + place.formatted_phone_number 
                         + "&save=yes'>" + "text this info" + "</a>";
              infowindow.setContent(contentStr);       //adds content to infowindow and link
              infowindow.open(map, marker);  	       //to send the text message and adds search to DB
            } else {
              var contentStr = "no result"; 
              infowindow.setContent(contentStr);
              infowindow.open(map, marker);
            }          
          });
        });
        markers.push(marker);
     } // end createMarker()

     google.maps.event.addDomListener(window, 'load', initialize);

    </script>
    <style>
      #map-canvas {
        float: left;
        width: 70%;
      }
      aside {
        float: left;
        width: 29%;
      #target {
        width: 345px;
      }
    </style>
  </head>
  <body>
      <div id="map-canvas"></div>
      <div id="panel">
        <input id="target" type="text" placeholder="Search Box">
      </div>
      <aside> 
        <?php //queries database for prior searches. Can send info to text script without saving to DB
		$dbhandle = sqlite_open('../db/test.db', 0666, $error);

		if (!$dbhandle) die ($error);

		$query = "SELECT * FROM addressText";
		$result = sqlite_query($dbhandle, $query);
		if (!$result) die("Cannot execute query.");

		while ($row = sqlite_fetch_array($result, SQLITE_ASSOC)) {
		    echo "<br>";
		    echo "<li>" . $row['Name']  . "<br>" . $row['Address']  . "<br>" . $row['Phone'] . "<br>";
		    echo "<a href='../sendmail.php?name=" . $row['Name']  . "&address=" . $row['Address']  . "&phone=" . $row['Phone'] . "&save=no'>text this info</a>";
		    echo "<br>";
		}

		sqlite_close($dbhandle);	    
        ?>
      </aside>
  </body>
</html>
