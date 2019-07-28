$(document).ready(function() {
    $(".head").hide();
    $(".button").hide();
    $(".input.one").hide();
    $(".input.two").hide();
    $(".input.three").hide();

    $(".head").transition('slide down', 900, function() {
        $(".button").show('slow');
        $(".input.one").show('slow');

    });
});

var input = document.querySelector('input[type="text"]');
var page = 0,
    totalpage = 0,
    gitem = 0,
    finish = 0,
    now = 0;
var glist = [],
    mlist = [];
var json = {};

$(".button").click(function() {
    if (finish == 1) {
        json["like"] = mlist;
        console.log(json);
        $(".loader").removeClass("disabled");
        $(".loader").addClass("active");

        $.ajax({
            url: "http://192.168.210.22:8000/new_user_list/",
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(json),
            dataType: 'json',
            success: function(data) {
                console.log("success");
                console.log(data);

                document.location.href = "index.html";
            },
            error: function(xhr, ajaxOptions, thrownError) {
                if (xhr.status == 200) {
                    alert(ajaxOptions);
                } else {
                    alert(xhr.status);
                    alert(thrownError);
                }
            }
        });
    }

    page++;
    if (page == 1) {
        $(".head").animate({ height: '150px' }, "slow");
        $(".head__title").text("", "slow");
        var name = input.value;
        json["name"] = name;
        $(".head__content").text("請勾選出所有感興趣的電影類別", "slow");
        $(".input.one").hide('slow');
        $(".input.two").show('slow');
        localStorage.setItem('name', name);

    } else if (page == 2) {
        json["genres"] = glist;
        now = 1;
        $(".head__content").text("勾選出所有喜歡/有興趣/看過的電影", "slow");
        $(".input.two").hide('slow');
        totalpage = page + json.genres.length - 1;
        $(".input.three").show('slow');
        getmlist(json.genres[gitem]);
        gitem++;
        if (json.genres.length == 1) {
            $(".button").text("完成");
            finish = 1;
        }
    } else if (page > 2 && page < totalpage) {
        $(".column").find(".box img").removeClass("click");
        getmlist(json.genres[gitem]);
        gitem++;
    } else if (page == totalpage) {
        $(".column").find(".box img").removeClass("click");
        getmlist(json.genres[gitem]);
        gitem++;

        $(".button").text("完成");
        finish = 1;
    }
});
$(".column").click(function() {
    if (now == 0) {
        var g = $(this).find("p").html();
        if (glist.indexOf(g) == -1)
            glist.push(g);
        else
            glist.splice(glist.indexOf(g), 1);
        console.log(glist);
    } else {
        var g = $(this).find("id").html();
        if (mlist.indexOf(g) == -1)
            mlist.push(g);
        else
            mlist.splice(mlist.indexOf(g), 1);
        console.log(mlist);
    }
    $(this).find(".box img").toggleClass("click");
});

function init(val) {
    //  alert(val);
    json = JSON.parse(val);
    $(".head__content").text(val.pic1);
};

function getmlist(gen) {
    var list;
    switch (gen) {
        case "Action":
            list = [19995, 140607, 135397, 24428, 168259];
            movie(list);
            break;
        case "Adventure":
            list = [12445, 68721, 38356, 122, 12155];
            movie(list);
            break;
        case "Animation":
            list = [109445, 324852, 10193, 129, 12599];
            movie(list);
            break;
        case "Comedy":
            list = [72105, 693, 18785, 211672, 8355];
            movie(list);
            break;
        case "Crime":
            list = [49026, 206647, 10764, 10528, 161];
            movie(list);
            break;
        case "Document":
            list = [240417, 1667, 195012, 1777, 16290];
            movie(list);
            break;
        case "Drama":
            list = [597, 8587, 452557, 50620, 119450];
            movie(list);
            break;
        case "Family":
            list = [10193, 12155, 278927, 672, 400650];
            movie(list);
            break;
        case "Fantasy":
            list = [259316, 411, 8871, 284054, 1865];
            movie(list);
            break;
        case "History":
            list = [652, 857, 616, 676, 449927];
            movie(list);
            break;
        case "Horror":
            list = [346364, 72190, 578, 9740, 259693];
            movie(list);
            break;
        case "Musical":
            list = [11631, 136799, 254470, 15121, 11887];
            movie(list);
            break;
        case "Romance":
            list = [24021, 13, 216015, 150689, 313369];
            movie(list);
            break;
        case "Sci-Fi":
            list = [37686, 181808, 68721, 38356, 49047];
            movie(list);
            break;
        case "War":
            list = [460555, 190859, 374720, 676, 1271];
            movie(list);
            break;
    }
}

function movie(id) {
    for (var i = 0; i < id.length; i++) {
        var box = $(".input.three").find(".grid").find(".column").eq(i);
        getMovieInfo(id[i], box);
    }
}

function getMovieInfo(id, box) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/movie/" + id + "?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            box.find("p").text(response.title);
            box.find("id").text(id);
            box.find("img").attr("src", "https://image.tmdb.org/t/p/w200/" + response.poster_path);
        },
    });
}