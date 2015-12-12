function favoriteScene(sceneid) {
    var url = "/scene/" + sceneid + "/favorite";

    if ($("#scene-heart-"+sceneid).hasClass("favorited")) {
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
            var icon = $("#scene-heart-"+sceneid);
            icon.removeClass("notfavorited").removeClass("fa-heart-o").addClass("fa-heart").addClass("favorited");
            icon.attr("onclick", "unfavoriteScene("+sceneid+")");

            // Increment by 1
            var spanEle = icon.parent().find("span");
            var newNumber = Number(spanEle.text()) + 1;
            spanEle.text(newNumber);
        } else {
        }
    });
}

function unfavoriteScene(sceneid) {
    var url = "/scene/" + sceneid + "/favorite";

    if ($("#scene-heart-"+sceneid).hasClass("notfavorited")) {
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
            var icon = $("#scene-heart-"+sceneid);
            icon.removeClass("favorited").removeClass("fa-heart").addClass("fa-heart-o").addClass("notfavorited");
            icon.attr("onclick", "favoriteScene("+sceneid+")");

            // Decrement by 1
            var spanEle = icon.parent().find("span");
            var newNumber = Number(spanEle.text()) - 1;
            spanEle.text(newNumber);
        } else {
        }
    });
}

function hideAllSceneRows() {
    $(".scene-art-row").css("display", "none");
    $(".scene-discussion-row").css("display", "none");

    // Reset tabs
    $("#scene-art-tab").removeClass('active');
    $("#scene-discussion-tab").removeClass('active');

}

function deleteScene(sceneid) {
    if(confirm("Are you sure?")) {
        var url = "/scene/" + sceneid;

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
                $("#scene-col-" + sceneid).remove();
            } else {
            }
        });
   }
}

function validateEditSceneForm() {
    return false;
}

$(document).ready(function() {
    $("#scene-art-tab").click(function() {
        //Set the profile form visible
        hideAllSceneRows();
        $(".scene-art-row").css("display", "");
        $("#scene-art-tab").addClass('active');
    });

    $("#scene-discussion-tab").click(function() {
        //Set the profile form visible
        hideAllSceneRows();
        $(".scene-discussion-row").css("display", "");
        $("#scene-discussion-tab").addClass('active');
    });
});
