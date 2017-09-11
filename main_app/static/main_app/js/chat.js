$('#chat-form').on('submit', function(event){
event.preventDefault();

$.ajax({
    url: '/post/',
    type: 'POST',
    data: { msgbox : $('#chat-msg').val()},
    
    success : function(json){
        $('#chat-msg').val('');
        $('#msg-list').append('<li class="chat chat-small row"><div class="col-xs-2 col-sm-4 col-lg-4"><div class="chat-avatar hidden-xs"><img src="/media/'+json.avatar+' " alt="Аватар" class=' + "img img-circle img-responsive img-center" + '/></div><div class="chat-info"><span class="small">'+json.user+'</span></div></div><div class="col-xs-10 col-sm-8 col-lg-8"><div class="chat-message">'+json.msg+'</div></div></li>')
        
        
        var charlist = document.getElementById('msg-list-body');
        charlist.scrollTop = charlist.scrollHeight;
    }
});
});

function getMessages(){
    if (!scrolling){
        $.get('/messages/', function(messages){
            $('#msg-list').html(messages);
            var charlist = document.getElementById('msg-list-body');
        charlist.scrollTop = charlist.scrollHeight;
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#msg-list-body').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 2500);
});

$(document).ready(function(){
    $('#send').attr('disabled','disabled');
    $('#chat-msg').keyup(function(){
        if($(this).val()!= ''){
            $('#send').removeAttr('disabled');
        }
        else {
     $('#send').attr('disabled','disabled');
        }
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});