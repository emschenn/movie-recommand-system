var nowbox;
$(document).ready(function() {
    nowbox = "rec";
    showbottom(nowbox);
    $(".more").hide();

});


$(".close").click(function() {
    hidebox();
    $("#" + nowbox).animate({ left: '120px' }, "slow");
    $("." + nowbox).animate({ width: '1130px' }, "slow");
    clearbut("#m-cat");
    clearbut("#m-list");
    clearbut("#m-rate");
    clearbut("#m-emo");
});

$("#m-rec").click(function() {
    nowbox = "rec";
    hidebox();
    showbottom(nowbox);
    $("#rec").animate({ left: '120px' }, "slow");
    $(".rec").animate({ width: '1130px' }, "slow");
    clearbut("#m-cat");
    clearbut("#m-list");
    clearbut("#m-rate");
    clearbut("#m-emo");
});

var cclick, eclick = 0;
$("#m-cat").click(function() {
    if (cclick == 0) {
        pressbut(this);
        clearbut("#m-emo");
        clearbut("#m-list");
        clearbut("#m-rate");
        $("#cat").animate({ left: '80px' }, "slow");
        $("#" + nowbox).animate({ left: '360px' }, "slow");
        $("." + nowbox).animate({ width: '890px' }, "slow");
        cclick = 1;
    } else {
        clearbut(this);
        hidebox();
        $("#" + nowbox).animate({ left: '120px' }, "slow");
        $("." + nowbox).animate({ width: '1130px' }, "slow");
        cclick = 0;
    }
});

$("#m-emo").click(function() {
    $.ajax({
        type: 'get',
        url: "http://192.168.210.10:8000/test/",
        dataType: "json",
        success: function(data) {
            console.log(data);
            $('#neutral').text(data[0].neutral);
            $('#happiness').text(data[0].happiness);
            $('#surprise').text(data[0].surprise);
            $('#sadness').text(data[0].sadness);
            $('#anger').text(data[0].anger);
            $('#disgust').text(data[0].disgust);
            $('#fear').text(data[0].fear);
            $('#contempt').text(data[0].contempt);
        },
        error: function(result) {
            console.log(result);
        }
    });
    if (eclick == 0) {
        pressbut(this);
        clearbut("#m-cat");
        clearbut("#m-list");
        clearbut("#m-rate");
        $("#emo").animate({ left: '80px' }, "slow");
        $("#" + nowbox).animate({ left: '360px' }, "slow");
        $("." + nowbox).animate({ width: '890px' }, "slow");
        eclick = 1;
    } else {
        hidebox();
        clearbut(this);
        $("#" + nowbox).animate({ left: '120px' }, "slow");
        $("." + nowbox).animate({ width: '1130px' }, "slow");
        eclick = 0;
    }
});

$("#m-rate").click(function() {
    nowbox = "rate";
    hidebox();
    pressbut(this);
    showbottom(nowbox);
    clearbut("#m-cat");
    clearbut("#m-list");
    clearbut("#m-emo");
    $("#" + nowbox).animate({ left: '120px' }, "slow");
    $("." + nowbox).animate({ width: '1130px' }, "slow");
    var json = {};
    //json["name"] = "1234";
    json['name'] = localStorage.getItem('name');

    $("#rated").empty();
    $.ajax({
        url: "http://192.168.210.10:8000/get_movie_rating/",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function(data) {
            console.log(data);
            for (var i = 0; i < data.tmdbId.length; i++) {
                showRatedList(data.tmdbId[i], data.rating[i]);
            }
        },
        error: function(xhr, ajaxOptions, thrownError) {
            if (xhr.status == 200) {
                console.log(ajaxOptions);
            } else {
                console.log(xhr.status);
            }
        }
    });
});

