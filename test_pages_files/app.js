$(function(){
    $('#button').click(function(){
        $.getJSON('http://localhost:5050', function(data){
            console.log(data);
        });
    });
}) 

$(function(){
    $('#button2').click(function(){
        var args = $("#args").val();
        $('body').append('<p>' + args + '<p>');
        $.getJSON('http://localhost:8000', function(data){
            console.log(data);
            var items = [];
            $.each( data.data, function( key, val ) {
                items.push( "<li id='" + key + "'>" + key + ": " + val + "</li>" );
            });
                
            $( "<ul/>", {
                "class": "my-new-list",
                html: items.join( "" )
                }).appendTo( "body" );
        });
    });
}) 

