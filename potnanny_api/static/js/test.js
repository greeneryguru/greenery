var globalChartRefs = {};
var overflowStates = {};

/*
 * load chart data for particular element
 */
function load_chart(id) {
  var atoms = id.split("_");

  $.get("{{ url_for('measurement.simple_graph') }}",
    { "sensors": atoms[1], "measurements": atoms[2], "hours": 12 },
    function(data){
      createChart(id, data, globalChartRefs);
    }, 'json');
}

$(document).ready(function() {
  /*
   * load our initial chart div overflow states, as thats what
   * defines 'visible' or not with the mini.css 'collapse' elements
   */
  $("[id*=chartdiv_]").each(function() {
    var id = this.id;
    var ovf = $("#" + this.id).css("overflow");
    overflowStates[this.id] = ovf;
  });

  /*
   * monitor for the chartdivs becoming visible
   */
   setInterval(function(){
     $("[id*=chartdiv_]").each(function() {
       var id = this.id;
       var ovf = $("#" + this.id).css("overflow");
       var atoms = id.split("_");
       var chart_id = ["chart",atoms[1],atoms[2]].join("_");
       if ( ovf != overflowStates[id] && ovf == "auto" ) {
         load_chart(chart_id);
       }
       overflowStates[id] = ovf;
     });
   },200);

  /*
   * refresh open graphs every n seconds
   */
  setInterval(function(){
    $("[id*=chart_]").each(function(){
      var id = this.id;
      var atoms = id.split("_");
      var chartdiv = ["chartdiv",atoms[1],atoms[2]].join("_");
      if (overflowStates[chartdiv] == 'auto') {
        load_chart(id);
      }
    });
  }, 5000);

  /*
   * refresh sensor measurements every n seconds
   */
  setInterval(function(){
    $("[id*=card_]").each(function(){
      var id = this.id;
      var atoms = id.split("_");
      $.get("/sensors/" + atoms[1] + "/measurements", {},
        function(data){
          for (k in data["measurements"]) {
            var myid = "gauge_" + atoms[1] + "_" + k;
            var myvalue = data["measurements"][k].toFixed(1);
            if (k == "temperature") {
              $("#" + myid).text(myvalue + "\xB0");
            } else if (k == "humidity" || k == "soil-moisture") {
              $("#" + myid).text(myvalue + "%");
            } else {
              $("#" + myid).text(myvalue);
            }
          }
        }, 'json');
    });
  }, 20000);
});
