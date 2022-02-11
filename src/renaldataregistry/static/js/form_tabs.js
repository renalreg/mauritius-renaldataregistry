$(document).ready(function () {

    var currentTab = 0; //Current tab is the first tab (0)
    showTab(currentTab); //Show the current tab

    function showTab(n) {
        //This function will display the specified tab of the form
        var numItems = $(".tab").length;
        $(".tab:eq(" + n + ")").css("display", "block");
        if (n == 0) {
            $(".prevBtn").css("display", "none");
        } else {
            $(".prevBtn").css("display", "inline");
        }
        if (n == (numItems - 1)) {
            $(".nextBtn").html("Submit");
        } else {
            $(".nextBtn").css("display", "inline");
            $(".nextBtn").html("Next");
        }
        //and run a function that displays the correct step indicator
        setupStepMark(n)
    }

    function setupStepMark(n) {
        //Removes the active class of all steps
        var i, x = $('.step');
        for (i = 0; i < x.length; i++) {
            $(".step:eq(" + i + ")").removeClass("active")
        }
        //and adds the active class to the current step of the form
        $(".step:eq(" + n + ")").addClass("active");
    }

    function validateForm() {
        //Validation of the form fields
        var x, y, valid = true;
        x = $(".tab:eq(" + currentTab + ") select").filter("[required]");
        y = $(".tab:eq(" + currentTab + ") input").filter("[required]");
        $.merge(x, y);
        x.map(function (idx, el) {
            $(el).removeClass("invalid");
            if ($(el).val() == "") {
                $(el).addClass("invalid");
                valid = false;
            }
        });
        if (valid) {
            $(".step:eq(" + currentTab + ")").addClass("finish");
        }
        return valid;
    }

    $(".nextBtn").click(function () {
        //Hide current and display next tab
        var x = $(".tab");

        if (currentTab == 0 && !validateForm()) return false;

        $(".tab:eq(" + currentTab + ")").css("display", "none");
        currentTab = currentTab + 1;

        if (currentTab >= x.length) {
            //if html is changed by user
            currentTab = 0;
            //submitting form:
            $("#mrr_form").submit();
        }
        showTab(currentTab);
    });

    $(".prevBtn").click(function () {
        //Hide current and display previous tab
        var x = $(".tab");
        $(".tab:eq(" + currentTab + ")").css("display", "none");
        currentTab = currentTab - 1;

        if (currentTab < 0) {
            //if html is changed by user
            currentTab = x.length - 1;
        }
        showTab(currentTab);
    });
})

