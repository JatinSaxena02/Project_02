var list=[]
var qnum=0
var questions=[]
var totalquestions=0
var clickcount={}

function createsubquestion(data,qnum)
{      var opt=['Normal','Mild','Modrate','Severe','Extream']
        j=0
        h=""
        console.log(data.result[qnum].question)
        $('#questiondiv').html("Que."+data.result[qnum].questionnumber+" "+data.result[qnum].question)
        for (let x in data.result2){
            console.log(data.result2[x].questionid)
            if(data.result2[x].questionid===data.result[qnum].questionid){
                h+=`<div class="row" style="padding-left: 15px;"><div class="col s12 " style="margin-top: 5px;margin-bottom:5px;font-size:12px;font-weight:600">Q${data.result2[x].subquestionnumber}. ${data.result2[x].subquestion}</div>`
                for(i=1;i<6;i++)
                {
                    if(i<2)
                    {
                         h+=`<div value="${i}" class="rate${data.result2[j].subquestionnumber} col blocks block-color" id="rate${data.result[qnum].questionnumber}${data.result2[x].subquestionnumber}${i}" >${opt[i-1]}<br>${i-1}</div>`
                    }
                    else
                    {
                        h+=`<div value="${i}" class="rate${data.result2[j].subquestionnumber} col blocks block-color" id="rate${data.result[qnum].questionnumber}${data.result2[x].subquestionnumber}${i}" style="margin-left:7px;">${opt[i-1]}<br>${i-1}</div>`
                    }
                    }
                    h+=`</div>`
                }
                j+=1

        }
            console.log(h)
            $('#scoreblocks').html(h)
}

function addinlist(data,qnum){
if (!(String(qnum) in clickcount)){
    clickcount[String(qnum)]=0
    temp={}
    length=0
    for (let x in data.result2)
    {
            if(data.result2[x].questionid===data.result[qnum].questionid)
            {
                length+=1
            }
    }

    for(i=1;i<=length;i++){
            temp1='rate'+String(i)
            temp[temp1]=0
    }
    list.push(temp)
    }
}

function onclicks(qnum,blockid){
    classname=$('#'+blockid).attr('class').split(" ")[0]
            if (classname in list[qnum]){
                list[qnum][classname]=$('#'+blockid).attr('value')
                $('.'+classname).each(function(){
                    $(this).removeClass('block-onclick-color').addClass('block-color')
                })
                $("#"+blockid).removeClass('block-color').addClass('block-onclick-color')
            }

        //Score board management
            totalsum=0
            outof=0
            $.each(list[qnum], function(key, value) {
              totalsum+=parseInt(value)
              outof+=5

            })
        $('#currentscore').html("Score "+String(totalsum)+"/"+String(outof))
}

function previoustab(){
        qnum--
        console.log("Qnum...",qnum)
        $('#heading').html(questions.result[qnum].specialization+" Index "+String(parseInt(qnum)+1)+"/"+String(totalquestions))
        createsubquestion(questions,qnum)
        //creating class div button list
         console.log(list)
         $.each(list[qnum], function(key, value)
         {
            console.log(value,key)
            if(value!=0){
            $('#rate'+String(qnum+1)+key[key.length-1]+String(value)).removeClass('block-color').addClass('block-onclick-color')
            }
         })

         if(qnum==0)
         {
           $('#btnprev1').html("")
           $('#btnnext1').removeClass('col s6').addClass('col s12')
         }

}
$(document).ready(function(){
    $.getJSON('/questionpage',{'splid':$('#splid').val()},function(data)
    {
       questions=data
        var len=data.result.length
        var length=0
        totalquestions=len
        $('#heading').html(data.result[qnum].specialization+" Index "+String(parseInt(qnum)+1)+"/"+String(totalquestions))
        createsubquestion(data,qnum)
        i=0

        //creating class div button list
         addinlist(data,qnum)
        console.log(list)

        //adding inital score
        totalsum=0
            outof=0
            $.each(list[qnum], function(key, value) {
              totalsum+=parseInt(value)
              outof+=5
            })
            $('#currentscore').html("Score "+String(totalsum)+"/"+String(outof))


    })

    $(document).click(function(event){
        //change div color
        blockid=event.target.id
        console.log(blockid)
        //for previous button
        if(blockid==='btnprev'){

            previoustab()
        }

        else if(blockid==='btnnext'){

            qnum+=1
        console.log("Qnum...",qnum)
        if(totalquestions>qnum)
        {
        $('#heading').html(questions.result[qnum].specialization+" Index "+String(parseInt(qnum)+1)+"/"+String(totalquestions))
        createsubquestion(questions,qnum)

        //creating class div button list
         addinlist(questions,qnum)
         console.log(list)

         //update score board
        totalsum=0
            outof=0
            $.each(list[qnum], function(key, value) {
              totalsum+=parseInt(value)
              outof+=5

            })
        $('#currentscore').html("Score "+String(totalsum)+"/"+String(outof))

        //autoselecting value
        $.each(list[qnum], function(key, value)
         {
            if(value!=0){
            $('#rate'+String(qnum+1)+key[key.length-1]+String(value)).removeClass('block-color').addClass('block-onclick-color')
            }
         })

         //adding prevous button
         if(qnum>=1)
         {
           $('#btnnext1').removeClass('col s12').addClass('col s6')
           temp1=`<button style="width:100%;border-radius:20px;background:rgb(17, 194, 214);" class="btnprev waves-effect wave-light btn" id='btnprev' type="button">Preivous</button>`
           $('#btnprev1').html(temp1)
         }


         }
        else{
            $.getJSON('/submitscore',{'score':JSON.stringify(list)},function(data){
                alert(data.result)
                payment(data.username,data.mobileno,data.email)
               // location.href="http://localhost:8000/submitscore"
            })
        }
      /**********Payments******************/

      function payment(username,mobileno,email){
    var options = {
	"key": "rzp_test_GQ6XaPC6gMPNwH",
	"amount": 100*100, // Example: 2000 paise = INR 20
	"name": "MedAsist",
	"description": "Payment for Subscription",
	"image": "/static/logo1.png",// COMPANY LOGO

	"handler": function (response) {
		console.log(response);

		// AFTER TRANSACTION IS COMPLETE YOU WILL GET THE RESPONSE HERE.
	},
	"prefill": {
		"name": username, // pass customer name
        "email":email,
		"contact":mobileno//customer phone no.
	},
	"notes": {
		"address": "address" //customer address
	},
	"theme": {
		"color": "#15b8f3" // screen color
	}
};
console.log(options);
var propay = new Razorpay(options);
propay.open();



}


      /**************************/

        }

        //onclock div color change
        onclicks(qnum,blockid)


    })

    $('.btnnext').click(function(){






    })

})