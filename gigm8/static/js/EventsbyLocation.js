/**
 * Created by Sufian on 4/12/2016.
 */

/**
 * Initializes the web page
 */
$(document).ready(function () {
    //Initialize the page
    loadSearchOptions();
    var page = getParameterByName('page')
    if(page !== null) {
        getEventsbyLocation(page, true)
    }else{
        getEventsbyLocation(1, true)
    }
});

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

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

/**
* Function to get the events by place
* @param page Number representing the page to get from the API
 * @param isPaginatorInit True is the paginator needs to be initialized
*/
function getEventsbyLocation(page, isPaginatorInit){
    //Clean the container
    var container = $("#eventsResult");
    container.empty();
    $.ajax({
      type: "GET",
      url: "/location/"+page,
      dataType: 'json',
      data: JSON.stringify({})
    })
    // this is a callback function which is triggered when the request has completed and appends the data to the row div
    .done(function( data ) {
        var events = data['events']
        var pageCount = data['pageCount']
        var newRow = true;
        for (var i=0; i < events.length; i++){
            var imagesrc = "";
            if(events[i].image !== null)
            {
                imagesrc = events[i].image.large.url
            }else{
                imagesrc = '/static/images/portfolio/muse.jpg'
            }
            if(newRow){
                container.append('<div class="row">');
                newRow = false;
            }
            container.append(
                 ' <div class="col-sm-3" >'+
                      '<figure class="wow fadeInLeft animated portfolio-item" data-wow-duration="500ms" data-wow-delay="0ms">'+
                         ' <div class="img-wrapper">'+
                           ' <img src="'+imagesrc+'" class="img-responsive" alt="" >'+
                            '<div class="overlay">'+
                               ' <div class="buttons">'+
                                    '<a href="/history">History</a>'+
                                    ' <a href="">Details</a>'+
                               ' </div>'+
                            '</div>'+
                       ' </div>'+
                        '<figcaption>'+
                        '<h4>'+
                           ' <a href="#">'+
                             events[i].title+
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
    });

    /**
     * Function to initialize the paginator
     * @param totalPages Number representing the total of pages of the search
     */
    function initializePaginator(totalPages){
        $('#paginator').twbsPagination({
            totalPages: totalPages,
            visiblePages: 5,
            initiateStartPageClick: false,
            onPageClick: function (event, page) {
                getEventsbyLocation(page, false);
            }
        });
    }
}