
  /*
   * Custom Label formatter
   * ----------------------
   */
  function labelFormatter(label, series) {
    return '<div style="font-size:13px; text-align:center; padding:2px; color: #fff; font-weight: 600;">'
      + label
      + '<br>'
      + Math.round(series.percent) + '%</div>'
  }

// 默认查询当前日期的数据
$(document).ready(function(){
    window.onload=function(){
        document.getElementById("summit_btn").click();
    }
    })

  /*
   * 获取所有日期
   * ----------------------
   */
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


  /*
   * 获取APM过滤器数据
   * ----------------------
   */
  var selectverison = ["3.14","3.15"]
  $(document).ready(function () {
        for (var i = 0; i < selectverison.length; i++) {
            $('#version').append('<option>' + selectverison[i] + '</option>')
        }
    })
  /*
   * 获取APM数据
   * ----------------------
   */

  var apmdate = []
  var charttype = 'column'
  function getdata(version,apmdata,Sdate,Edate){//version、apmdate、apmdata是数组
      apmdate = getAll(Sdate,Edate)
      if (apmdate.length >1){
          charttype = 'line'
      }

      $.ajax({
          url:"/TItest/",
          type:'post',
          async: false,
          data: {
                "version":version,
                "start_date":Sdate,
                "end_date":Edate
            },
          success:function(data){
              var testdata=[]
              for (var j = 0; j < apmdate.length; j+=1) {
                  testdata.push(data['data'][0][j]['apmdata'])
                  var json_data =
                  {
                      name: version,
                      data: testdata
                  }
              }
              apmdata.push(json_data)


          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }


  var apmdata = []
  var today=new Date();
  today = today.format("yyyy-MM-dd").toString()
  var startdate = today
  var enddate =  today
  $("#summit_btn").click(function (){
      apmdata=[]//每次都将数据清0，不然会一直叠加
      var elt =document.getElementById('datetext').value;
      var datevalue = elt.toString()
      startdate = datevalue.split("/")[0].trim()
      enddate = datevalue.split("/")[1].trim()
      console.log(startdate)
      console.log(enddate)
      for (var a =0;a < selectverison.length;a+=1){
          getdata(selectverison[a],apmdata,startdate,enddate)
      }
  /*
   * Highcharts
   * ----------------------
   */
  var chart = Highcharts.chart('container', {
    chart: {
        type: charttype
    },
    title: {
        text: 'Start Up Time'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: apmdate
    },
    yAxis: {
        title: {
            text: 'Time (ms)'
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
    series: apmdata
});
  })

