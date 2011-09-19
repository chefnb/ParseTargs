

google.load("visualization", "1", {packages:["corechart"]});
 
// onload initialization
$(function(){
   $.post('/parseTargs/getStatus',{}, function(data) { 
         if (data!=0) { // show previous update results

            updateTable(data)  // show table summary
            initCharts()  // draw the features histograms 
            $('#chartspace').show()  
            $('#loading').hide()
            $('#partial_summary').hide()

              $.get('/parseTargs/getSummary',{}, function(data) {   
               $('#summary').html(data)
               })
           }

          else $('#loading').hide()  // no previous update found
        } )
   })  




var targsDownload = function(){  // Step one of the full update: Download TargetsV2.xml from url

  if (window.confirm("This will overwrite any previous updates. Proceed?"))  {    

    $('#last_update').remove();
    $('#monitor').hide();
    $('#downloading').show();
    $.post('/parseTargs/download',{}, function(data) {
      
           if (data ==1) {   $('#downloading').html("Downloading TargetDB... completed");
                             parseTargs.start()     }

           else $('#downloading').html("Sorry! The download didn't work. Refresh page to try again")
             })

   }


}
     




var parseTargs = {                  // Step two of the full update: Parse the download into sqlite3 database
  
     start: function(){
  
           $('#monitor').show();
           $('#summary').html("");         // clear the results table
           $('#partial_summary').show();   
           $('#chartspace').hide()  
            

           document.getElementById('busy_icon').style.visibility='visible'
           $.get('/parseTargs/start')
           setTimeout("parseTargs.poll()", 200)
   
             },

     poll: function(){      
       
              $.post('/parseTargs/getStatus',{}, function(data) {
                     updateTable(data)
                     if (data.status=="building") setTimeout("parseTargs.poll()", 500); 
                     else parseTargs.close()
               });
            },

      close: function(){    
              document.getElementById('busy_icon').style.visibility='hidden'  
              $('#partial_summary').hide()
              $.get('/parseTargs/getSummary',{}, function(data) {  $('#summary').html(data) })
              $.get('/parseTargs/getHistogramData',{}, function() {   
                           
               window.alert("parseTargs update complete\nHit refresh for features barcharts\n\nGenerated in workspace directory:\nparseTargs.db\nsummary.html\nbarchart_data.js")
               })
        }

}



 var updateTable = function(data){
            $("#status").html(data.status) 
            $("#parsed").html(data.records_parsed) 
            $("#datestamp").html(data.datestamp) 


            $("#sctot").html(data.sctot) 
            $("#smtot").html(data.smtot) 
            $("#ictot").html(data.ictot) 
            $("#imtot").html(data.imtot) 
}


