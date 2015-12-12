function favoriteArt(artid) {
    var url = "/art/" + artid + "/favorite";

    if ($("#art-heart-"+artid).hasClass("favorited")) {
        // User has already favorited so return
        return;
    }

    $.ajax(url, {
        type: "POST",
        statusCode: {
            403: function() {
                showLoginModal();
            },
        },
    }).success(function(data) {
        if (data.status == "OK") {
            var icon = $("#art-heart-"+artid);
            icon.removeClass("notfavorited").removeClass("fa-heart-o").addClass("fa-heart").addClass("favorited");
            icon.attr("onclick", "unfavoriteArt("+artid+")");
            // Increment by 1
            var spanEle = icon.parent().find("span");
            var newNumber = Number(spanEle.text()) + 1;
            spanEle.text(newNumber);
        } else {
        }
    });
}

function unfavoriteArt(artid) {
    var url = "/art/" + artid + "/favorite";

    if ($("#art-heart-"+artid).hasClass("notfavorited")) {
        // User has already favorited so return
        return;
    }

    $.ajax(url, {
        type: "DELETE",
        statusCode: {
            403: function() {
                showLoginModal();
            },
        },
    }).success(function(data) {
        if (data.status == "OK") {
            var icon = $("#art-heart-"+artid);
            icon.removeClass("favorited").removeClass("fa-heart").addClass("fa-heart-o").addClass("notfavorited");
            icon.attr("onclick", "favoriteArt("+artid+")");
            // Decrement by 1
            var spanEle = icon.parent().find("span");
            var newNumber = Number(spanEle.text()) - 1;
            spanEle.text(newNumber);
        } else {
        }
    });
}

function deleteArt(artid) {
    if(confirm("Are you sure?")) {
        var url = "/art/" + artid;

        $.ajax(url, {
            type: "DELETE",
            statusCode: {
                403: function() {
                    showLoginModal();
                },
            },
        }).success(function(data) {
            if (data.status == "OK") {
                // Find the element and delete
                $("#art-col-" + artid).remove();
            } else {
            }
        });
   }
}

function validateEditArtForm() {
    var valid = true;
    var artTitle = $("#edit-art-form #art-title").val().trim();

    if(artTitle.length == 0) {
        $("#edit-art-form #art-title").parent().addClass("has-error");
        valid = false;
    } else {
        $("#edit-art-form #art-title").parent().removeClass("has-error");
    }

    return valid;
}

$(document).ready(function() {
});
