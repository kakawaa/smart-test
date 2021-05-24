Date.prototype.format = function() {
　　　　　var s = '';
　　　　　var mouth = (this.getMonth() + 1)>=10?(this.getMonth() + 1):('0'+(this.getMonth() + 1));
　　　　　var day = this.getDate()>=10?this.getDate():('0'+this.getDate());
　　　　　s += this.getFullYear() + '-'; // 获取年份。
　　　　　s += mouth + "-"; // 获取月份。
　　　　　s += day; // 获取日。
　　　　　return (s); // 返回日期。
　　};
function getAll(begin, end) {
　　　　var arr = [];
　　　　var ab = begin.split("-");
　　　　var ae = end.split("-");
　　　　var db = new Date();
　　　　db.setUTCFullYear(ab[0], ab[1] - 1, ab[2]);
　　　　var de = new Date();
　　　　de.setUTCFullYear(ae[0], ae[1] - 1, ae[2]);
　　　　var unixDb = db.getTime() - 24 * 60 * 60 * 1000;
　　　　var unixDe = de.getTime() - 24 * 60 * 60 * 1000;
　　　　for (var k = unixDb; k <= unixDe;) {
　　　　　　//console.log((new Date(parseInt(k))).format());
　　　　　　k = k + 24 * 60 * 60 * 1000;
　　　　　　arr.push((new Date(parseInt(k))).format());
　　　　}
　　　　return arr;
}


var api_infos_table= $('#api_infos_table').DataTable({
    "pageLength": 10,
    "paging": true, <!-- 允许分页 -->
    "lengthChange": false, <!-- 允许改变每页显示的行数 -->
    "searching": true, <!-- 允许内容搜索 -->
    "ordering": false, <!-- 允许排序 -->
    "info": false, <!-- 显示信息 -->
    "autoWidth": false, <!-- 固定宽度 -->
    "pagingType": "full_numbers",
    "language": {
        "paginate": {
            "next": ">",
            "previous": "<"
        },
    },
    "order": [[0, "desc"]],
    dom: 't<"bottom"ip><"clear">',
    "columnDefs": [
        {"orderable": false, "targets": -1}
    ]
    });

// 筛选项目
var selectproject=''
$('#project').on('keyup change', function () {
        selectproject=this.value
        if (this.value !== "All") {
            api_infos_table
                .column(1)
                .search(this.value)
                .draw();
        } else {
            api_infos_table
                .column(1)
                .search("")
                .draw();


        }

    });

$('#errortype').on('keyup change', function () {
        if (this.value !== "All") {
            api_infos_table
                .column(3)
                .search(this.value)
                .draw();
        } else {
            api_infos_table
                .column(3)
                .search("")
                .draw();


        }

    });




// 默认查询当前日期的数据
$(document).ready(function(){
    window.onload=function(){
        document.getElementById("summit_btn").click();
    }
    })
var timedata=[]
var charttype = 'line'
var project_list=[]
function getproject(project,Sdate,Edate){//version、apmdate、apmdata是数组
      $.ajax({
          url:"/api_monitor_api/",
          type:'get',
          async: false,
          data: {
                "project":project,
                "sdate":Sdate,
                "edate":Edate
            },
          success:function(data){
              project_list = data['project']

          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }
function getdata(project,apidata,Sdate,Edate,singleapi_data){//version、apmdate、apmdata是数组
      apmdate = getAll(Sdate,Edate)
      timedata = []
      if (apmdate.length >1){
          charttype = 'line'
      }

      $.ajax({
          url:"/api_monitor_api/",
          type:'get',
          async: false,
          data: {
                "project":project,
                "sdate":Sdate,
                "edate":Edate
            },
          success:function(data){
              var errornum=[]
              timedata=data['data'][0]['ctime']
              errornum=data['data'][0]['errornum']
              var apidata_list=data['apidata']
              var json_data =
                  {
                      name: project,
                      data: errornum
                  }
              apidata.push(json_data)


              for(var i=0;i<apidata_list.length;i+=1)
              {
                  var api = data['apidata'][i]['api']
                  var ynum = data['apidata'][i]['errornum']

                  var api_json_data =
                  {
						name: api,
						y: ynum
                  }
                  singleapi_data.push(api_json_data)
              }

              //console.log(singleapi_data)



          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }

var today=new Date();
today = today.format("yyyy-MM-dd").toString()
var startdate = today
var enddate =  today
var apidata=[]
var singleapi_data=[]
getproject('All',startdate,enddate)
//console.log(project_list)
$("#summit_btn").click(function (){
    apidata=[]//每次都将数据清0，不然会一直叠加
    singleapi_data=[]
    var elt =document.getElementById('datetext').value;
    var datevalue = elt.toString()
    startdate = datevalue.split("/")[0].trim()
    enddate = datevalue.split("/")[1].trim()
    if(selectproject=='All' || selectproject==''){
        //selectproject = 'StarHalo'
        //getdata(selectproject,apidata,startdate,enddate,singleapi_data)
        //console.log(singleapi_data)
        selectproject='All'
        for(var i=0;i<project_list.length;i+=1){
            getdata(project_list[i],apidata,startdate,enddate,singleapi_data)
        }
    }else {
        getdata(selectproject,apidata,startdate,enddate,singleapi_data)
    }


  /*
  /*
   * Highcharts
   * ----------------------
   */
  Highcharts.chart('container_type', {
		chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false,
				type: 'pie'
		},
		title: {
				text: 'Error Ratio（'+selectproject+'）'
		},

		tooltip: {
				pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
		},
		plotOptions: {
				pie: {
						allowPointSelect: true,
						cursor: 'pointer',
						dataLabels: {
								enabled: true,
								format: '<b>{point.name}</b>: {point.percentage:.1f} %',
								style: {
								        fontFamily:'宋体',
										color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
								}
						}
				}
		},
		series: [{
				name: 'Brands',
				colorByPoint: true,
				data: singleapi_data
		}]
})
  Highcharts.chart('container_num', {

    chart: {
        type: charttype,

    },
    title: {
        text: 'Error Nums ('+selectproject+')',
        labels: {
	            	formatter: function () {
                    	return this.value
                	},
	                style: {
						color: '#fff'
					}
	            }
    },

    subtitle: {
        text: '',
        labels: {
	            	formatter: function () {
                    	return this.value
                	},
	                style: {
						color: '#fff'
					}
	            }
    },
    xAxis: {
        categories: timedata,
        labels: {
	            	formatter: function () {
                    	return this.value
                	},
	                style: {
						color: '#fff'
					}
	            }
    },
    yAxis: {
        title: {
            text: ''
        },
        labels: {
	            	formatter: function () {
                    	return this.value
                	},
	                style: {
						color: '#fff'
					}
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
    series: apidata
});})


