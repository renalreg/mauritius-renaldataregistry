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
    var current_krt_mod = $("select#id_krt_present-modality option:selected").text();
    // modality 3 = HD
    if (current_krt_mod == "HD") {
        $("#div_id_krt_present-hd_unit").show();
    } else {
        $("#div_id_krt_present-hd_unit").hide();
    }
    $("#id_krt_present-modality").change(function (event) {
        var current_krt_mod = $("select#id_krt_present-modality option:selected").text();
        // modality 3 = HD
        if (current_krt_mod == "HD") {
            $("#div_id_krt_present-hd_unit").show();
        } else {
            $("#div_id_krt_present-hd_unit").val('');
            $("#div_id_krt_present-hd_unit").hide();
        }
    })

    function process(date){
        const [day, month, year] = date.split('/');
        return new Date(+year, month - 1, +day);
    }

    // validate sequence of dates in chronology (basic validation)
    $(".datepickerinput").on("dp.change", function(event){
        var date_first = $("#id_krt_first-start_date").val();
        var date2 = $("#id_krt_2-start_date").val();
        var date3 = $("#id_krt_3-start_date").val();
        var date4 = $("#id_krt_4-start_date").val();
        var date5 = $("#id_krt_5-start_date").val();
        var date_present = $("#id_krt_present-start_date").val();

        if (process(date_first) >= process(date2) || process(date2) >= process(date3) || process(date3) >= process(date4) || process(date4) >= process(date5) || process(date5) >= process(date_present)) {
            $(this).addClass('redBorder');
            $('.nextBtn').addClass('grayText').prop('disabled', 1);
            $('.prevBtn').addClass('grayText').prop('disabled', 1);
        }else{
            $(this).removeClass('redBorder');
            $('.nextBtn').removeClass('grayText').prop('disabled', 0);
            $('.prevBtn').removeClass('grayText').prop('disabled', 0);
        }
    });

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

    
    $('[data-bs-toggle="tooltip"]').tooltip();

})