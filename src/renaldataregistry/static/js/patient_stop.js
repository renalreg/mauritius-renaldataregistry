$(document).ready(function () {
    var stop_reason = $("select#id_stop_reason").val();
    // ENDREASON_CHOICES = (
    //     ("D", "Died"),
    //     ("RKF", "Recovered kidney function"),
    //     ("DR", "Doctor’s recommendation"),
    //     ("LF", "Lost to follow-up"),
    //     ("LM", "Left Mauritius"),
    //     ("FC", "Patient or family choice"),
    // )
    if (stop_reason == 'D') {
        $(".dod").show();
    } else {
        $(".dod").hide();
    }
    $("#id_stop_reason").change(function (event) {
        var stop_reason = $(this).val();

        if (stop_reason == 'D') {
            $(".dod").show();
        } else {
            $(".dod").hide();
        }
    })
})