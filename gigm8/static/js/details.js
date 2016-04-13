/**
 * Created by Sufian on 4/13/2016.
 */
$(document).ready(function () {
    //Initialize the page
     getEventsDetails()

});

function getEventsDetails(){
    //Clean the container
    var container = $("#details");
    $.ajax({
      type: "GET",
      url: "/getdetails/",
      dataType: 'json',
      data: JSON.stringify({})
    })
    // this is a callback function which is triggered when the request has completed and appends the data to the row div
    .done(function( data ) {

         var imagesrc = "";
            if(data['image']!== null)
            {    var images = data['image']
                 for (var i=0; i < images.length; i++){
                     imagesrc=images[1]['large']['url']
                 }
            }else{
                imagesrc = '/static/images/portfolio/muse.jpg'
            }

            if(data['description']!== null)
            {    var description = data['description']

            }else{
                description = 'No Description Available'
            }
              if(data['performer']!== null)
            {    var performer = data["performer"]['performer']['name']

            }else{
                performer = 'No Performers Listed'
            }

            container.append(
                 '<div class="row">'+
                   '<div class="col-md-3" style="margin-top:50px">'+
                        ' <img src="'+imagesrc+'" class="img-responsive" alt=""  >'+
                   '</div>'+
                     '<div class="col-md-9" style="margin-top:50px">'+
                        '<h4>'+
                        ' <p style="margin-left:100px">Title: '+data['title']+'</p>'+
                          '</h4>'+
                         '<p style="margin-left:100px">Performers: '+performer+'</p>'+
                         '<p style="margin-left:100px">Venue: '+data['venueName']+'</p>'+
                          '<p style="margin-left:100px">Date: '+data['date']+'</p>'+
                          '<button type="button" class="btn btn-success" style="margin-left:100px">Buy Tickets!</button>'+
                     '</div>'+
                    '</div>'+
                    '<div style="margin-top:50px"><p>Description:</p><p style="margin-left:20px">'+description+'</p></div>'

            );


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