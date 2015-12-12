
function showAddMediaModel(mode) {
    console.log("Showing modal");
    if (userLoggedIn) {
        $('#add-scene-modal').modal('show');
    } else {
        showLoginModal();
    }
}

function hideAllBookContentRows() {
    $(".book-scene-row").css("display", "none");
    $(".book-character-row").css("display", "none");
    $(".book-map-row").css("display", "none");
    $(".book-art-row").css("display", "none");
    $(".book-discussion-row").css("display", "none");

    // Reset tabs
    $("#book-scene-tab").removeClass('active');
    $("#book-art-tab").removeClass('active');
    $("#book-character-tab").removeClass('active');
    $("#book-map-tab").removeClass('active');
    $("#book-discussion-tab").removeClass('active');
}

function favoriteBook(bookid) {
    var url = "/book/" + bookid + "/favorite";

    if ($("#book-heart-"+bookid).hasClass("favorited")) {
        // User has already favorited so return
        return;
    }


    $.ajax(url, {
        type: "POST",
        statusCode: {
            403: function() {
                mixpanel.track("Anonymous User Favorited Book", {
                    bookid: bookid,
                });
                showLoginModal();
            },
        },
    }).success(function(data) {
        if (data.status == "OK") {
            var icon = $("#book-heart-"+bookid);
            icon.removeClass("notfavorited").removeClass("fa-heart-o").addClass("fa-heart").addClass("favorited");
            icon.attr("onclick", "unfavoriteBook("+bookid+")");

            // Increment by 1
            var spanEle = icon.parent().find("span");
            var newNumber = Number(spanEle.text()) + 1;
            spanEle.text(newNumber);
        } else {
        }
        mixpanel.track("Logged In User Favorited Book", {
            bookid: bookid,
        });
    });
}

function unfavoriteBook(bookid) {
    var url = "/book/" + bookid + "/favorite";

    if ($("#book-heart-"+bookid).hasClass("notfavorited")) {
        // User has already favorited so return
        return;
    }

    $.ajax(url, {
        type: "DELETE",
        statusCode: {
            403: function() {
                showLoginModal();
                mixpanel.track("Anonymous User UnFavorited Book", {
                    bookid: bookid,
                });
            },
        },
    }).success(function(data) {
        if (data.status == "OK") {
            var icon = $("#book-heart-"+bookid);
            icon.removeClass("favorited").removeClass("fa-heart").addClass("fa-heart-o").addClass("notfavorited");
            icon.attr("onclick", "favoriteBook("+bookid+")");

            // Decrement by 1
            var spanEle = icon.parent().find("span");
            var newNumber = Number(spanEle.text()) - 1;
            spanEle.text(newNumber);
        } else {
        }
        mixpanel.track("Logged In User UnFavorited Book", {
            bookid: bookid,
        });
    });
}


$(document).ready(function() {
    // Setup the login/create profile links

    //
    // Book Tabs (Scene, Character, Art, Comments
    //
    if (typeof(bookid) != "undefined") {
        var trackingInfo = {
            "bookid": bookid,
            "bookTitle": bookTitleUrl,
        }
    } else {
        var trackingInfo = {};
    }

    $("#book-scene-tab").click(function() {
        //Set the profile form visible
        hideAllBookContentRows();
        $(".book-scene-row").css("display", "");
        $("#book-scene-tab").addClass('active');
        mixpanel.track("Book Scene Tab Shown", trackingInfo);
    });

    $("#book-character-tab").click(function() {
        //Set the profile form visible
        hideAllBookContentRows();
        $(".book-character-row").css("display", "");
        $("#book-character-tab").addClass('active');
        mixpanel.track("Book Character Tab Shown", trackingInfo);
    });

    $("#book-map-tab").click(function() {
        //Set the profile form visible
        hideAllBookContentRows();
        $(".book-map-row").css("display", "");
        $("#book-map-tab").addClass('active');
        mixpanel.track("Book Map Tab Shown", trackingInfo);
    });

    $("#book-art-tab").click(function() {
        //Set the profile form visible
        hideAllBookContentRows();
        $(".book-art-row").css("display", "");
        $("#book-art-tab").addClass('active');
        mixpanel.track("Book Art Tab Shown", trackingInfo);
    });

    $("#book-discussion-tab").click(function() {
        //Set the profile form visible
        hideAllBookContentRows();
        $(".book-discussion-row").css("display", "");
        $("#book-discussion-tab").addClass('active');
        mixpanel.track("Book Discussion Tab Shown", trackingInfo);
    });
});
