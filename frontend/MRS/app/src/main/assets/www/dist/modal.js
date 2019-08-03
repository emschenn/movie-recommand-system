var isinlist = 0;

function moreInfo(id, added, rated) {
    $('.modal').toggleClass('is-visible');
    $(".tooltiptext").hide();
    $(".modal-rate svg").hide('slow'),
        function() {

        };
    if (added == 1) {
        isinlist = 1;
        $(".m-button span").text("從清單中移除");
        $(".m-button>button").attr('data-value', '移除成功');
    } else {
        isinlist = 0;
        $(".m-button span").text("加入觀看清單");
        $(".m-button>button").attr('data-value', '添加成功');
    }
    if (rated > 0) {
        clearRate();
        setRate(rated);
    } else {
        clearRate();
    }
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/movie/" + id + "?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            d3rate(response.vote_average / 2);
            $(".modal id").text(id);
            $(".modal-header #title").text(response.original_title);
            $(".modal-header img ").attr("src", "https://image.tmdb.org/t/p/w780/" + response.backdrop_path);
            $(".modal-content #overview").text(response.overview);
            $(".modal-content .modal-info #year").text(response.release_date.slice(0, 4));
            $(".modal-content .modal-info #lang").text(response.original_language);

            var g = "";
            if (response.genres.length >= 2) {
                g = g + response.genres[0].name + ", ";
                g = g + response.genres[1].name;
            } else {
                g = g + response.genres[0].name;
            }
            console.log(g);
            $(".modal-content .modal-info #genres").text(g);
            console.log(response);

        },
    });
}

$('.modal-toggle').on('click', function(e) {
    $('.modal').toggleClass('is-visible');
    $(".tooltiptext").hide();
    if (!$('.modal').hasClass('is-visible')) {
        $(".modal-rate svg").hide('slow'),
            function() {
                $(".modal-rate svg").remove();
            };

        $(".more").animate({ width: '0vw' }, "slow", function() {
            $(".swipeimg").show();
            $(".more").hide();

        });
        $(".modal").animate({ left: '0vw' }, "slow");
    }
});
$('c.close').on('click', function(e) {
    $('.modal').toggleClass('is-visible');
    $(".tooltiptext").hide();
    if (!$('.modal').hasClass('is-visible')) {
        $(".modal-rate svg").hide('slow'),
            function() {
                $(".modal-rate svg").remove();
            };
    }
});

