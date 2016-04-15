/**
 * Created by Sufian on 4/12/2016.
 */

/**
 * Initializes the web page
 */
$(document).ready(function () {
    //Initialize the page
    loadSearchOptions();
    //Binds the click event for the search button
    $("#btnSearch").click(function(){
        searchEvents();
    });
    //By default search by geoLocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setGeolocation);
    } else {
        //Geolocation not supported.
    }
});

/**
 * Function that triggers the search and validates that the users selects a type and provides and input.
 */
function searchEvents(){
    var typeSearch = $('.input-group #searchBy').val();
    if(typeSearch === "" || typeSearch === null){
        console.log("No type of serach defined");
        return;
    }
    var inputSearch = $("#txtSearchInput").val();
    if(inputSearch === "" || inputSearch === null){
        console.log("No input search provided");
        return;
    }
    if(typeSearch === "byCity"){
        //Look for location. Pass the input search param.
        getEventsbyLocation(1, true);
    }
    else if(typeSearch === "byArtist"){
        getArtistByName(1, true);
    }
}

/**
 * Function that initializes the search options drop down list
 */
function loadSearchOptions(){
    $('.search-panel .dropdown-menu').find('a').click(function(e) {
        e.preventDefault();
        var param = $(this).attr("href").replace("#","");
        var concept = $(this).text();
        $('.search-panel span#searchBy').text(concept);
        $('.input-group #searchBy').val(param);
    });
}

/**
* Function to get the events by place
* @param page Number representing the page to get from the API
 * @param isPaginatorInit True is the paginator needs to be initialized
*/
function getEventsbyLocation(page, isPaginatorInit) {
    //Clean the container
    cleanContainers();
    var container = $("#eventsResult");
    var location = $("#txtSearchInput").val();
    $("#txtTypeSearch").val("location");
    container.empty();
    $.ajax({
        type: "POST",
        url: "/location/" + page+ "/",
        dataType: 'json',
        data: {"location": location}
    })
    // this is a callback function which is triggered when the request has completed and appends the data to the row div
    .done(function (data) {
        renderEvents(data, isPaginatorInit);
    });
}

/**
* Function to search artists
* @param page Number representing the page to get from the API
 * @param isPaginatorInit True is the paginator needs to be initialized
*/
function getArtistByName(page, isPaginatorInit) {
    //Clean the container
    cleanContainers();
    if($('#paginator').data("twbs-pagination")){
        $('#paginator').twbsPagination('destroy');
    }
    var container = $("#eventsResult");
    var artistName = $("#txtSearchInput").val();
    $("#txtTypeSearch").val("location");
    container.empty();
    $.ajax({
        type: "POST",
        url: "/artist_name/" + page + "/",
        dataType: 'json',
        data: {"artistName": artistName}
    })
    // this is a callback function which is triggered when the request has completed and appends the data to the row div
    .done(function (data) {
        if(data['performers'].length > 0){
            renderArtist(data);
        }
        else{
            var container = $("#artistsResult")
            container.append(
                '<div class="row">' +
                    ' <div class="col-sm-12 text-center" >' +
                        "<h4 class='media-heading'>We didn't find any artist with this name :( </h4>" +
                    '</div>' +
                '</div>'
            );
        }
    });
}

/**
 * Sets the position for future use
 * @param position object with the geolocation information
 */
function setGeolocation(position){
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    $("#txtLatitude").val(latitude);
    $("#txtLongitude").val(longitude);
    getEventsByGeolocation(1, true);
}

/**
* Function to get the events by place
* @param page Number representing the page to get from the API
 * @param isPaginatorInit True is the paginator needs to be initialized
*/
function getEventsByGeolocation(page, isPaginatorInit) {
    //Clean the container
    cleanContainers();
    var latitude = $("#txtLatitude").val();
    var longitude = $("#txtLongitude").val();
    $("#txtTypeSearch").val("geolocation");
    $.ajax({
        type: "GET",
        url: "/events_geolocation/" + latitude + "/" + longitude + "/" +page,
        dataType: 'json',
        data: JSON.stringify({})
    })
    // this is a callback function which is triggered when the request has completed and appends the data to the row div
    .done(function (data) {
        renderEvents(data, isPaginatorInit);
    });
}

/**
 * Function that cleans the containers for artists and events
 */
function cleanContainers(){
    var container = $("#eventsResult");
    container.empty();
    var containerArt = $("#artistsResult");
    containerArt.empty();
}

/**
 * Function that renders the events retrieves as a result of the search
 * @param data Json containing the events
 * @param isPaginatorInit True if the paginator needs to be initialized
 */
