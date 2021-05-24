function loading() {
		$('body').loading({
			loadingWidth:120,
			title:'',
			name:'test',
			discription:'',
			direction:'column',
			type:'origin',
			// originBg:'#71EA71',
			originDivWidth:100,
			originDivHeight:40,
			originWidth:6,
			originHeight:6,
			smallLoading:false,
			loadingMaskBg:'rgba(0,0,0,0.2)'
		});

		setTimeout(function(){
			//removeLoading('test');
		},3000);
	}
var competitor_project='NA'
function getdata(logname,compare_project){
      $.ajax({
          url:"/apm_detail_api/",
          type:'post',
          async:true,
          cache: false,
          data: {
                "logname":logname,
                "Compare_project":compare_project
            },
          beforeSend: function () {
              loading();
            },
          complete: function () {
              removeLoading('test');
            },
          success:function(data){
              var CpuData= []
              var MemData= []
              var FpsData= []
              var FlowData= []
              var TimeData = []

              var competitor_CpuData= []
              var competitor_MemData= []
              var competitor_FpsData= []
              var competitor_FlowData= []

              console.log(data)
              $('#competitor_project').empty()
              competitor_project=data['Competitor_project_list'][0]
              for (var i = 0; i < data['Competitor_project_list'].length; i++) {
                  $('#competitor_project').append('<option>' + data['Competitor_project_list'][i] + '</option>')
              }
              for (var j = 0; j < data['data'].length; j+=1) {
                  CpuData.push(data['data'][j]['apmdata'][0])
                  MemData.push(data['data'][j]['apmdata'][1])
                  FpsData.push(data['data'][j]['apmdata'][2])
                  FlowData.push(data['data'][j]['apmdata'][3])
                  TimeData.push(data['data'][j]['time'])
              }

              var charttype = 'spline'
              if (compare_project=="NA"){
                  var chart = Highcharts.chart('container_cpu', {
    chart: {
        type: charttype
    },
    title: {
        text: 'CPU'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (%)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: CpuData
    }]
});
                  var chart = Highcharts.chart('container_mem', {
    chart: {
        type: charttype
    },
    title: {
        text: 'MEM INFO'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (KB)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: MemData
    }]
});
                  var chart = Highcharts.chart('container_fps', {
    chart: {
        type: charttype
    },
    title: {
        text: 'FPS'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (HZ)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: FpsData
    }]
});
                  var chart = Highcharts.chart('container_flow', {
    chart: {
        type: charttype
    },
    title: {
        text: 'Data Usage'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (KB)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: FlowData
    }]
});
              }else{
                  for (var j = 0; j < data['data'].length; j+=1) {
                      competitor_CpuData.push(data['Competitor_data'][j]['apmdata'][0])
                      competitor_MemData.push(data['Competitor_data'][j]['apmdata'][1])
                      competitor_FpsData.push(data['Competitor_data'][j]['apmdata'][2])
                      competitor_FlowData.push(data['Competitor_data'][j]['apmdata'][3])
                  }
                  var chart = Highcharts.chart('container_cpu', {
    chart: {
        type: charttype
    },
    title: {
        text: 'CPU'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (%)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: CpuData
    },
    {
        name: compare_project,
        data: competitor_CpuData
    }]
});
                  var chart = Highcharts.chart('container_mem', {
    chart: {
        type: charttype
    },
    title: {
        text: 'MEM INFO'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (KB)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: MemData
    },
    {
        name: compare_project,
        data: competitor_MemData
    }]
});
                  var chart = Highcharts.chart('container_fps', {
    chart: {
        type: charttype
    },
    title: {
        text: 'FPS'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (HZ)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: FpsData
    },
    {
        name: compare_project,
        data: competitor_FpsData
    }]
});
                  var chart = Highcharts.chart('container_flow', {
    chart: {
        type: charttype
    },
    title: {
        text: 'Data Usage'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: TimeData
    },
    yAxis: {
        title: {
            text: 'Value (KB)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: data['project'],
        data: FlowData
    },
    {
        name: compare_project,
        data: competitor_FlowData
    }]
});
              }

          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }

var logname = document.getElementById("logname").innerText
console.log('logname:'+logname)
getdata(logname,'NA')

$('#competitor_project').on('keyup change', function () {
    competitor_project=this.value;
});

$('#summit_btn').click(function () {
    if(logname && competitor_project){
        getdata(logname,competitor_project)
    }else {
        alert('no logname or competitor_project')
    }
})

$(document).ready(function () {
    document.getElementById("summit_btn").click();
});