/* add to list */
$('.m-button').on('click', function(e) {
    $("button").attr("aria-expanded", "true");
    var id = $(this).parent().parent().parent().parent().children('id').text();
    setTimeout(function() {
        $("button").attr("aria-expanded", "false");
    }, 800);
    var json = {};
    //json["name"] = "1234";
    json['name'] = localStorage.getItem('name');

    json["tmdbId"] = id;
    console.log(json);
    if (isinlist == 1) {
        //remove
        console.log("remove");
        isinlist = 0;
        $(".m-button span").text("加入觀看清單");
        $(".m-button>button").attr('data-value', '移除成功');
        $.ajax({
            url: SERVER_URL + "remove_favorite/",
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(json),
            dataType: 'json',
            success: function(data) {

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
    } else {
        $.ajax({
            url: SERVER_URL + "update_favorite/",
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(json),
            dataType: 'json',
            success: function(data) {
                console.log("success");
                console.log(data);
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
        isinlist = 1;
        $(".m-button span").text("從清單中移除");
        $(".m-button>button").attr('data-value', '添加成功');
    }
});

/* rate */
$('#stars li').on('click', function() {
    var onStar = parseInt($(this).data('value'), 10); // The star currently selected
    var stars = $(this).parent().children('li.star');
    console.log(onStar);

    var id = $(this).parent().parent().parent().parent().children('id').text();
    clearRate();
    for (i = 0; i < onStar; i++) {
        $(stars[i]).addClass('selected');
        $(stars[i]).addClass('animated bounceIn');
    }
    var ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
    var json = {};
    //json["name"] = "1234";
    json['name'] = localStorage.getItem('name');

    json["rating"] = ratingValue;
    json["tmdbId"] = id;
    console.log(json);
    $.ajax({
        url: SERVER_URL + "update_rating/",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function(data) {
            console.log("success");
            console.log(data);
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
    $(function() {
        $(".tooltiptext").text(ratingValue + "顆星!");
        $(".tooltiptext").show();
        $('.tooltiptext').addClass('animated bounce');
        setTimeout(function() {
            //$('.tooltiptext').removeClass('bounce');
            $(".tooltiptext").hide();
        }, 950);
    });

});

function setRate(s) {
    var stars = $('#stars li').parent().children('li.star');
    var id = $(this).parent().parent().parent().parent().children('id').text();
    for (i = 0; i < s; i++) {
        $(stars[i]).addClass('selected');
        $(stars[i]).addClass('animated bounceIn');
    }
}

function clearRate() {
    var stars = $('#stars li').parent().children('li.star');
    for (i = 0; i < stars.length; i++) {
        $(stars[i]).removeClass('selected');
        $(stars[i]).removeClass('animated bounceIn');
    }
}

function d3rate(percent) {

    var duration = 1500,
        transition = 200,
        width = 130,
        height = 130;

    var dataset = {
            lower: calcPercent(0),
            upper: calcPercent(percent)
        },
        radius = Math.min(width, height) / 3,
        pie = d3.layout.pie().sort(null),
        format = d3.format(".1f");

    var arc = d3.svg.arc()
        .innerRadius(radius * .8)
        .outerRadius(radius);

    var svg = d3.select(".modal-rate").insert("svg", "#slider-vertical")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var path = svg.selectAll("path")
        .data(pie(dataset.lower))
        .enter().append("path")
        .attr("class", function(d, i) {
            return "color" + i
        })
        .attr("d", arc)
        .each(function(d) {
            this._current = d;
        });

    var text = svg.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", ".3em");

    var progress = 0;

    var timeout = setTimeout(function() {
        clearTimeout(timeout);
        path = path.data(pie(dataset.upper));
        path.transition().duration(duration).attrTween("d", function(a) {
            var i = d3.interpolate(this._current, a);
            var i2 = d3.interpolate(progress, percent)
            this._current = i(0);
            return function(t) {
                text.text(format(i2(t)));
                return arc(i(t));
            };
        });
    }, 200);

    function calcPercent(percent) {
        return [percent, 5 - percent];
    };
}

// for more info
var container = document.querySelector(".swipe");
var moreison = false;
container.addEventListener("touchstart", startTouch, false);
container.addEventListener("touchmove", moveTouch, false);
var initialX = null;
var initialY = null;

function startTouch(e) {
    initialX = e.touches[0].clientX;
    initialY = e.touches[0].clientY;
};

function moveTouch(e) {
    if (initialX === null) {
        return;
    }
    if (initialY === null) {
        return;
    }
    var currentX = e.touches[0].clientX;
    var currentY = e.touches[0].clientY;
    var diffX = initialX - currentX;
    var diffY = initialY - currentY;
    if (Math.abs(diffX) > Math.abs(diffY)) {
        // sliding horizontally
        if (diffX > 0) {
            // swiped left
            console.log("swiped left");
            moreison = false;
            $(".more").animate({ width: '0vw' }, "slow", function() {
                $(".swipeimg").show();
                $(".more").hide();

            });
            $(".modal").animate({ left: '0vw' }, "slow");
        } else {
            // swiped right
            var id = $(this).parent().parent().parent().children('.modal.is-visible').children('.modal-wrapper.modal-transition').children('id').text();
            console.log(id);
            console.log("swiped right");
            moreison = true;
            $(".swipeimg").hide();
            $(".more").show();
            $(".modal").animate({ left: '10vw' }, "slow");
            $(".more").animate({ width: '22vw' }, "slow");
            getmoreinfo();
        }
        initialX = null;
        initialY = null;
        e.preventDefault();
    };
}



function getmoreinfo() {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "https://api.themoviedb.org/3/trending/movie/week?api_key=129d4541708a331707bc51ae50d8373c",
        method: "GET",
        headers: {},
        data: "{}",
        success: function(response) {
            console.log(response);
            for (i = 0; i < 10; i++) {
                $(".more").append("<div class='movie' onclick='moreInfo(" + response.results[i].id + ",0,0)'>" +
                    "<div class='img'> <img src='https://image.tmdb.org/t/p/w154/" + response.results[i].poster_path + "' style='width: 200px;'> </div>" +
                    "<div class='title'>" + response.results[i].original_title + "</div>" +
                    "</div>");
            }
        },
    });
}