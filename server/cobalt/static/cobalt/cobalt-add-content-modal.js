var selectedSceneType = null;
var selectedScene = null;
var cachedScenes = null; //Object where sceneid : scene
var currentModal = null; // Should be either art or scene
var sceneTypes = {
    gnrc: "Scene",
    char: "Character",
    map: "Map",
};

var supportedTypes = [
    "image/jpeg",
    "image/png",
];

function changeModalContentToBookSelection() {
    showSelectBookModal();
    if(currentModal == "art") {
    } else { 
        hideAddSceneModal();
    }
}

function changeModalContentToAddScene() {
    hideSelectBookModal();
    showAddSceneModal();
}

function showSelectBookModal() {
    if(currentModal == "art") {
        $("#add-art-modal #book-modal-body").css("display", "");
        hideArtForm();
        hideChooseSceneType();
        hideChooseScene();
    } else {
        $("#add-scene-modal #book-modal-header-content").css("display", "");
        $("#add-scene-modal #book-modal-body").css("display", "");
        $("#add-scene-modal #select-book-next-button").css("display", "");
    }
}

function hideSelectBookModal() {
    $("#book-modal-header-content").css("display", "none");
    $("#book-modal-body").css("display", "none");
    $("#select-book-next-button").css("display", "none");
}

function showAddSceneModal() {
    $("#scene-modal-header-conent").css("display","");
    $("#scene-modal-body").css("display", "");
    $("#add-scene-save-button").css("display", "");
}

function triggerAddSceneModal() {
    if (userLoggedIn) {
        $('#add-scene-modal').modal('show');
        currentModal = "scene";
        mixpanel.track("Trigger Add Scene Modal",{
            bookid: bookid,
            bookTitleUrl: bookTitleUrl,
        });
    } else {
        showLoginModal();
    }
}

function triggerAddArtModal() {
    if (userLoggedIn) {
        $('#add-art-modal').modal('show');
        currentModal = "art";
        mixpanel.track("Trigger Add Art Modal",{
            bookid: bookid,
            bookTitleUrl: bookTitleUrl,
        });
    } else {
        showLoginModal();
    }
}

function hideAddSceneModal() {
    console.log("Hiding add scene modal");
    $("#scene-modal-header-conent").css("display","none");
    $("#scene-modal-body").css("display", "none");
    $("#add-scene-save-button").css("display", "none");
}

function modalSearchBook() {
    if(currentModal == "art") {
        var data = $("#add-art-modal #book-search-input").val();
    } else {
        var data = $("#add-scene-modal #book-search-input").val();
    }

    var url="/book/search?q=" + data;

    // Validate input
    if (data.length == 0) {
        if(currentModal == "art") {
            $("#add-art-modal #book-search-error span").text("Please enter a some words");
        } else {
            $("#add-scene-modal #book-search-error span").text("Please enter a some words");
        }
        return;
    } else {
        if(currentModal == "art") {
            $("#add-art-modal #book-search-error span").text("");
        } else {
            $("#add-scene-modal #book-search-error span").text("");
        }
    }

    // Set loading and clear current search results
    var spinner = '<span id="loading-spinner" class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span>';
    if(currentModal == "art") {
        $("#add-art-modal #search-btn").prepend(spinner);
        $("#add-art-modal #search-btn").attr("disabled","true");
    } else {
        $("#add-scene-modal #search-btn").prepend(spinner);
        $("#add-scene-modal #search-btn").attr("disabled","true");
    }
    $(".list-group-item").remove();

    $.ajax(url)
        .success(function(data) {
            if (data.status == "OK") {
                if(currentModal == "art") {
                    $("#add-art-modal #book-search-error span").text("");
                    var resultsGroup = $("#add-art-modal #book-search-results-group");
                } else {
                    $("#add-scene-modal #book-search-error span").text("");
                    var resultsGroup = $("#add-scene-modal #book-search-results-group");
                }

                // Add books to div
                for(var i=0; i < data.results.length; i++) {
                    var book = data.results[i];
                    if(currentModal == "art") {
                        var bookurl = "/book/" + book.title_url+"?addart=true";
                    } else {
                        var bookurl = "/book/" + book.title_url+"?addscene=true";
                    }
                    var newEle = '<a href="'+bookurl+'" class="list-group-item"><h4 class="list-group-item-heading">'+book.title+'</h4><p class="list-group-item-text">'+book.short_summary+'</p></a>';
                    resultsGroup.append(newEle);
                }
            } else {
                console.log("Error searching");
                console.log(data);
                if(currentModal == "art") {
                    $("#add-art-modal #book-search-error span").text(data.message);
                } else {
                    $("#add-scene-modal #book-search-error span").text(data.message);
                }
            }
        })
        .error(function() {
            if(currentModal == "art") {
                $("#add-art-modal #book-search-error span").text("There was an error searching. Please try again in a little bit.");
            } else {
                $("#add-scene-modal #book-search-error span").text("There was an error searching. Please try again in a little bit.");
            }
        })
        .always(function() {
            if(currentModal == "art") {
                $("#add-art-modal #loading-spinner").remove();
                $("#add-art-modal #search-btn").removeAttr("disabled");
            } else {
                $("#add-scene-modal #loading-spinner").remove();
                $("#add-scene-modal #search-btn").removeAttr("disabled");
            }
        });
}

