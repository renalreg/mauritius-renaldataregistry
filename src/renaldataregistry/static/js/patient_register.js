$(document).ready(function () {
    var krt_status = $("select#id_in_krt_modality").val();
    if (krt_status == "Y") {
        $("#current_krt_modality").show();
        $("#div_id_creatinine").hide();
        $("#div_id_egfr").hide();
        $("#div_id_hb").hide();
        $("#div_id_measurement_date").hide();
    } else {
        $("#current_krt_modality").hide();
        $("#div_id_creatinine").show();
        $("#div_id_egfr").show();
        $("#div_id_hb").show();
        $("#div_id_measurement_date").show();
    }
    $("#id_in_krt_modality").change(function (event) {
        var krt_status = $("select#id_in_krt_modality").val();
        if (krt_status == "Y") {
            $("#current_krt_modality").show();
            $("#div_id_creatinine").hide();
            $("#div_id_egfr").hide();
            $("#div_id_hb").hide();
            $("#div_id_measurement_date").hide();
        } else {
            $("#current_krt_modality").hide();
            $("#div_id_creatinine").show();
            $("#div_id_egfr").show();
            $("#div_id_hb").hide();
            $("#div_id_measurement_date").show();
        }
    })
    var current_krt_mod = $("select#id_patientkrtmodality_set-5-modality option:selected").text();
    // modality 3 = HD
    if (current_krt_mod == "HD") {
        $("#div_id_patientkrtmodality_set-5-hd_unit").show();
    } else {
        $("#div_id_patientkrtmodality_set-5-hd_unit").hide();
    }
    $("#id_patientkrtmodality_set-5-modality").change(function (event) {
        var current_krt_mod = $("select#id_patientkrtmodality_set-5-modality option:selected").text();
        // modality 3 = HD
        if (current_krt_mod == "HD") {
            $("#div_id_patientkrtmodality_set-5-hd_unit").show();
        } else {
            $("#div_id_patientkrtmodality_set-5-hd_unit").val('');
            $("#div_id_patientkrtmodality_set-5-hd_unit").hide();
        }
    })

    $("#id_health_institution").change(function (event) {
        var url = $("#mrr_form").attr("data-units-url");
        var hi_id = $(this).val();

        $.ajax({
            url: url,
            data: {
                'hi_id': hi_id
            },
            success: function (data) {
                $("#id_unit").html(data);
            }
        });
    });
})