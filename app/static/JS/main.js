$(function () {
    $('#hide_button').on('click', () => {
        if ($('#hide_zone').css('display') == 'block') {
        // 表示されている場合の処理
        $('#hide_zone').hide();
        } else {
        // 非表示の場合の処理
        $('#hide_zone').show();
        }
    });
    });

    const target_button = document.getElementById('men_submit_button');
    const target_msg = document.getElementById('men_loading');
    target_button.addEventListener('click', () => {
        target_button.style.display = "none";
        target_msg.style.display = "block";
    }, false);

    $('#attachment .fileinput').on('change', function () {
        var file = $(this).prop('files')[0];
        $(this).closest('#attachment').find('.filename').text(file.name);
        });


    $("#layout_select").change(function () {
	var extraction_val = $("#layout_select").val();
	if(extraction_val == "men_ito") {
		$('#ito_page').css('display', 'block');
	}else{
		$('#ito_page').css('display', 'none');
    }
    });