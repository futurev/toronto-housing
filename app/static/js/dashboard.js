var dqChart = dc.lineChart('#dq-chart');
var coChart = dc.lineChart('#co-chart');
var openChart = dc.lineChart('#open-chart');
var utilChart = dc.lineChart('#util-chart');
var volumeChart = dc.barChart('#volume-chart');
var prtflChart = dc.pieChart('#portfolio-chart');
var dtiChart = dc.pieChart('#dti-chart');
var yearChart = dc.pieChart('#year-chart');


function loadGraphs(data) {
  data = data.results;
  console.log(data)

  var dateFormat = d3.time.format('%Y-%m-%d');
  var numberFormat = d3.format('.2f');

  function parseData(d) {
      d.dd = dateFormat.parse(d.dt);
      d.month = d3.time.month(d.dd); // pre-calculate month for better performance
  }
  data.A.forEach(function(d){ parseData(d)});

  var cfa = crossfilter(data.A);

  var yearDimension = cfa.dimension(function (d) {
      return d3.time.year(d.dd).getFullYear();
  });

  var dateDimension = cfa.dimension(function (d) {
      return d.dd;
  });

  var prtflDimension = cfa.dimension(function (d) {
    return d.portfolio;
  });

  var dtiDimension = cfa.dimension(function (d) {
    return d.dti_band;
  });

  var prtflGroup = prtflDimension.group().reduceSum(function(d) {
    return d.open_cnt
  });


  var dtiGroup = dtiDimension.group().reduceSum(function(d) {
    return d.open_cnt
  });

  var yearGroup = yearDimension.group().reduceSum(function(d) {
    return d.open_cnt
  });

  var openCntGroup = dateDimension.group().reduceSum(function (d) {
    return d.open_cnt;
  });

  var mainGroup = dateDimension.group().reduce(
          /* callback for when data is added to the current filter results */
          function (p, v) {
              ++p.count;
              p.open_cnt += v.open_cnt;
              p.open_bal += v.open_bal;
              p.open_cl_amt += v.open_cl_amt;
              p.dq60plus += v.dq60plus;
              p.dq120plus += v.dq120plus;
              p.co_cnt += v.co_cnt;
              p.dq60PO = p.open_cnt? (p.dq60plus/p.open_cnt)*100 : 0;
              p.dq120PO = p.open_cnt? (p.dq120plus/p.open_cnt)*100 : 0;
              p.pbad = p.open_cnt? (p.co_cnt/p.open_cnt)*100*12 : 0;
              p.util = p.open_cl_amt? (p.open_bal/p.open_cl_amt)*100 : 0;
              return p;
          },
          /* callback for when data is removed from the current filter results */
          function (p, v) {
              --p.count;
              p.open_cnt -= v.open_cnt;
              p.open_bal -= v.open_bal;
              p.open_cl_amt -= v.open_cl_amt;
              p.dq60plus -= v.dq60plus;
              p.dq120plus -= v.dq120plus;
              p.co_cnt -= v.co_cnt;
              p.dq60PO = p.open_cnt? (p.dq60plus/p.open_cnt)*100 : 0;
              p.dq120PO = p.open_cnt? (p.dq120plus/p.open_cnt)*100 : 0;
              p.pbad = p.open_cnt? (p.co_cnt/p.open_cnt)*100*12 : 0;
              p.util = p.open_cl_amt? (p.open_bal/p.open_cl_amt)*100 : 0;
              return p;
          },
          /* initialize p */
          function () {
              return {
                  count: 0,
                  open_cnt: 0,
                  dq60plus: 0,
                  dq120plus: 0,
                  dq60PO: 0,
                  dq120PO: 0,
                  co_cnt: 0,
                  pbad: 0,
                  open_bal: 0,
                  open_cl_amt: 0,
                  util: 0
              };
          }
      );

  function mainareaChart(chart) {
    chart.renderArea(true)
    .height(250)
    .transitionDuration(1000)
    .margins({top: 15, right: 50, bottom: 25, left: 50})
    .dimension(dateDimension)
    .mouseZoomable(false)
    .x(d3.time.scale().domain([new Date(2012, 0, 1), new Date(2017, 6, 1)]))
    .xUnits(d3.time.day)
    .elasticY(true)
    .renderHorizontalGridLines(true)
    .legend(dc.legend().x(chart.width()-300).y(0).itemHeight(13).itemWidth(115).gap(5)
    .horizontal(true))
    .brushOn(false);

    return chart;
  }

  mainareaChart(utilChart)
      .yAxisLabel('Util %')
      .group(mainGroup, 'Utilization').valueAccessor(function (d) {
          return d.value.util;
      })
      .title('Utilization', function (d) {
          var value = d.value.util;
          if (isNaN(value)) {
              value = 0;
          }
          return dateFormat(d.key) + '\n' + numberFormat(value);
      })
      .xAxis().tickFormat(d3.time. format('%Y-%m')).ticks(10);


  mainareaChart(dqChart)
      .yAxisLabel('DQ/Open %')
      .group(mainGroup, 'DQ60+/Open %', function (d) {
          return d.value.dq60PO;
      })
      .stack(mainGroup, 'DQ120+/Open %', function (d) {
          return d.value.dq120PO;
      })
      .title('DQ60+/Open %', function (d) {
          var value = d.value.dq60PO;
          if (isNaN(value)) {
              value = 0;
          }
          return dateFormat(d.key) + '\n' + numberFormat(value);
      })
      .title('DQ120+/Open %', function (d) {
          var value = d.value.dq120PO;
          if (isNaN(value)) {
              value = 0;
          }
          return dateFormat(d.key) + '\n' + numberFormat(value);
      })
      .xAxis().tickFormat(d3.time. format('%Y-%m')).ticks(10);


    mainareaChart(coChart)
        .yAxisLabel('Pbad %')
        .group(mainGroup, 'Annualized Pbad %').valueAccessor(function (d) {
            return d.value.pbad;
        })
        .title('Annualized Pbad %', function (d) {
            var value = d.value.pbad;
            if (isNaN(value)) {
                value = 0;
            }
            return dateFormat(d.key) + '\n' + numberFormat(value);
        })
        .xAxis().tickFormat(d3.time. format('%Y-%m')).ticks(10);


      mainareaChart(openChart)
          .group(openCntGroup, 'Open Count').valueAccessor(function (d) {
              return d.value;
          })
          .title('Open count', function (d) {
              var value = d.value;
              if (isNaN(value)) {
                  value = 0;
              }
              return dateFormat(d.key) + '\n' + numberFormat(value);
          })
          .xAxis().tickFormat(d3.time. format('%Y-%m')).ticks(10);



      //#### Range Chart
      volumeChart
          .height(75)
          .margins({top: 0, right: 50, bottom: 20, left: 50})
          .dimension(dateDimension)
          .group(openCntGroup)
          .valueAccessor(function (d) {
              return d.value/100;
          })
          .centerBar(true)
          .brushOn(true)
          .elasticY(true)
          .gap(1)
          .x(d3.time.scale().domain([new Date(2012, 0, 1), new Date(2017, 6, 1)]))
          .xUnits(d3.time.month)
          .yAxis().ticks(0)
          ;


    function buildPieChart(chart, dimension, group) {
      chart
        .height(280)
        .radius(100)
        .innerRadius(30)
        .dimension(dimension)
        .group(group)
        .title(function (d) {
            return d.key;
        })
        .legend(dc.legend());

      chart.on('pretransition', function(chart) {
      chart.selectAll('.dc-legend-item text')
          .text('')
        .append('tspan')
          .text(function(d) { return d.name; })
      });

      return chart;
    }

    buildPieChart(prtflChart, prtflDimension, prtflGroup);
    buildPieChart(dtiChart, dtiDimension, dtiGroup);
    buildPieChart(yearChart, yearDimension, yearGroup);


// code below from https://github.com/dc-js/dc.js/blob/master/web/examples/multi-focus.html
      // we need to this helper function out of coordinateGridMixin
    function rangesEqual(range1, range2) {
        if (!range1 && !range2) {
            return true;
        }
        else if (!range1 || !range2) {
            return false;
        }
        else if (range1.length === 0 && range2.length === 0) {
            return true;
        }
        else if (range1[0].valueOf() === range2[0].valueOf() &&
            range1[1].valueOf() === range2[1].valueOf()) {
            return true;
        }
        return false;
    }

    // monkey-patch the first chart with a new function
    // technically we don't even need to do this, we could just change the 'filtered'
    // event externally, but this is a bit nicer and could be added to dc.js core someday
    volumeChart.focusCharts = function (chartlist) {
        if (!arguments.length) {
            return this._focusCharts;
        }
        this._focusCharts = chartlist; // only needed to support the getter above
        this.on('filtered', function (range_chart) {
            if (!range_chart.filter()) {
                dc.events.trigger(function () {
                    chartlist.forEach(function(focus_chart) {
                        focus_chart.x().domain(focus_chart.xOriginalDomain());
                    });
                });
            } else chartlist.forEach(function(focus_chart) {
                if (!rangesEqual(range_chart.filter(), focus_chart.filter())) {
                    dc.events.trigger(function () {
                        focus_chart.focus(range_chart.filter());
                    });
                }
            });
        });
        return this;
    };
    volumeChart.focusCharts([dqChart, coChart, openChart, utilChart]);
//end

  console.log('rendering')
  dc.renderAll();

}