function createScene() {
    if (!sceneModalFormValid()) { return; }

    var title =$("#scene-title").val();
    var startPage = $("#start-page").val();
    var endPage = $("#end-page").val();
    var text = $("#scene-text").val();
    var nsfw = $("#scene-nsfw").is(":checked");
    var sceneType = $("#scene-type").val();

    var url = "/book/" + bookTitleUrl + "/scene";

    $.ajax(url, {
        type: "POST",
        data: {
            title: title,
            startPage: startPage,
            endPage: endPage,
            text: text,
            nsfw: nsfw,
            sceneType: sceneType,
        },
    }).success(function(data) {
        if (data.status == "OK") {
            // Redirect to the new scene page
            window.location.replace(data.newSceneUrl);
        } else {
            setLoginModalError(data.message);
        }
        mixpanel.track("Create Scene", {
            sceneid: data.sceneid,
            scenetype: sceneType,
        });
    });

    console.log(url);
}

function createArt() {
    var url = "/book/" + bookTitleUrl + "/art";

    $('#add-art-form').fileupload({
        dataType: 'json',
        done: function (e, data) {
            console.log("Done uploading file");
        },
    });
}

function sceneModalFormValid() {
    console.log("Validate");
    var valid = true;

    var title =$("#scene-title").val().trim();
    var startPage = $("#start-page").val().trim();
    var endPage = $("#end-page").val().trim();
    var text = $("#scene-text").val().trim();
    var nsfw = $("#scene-nsfw").is(":checked");

    // Title and text are required
    if (title.length == 0) {
        $("#scene-title").parent().addClass("has-error");
        valid = false;
    } else {
        $("#scene-title").parent().removeClass("has-error");
    }

    //xor
    if(startPage.length == 0 && endPage.length > 0) {
        $("#start-page").parent().parent().prepend('<label class="control-label text-danger" style="margin-left:15px;" id="startPageError">Please enter "start page" also</label>');
    } else if (startPage.length > 0 && endPage.length == 0) {
        $("#start-page").parent().parent().prepend('<label class="control-label text-danger" style="margin-left:15px;" id="startPageError">Please enter "end page" also</label>');
    } else {
        $("#start-page").parent().removeClass("has-error");
        $("#end-page").parent().removeClass("has-error");
        $("#startPageError").remove();
    }

    var sceneType = $("#scene-type").val();

    // For now only start/end page required
    if (sceneType == null) {
        valid = false;
        $("#scene-type").parent().addClass("has-error");
    } else {
        $("#scene-type").parent().removeClass("has-error");
    }

    if (sceneType == "gnrc") {
        if(startPage.length == ""){
            $("#start-page").parent().addClass("has-error");
            valid = false;
        } else {
            $("#start-page").parent().removeClass("has-error");
        }

        if(endPage.length == ""){
            $("#end-page").parent().addClass("has-error");
            valid = false;
        } else {
            $("#end-page").parent().removeClass("has-error");
        }

        if(startPage.length > 0 && endPage.length > 0){
            if(Number(startPage) > Number(endPage)) {
                $("#start-page").parent().addClass("has-error");
                $("#end-page").parent().addClass("has-error");
                $("#start-page").parent().parent().prepend('<label class="control-label text-danger" style="margin-left:15px;" id="startPageError">Start page must come befoe end page</label>');
                valid = false;
            } else {
                $("#start-page").parent().removeClass("has-error");
                $("#end-page").parent().removeClass("has-error");
                $("#startPageError").remove();
            }
        }

        if(text.length == "") {
            $("#scene-text").parent().addClass("has-error");
        } else {
            $("#scene-text").parent().removeClass("has-error");
        }
    }
    
    return valid;
}

function clearModalErrors() {
    $("#scene-title").parent().removeClass("has-error");
    $("#start-page").parent().removeClass("has-error");
    $("#end-page").parent().removeClass("has-error");
    $("#scene-text").parent().removeClass("has-error");
}

