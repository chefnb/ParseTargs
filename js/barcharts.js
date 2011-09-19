 
/* 
Barchart rendering of json-formatted TargetDB data using Google Visualization API

Author: Nick Braun 2011

*/

   var charts=[]   
   var chartLookup  // logic for the selection boxes
 
    
    function initCharts(){
       charts[0]= new TDBchart(0,data.length_g)   // cytoplasmic proteins length distribution
       charts[1]= new TDBchart(1,data.length_m)   // membrane proteins        "
       charts[2]= new TDBchart(2,data.de_g)       // cytoplasmic proteins DE count
       charts[3]= new TDBchart(3,data.de_m)       // membrane proteins     "  
      

       chartLookup=[[0,2],[1,3]]

       document.getElementById('CorM').selectedIndex=0
       document.getElementById('LorDE').selectedIndex=0

       charts[0].binsizeSelector.element.selectedIndex=2  // set the bin sizes
       charts[1].binsizeSelector.element.selectedIndex=2 
       charts[2].binsizeSelector.element.selectedIndex=2
       charts[3].binsizeSelector.element.selectedIndex=2

       selectionUpdate()    // initialize the selection boxes
       

      }
  

  function selectionUpdate(){  

     for (var i = 0; i < charts.length; i++){  
       
       if (chartLookup[document.getElementById('CorM').selectedIndex][document.getElementById('LorDE').selectedIndex]==i) 
         charts[i].show()
       else  
         charts[i].hide()
       
      }

    }

//******************
//  TDB chart object
//******************


function TDBchart(index,data){
 
     this.index=index
     this.data=data
     var element = document.createElement('div');
     var chart = new google.visualization.BarChart(element) 
   
     this.draw = function(binsize){     // NB binsize is the index of a binsize list
 
        var bars_tot=data[binsize].bar.length   // no of bars
        chart.draw(theBars(binsize,bars_tot),{
                   fontSize:10, 
                   chartArea: {top: 10, height:"90%"}, 
                   width: 700, 
                   height: 15*bars_tot +400,
                   colors: ['#a88','#8aa']
            })
 
        }
       
  
      var theBars= function(binsize,bars_tot){  // read the data into a google's table format

         var table = new google.visualization.DataTable();  
           table.addColumn('string', 'length');
           table.addColumn('number', 'soluble');
           table.addColumn('number', 'insoluble');
           table.addRows(bars_tot);

         for (var i=0;i<bars_tot; i++) {
            table.setValue(i, 0, data[binsize].bar[i].label);
            table.setValue(i, 1, data[binsize].bar[i].s);
            table.setValue(i, 2, data[binsize].bar[i].i);
             }
         return table
       }
         
      this.binsizeSelector = {
 
        element: document.createElement('select'),
        init: function(){
                   this.element.setAttribute('onchange',"charts["+index+"].draw(this.selectedIndex)");  
                    // selection event handler
                   for (var i=0;i<data.length; i++) {   // loop over no of binsizes and create option for each
                      var option = document.createElement('option');
                      option.innerHTML= data[i].binsize
                      this.element.appendChild(option)
                   }
                    document.getElementById('binsize').appendChild(this.element);
               }
       }

     this.hide = function() {
        element.style.display = 'none'
        this.binsizeSelector.element.style.display = 'none'
          }

     this.show = function() {
        this.draw(this.binsizeSelector.element.selectedIndex)
        element.style.display = 'inline'
        this.binsizeSelector.element.style.display = 'inline'
          }

  
      document.getElementById('chart').appendChild(element);
      this.binsizeSelector.init()
    
}

