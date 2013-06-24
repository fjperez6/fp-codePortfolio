Ext.setup({
    tabletStartupScreen: 'tablet_startup.png',
    phoneStartupScreen: 'phone_startup.png',
    icon: 'icon.png',
    glossOnIcon: false,
    onReady: function() {

       positionHome = new google.maps.LatLng(21.30870,-157.847647),  //Mi casa
       positionWaikiki = new google.maps.LatLng(21.27121,-157.822466),  //Waikiki beach
       positionPaddleboard = new google.maps.LatLng(21.397459,-157.727623),  //Kailua beach
       positionGreenflash = new google.maps.LatLng(21.317522,-158.115578),  //Green Flash 


            infowindow1 = new google.maps.InfoWindow({
                content: '<h2 id="firstHeading" class="firstHeading">My house</h2>'+
                '<img src="images/downtown.jpg" width=150 height=100>'
            }),

            infowindow2 = new google.maps.InfoWindow({
                content: '<h2 id="firstHeading" class="firstHeading">Waikiki Beach</h2>'+
                '<img src="images/waikiki.jpg" width=150 height=100>'
            }),

            infowindow3 = new google.maps.InfoWindow({
                content: '<h2 id="firstHeading" class="firstHeading">Paddle Board Beach</h2>'+
                '<img src="images/kailua.jpeg" width=150 height=100>'
            }),

            infowindow4 = new google.maps.InfoWindow({
                content: '<h2 id="firstHeading" class="firstHeading">Green Flash Beach</h2>'+
                '<img src="images/Inferior_Mirage_green_flash.jpg" width=150 height=100>'
            }),



                //Tracking Marker Image
                image = new google.maps.MarkerImage(
                    'point.png',
                    new google.maps.Size(32, 31),
                    new google.maps.Point(0,0),
                    new google.maps.Point(16, 31)
                  ),

                shadow = new google.maps.MarkerImage(
                    'shadow.png',
                    new google.maps.Size(64, 52),
                    new google.maps.Point(0,0),
                    new google.maps.Point(-5, 42)
                  ),

        mapdemo = new Ext.Map({

            mapOptions : {
                center : new google.maps.LatLng(21.30870, -157.847647), 
                zoom : 12,
                mapTypeId : google.maps.MapTypeId.ROADMAP,
                navigationControl: true,
                navigationControlOptions: {
                        style: google.maps.NavigationControlStyle.DEFAULT
                    }
            },

            listeners : {
                maprender : function(comp, map){
                    var marker1 = new google.maps.Marker({
                                     position: positionHome,
                                     title : 'my house', 
                                     map: map
                                });

                    var marker2 = new google.maps.Marker({
                                     position: positionWaikiki,
                                     title : 'Waikiki Beach', 
                                     map: map
                                });

                    var marker3 = new google.maps.Marker({
                                     position: positionPaddleboard,
                                     title : 'Paddle Boarding Beach', 
                                     map: map
                                });

                    var marker4 = new google.maps.Marker({
                                     position: positionGreenflash,
                                     title : 'Green Flash Beach', 
                                     map: map
                                });

                                google.maps.event.addListener(marker1, 'mousedown', function() {
                                     infowindow1.open(map, marker1);
                                });

                                google.maps.event.addListener(marker2, 'mousedown', function() {
                                     infowindow2.open(map, marker2);
                                });

                                google.maps.event.addListener(marker3, 'mousedown', function() {
                                     infowindow3.open(map, marker3);
                                });

                                google.maps.event.addListener(marker4, 'mousedown', function() {
                                     infowindow4.open(map, marker4);
                                });

                },

            }
        });

        new Ext.Panel({
            fullscreen: true,
            items: [mapdemo]
        });

    }
});
