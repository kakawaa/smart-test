function loading() {
		$('body').loading({
			loadingWidth:120,
			title:'',
			name:'test',
			discription:'',
			direction:'column',
			type:'origin',
			// originBg:'#71EA71',
			originDivWidth:40,
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

var startuptime_table = $('#startuptime_infos_table').DataTable({
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

var performance__table = $('#performance_infos_table').DataTable({
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

// TYPE过滤
$('#type').on('keyup change', function () {
        console.log(this.value)
        // console.log(table.column(2))
        if (this.value == "Time Cost" ) {
            document.getElementById("performacecard_table").style.display="none";
            document.getElementById("timecard_table").style.display="block";

            document.getElementById("scene_lable_timecost").style.display="block";
            document.getElementById("scene_select_timecost").style.display="block";

            document.getElementById("Competitor_lable_timecost").style.display="block";
            document.getElementById("Competitor_select_timecost").style.display="block";

            document.getElementById("summit_btn").style.display="block";
        } else if (this.value == "Performance") {
            document.getElementById("timecard_table").style.display="none";
            document.getElementById("performacecard_table").style.display="block";
            document.getElementById("timecost_chart").style.display="none";

            document.getElementById("scene_lable_timecost").style.display="none";
            document.getElementById("scene_select_timecost").style.display="none";

            document.getElementById("Competitor_lable_timecost").style.display="none";
            document.getElementById("Competitor_select_timecost").style.display="none";

            document.getElementById("summit_btn").style.display="none";


        }else{
            document.getElementById("performacecard_table").style.display="block";
            document.getElementById("timecard_table").style.display="block";

            document.getElementById("scene_lable_timecost").style.display="none";
            document.getElementById("scene_select_timecost").style.display="none";
            document.getElementById("timecost_chart").style.display="none";

            document.getElementById("Competitor_lable_timecost").style.display="none";
            document.getElementById("Competitor_select_timecost").style.display="none";
            document.getElementById("summit_btn").style.display="none";


        }

    });


  /*
   * 获取APM数据
   * ----------------------
   */
  var scene=''
  var competitor=''
  function getdata(pkgname){
      var Version=[]
      var charttype = 'column'
      $.ajax({
          url:"/apm_api/",
          type:'post',
          async:true,
          cache: false,
          data: {
                "pkgname":pkgname,
                "scene":scene,
                "compare_project":competitor
            },
          beforeSend: function () {
                loading();

            },
          complete: function () {
                removeLoading('test');
            },
          success:function(data){
             console.log(data)
             var Time_data=[]
             var Competitor_Time_data=[]
             for(var i =0;i<data['Time_data'].length;i+=1){
                 Time_data.push(data['Time_data'][i])
             }
             for(var i =0;i<data['Compare_data'].length;i+=1){
                 Competitor_Time_data.push(data['Compare_data'][i])
             }
              for(var i =0;i<data['Version'].length;i+=1){
                 Version.push(data['Version'][i])
             }
             var chart = Highcharts.chart('container_timecost', {
                 chart: {
                     type: charttype
                 },
                 title: {
                     text: scene
                 },
                 subtitle: {
                     text: ''
                 },
                 xAxis: {
                     categories: Version
                 },
                 yAxis: {
                     className: 'highcharts-color-1',
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
                     },
                     column: {
                         borderRadius: 5
                     }
                     },
                 series: [{
                     name: projectname,
                     data: Time_data
                 },
                 {
                     name: competitor,
                     data: Competitor_Time_data,
                 }]
             });
              },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }


// 项目过滤
var projectname
$('#project').on('keyup change', function () {
        projectname=this.value
        if (this.value !== "All") {
            startuptime_table.column(1).search(this.value).draw();
            performance__table.column(1).search(this.value).draw();
        } else {
            startuptime_table.column(1).search("").draw();
            performance__table.column(1).search("").draw();


        }

    });

$('#scene_timecost').on('keyup change', function () {
    scene=this.value;
    if (this.value !== "All") {
            startuptime_table.column(3).search(this.value).draw();
        } else {
            startuptime_table.column(3).search("").draw();

        }
});

$('#Competitor_timecost').on('keyup change', function () {
    competitor=this.value;
});

$('#summit_btn').click(function () {
    document.getElementById("timecard_table").style.display="none";
    if(scene && projectname && competitor && competitor!=projectname && scene!='All' && projectname!='All'&& competitor!='All'){
        document.getElementById("timecost_chart").style.display="block";
        getdata(projectname,scene)
    }else {
        if(!projectname){
            alert('project、scene、competitor的值不能为All')
        }else if(!scene){
            alert('project、scene、competitor的值不能为All')
        }else if(!competitor){
            alert('project、scene、competitor的值不能为All')
        }else if(projectname==competitor){
            alert('project和competitor不能相同')
        }else {
            alert('project、scene、competitor的值不能为All')
        }
    }
})

var id
var status
//edit_timecost点击
$('#startuptime_infos_table tbody').on('click', '#edit_timecost', function () {
    id =startuptime_table.row($(this).parents('tr')).data()[0]
    var timecost_info={}

    $.ajax({
        url:"/get_timecost_info/",
        type:'post',
        async: true,
        data: {
            "id":id
        },
        beforeSend:function () {
            loading();
            $('#edit_project').empty()
            $('#timecost_value').empty()
            $('#edit_status').empty()
            $('#edit_scene').empty()
            },
        success:function(data){
            timecost_info = data['data']
            $('#edit_project').val(timecost_info['project'])
            $('#edit_scene').val(timecost_info['scene'])
            $('#timecost_value').val(timecost_info['timecost'])
            status = timecost_info['status']
            console.log(timecost_info['status'])
            $('#edit_status').append('<option>'+timecost_info['status']+'</option>')
            if(timecost_info['status']=='Competitor'){
                $('#edit_status').append('<option>Online</option>');
                $('#edit_status').append('<option>Offline</option>');
                $('#edit_status').append('<option>Delete</option>');
            }else if(timecost_info['status']=='Online'){
                $('#edit_status').append('<option>Offline</option>');
                $('#edit_status').append('<option>Competitor</option>');
                $('#edit_status').append('<option>Delete</option>');
            }else{
                $('#edit_status').append('<option>Online</option>');
                $('#edit_status').append('<option>Competitor</option>');
                $('#edit_status').append('<option>Delete</option>');
            }

        },
        complete:function () {
            removeLoading('test');
            },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            $('#edit_project').val('')
            $('#timecost_value').val('')
        }});





});

$('#startuptime_infos_table tbody').on('click', '#view_timecost', function () {
    id =startuptime_table.row($(this).parents('tr')).data()[0]
    var timecost_info={}

    $.ajax({
        url:"/get_timecost_info/",
        type:'post',
        async: true,
        data: {
            "id":id
        },
        beforeSend:function () {
            loading();

            },
        success:function(data){
            var time_detail = data['time_detail']
            console.log(time_detail)
            if(time_detail){
                var input = eval('(' + time_detail + ')');
            }else{
                var input = time_detail;
            }

            var options = {
		      collapsed: $('#collapsed').is(':checked'),
		      withQuotes: $('#with-quotes').is(':checked')
		    };
            $('#json').jsonViewer(input, options);



        },
        complete:function () {
            removeLoading('test');
            },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            removeLoading('test');
            alert('error')
        }});





});


$('#edit_status').on('keyup change', function () {
    status = this.value
});

//time cost 保存
$('#edit_save').click(function () {
        var project = $('#edit_project').val()
        var timevalue = $('#timecost_value').val()
        var scene = $('#edit_scene').val()

        $.ajax({
            url: "/update_timecost/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                id: id,
                project:project,
                status:status,
                timevalue: timevalue,
                scene:scene
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
                $('#edit_close').click()
                location.reload();
            },
            success: function (data) {
                console.log(data)
            }
        })

})



//添加timecost data
$('#add_save').click(function () {
    var project = $('#add_project').val()
    var version = $('#add_version').val()
    var scene = $('#add_scene').val()
    var timecost = $('#add_timecost').val()
    $.ajax({
            url: "/insert_timecost/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                project: project,
                version:version,
                scene: scene,
                timecost:timecost
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
                $('#add_close').click()
                location.reload()
            },
            success: function (data) {
                console.log(data)
            }
        })
})




