$(function(){
    $('#button2').click(function(){
        var param = $("#args").val();
//         $('body').append('<p>' + args + '<p>');
        var tags = {args: param}
        $.getJSON('http://localhost:5050',  tags, function(data){
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