function renderEvents(data, isPaginatorInit){
    var container = $("#eventsResult");
    var events = data['events'];
    var pageCount = data['pageCount'];
    var newRow = true;
    //Message
    container.append(
        '<div class="row">' +
            ' <div class="col-sm-12 text-center" >' +
                '<h4 class="media-heading">Take a look to this gigs :) </h4>' +
            '</div>' +
        '</div>'
    );
    for (var i=0; i < events.length; i++){
        var imagesrc = "";
        if(events[i].image !== null)
        {
            imagesrc = events[i].image.large.url
        }else{
            imagesrc = '/static/images/portfolio/no-picture.jpeg'
        }
        if(newRow){
            container.append('<div class="row">');
            newRow = false;
        }
        var nameHistory = "";
        var performers = events[i].performers;
        if(performers !== null  && performers.length > 0){
            if(performers[0] !== null) {
                nameHistory = performers[0].name;
            }
            else{
                nameHistory = events[i].title;
            }
        }
        else{
            nameHistory = events[i].title;
        }
        nameHistory = nameHistory.replace(/[^\w0-9]/gi, "_")
        nameHistory = nameHistory.trim().toLocaleLowerCase();
        container.append(
             ' <div class="col-sm-3" >'+
                  '<figure class="wow fadeInLeft animated portfolio-item" data-wow-duration="500ms" data-wow-delay="0ms">'+
                     ' <div class="img-wrapper">'+
                       ' <img src="'+imagesrc+'" class="img-responsive" alt="" >'+
                        '<div class="overlay">'+
                           ' <div class="buttons">'+
                                '<a href="/history/' + nameHistory + '">History</a>'+
                                ' <a id="open"  href="/Details/?id='+events[i].id +'">Details</a>'+
                           ' </div>'+
                        '</div>'+
                   ' </div>'+
                    '<figcaption>'+
                    '<h4>'+
                       ' <a href="#">'+
                         events[i].title +
                        ' </a>'+
                   ' </h4>'+
                   ' <p>' + events[i].cityName +'<br/>'+ events[i].startTime+
                   '</p>'+
                    '<p>'+ events[i].venueName+
                             '</p>'+
                  ' </figcaption>'+
                 '</figure>'+
            '</div>'
        );
        if((i+1)%4 == 0){
            container.append('</div>');
            newRow = true;
        }
    }
    //Call the initialization of the paginator
    if(isPaginatorInit){
        initializePaginator(pageCount);
    }
}

/**
 * Function that renders the artists
 * @param data Json containing the artists
 */
function renderArtist(data){
    cleanContainers();
    var container = $("#artistsResult");
    var artists = data['performers'];
    var newRow = true;
    //Message
    container.append(
        '<div class="row">' +
            ' <div class="col-sm-12 text-center" >' +
                '<h4 class="media-heading">We found this artists for you :) </h4>' +
            '</div>' +
        '</div>'
    );
    for (var i=0; i < artists.length; i++){
        var imagesrc = "";
        if(artists[i].image !== null)
        {
            imagesrc = artists[i].image.large.url
        }else{
            imagesrc = '/static/images/portfolio/no-picture.jpeg'
        }
        if(newRow){
            container.append('<div class="row">');
            newRow = false;
        }
        var nameHistory = artists[i].name;
        nameHistory = nameHistory.replace(/[^\w0-9]/gi, "_").trim().toLocaleLowerCase();
        container.append(
             ' <div class="col-sm-3" >'+
                  '<figure class="wow fadeInLeft animated portfolio-item" data-wow-duration="500ms" data-wow-delay="0ms">'+
                     ' <div class="img-wrapper">'+
                       ' <img src="'+imagesrc+'" class="img-responsive" alt="" >'+
                        '<div class="overlay">'+
                           ' <div class="buttons">'+
                                '<a href="/history/' + nameHistory + '">History</a>' +
                           ' </div>'+
                        '</div>'+
                   ' </div>'+
                    '<figcaption>'+
                    '<h4>'+
                       ' <a href="#">'+
                         artists[i].name +
                        ' </a>'+
                   ' </h4>'+
                    '<p>' +
                        (artists[i].short_bio == null ? "" : artists[i].short_bio) +
                     '</p>'+
                  ' </figcaption>'+
                 '</figure>'+
            '</div>'
        );
        if((i+1)%4 == 0){
            container.append('</div>');
            newRow = true;
        }
    }
}

/**
 * Function to initialize the paginator
 * @param totalPages Number representing the total of pages of the search
 */
function initializePaginator(totalPages){
    if($('#paginator').data("twbs-pagination")){
        $('#paginator').twbsPagination('destroy');
    }
    $('#paginator').twbsPagination({
        totalPages: totalPages,
        visiblePages: 5,
        initiateStartPageClick: false,
        onPageClick: function (event, page) {
            var typeSearch = $("#txtTypeSearch").val();
            if(typeSearch === "location"){
                getEventsbyLocation(page, false);
            }
            else if(typeSearch === "geolocation"){
                getEventsByGeolocation(page, false);
            }
            else{
                //This should be the function to get events by Artists
            }

        }
    });
}