$("#m-list").click(function() {
    nowbox = "list";
    showbottom(nowbox);
    hidebox();
    pressbut(this);
    clearbut("#m-cat");
    clearbut("#m-emo");
    clearbut("#m-rate");
    $("#" + nowbox).animate({ left: '120px' }, "slow");
    $("." + nowbox).animate({ width: '1130px' }, "slow");
    var json = {};
    // json["name"] = "1234";
    json['name'] = localStorage.getItem('name');
    $("#unwatch").empty();
    $.ajax({
        url: "http://192.168.210.10:8000/get_favorite/",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function(data) {
            for (var i = 0; i < data.success.length; i++) {
                showWatchList(data.success[i]);
                console.log(data.success[i]);
            }
        },
        error: function(xhr, ajaxOptions, thrownError) {
            if (xhr.status == 200) {
                console.log(ajaxOptions);
            } else {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
    });
});

function hidebox() {
    $("#cat").animate({ left: '-300px' }, "slow");
    $("#emo").animate({ left: '-300px' }, "slow");
}

function clearbut(b) {
    $(b).animate({
        backgroundColor: "#F0F0F0",
        color: "#000000",
        height: 20,
        width: 40,
        marginLeft: 10,
    }, "1000");
}

function pressbut(b) {
    $(b).animate({
        backgroundColor: "#FFE375",
        color: "#ffffff",
        height: 75,
        width: 20,
        marginLeft: 30,
    }, "1000");
}

function showbottom(n) {
    $("#list").hide();
    $("#rec").hide();
    $("#rate").hide();
    $("#result").hide();
    $("#info").hide();
    $("#" + n).show("slow");
}


function searchRequest(searchTitle) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/search/movie?query=" + searchTitle + "&api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            console.log(response);
            $('#result .title').text("共 " + response.total_results + " 筆搜尋結果");
            for (i = 0; i < response.total_results; i++) {
                $(".result").append("<div class='col' onclick='moreInfo(" + response.results[i].id + ",0,0)'>" +
                    "<img src='https://image.tmdb.org/t/p/w154/" + response.results[i].poster_path + "' style='width:145px'>" +
                    "<p class='mtitle'>" + response.results[i].original_title + "</p>" +
                    "</div>");
            }
        },
    });
};

function showWatchList(id) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/movie/" + id + "?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            console.log(response);
            $("#unwatch.result").append("<div class='col' onclick='moreInfo(" + response.id + ",1,0)'>" +
                "<img src='https://image.tmdb.org/t/p/w154/" + response.poster_path + "' style='width:145px'>" +
                "<p class='mtitle'>" + response.original_title + "</p>" +
                "</div>");

        },
    });
};


function showRatedList(id, rated) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/movie/" + id + "?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            console.log(response);
            $("#rated.result").append("<div class='col' onclick='moreInfo(" + response.id + ",0," + rated + ")'>" +
                "<img src='https://image.tmdb.org/t/p/w154/" + response.poster_path + "' style='width:145px'>" +
                "<p class='mtitle'>" + response.original_title + "</p>" +
                "</div>");

        },
    });
};

function search(e) {
    e.preventDefault();
    var searchTitle = input.value;
    console.log(searchTitle)
    searchRequest(searchTitle);
    input.value = "";
    hidebox();
    clearbut("#m-cat");
    clearbut("#m-emo");
    clearbut("#m-rate");
    clearbut("#m-list");
    clearbut("#m-rec");
    nowbox = "result";
    showbottom(nowbox);
    $(".result").text("");
}


var form = document.querySelector("#search");
var input = document.querySelector('input[type="text"]');
form.addEventListener("submit", search);


function searchCat(cat, id) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/discover/movie?api_key=129d4541708a331707bc51ae50d8373c&sort_by=popularity.desc&include_adult=false&include_video=false&with_genres=" + id,
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            console.log(response);
            $('#result .title').text(" 共 " + response.total_results + " 部電影");
            for (i = 0; i < response.total_results; i++) {
                $(".result").append("<div class='col' onclick='moreInfo(" + response.results[i].id + ",0,0)'>" +
                    "<img src='https://image.tmdb.org/t/p/w154/" + response.results[i].poster_path + "' style='width:145px'>" +
                    "<p class='mtitle'>" + response.results[i].original_title + "</p>" +
                    "</div>");
            }

        },
    });
};

$("category").click(function() {
    var id, cat;
    id = $(this).children("id").text();
    cat = $(this).text();
    console.log(id);
    searchCat(cat, id);
    hidebox();
    clearbut("#m-cat");
    nowbox = "result";
    showbottom(nowbox);
    $("#" + nowbox).animate({ left: '120px' }, "slow");
    $("." + nowbox).animate({ width: '1130px' }, "slow");
    $(".result").text("");
})