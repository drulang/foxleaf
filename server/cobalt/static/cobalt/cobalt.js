

function showLoginModal(mode) {
    console.log("Showing modal");

    if(mode == "signupLink") {
        mixpanel.track("Signup Modal Shown");
        switchLoginModalToCreateProfileMode();
    } else {
        mixpanel.track("Login Modal Shown");
        switchLoginModalToLoginMode();
    }
    $('#loginModal').modal('show');
}

function switchLoginModalToCreateProfileMode() {
    console.log("Switching modes");
    $("#email-form-group").css("display","");
    $("#confirm-password-form-group").css("display","");
    $("#create-profile-msg").css("display", "none");
    $("#login-profile-msg").css("display", "");

    // Change button
    $("#login-button").css("display", "none");
    $("#create-button").css("display", "");

    //Change Title
    $("#login-modal-title").text("Create Profile");
    setLoginModalError(""); // Clear error
}

function switchLoginModalToLoginMode() {
    $("#email-form-group").css("display","none");
    $("#confirm-password-form-group").css("display","none");
    $("#create-profile-msg").css("display", "");
    $("#login-profile-msg").css("display", "none");

    // Change button
    $("#login-button").css("display", "");
    $("#create-button").css("display", "none");

    //Change Title
    $("#login-modal-title").text("Login");
    setLoginModalError(""); // Clear error

    ////////////
    //
    // Remove these lines for live
    $("#username").css("display", "");
    $("#password").css("display", "");
    //
    ///////////
}

function login() {
    console.log("Logging in");
    var username = $("#username").val();
    var password = $("#password").val();
    
    var url="/weblogin/";

    if(!userCredentialsValid(username, password)) {
        return;
    }

    $.ajax(url, {
        type: "POST",
        data: {
            username: username,
            password: password,
        },
    }).success(function(data) {
        console.log("DONE: " + data);
        if (data.status == "OK") {
            $('#loginModal').modal('hide');
            // Show the profile navbar
            $("#profile-navbar-item").removeClass("hidden");
            $(".user-points").removeClass("hidden");
            $(".user-badges").removeClass("hidden");
 
            // Set points
             $(".user-points").find("span").text(data.points + " ");
             $(".user-badges").find("span").text(data.badges + " ");

            $("#login-navbar-item").addClass("hidden");
            $(".user-profile-img").attr("src","/userprofileimage/" + data.userid)
            setLoginModalError(""); // Clear error
            userLoggedIn = true;

            mixpanel.identify(username);
        } else {
            setLoginModalError(data.message);
        }
    });
}

function userCredentialsValid(username, password) {
    setLoginModalError("");

    var valid = true;

    // Check Username
    if (username.length == 0) {
        setFormGroupIdWithError("username-form-group", "Required");
        valid = false;
    } else {
        removeFormGroupIdError("username-form-group");
    }
    
    // Check Password
    if (password.length == 0) {
        setFormGroupIdWithError("password-form-group", "Required");
        valid = false;
    } else {
        removeFormGroupIdError("password-form-group");
    }

    return valid;
}

function userProfileValid(username, email, password, confirmPassword) {
    var valid = userCredentialsValid(username, password);

    // Check Confirm Password
    if (confirmPassword.length == 0) {
        setFormGroupIdWithError("confirm-password-form-group", "Required");
        valid = false;
    } else if (password != confirmPassword) {
        setFormGroupIdWithError("confirm-password-form-group", "Does not match password");
        valid = false;
    }
    else {
        removeFormGroupIdError("confirm-password-form-group");
    }

    // Check Email
    if (email.length == 0) {
        setFormGroupIdWithError("email-form-group", "Required");
        valid = false;
    } else if (!validateEmail(email)) {
        valid = false;
        setFormGroupIdWithError("email-form-group", "Invalid email");
    }

    return valid;
}

function setLoginModalError(message) {
    $("#login-error").text(message);
}

function setFormGroupIdWithError(inputid, message) {
    var inputEle = $("#" + inputid);
    inputEle.addClass("has-error");

    var labelEle = inputEle.find("label");
    if(message) {
        if(labelEle.length == 0) { // Was not able to find the ele
            var spanEle = '<label class="control-label" for="inputError2">'+message+'</label>';
            inputEle.prepend(spanEle);
        } else {
            labelEle.text(message);
        }
    }
}

