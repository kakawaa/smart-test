Highcharts.chart('container', {
        chart: {
            type: 'area',
//                animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: function() {

                    // set up the updating of the chart each second
                    var series0 = this.series[0],series1= this.series[1];
                    setInterval(function() {
                        var x = (new Date()).getTime(), // current time
                            y = Math.random(),system=Math.random();
            console.log(x)
            $.ajax({
                url:"/getCPUInfo/",
                async:false,
                success:function(data){
                        var jsondata= JSON.parse(data);
                        y = jsondata.user;
                        system = jsondata.system;
                }

            });
//                alert('x and y is :'+x+","+y);

                series0.addPoint([x, y], true, true);
                series1.addPoint([x,system],true,true);
                    }, 1000);
                }
            }
        },
        title: {
            text: "Live CPU and System Data(%)"
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 15
        },
        yAxis: {
            title: {
                text: 'Value'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
                    Highcharts.numberFormat(this.system, 2);
            }
        },
        legend: {
            enabled:true
        },
        plotOptions:{
            area:{
            //    fillColor:'#ecae3d',
                fillOpacity:0.8,

                marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2,
                        states: {
                            hover: {
                                enabled: true
                            }
                        }
                }
            }

        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'User data',
            data: (function() {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    i;

                for (i =-19 ; i <= 0; i++) {
                    data.push({
                        x: '',
                        y: usrcpu //Math.random()
                    });
                }
                return data;
            })(),
        //    color:'#f28f43'
        },
        {name:'System data',
        data:(function(){
            var data=[],
            time =(new Date()).getTime(),
            i;
            for(i=-19;i<=0;i++){
                data.push({
                    x:'',
                    y:systemcpu//Math.random()
                });
            }
            return data;
        })(),
        //color:'#492970'
        }
]
    });