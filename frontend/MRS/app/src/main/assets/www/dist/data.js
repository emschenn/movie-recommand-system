$(document).ready(function() {
    /*emotion*/
    $.ajax({
        async: true,
        crossDomain: true,
        url: SERVER_URL + "test/",
        method: "GET",
        dataType: "json",
        success: function(data) {
            localStorage.setItem('name', data[0].name);
            console.log(data);
            $('#helloname').text("Hello! " + data[0].name);
            $('#neutral').text(data[0].neutral);
            $('#happiness').text(data[0].happiness);
            $('#surprise').text(data[0].surprise);
            $('#sadness').text(data[0].sadness);
            $('#anger').text(data[0].anger);
            $('#disgust').text(data[0].disgust);
            $('#fear').text(data[0].fear);
            $('#contempt').text(data[0].contempt);
            getMovieId(data[0].movie1, "#em.rec");
            getMovieId(data[0].movie2, "#em.rec");
            getMovieId(data[0].movie3, "#em.rec");
            // getMovieId(data[0].movie4, "#em.rec");
            // getMovieId(data[0].movie5, "#em.rec");
            // getMovieId(data[0].movie6, "#em.rec");
            // getMovieId(data[0].movie7, "#em.rec");
            // getMovieId(data[0].movie8, "#em.rec");
            // getMovieId(data[0].movie9, "#em.rec");
            // getMovieId(data[0].movie10, "#em.rec");
            /* bpr */
            getMovieId(data[0].recommandation1, "#bpr.rec");
            getMovieId(data[0].recommandation2, "#bpr.rec");
            getMovieId(data[0].recommandation3, "#bpr.rec");
            getMovieId(data[0].recommandation4, "#bpr.rec");

            getMovieId(data[0].recommandation5, "#bpr.rec");

        },
        error: function(result) {
            console.log(result);
        }
    });
    /* BPR 
    $.ajax({
        async: true,
        crossDomain: true,
        url: "http://192.168.210.32:8000/test/",
        method: "GET",
        dataType: "json",
        success: function(data) {
            console.log(data);

            
        },
        error: function(result) {
            console.log(result);
        }
    });
*/
    /*hit this week*/
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/trending/movie/week?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            console.log(response);
            for (i = 0; i < 15; i++) {
                $("#top.rec").append("<div class='col' onclick='moreInfo(" + response.results[i].id + ",0,0)'>" +
                    "<img src='https://image.tmdb.org/t/p/w154/" + response.results[i].poster_path + "' style='width:145px'>" +
                    "<p class='mtitle'>" + response.results[i].original_title + "</p>" +
                    "</div>");
            }
        },
    });
});



function getMovieId(id, div) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/movie/" + id + "?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            $(div).append("<div class='col' onclick='moreInfo(" + response.id + ",0,0)'>" +
                "<img src='https://image.tmdb.org/t/p/w300/" + response.poster_path + "' style='width:145px'>" +
                "<p class='mtitle'>" + response.title + "</p>" +
                "</div>");
        },
    });
}