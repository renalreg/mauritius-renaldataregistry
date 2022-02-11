$(document).ready(function () {
    var modality = $("select#id_modality").val();
    if (modality == 3) {
        $("#div_id_hd_unit").show();
    } else {
        $("#div_id_hd_unit").hide();
    }
    $("#id_modality").change(function (event) {
        var modality = $("select#id_modality").val();
        if (modality == 3) {
            $("#div_id_hd_unit").show();
        } else {
            $("#div_id_hd_unit").val('');
            $("#div_id_hd_unit").hide();
        }
    })
})