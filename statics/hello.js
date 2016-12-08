var say_hello = function(msg) {
	alert(msg);
}

$(document).ready(function() {

    $.ajax({
        url: "/photos/",
        method: "GET",
        datatType: "json"
    }).done(function(data) {
        console.log(data);
    }).fail(function(data) {
        console.log("ajax error");
        console.log(data);
    });

    $('#filter_nav button').on('click', function(e) {
        var value = $(this).val();
        console.log('clicked ' + value);

        $('#preview').vintage({
            mime: 'image/png'
        }, vintagePresets[value]);
        return false;
    });

    $('#form-post').on('submit', function(e) {
        var image = $('#preview').attr('src');
        if ( image ) {
            $('input[name="filtered_image"]').val(image);
        }
        else {
            $('input[name="filtered_image"]').val('');
        }
    });

    $('#id_image').on('change', function(e) {
        var reader = new FileReader();
        reader.onerror = function(e) { console.log(e); }
        reader.onloadend = function(e) {
            if ( (/^data\:image\/(png|jpeg);base64/i).test(e.target.result) ) {
                // console.log(e.target.result);
                 $('#preview').attr('src', e.target.result).show(); 
            }
            else { 
                if ( e.total == 0 || e.loaded == 0 ) {
                    alert('파일을 가져오지 못 했습니다.'); 
                } 
                else { 
                    alert('허용된 사진 파일이 아닙니다.'); 
                }
            }
        }
        reader.readAsDataURL(this.files[0]); // file --> base64 format
    });

});

