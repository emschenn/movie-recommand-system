$(document).ready(function() {
    /*emotion*/
    $.ajax({
        async: true,
        crossDomain: true,
        url: SERVER_URL + "test/",
        method: "GET",
        dataType: "json",
        success: function(data) {
            localStorage.setItem('name', data.name);
            console.log(data);
            $('#helloname').text(data.name);
            $('#neutral').text(data.neutral);
            $('#happiness').text(data.happiness);
            $('#surprise').text(data.surprise);
            $('#sadness').text(data.sadness);
            $('#anger').text(data.anger);
            $('#disgust').text(data.disgust);
            $('#fear').text(data.fear);
            $('#contempt').text(data.contempt);
            for (var i = 0; i < data.recommandation.length; i++) {
                getMovieId(data.recommandation[i], "#em.rec");

            }
            for (var i = 0; i < data.movie.length; i++) {
                getMovieId(data.movie[i], "#bpr.rec");

            }


        },
        error: function(result) {
            console.log(result);
        }
    });

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