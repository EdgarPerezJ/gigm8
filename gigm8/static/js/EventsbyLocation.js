/**
 * Created by Sufian on 4/12/2016.
 */
$(document).ready(function () {
    //Initialize the page
    var page=getParameterByName('page')
    if(page!==null) {
        getEventsbyLocation(page)
    }else{
        getEventsbyLocation(1)
    }

});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function getEventsbyLocation(page){
    $.ajax({
      type: "GET",
      url: "/location/"+page,
      dataType: 'json',
      data: JSON.stringify({})
    })
    // this is a callback function which is triggered when the request has completed and appends the data to the row div
    .done(function( data ) {
        var events = data['events']
        var pageCount=data['pageCount']
        var row = $("#row1");
        var pages=$("#pages");
        var next= $("#next");
        var prev= $("#prev");

        for (var i=0; i < events.length; i++){
            if(events[i].image!==null)
              {
                 var imagesrc=events[i].image.large.url
              }else{
              imagesrc='/static/images/portfolio/muse.jpg'
              }
            row.append(
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
        }
        for (var i=1; i < pageCount; i++){

            $('<li><a href="?page='+[i]+'" value="'+[i]+'">'+ [i]+'</a>'+'</li>').insertBefore("#before");


        }

        var newpage=parseInt(page)+1
        var prevpage=parseInt(page)-1
        next.attr("href","?page="+newpage)
        prev.attr("href","?page="+prevpage)

    });
}