$(document).ready(function () {
    var krt_status = $("select#id_krt_status").val();
    if (krt_status == 1) {
        $("#div_initialKRTmod_hd_unit").show();
        $("#div_id_creatinine").hide();
        $("#div_id_egfr").hide();
        $("#div_id_measurement_date").hide();
    } else {
        $("#div_initialKRTmod_hd_unit").hide();
        $("#div_id_creatinine").show();
        $("#div_id_egfr").show();
        $("#div_id_measurement_date").show();
    }
    $("#id_krt_status").change(function (event) {
        var krt_status = $("select#id_krt_status").val();
        if (krt_status == 1) {
            $("#div_initialKRTmod_hd_unit").show();
            $("#div_id_creatinine").hide();
            $("#div_id_egfr").hide();
            $("#div_id_measurement_date").hide();
        } else {
            $("#div_initialKRTmod_hd_unit").val('');
            $("#div_initialKRTmod_hd_unit").hide();
            $("#div_id_creatinine").show();
            $("#div_id_egfr").show();
            $("#div_id_measurement_date").show();
        }
    })
})