
function postComment(url, source) {
    console.log(url);
    var commentText =  $("#comment-text-area").val().trim();

    if(commentText == "") {
        $("#comment-error").text("Comment cannot be empty");
    } else {
        $("#comment-error").text("");
    }
    $.ajax(url, {
        type: "POST",
        data: {
            comment: commentText,
        },
        statusCode: {
            403: function() {
                showLoginModal();
            },
        },
    }).success(function(data) {
        $(".comment-form").append(data);
        mixpanel.track("Posted Comment", {
            "comment": commentText,
            "source": source,
        });
    });
}

function postArtComment(artid) {
    var url = "/art/" + artid + "/comment";
    postComment(url, "art");
}

function postBookComment(bookid) {
    var url = "/book/" + bookid + "/comment";
    postComment(url, "book");
}

function collapseComment() {
    var iconEle  = $(event.target);
    if (iconEle.hasClass("fa-plus-square-o")) {
        var firstHiddenEle = iconEle.parent().parent().parent().find(".comment-body")[0];
        $(firstHiddenEle).css("display", "");
    } else {
        var firstVisibleEle = iconEle.parent().parent().parent().find(".comment-body")[0];
        $(firstVisibleEle).css("display", "none");
    }

    $(event.target).toggleClass("fa-plus-square-o");
    $(event.target).toggleClass("fa-minus-square-o"); 
}

function createReplyForm() {
    var replyLink = $(event.target);
    var actionList = replyLink.parent().parent();

   var forms =  actionList.parent().find("form");

   for(var i =0; i < forms.length; i++) {
       forms[i].remove();
   }

   var form = '<form><div class="form-group"> <textarea class="form-control" placeholder="Reply..."></textarea></div><button type="button" class="btn btn-xs btn-default" onclick="replyToComment();">Submit</button><button type="button" class="btn btn-xs btn-default" onclick="cancelReply();">Cancel</button></form>';

    actionList.after(form);
}

function createEditForm() {
    createReplyForm();
    var form = $(event.target).parent().parent().parent().find("textarea");
    var text = $($(event.target).parent().parent().parent().find(".comment")[0]).text();
    var saveButton = $(event.target).parent().parent().parent().find("button").attr("onclick", "editComment();")
    form.text(text);
}

function cancelReply() {
    console.log("Cancel Reply");
    var formGroup = $(event.target).parent().remove();
}

function replyToComment() {
    var submitButton = $(event.target);
    var commentid = submitButton.closest(".comment-body").attr("commentid");
    var url = "/comment/" + commentid+ "/reply";
    var commentText = submitButton.parent().find("textarea").val();

    $.ajax(url, {
        type: "POST",
        data: {
            comment: commentText,
        },
        statusCode: {
            403: function() {
                showLoginModal();
            },
        },
    }).success(function(data) {
        submitButton.closest("form").replaceWith(data);
        mixpanel.track("Reply To Comment", {
            "comment": commentText,
        });
    });
}

function editComment() {
    var submitButton = $(event.target);
    var commentid = submitButton.closest(".comment-body").attr("commentid");
    var url = "/comment/" + commentid+ "/edit";
    var commentText = submitButton.parent().find("textarea").val();

    $.ajax(url, {
        type: "POST",
        data: {
            comment: commentText,
        },
        statusCode: {
            403: function() {
                showLoginModal();
            },
        },
    }).success(function(data) {
        // I was drinking when I wrote most of this
        $(submitButton.closest(".comment-body").find(".comment")[0]).text(commentText);
        $(submitButton.closest("form")[0]).remove();
    });
}

function deleteComment(commentid) {
    var deleteButton = $(event.target);
    if(confirm("Are you sure?")) {
        var url = "/comment/" + commentid;
        $.ajax(url, {
            type: "DELETE",
            statusCode: {
                403: function() {
                    showLoginModal();
                },
            },
        }).success(function(data) {
            console.log("Deleted");
            // Delete the comment from the DOM
            $(deleteButton.closest(".comment-body").find(".comment")[0]).text("[ deleted ]");
            $(deleteButton.closest(".comment-body").find("ul")[0]).remove();
            mixpanel.track("Delete Comment", {
                "commentid": commentid,
            });
        });
    }
}

function upvoteComment(commentid) {
    // Make sure user hasn't already upvoted this
    if ($(event.target).hasClass("text-success")) {
        return;
    }

    voteComment(commentid, "upvt");
    // Change the color
    $(event.target).addClass("text-success");
    $(event.target).closest("ul").find(".downvote").removeClass("text-danger");
    //Increment count by 1
    var upvoteCntEle = $(event.target).closest("ul").find(".upvote-cnt");
    var newCount = Number(upvoteCntEle.text()) + 1;
    upvoteCntEle.text(newCount);
}

function downvoteComment(commentid) {
    // Make sure user hasn't already upvoted this
    if ($(event.target).hasClass("text-danger")) {
        return;
    }
    voteComment(commentid, "dwnvt");
    $(event.target).addClass("text-danger");
    $(event.target).closest("ul").find(".upvote").removeClass("text-success");

    var upvoteCntEle = $(event.target).closest("ul").find(".upvote-cnt");
    var newCount = Number(upvoteCntEle.text()) - 1;
    upvoteCntEle.text(newCount);
}

function voteComment(commentid, votetypcd) {
    console.log("vote: " + commentid + " type: " + votetypcd);
    var url = "/comment/"+commentid+"/vote";

    $.ajax(url, {
        type: "POST",
        data: {
            upvotetype: votetypcd,
        },
        statusCode: {
            403: function() {
                showLoginModal();
            },
        },
    }).success(function(data) {
        console.log("Successfully voted for comment");
        if (votetypcd == "upvt") {
            console.log("upvote");
            $("#upvote-" + commentid).css("color", "green");
            $("#downvote-" + commentid).css("color", "");
        } else {
            $("#upvote-" + commentid).css("color", "");
            $("#downvote-" + commentid).css("color", "red");
        }
    });
}

