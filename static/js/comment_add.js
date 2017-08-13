$('#comment__new').click(function (e){
    e.preventDefault();
        $.ajax({
        url: $('form[name=comment_new]').attr('action'),
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'message': $('form textarea[name=message]').val(),
        },
        success: function(data){
            if (data){
                $('.comments').html(data);
            window.scrollTo(0, document.body.scrollHeight);
            }
            else{
                console.error('데이터가 안넘어옴');
            }
        },
        error: function(xhr,errmsg,err){
            console.error(err);
        },
        complete: function() {
            $.getScript(js_root, function(){});
        }
    });
});