function showArtForm() {
    $("#add-art-form").css('display','');
    $("#add-art-buttons").css('display','');
    hideChooseSceneType();
    hideChooseScene();
    mixpanel.track("User Shown Add Art Modal");
}

function hideArtForm() {
    $("#add-art-form").css('display','none');
    $("#add-art-buttons").css('display','none');
}

function hideChooseScene() {
    $("#choose-scene").css("display","none");
    $("#choose-scene-buttons").css("display","none");
    $("#select-scene-next-button").attr("disabled", "true");
}

function showChooseScene() {
    $("#choose-scene").css("display","");
    $("#choose-scene-buttons").css("display","");
    hideArtForm();
}

function showChooseSceneType() {
    $("#choose-scene-type").css("display","");
}

function hideChooseSceneType() {
    $("#choose-scene-type").css("display","none");
}

function goBackFromAddArtModal() {
    if(selectedSceneType) {
        $("#select-scene-next-button").removeAttr("disabled");
        showChooseScene();
    } else {
        resetArtForm();
    }
}

function resetSceneForm() {
    $("#scene-modal-header-conent").css("display","");
    $("#scene-modal-body").css("display", "");
    $("#add-scene-save-button").css("display", "");

    $("#add-scene-modal #book-modal-header-content").css("display", "none");
    $("#add-scene-modal #book-modal-body").css("display", "none");
    $("#add-scene-modal #select-book-next-button").css("display", "none");
}

function resetArtForm() {
    hideArtForm();
    hideChooseScene();
    showChooseSceneType();
    hideArtBookSelectionModal();
    selectedSceneType = null;
    selectedScene = null;
}

function hideArtBookSelectionModal() {
    $("#add-art-modal #book-modal-body").css("display", "none");
}

function showSelectScene(scenetype) {
    selectedSceneType = scenetype;
    showChooseScene();
    hideChooseSceneType();
    loadScenesForBook(scenetype);
    mixpanel.track("User Selected Scene Type", {
        sceneType: scenetype,
    });
}

function setSelectedScene(sceneid) {
    selectedScene = cachedScenes[sceneid];
    $(".list-group-item.active").removeClass("active");
    $(event.target).closest(".list-group-item").addClass("active");
    $("#select-scene-next-button").removeAttr("disabled");
}

function loadScenesForBook(scenetype) {
    console.log("Loading scenens for book with id: " + bookid);
    $(".list-group-item").remove();
    $(".no-book-scene").remove();

    var url = "/book/"+bookTitleUrl+"/scene?scenetypcd=" + scenetype;
    $.ajax(url, {
        type: "GET",
        contentType: "application/json",
    }).success(function(data) {
        if (data.status == "OK") {
            // Redirect to the new scene page
            cachedScenes = {};
            var resultsGroup = $("#book-scene-results-group");
            if(data.scenes.length > 0) {
                // Add scenes to div
                for(var i=0; i < data.scenes.length; i++) {
                    var scene = data.scenes[i];
                    cachedScenes[scene.id] = scene;

                    var newEle = '<a href="javascript:;" class="list-group-item" onclick="setSelectedScene('+scene.id+');"><h4 class="list-group-item-heading">'+scene.title+'</h4><p class="list-group-item-text">'+scene.text+'</p></a>';
                    resultsGroup.append(newEle);
                }
            } else {
                //Display no content and disabled next button
                var addSceneButton = '<button type="button" class="add-scene-button btn btn-success btn-sm" onclick="switchToAddSceneModal();">Add '+sceneTypes[selectedSceneType]+'</button>';
                var info = '<div class="paper paper-blue paper-small no-book-scene">There are no '+sceneTypes[selectedSceneType]+'s. Be the first! ' + addSceneButton+'</div>';
                resultsGroup.append(info);
            }
        } else {
            $("#book-scene-error span").text("Unable to load scenes for book at this time");
        }
    });
}

function switchToAddSceneModal() {
    $('#add-art-modal').modal('hide');
    $('#add-scene-modal').modal('show');
}

