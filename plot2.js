var blue_to_brown = d3.scale.linear()
  .domain([0, 45])
  .range(["steelblue", "brown"])
  .interpolate(d3.interpolateLab);

// interact with this variable from a javascript console
var pc1 = d3.parcoords()("#example")

// load csv file and create the chart
d3.csv('vehicles.csv', function(data) {
  var range = pc1.height() - pc1.margin().top - pc1.margin().bottom;
  var minP = d3.min(data, function(d) {
      return parseInt(d['HP']);
  });
  var maxP = d3.max(data, function(d) {
      return parseInt(d['HP']);
  });
  var logP = d3.scale.log().domain([minP, maxP]).range([range, 1]);

  var minC = d3.min(data, function(d) {
      return parseInt(d['cost_vehicle']);
  });
  var maxC = d3.max(data, function(d) {
      return parseInt(d['cost_vehicle']);
  });
  var logC = d3.scale.log().domain([minC, maxC]).range([range, 1]);

  var dimensions = {
    "drivetrain":{title: "Drivetrain"},
    "MPGe":{title: "Electric cons "},
    "MPG":{title: "Consommation"},
    "HP":{title: 'Power',yscale: logP,tickFormat: function(d){return logP.tickFormat(15,d3.format(",d"))(d)}},
    "emit_fuelcons":{title: 'Em fuel cons'},
    "emit_vehicleprod":{title: 'Em vehicule prod'},
    "cost_vehicle":{title: 'Vehicule cost',yscale: logC,tickFormat: function(d){return logC.tickFormat(15,d3.format(",d"))(d)}},
    "cost_fuel":{title: 'Fuel cost'},
    "cost_maintenance":{title: 'Maintenance cost'},
    "emit_batteryprod":{title: 'Em battery prod'},
    "emit_fuelprod":{title: 'Em fuel prod'},
    "Brands":{title: 'Brand'}};



  pc1
    .data(data)
    .alphaOnBrushed(0.1)
    .dimensions(dimensions)
    //.hideAxis(["VehicleId","brand + Model"])
    .composite("darken")
    .color(function(d) { return blue_to_brown(d['Brandsid']); })  // quantitative color scale
    .alpha(0.5)
    .mode("queue")
    .render()
    .rate(100)
    .brushMode("1D-axes")  // enable brushing
    .reorderable()
    .interactive()  // command line mode

  var explore_count = 0;
  var exploring = {};
  var explore_start = false;
  pc1.svg
    .selectAll(".dimension")
    .style("cursor", "pointer")
    .on("click", function(d) {
      exploring[d] = d in exploring ? false : true;
      event.preventDefault();
      if (exploring[d]) d3.timer(explore(d,explore_count));
    });

  function explore(dimension,count) {
    if (!explore_start) {
      explore_start = true;
      d3.timer(pc1.brush);
    }
    var speed = (Math.round(Math.random()) ? 1 : -1) * (Math.random()+0.5);
    return function(t) {
      if (!exploring[dimension]) return true;
      var domain = pc1.yscale[dimension].domain();
      var width = (domain[1] - domain[0])/4;

      var center = width*1.5*(1+Math.sin(speed*t/1200)) + domain[0];

      pc1.yscale[dimension].brush.extent([
        d3.max([center-width*0.01, domain[0]-width/400]),
        d3.min([center+width*1.01, domain[1]+width/100])
      ])(pc1.g()
          .filter(function(d) {
            return d == dimension;
          })
      );
    };
  };

});
