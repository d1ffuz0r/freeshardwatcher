function get(nick){
    $.post("/get/", {
        "nick": nick,
        "from": $(".dfrom").val(),
        "to": $(".dto").val()},
        function(data){
        var data = jQuery.parseJSON(data);
        if(data.message){
            alert("Not found");
        }
        else{
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
            $('.visualize').trigger('visualizeRefresh');
        }
    });
}

// Run the script on DOM ready:
$(function(){
	$('table').visualize({type: 'line', width: '1100%'});

    $("#send").live("click", function(){
        get($("#char").val().toString());
    });

    $(".datap").datepicker({
        dateFormat: "dd.mm.yy"
    });
});