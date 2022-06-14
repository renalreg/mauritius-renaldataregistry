$(document).ready(function () {
    var initial_access = $("select#id_hd_initialaccess").val();
    // INITIALACCESS_CHOICES = (
    //     (0, "Unknown"),
    //     (1, "AVF"),
    //     (2, "AVG"),
    //     (3, "TC"), <-- TC is 3
    //     (4, "NTC"), <--NTC is 4
    // )
    if (initial_access == 3 || initial_access == 4) {
        $("#div_id_hd_tc_ntc_reason").show();
    } else {
        $("#div_id_hd_tc_ntc_reason").hide();
    }
    $("#id_hd_initialaccess").change(function (event) {
        var initial_access = $(this).val();

        if (initial_access == 3 || initial_access == 4) {
            $("#div_id_hd_tc_ntc_reason").show();
        } else {
            $("#div_id_hd_tc_ntc_reason").hide();
        }
    })
})