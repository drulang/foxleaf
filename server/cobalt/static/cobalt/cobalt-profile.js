
function validatePasswordChange() {
    var password = $("#change-password").val();
    var confirmPassword = $("#change-confirm-password").val();

    setPasswordFormError("");
    if (password != confirmPassword) {
        setPasswordFormError("Passwords do not match");
        return false;
    }

    return true;
}


function setPasswordFormError(message) {
    $("#password-form-error").text(message);
}

function resendEmailVerification() {
    var url = "/resendemailverification";
    $.ajax(url, {})
    .success(function(data) {
        if (data.status == "OK") {
            //TODO: Need to change the alert
            console.log("Status: " + data.status);
            $("#email-confirmation-alert").empty();
            $("#email-confirmation-alert").text("Success! You should receive an email shortly.  If you're having trouble please let us know at hello@bluebutter.com");
            $("#email-confirmation-alert").removeClass("alert-warning");
            $("#email-confirmation-alert").addClass("alert-success");
        } else {
        }
        mixpanel.track("Resend Email Verification");
    });
}

function profileImageFormValid() {
    if($("#profile-image-file").val().length > 0) {
        $("#profile-image-error").text("");
        mixpanel.track("User Changed Profile Image");
        return true;
    } else {
        $("#profile-image-error").text("Please select a file");
        return false;
    }
}

$(document).ready(function() {
    $("#profile-form-link").click(function() {
        //Set the profile form visible
        $("#profile-form").css("display", "");
        $("#password-form").css("display", "none");


        // Change which tab is visible
        $("#password-form-tab").removeClass('active');
        $("#profile-form-tab").addClass('active');
    });

    $("#password-form-link").click(function() {
        //Set the password form visiebl
        $("#profile-form").css("display", "none");
        $("#password-form").css("display", "");

        //Change the tab
        $("#password-form-tab").addClass('active');
        $("#profile-form-tab").removeClass('active');
    });
});
