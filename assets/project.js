$(document).ready(function(){
$.getJSON('/specializationdisplayallJSON',function(data){

    data.result.map((item)=>{
    $('#special').append($('<option>').text(item.specialization).val(item.specializationid))

    })

})


})