$(document).ready(function() {
    // Remove add scene button from form
    $(".modal-body #add-scene-form #add-scene-form-button").remove();

    $('#add-art-link').click(function(){
        triggerAddArtModal();
     });


    $("#scene-type").change(function(data) {
        clearModalErrors();
        var sceneType = $(event.target).val();
        if (sceneType == "char") {
            $("#start-page").attr("placeholder", "Start Page (Optional)");
            $("#end-page").attr("placeholder", "End Page (Optional)");
            $("#scene-title").attr("placeholder", "Character Name");
            $("#scene-text").attr("placeholder", "(Optional)");
        } else if (sceneType == "map"){
            $("#start-page").attr("placeholder", "Start Page (Optional)");
            $("#end-page").attr("placeholder", "End Page (Optional)");
            $("#scene-title").attr("placeholder", "Map/Place Name");
            $("#scene-text").attr("placeholder", "(Optional)");
        } else {
            // Assume it's general scene
            $("#start-page").attr("placeholder", "Start Page");
            $("#end-page").attr("placeholder", "End Page");
            $("#scene-title").attr("placeholder", "Scene Name");
            $("#scene-text").attr("placeholder", "");
        }
    });

    // Launch the add scene modal
    if(window.location.href.indexOf("addscene=true") > 1) {
        triggerAddSceneModal();
    } else if (window.location.href.indexOf("addart=true") > 1) {
        triggerAddArtModal();
    }

    $('#add-scene-link').click(function(){
        currentModal = "scene";
        var id = $(this).attr('id');
        showAddMediaModel(id);
     });


    // Register for events
    $('#add-art-modal').on('hidden.bs.modal', function (e) {
        resetArtForm();
     });

    $('#add-scene-modal').on('hidden.bs.modal', function (e) {
        resetSceneForm();
     });

function addArtFormValid() {
    var valid = true;
    var artTitle = $("#art-title").val().trim();

    if ($("#art-type").val() == null) {
        valid = false;
        $("#art-type").parent().addClass("has-error");
    } else {
        $("#art-type").parent().removeClass("has-error");
    }

    if(artTitle.length == 0) {
        $("#art-title").parent().addClass("has-error");
        valid = false;
    } else {
        $("#art-title").parent().removeClass("has-error");
    }

    return valid;
}

$('#add-art-form').fileupload({
  // This function is called when a file is added to the queue
  add: function (e, data) {
    if ($.inArray(data.files[0].type, supportedTypes) == -1) {
        // Add the HTML to the UL element
        var ele = '<div class="alert alert-danger file-alert">Unsupported file type</div>';
        data.context = $("#file-list").html(ele);
        return;
    } else {
        // Append the file name and file size
        var ele = '<div class="alert alert-success file-alert"><i class="fa fa-file-image-o"></i> ' + data.files[0].name + '</div>';
        data.context = $("#file-list").html(ele);
    }

    // Automatically upload the file once it is added to the queue
    $("#add-art-save-button").click(function() {
        if(!addArtFormValid()) { 
            return ;
        } else if(selectedScene != null) {
            var inputEle = '<input type="hidden" name="sceneid" value="'+selectedScene.id+'"/>';
            $("#add-art-form").append(inputEle);
        }

        // Show loading
        var spinner = '<span id="loading-spinner" class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span>';
        $("#add-art-save-button").prepend(spinner);
        $("#add-art-save-button").attr("disabled","true");

        data.submit();
        mixpanel.track("Add Art Form Completed", { 
            bookid: bookid,
            bookTitleUrl: bookTitleUrl,
        });
    });
    $("#add-art-save-button").removeAttr("disabled");
  },
  error: function(data) {
    if(data.responseText.indexOf("Unsupported content") > -1) {
        var errorSpan = '<span class="text-danger">Unsupported content type for image</span>';
        mixpanel.track("Unsupported Content Type", {
            error: data,
        });
    } else if (data.responseText.indexOf("Title cannot be empty") > -1) {
        var errorSpan = '<span class="text-danger">Art title cannot be empty</span>';
    } else if (data.responseText.indexOf("greater than") > -1) {
        var errorSpan = '<span class="text-danger">Image cannot be larger than 25MB</span>';
    } else {
        var errorSpan = '<span class="text-danger">Error processing form. Please try again in a little bit</span>';
    }
    $("#art-modal-body").append(errorSpan);
    // Remove loading
    $("#loading-spinner").remove();
    $("#add-art-save-button").removeAttr("disabled");
  },
  done: function(data, response) {
     var data = response.response().result;
     window.location.replace(data.artURL);
  },
});

//Helper function for calculation of progress
function formatFileSize(bytes) {
    if (typeof bytes !== 'number') {
        return '';
    } else if (bytes >= 1000000000) {
        return (bytes / 1000000000).toFixed(2) + ' GB';
    } else if (bytes >= 1000000) {
        return (bytes / 1000000).toFixed(2) + ' MB';
    } else {
        return (bytes / 1000).toFixed(2) + ' KB';
    }
}

});
