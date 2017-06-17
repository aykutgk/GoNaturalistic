//Login Page Custom JS///////////////////////////////////////////////////////////////////
var buttonHtml = $("#submitLoginButton").html();
$("#userLoginForm").on("submit", function(event) {
    event.preventDefault();
    var serializedData = $("#userLoginForm").serialize();
    var formArray = $("#userLoginForm").serializeArray();
    var flag = false;
    flag = validateForm(formArray);
    if (!flag) {
        $("#submitLoginButton").html('<i class="fa fa-spinner fa-fw fa-spin"></i>');
        $("fieldset").attr("disabled", true);
        $.post("/user/login/", serializedData, "json").done(function(data) {
            $.each(data, function(key, val) {
                if (val == "valid") {
                    loginFormError("", "remove");
                    //location.assign("/");
		    location.reload();
                } else if (val == "invalid") {
                    $("fieldset").removeAttr("disabled");
                    $("#submitLoginButton").html(buttonHtml);
                    loginFormError("Wrong email and password combination.", "add");
                } else if (val == "inactive") {
                    $("fieldset").removeAttr("disabled");
                    $("#submitLoginButton").html(buttonHtml);
                    loginFormError("Sorry your account is inactive.", "add");
                } else if (val == "invalid email") {
                    $("fieldset").removeAttr("disabled");
                    $("#submitLoginButton").html(buttonHtml);
                    loginFormError("Please enter a valid email address.", "add");
                }
            });
        }).fail(function() {
            jQuery().gocodemeAlert("Sorry, your request could not be processed<br>Reloading the page...", "danger");
            setTimeout(function() {
                location.reload();
            }, 3000);
        });
    }
});
/////////////////////////////////////////////////////////

