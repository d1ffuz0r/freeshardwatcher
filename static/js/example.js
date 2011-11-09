// Run the script on DOM ready:
$(function(){
	$('table').visualize({type: 'line', width: '1100%'});

    $("#send").live("click", function(){
        $.get("/get/" + $("#char").val().toString() + "/", function(data){
            var data = jQuery.parseJSON(data);
            $('.all').empty().append("<td></td>");
            for(var i in data.all){
                var val = data.all[i];
                $('.all').append("<th scope='col'>"+val+"</th>");
            }
            $("tbody").empty().append("<tr class='player'><th scope='row'>"+$("#char").val().toString()+"</th></tr>");
            for(var i in data.stat){
                var val = data.stat[i];
                $('.player').append("<td>"+val+"</td>");
            }
            console.log("pre init");
            $('.visualize').trigger('visualizeRefresh');
            console.log("post init");
        });
    });
});