function removeFormGroupIdError(inputid) {
    var inputEle = $("#" + inputid);
    inputEle.removeClass("has-error");
    inputEle.find("label").remove();
}

function createProfile() {
    var username = $("#username").val();
    var password = $("#password").val();
    var email = $("#email").val();
    var confirmPassword = $("#confirm-password").val();

    if(!userProfileValid(username, email, password, confirmPassword)) {
        return;
    }

    var url = "/createprofile/";
    $.ajax(url, {
        type: "POST",
        data: {
            username: username,
            password: password,
            email: email,
        },
    }).success(function(data) {
        console.log("DONE: " + data);
        if (data.status == "OK") {
            $('#loginModal').modal('hide');
            // Show the profile navbar
            $("#profile-navbar-item").removeClass("hidden");
            $("#login-navbar-item").addClass("hidden");
            setLoginModalError(""); // Clear error

            mixpanel.identify(username);
            mixpanel.people.set({ 
                "username": username,
                "email": email,
            });
        } else {
            setLoginModalError(data.message);
        }
    });
    
}

function clearLogin() {
    $("#username").val("");
    $("#email").val("");
    $("#password").val("");
    $("#confirm-password").val("");

    // Remove any errors
    removeFormGroupIdError("email-form-group");
    removeFormGroupIdError("username-form-group");
    removeFormGroupIdError("password-form-group");
    removeFormGroupIdError("confirm-password-form-group");
}

function validateEmail(email) 
{
    // Validates anysthing@anythning.anything
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function search(query) {
    window.location.replace("/search?q=" + query);
}

function searchFromToolbar() {
    var q = $("#toolbar-search").val();
    mixpanel.track("Toolbar Search", {
        query: q,
    });
}

function jumbotronSearch() {
    console.log("Jumbotron search");
    var query = $("#jumbotron-search").val();
    mixpanel.track("Jumbotron Search", {
        "query": query,
    });
    search(query);
}

function signupProfile() {
    var email = $("#email").val().trim();
    if (email.length == 0 || !validateEmail(email)) {
        $("#email").parent().addClass('has-error');
        return;
    }
    var url = "/signup/";
    $.ajax(url, {
        type: "POST",
        data: {
            email: email,   
        },
    }).success(function(data) {
        if (data.status == "OK") {
            $("#signup-alert").removeClass("paper-pink");
            $("#signup-alert").addClass("paper-green");
            $("#signup-alert").empty();
            var msg = '<span class="text-success">You\'ve signed up!</span>';
            $("#signup-alert").html(msg);
            $("#email").remove();

        } else {
            setLoginModalError(data.message);
        }
    }).error(function(data) {
        $("#signup-alert").removeClass("paper-green");
        $("#signup-alert").addClass("paper-pink");
        $("#signup-alert").empty();
        if(data.responseText.indexOf("IntegrityError") > -1) {
            var msg = '<span class="text-danger">Email already signed up.</span>';
        } else { 
        }
        $("#signup-alert").html(msg);
    });
}

$(document).ready(function() {
    // Setup the login/create profile links
    $('#loginLink').click(function(){
        var id = $(this).attr('id');
        showLoginModal(id);
    });

    $('#signupLink').click(function(test){
        var id = $(this).attr('id');
        showLoginModal(id);
    });

    // Add hover events for all book overlays
    $(".book-display").hover(function() {
        $(this).parent().parent().find(".book-actions-overlay").toggleClass("hidden");
    });
    $(".book-actions-overlay").hover(function() {
        $(this).parent().parent().find(".book-actions-overlay").toggleClass("hidden");
    });

    // Add hover events for all art overlays
    $(".art-wall-img").hover(function() {
        $(this).find(".artist-info").toggleClass('hidden');
        $(this).find(".art-img").toggleClass("see-through");
    });

    $("#logout-link").click(function() {
        mixpanel.track("User logged out");
    });

    $("#update-profile-btn").click(function() {
        console.log("Updating");
        mixpanel.people.set({ 
            "$first_name": $("#fname").val().trim(),
            "$last_name": $("#lname").val().trim(),
        });
        mixpanel.identify($("#username-p").text());
    });
});
