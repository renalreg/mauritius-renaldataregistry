$(document).ready(function () {
    var modality = $("select#id_modality").val();
    if (modality == 3) {
        $("#div_id_hd_unit").show();
        $("#div_id_hd_initialaccess").show();
        $("#div_id_hd_sessions").show();
        $("#div_id_hd_minssessions").show();
        $("#div_id_hd_adequacy_urr").show();
        $("#div_id_hd_adequacy_kt").show();
        $("#div_id_hd_ntcreason").show();
        $("#div_id_pd_exchangesday").hide();
        $("#div_id_pd_fluidlitresday").hide();
        $("#div_id_pd_adequacy").hide();
        $("#div_id_pd_bp").hide();
    } else {
        if (modality == 4) {
            $("#div_id_hd_unit").hide();
            $("#div_id_hd_initialaccess").hide();
            $("#div_id_hd_sessions").hide();
            $("#div_id_hd_minssessions").hide();
            $("#div_id_hd_adequacy_urr").hide();
            $("#div_id_hd_adequacy_kt").hide();
            $("#div_id_hd_ntcreason").hide();
            $("#div_id_pd_exchangesday").show();
            $("#div_id_pd_fluidlitresday").show();
            $("#div_id_pd_adequacy").show();
            $("#div_id_pd_bp").show();
        }else{
            $("#div_id_hd_unit").hide();
            $("#div_id_hd_initialaccess").hide();
            $("#div_id_hd_sessions").hide();
            $("#div_id_hd_minssessions").hide();
            $("#div_id_hd_adequacy_urr").hide();
            $("#div_id_hd_adequacy_kt").hide();
            $("#div_id_hd_ntcreason").hide();
            $("#div_id_pd_exchangesday").hide();
            $("#div_id_pd_fluidlitresday").hide();
            $("#div_id_pd_adequacy").hide();
            $("#div_id_pd_bp").hide();
        }
    }
    $("#id_modality").change(function (event) {
        var modality = $("select#id_modality").val();
        if (modality == 3) {
            $("#div_id_hd_unit").show();
            $("#div_id_hd_initialaccess").show();
            $("#div_id_hd_sessions").show();
            $("#div_id_hd_minssessions").show();
            $("#div_id_hd_adequacy_urr").show();
            $("#div_id_hd_adequacy_kt").show();
            $("#div_id_hd_ntcreason").show();
            $("#div_id_pd_exchangesday").hide();
            $("#div_id_pd_fluidlitresday").hide();
            $("#div_id_pd_adequacy").hide();
            $("#div_id_pd_bp").hide();
        } else {
            if (modality == 4) {
                $("#div_id_hd_unit").val('');
                $("#div_id_hd_unit").hide();
                $("#div_id_hd_initialaccess").hide();
                $("#div_id_hd_sessions").hide();
                $("#div_id_hd_minssessions").hide();
                $("#div_id_hd_adequacy_urr").hide();
                $("#div_id_hd_adequacy_kt").hide();
                $("#div_id_hd_ntcreason").hide();
                $("#div_id_pd_exchangesday").show();
                $("#div_id_pd_fluidlitresday").show();
                $("#div_id_pd_adequacy").show();
                $("#div_id_pd_bp").show();
            }else{
                $("#div_id_hd_unit").hide();
                $("#div_id_hd_initialaccess").hide();
                $("#div_id_hd_sessions").hide();
                $("#div_id_hd_minssessions").hide();
                $("#div_id_hd_adequacy_urr").hide();
                $("#div_id_hd_adequacy_kt").hide();
                $("#div_id_hd_ntcreason").hide();
                $("#div_id_pd_exchangesday").hide();
                $("#div_id_pd_fluidlitresday").hide();
                $("#div_id_pd_adequacy").hide();
                $("#div_id_pd_bp").hide();
            }
        }
    })
})