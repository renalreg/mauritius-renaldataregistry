$(document).ready(function () {
    var modality = $("select#id_modality").val();
    var initial_access = $("select#id_hd_initialaccess").val();

    // Patient is in dialysis in modes HD (2) or PD (3)
    if (modality == 2 || modality ==3) {
        $("#div_id_delay_start").show();
        $("#div_id_delay_beforedialysis").show();
    } else {
        $("#div_id_delay_start").hide();
        $("#div_id_delay_beforedialysis").hide();
    }
    // HD modality is 2
    if (modality == 2) {
        $("#div_id_hd_unit").show();
        $("#div_id_hd_initialaccess").show();
        $("#div_id_hd_privatestart").show();
    } else {
        $("#div_id_hd_unit").hide();
        $("#div_id_hd_initialaccess").hide();
        $("#div_id_hd_privatestart").hide();
    }

    // PD modality is 3
    if (modality == 3) {
        $("#div_id_pd_catheterdays").show();
        $("#div_id_pd_insertiontechnique").show();
    } else {
        $("#div_id_pd_catheterdays").hide();
        $("#div_id_pd_insertiontechnique").hide();
    }

    // Why AVF/AVG not used to initiate HD?
    // (0, "Unknown"),
    // (1, "AVF"),
    // (2, "AVG"),
    // (3, "TC"),
    // (4, "NTC"),
    if (initial_access == 3 || initial_access == 4) {
        $("#div_id_hd_unusedavfavgreason").show();
    } else {
        $("#div_id_hd_unusedavfavgreason").val('');
        $("#div_id_hd_unusedavfavgreason").hide();
    }
    
    $("#id_modality").change(function (event) {
        var modality = $("select#id_modality").val();

        if (modality == 2 || modality ==3) {
            $("#div_id_delay_start").show();
            $("#div_id_delay_beforedialysis").show();
        } else {
            $("#div_id_delay_start").hide();
            $("#div_id_delay_beforedialysis").hide();
        }

        // HD
        if (modality == 2) {
            $("#div_id_hd_unit").show();
            $("#div_id_hd_initialaccess").show();
            $("#div_id_hd_privatestart").show();
        } else {
            $("#div_id_hd_unit").val('');
            $("#div_id_hd_unit").hide();

            $("#div_id_hd_initialaccess").val('');
            $("#div_id_hd_initialaccess").hide();
            
            $("#div_id_hd_privatestart").val('');
            $("#div_id_hd_privatestart").hide();
        }

        // PD
        if (modality == 3) {
            $("#div_id_pd_catheterdays").show();
            $("#div_id_pd_insertiontechnique").show();
        } else {
            $("#div_id_pd_catheterdays").hide();
            $("#div_id_pd_insertiontechnique").hide();
        }
    })

    // Why AVF/AVG not used to initiate HD?
    // (0, "Unknown"),
    // (1, "AVF"),
    // (2, "AVG"),
    // (3, "TC"),
    // (4, "NTC"),
    $("select#id_hd_initialaccess").change(function (event) {
        if ($(this).val() == 3 || $(this).val() == 4) {
            $("#div_id_hd_unusedavfavgreason").show();
        } else {
            $("#div_id_hd_unusedavfavgreason").val('');
            $("#div_id_hd_unusedavfavgreason").hide();
        }
    });

})