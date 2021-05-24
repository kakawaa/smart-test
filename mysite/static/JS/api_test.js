var project = ''
console.log(project)
var env = 'Test'
var taskname = ''
var timercheck = 'false'
var timevalue = '0'
var timetype = 'Min'
var creater = document.getElementById("creater").value
var task_env = 'Test'
var task_project = $('#task_project').val()
var action_type = 'Task'
var apilist = []
var request_txt=''
var response_txt=''
var apiurl = ''

//task_project赋值
$('#task_project').on('keyup change', function () {
    task_project = this.value
    });

//task赋值
$('#task_name').on('keyup change', function () {
    taskname = this.value
    });

//task_env赋值
$('#task_env').on('keyup change', function () {
    task_env = this.value
    });

//timevalue赋值
$('#time_value').on('keyup change', function () {
    timevalue = this.value
    });

//timetype赋值
$('#time_type').on('keyup change', function () {
    timetype = this.value
    });

//checkboxSuccess按钮切换
$('#checkboxSuccess').on('keyup change', function () {
    if (this.checked ===true) {
        timercheck='true';
        //timevalue=$('#time_value').val().trim()
        //console.log(timevalue)
        $("#timer_form").show();
    }
    else {
        document.getElementById("timer_form").style.display="none";

    }

});

//loading效果
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

//json格式化
function parse(str) {
        return JSON.stringify(JSON.parse(str), null, "\t");
    }
//json格式检查
function isJSON(str) {
    if (typeof str == 'string') {
        try {
            var obj=JSON.parse(str);
            if(typeof obj == 'object' && obj ){
                return true;
            }else{
                return false;
            }

        } catch(e) {
           spop({
               template: 'not json , please check request and case!',
               position  : 'top-center',
               style: 'error',
               autoclose: 3000
                });
           return false;
        }
    }
    else{
        spop({
            template: 'not string!',
            position  : 'top-center',
            style: 'error',
            autoclose: 3000
        });
    }
}

//封装解密接口
function getdata(opdetail, cb){
  $.ajax({
     url:"http://14.23.91.210:5907/coder/"+opdetail,
     dataType:'jsonp',
     processData: false,
     type:'post',
     success:function(data){
      cb(data)
     },
     error:function(XMLHttpRequest, textStatus, errorThrown) {
       alert(XMLHttpRequest.status);
       alert(XMLHttpRequest.readyState);
       alert(textStatus);
     }});
 }
//vidmate解密
function vdm_decrypt(){
    var val = $("#response").val();
    try{
        var json_val = JSON.parse(val);
        getdata("vdm_decrypt?data="+encodeURIComponent(json_val['data']), function(val) {
        $('#response').val(parse(val));
        //json美化
        try {
        var input = eval('(' + $('#response').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
	    var options = {
		      collapsed: $('#collapsed').is(':checked'),
		      withQuotes: $('#with-quotes').is(':checked')
		    };
        $('#json').jsonViewer(input, options);
        });}
    catch{
        getdata("vdm_decrypt?data="+encodeURIComponent(val), function(val) {
        $('#response').val(parse(val));
      });}



    return false;
}

function decrypt(){
    var val = $("#response").val();
    try{
        json_val = JSON.parse(val);
        getdata("decrypt?data="+encodeURIComponent(json_val['data']), function(val) {
        $('#response').val(parse(val));
        //json美化
        try {
        var input = eval('(' + $('#response').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
	    var options = {
		      collapsed: $('#collapsed').is(':checked'),
		      withQuotes: $('#with-quotes').is(':checked')
		    };
        $('#json').jsonViewer(input, options);
        });}
    catch{
        getdata("vdm_decrypt?data="+encodeURIComponent(val), function(val) {
        $('#response').val(parse(val));
      });}



    return false;
}

//获取请求内容
function getrequest(type,url){
                $.ajax({
                    url:"/getpost/",
                    type:'post',
                    async: true,
                    data: {
                        "type":type,
                        "url":url
                    },
                    beforeSend:function () {
                        loading();
                        },
                    success:function(data){
                        request_txt= data['result']
                    },
                    complete:function () {
                        removeLoading('test');
                        if(type=='request'){
                            $("#request").val(parse(request_txt));
                        }else{
                            $("#response").val(parse(request_txt));
                        }
                        },
                    error:function(XMLHttpRequest, textStatus, errorThrown) {
                        $("#request").val('no api');;
                    }});
            }
//获取返回内容
function getresponse(payload,url,post_type){
                $.ajax({
                    url:"/apipost/",
                    type:'post',
                    async: true,
                    data: {
                        "payload":payload,
                        "url":url,
                        "post_type":post_type
                    },
                    beforeSend:function () {
                        loading();
                        },
                    success:function(data){
                        response_txt= data['result']
                    },
                    complete:function () {
                        removeLoading('test');
                        $("#response").val(parse(response_txt));
                    },
                    error:function(XMLHttpRequest, textStatus, errorThrown) {
                        $("#response").val('no api');
                    }});
            }

var apitest_table = $('#apitest_table').DataTable({
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

//project过滤
$('#type_project').on('keyup change', function () {
    task_project = this.value;
    if (task_project=='All'){
             apitest_table
            .column(1)
            .search('')
            .draw();
         }else{
             apitest_table
            .column(1)
            .search(this.value)
            .draw();
         }
});

//post_project过滤
$('#type_project_post').on('keyup change', function () {
    $('#response').val('')
    project = this.value;
     if (action_type=='Post'){
        $.ajax({
                    url:"/getapi/",
                    type:'post',
                    async: true,
                    data: {
                        "env":env,
                        "project":project
                    },
                    beforeSend:function () {
                        loading();
                        },
                    success:function(data){
                        $('#type_api').empty()
                        apilist= data['result']
                        for (var i = 0; i < apilist.length; i++) {
                            $('#type_api').append('<option>' + apilist[i] + '</option>')
                        };
                    },
                    complete:function () {
                        removeLoading('test');
                        //console.log(apilist[0])
                        getrequest('request',apilist[0])
                        //getrequest('response',apilist[0])
                        apiurl = apilist[0]
                        },
                    error:function(XMLHttpRequest, textStatus, errorThrown) {
                        alert('没有api信息');
                    }});
    }else {
         if (project=='All'){
             apitest_table
            .column(1)
            .search('')
            .draw();
         }else{
             apitest_table
            .column(1)
            .search(this.value)
            .draw();
         }

     }
});
//按env过滤
$('#type_env').on('keyup change', function () {
    $('#response').val('')
    env = this.value;
    if (action_type=='Post'){
        $.ajax({
                    url:"/getapi/",
                    type:'post',
                    async: true,
                    data: {
                        "env":env,
                        "project":project
                    },
                    beforeSend:function () {
                        loading();
                        },
                    success:function(data){
                        $('#type_api').empty()
                        apilist= data['result']
                        for (var i = 0; i < apilist.length; i++) {
                            $('#type_api').append('<option>' + apilist[i] + '</option>')
                        };
                    },
                    complete:function () {
                        removeLoading('test');
                        //console.log(apilist[0])
                        getrequest('request',apilist[0])
                        //getrequest('response',apilist[0])
                        apiurl = apilist[0]
                        },
                    error:function(XMLHttpRequest, textStatus, errorThrown) {
                        alert(XMLHttpRequest.status);
                    }});
    }else {
        apitest_table
            .column(2)
            .search(this.value)
            .draw();
    }
});

//task过滤
$('#keyword_txt').on('keyup change', function search() {
    var keyword = document.getElementById("keyword_txt").value
    if (keyword == "") {
        apitest_table.column(3).search("").draw();
    } else {
        apitest_table.column(3).search(keyword).draw();
    }

});

//添加task
$('#task_save').click(function () {
    $.ajax({
            url: "/insert_task/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                project: task_project,
                env:task_env,
                taskname: taskname,
                timercheck:timercheck,
                timevalue: timevalue,
                timetype:timetype,
                creater:creater
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
                $('#task_close').click()
                location.reload()
            },
            success: function (data) {
                console.log("taskname:"+taskname)
                console.log("project:"+project)
                console.log("env:"+env)
                console.log("timercheck:"+timercheck)
                console.log("timevalue:"+timevalue)
                console.log("timetype:"+timetype)
                console.log("data:"+data)
                spop({
                    template: 'success',
                    position  : 'top-center',
                    style: 'success',
                    autoclose: 2000
                });
            }
        })
})

//run_btn点击
$('#apitest_table tbody').on('click', '#run_btn', function () {
    var id =apitest_table.row($(this).parents('tr')).data()[0]
    var project =apitest_table.row($(this).parents('tr')).data()[1]
    var env =apitest_table.row($(this).parents('tr')).data()[2]
    var task =apitest_table.row($(this).parents('tr')).data()[3]
    var creater = apitest_table.row($(this).parents('tr')).data()[5]
    var result = 'None'
    $.ajax({
            url: "/update_task/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                update_type:'status',
                id: id,
                status:'Running'
            },

            beforeSend: function () {
                //LoadStart();
                toastr.success("Start Running 【"+task+"】");

            },
            complete: function () {
                $.ajax({
                    url: "/run_task/",
                    type: "POST",
                    async:true,
                    cache: false,
                    data: {
                        id:id,
                        project: project,
                        task:task,
                        env:env,
                        creater:creater
                    },

                    beforeSend: function () {},
                    complete: function () {
                        $.ajax({
                            url: "/update_task/",
                            type: "POST",
                            async:true,
                            cache: false,
                            data: {
                                update_type:'status',
                                id: id,
                                status:result
                            },

                            beforeSend: function () {},
                            complete: function () {
                                location.reload();
                            },
                            success: function (data) {
                                console.log(data)
                            },
                        })

                    },
                    success: function (data) {
                        console.log(data)
                        result=data['status']
                    },
                    error:function(XMLHttpRequest, textStatus, errorThrown) {
                        alert('Do not find api info !!!');
                        result='Error'

                    }

                })
            },
            success: function (data) {
                console.log(data)
            }
        })


});

//stop_btn点击
$('#apitest_table tbody').on('click', '#stop_btn', function () {
    var id =apitest_table.row($(this).parents('tr')).data()[0]
    $.ajax({
            url: "/update_task/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                update_type:'status',
                id: id,
                status:'None'
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
                location.reload()
            },
            success: function (data) {
                console.log(data)
            }
        })

});

//add_case点击
var id
var task
$('#apitest_table tbody').on('click', '#add_case', function () {
    var creater = apitest_table.row($(this).parents('tr')).data()[5]
    console.log(creater)
    if(creater!="TI"){
        $('#case_api').removeAttr('disabled')
    }else {
        $('#case_api').removeAttr('disabled')
    }
    id =apitest_table.row($(this).parents('tr')).data()[0]
    var project =apitest_table.row($(this).parents('tr')).data()[1]
    var env =apitest_table.row($(this).parents('tr')).data()[2]
    task = apitest_table.row($(this).parents('tr')).data()[3]
    var url = ''
    var request_content = ''
    var value_content = ''
    $('#case_project').empty()
    $('#case_env').empty()
    $('#case_project').append('<option>' + project + '</option>')
    $('#case_env').append('<option>' + env + '</option>')
    $.ajax({
        url:"/getapi/",
        type:'post',
        async: true,
        data: {
            "task":task
        },
        beforeSend:function () {
            loading();
            $('#case_api').empty()
            $('#case_request').empty()
            $('#case_value').empty()
        },
        success:function(data){
            url = data['url']
            request_content = data['request_content']
            value_content = data['response_content']
            console.log(url)
            $('#case_api').val(url)
            if(isJSON(request_content) && isJSON(value_content)){
                $('#case_request').val(parse(request_content))
                $('#case_value').val(parse(value_content))
            }else{
                $('#case_request').val(request_content)
                $('#case_value').val(value_content)
            }

        },
        complete:function () {
            removeLoading('test');
            },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            $('#case_request').val('')
            $('#case_value').val('')
        }});




});

//添加case_save
$('#case_save').click(function () {
        console.log(id)
        var request_content = $('#case_request').val()
        var value_content = $('#case_value').val()
        var case_api = $('#case_api').val().trim()
        if(isJSON(request_content) && isJSON(value_content)){
            $.ajax({
            url: "/update_case/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                id: id,
                api:task,
                url:case_api,
                request_content: request_content,
                case:value_content
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
                $('#case_close').click()
                //location.reload();
            },
            success: function (data) {
                console.log("case"+value_content)
                spop({
                    template: 'success',
                    position  : 'top-center',
                    style: 'success',
                    autoclose: 2000
                });
            }
        })
        }else {
            console.log('not json')
        }
})


//edit_task点击
$('#apitest_table tbody').on('click', '#edit_task', function () {

    var id =apitest_table.row($(this).parents('tr')).data()[0]
    var taskinfo={}
    var timercheck = 'true'
    var task_env = 'Test'
    var task_timetype = 'Min'
    //edit_checkboxSuccess按钮切换
    $('#edit_checkboxSuccess').on('keyup change', function () {
        if (this.checked ===true) {
            timercheck = 'true'
            $("#edit_timer_form").show();
        }
        else {
            timercheck='false'
            document.getElementById("edit_timer_form").style.display="none";

        }

    });

    $.ajax({
        url:"/get_task/",
        type:'post',
        async: true,
        data: {
            "id":id
        },
        beforeSend:function () {
            loading();
            $('#case_api').empty()
            $('#edit_task_project').empty()
            $('#edit_task_name').empty()
            $('#edit_task_env').empty()
            $('#edit_checkboxSuccess').removeAttr("checked")
        },
        success:function(data){
            taskinfo = data['data']
            $('#edit_task_project').val(taskinfo['project'])
            $('#edit_task_name').val(taskinfo['task'])
            task_env=taskinfo['env']
            $('#edit_task_env').append('<option>'+taskinfo['env']+'</option>')
            if(taskinfo['env']=='Test'){
                $('#edit_task_env').append('<option>Prod</option>');
            }else{
                $('#edit_task_env').append('<option>Test</option>');
            }
            console.log(taskinfo['timer'])

            if(taskinfo['timer']=='true'){
                $('#edit_checkboxSuccess').attr("checked","checked")
                $("#edit_timer_form").show();
            }else{
                timercheck = 'false'
                $('#edit_checkboxSuccess').removeAttr("checked")
                $("#edit_timer_form").hide();
            }
            $('#edit_time_value').val(taskinfo['timevalue'])
        },
        complete:function () {
            removeLoading('test');
            },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            $('#case_request').val('')
            $('#case_value').val('')
        }});

    $('#edit_task_env').on('keyup change', function () {
            task_env = this.value
        });

    $('#edit_time_type').on('keyup change', function () {
            task_timetype = this.value
        });
    //task保存
    $('#edit_task_save').click(function () {
        var project = $('#edit_task_project').val()
        var timevalue = $('#edit_time_value').val()

        $.ajax({
            url: "/update_task/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                id: id,
                project:project,
                env:task_env,
                timercheck: timercheck,
                timetype:task_timetype,
                timevalue:timevalue
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
                $('#edit_task_close').click()
                location.reload();
            },
            success: function (data) {
                console.log(data)
            }
        })

})


});


//action切换
$('#action_type').on('keyup change', function () {
        action_type = this.value
        if (action_type == "Post") {
            project= $('#type_project_post').val()
            document.getElementById("tableform").style.display="none";
            document.getElementById("keywordfrom").style.display="none";
            document.getElementById("task_btn").style.display="none";
            document.getElementById("jsoncard").style.display="none";
            document.getElementById("select_project").style.display="none";
            $('#apitxt').show()
            $('#apitable_form').show()
            $('#select_api').show()
            $('#post_btn').show()
            $('#decode_btn').show()
            $('#request').show()
            $('#response').show()
            $('#select_project_post').show()
            //project赋值
            $.ajax({
                    url:"/getapi/",
                    type:'post',
                    async: true,
                    data: {
                        "env":env,
                        "project":project
                    },
                    beforeSend:function () {
                        loading();
                        },
                    success:function(data){
                        $('#type_api').empty()
                        apilist= data['result']
                        for (var i = 0; i < apilist.length; i++) {
                            $('#type_api').append('<option>' + apilist[i] + '</option>')
                        };
                    },
                    complete:function () {
                        removeLoading('test');
                        //console.log(apilist[0])
                        getrequest('request',apilist[0])
                        //getrequest('response',apilist[0])
                        apiurl = apilist[0]
                        },
                    error:function(XMLHttpRequest, textStatus, errorThrown) {
                        alert('no api');
                    }});

            $('#type_api').on('keyup change', function () {
                apiurl = this.value
                getrequest('request',apiurl)
                getrequest('response',apiurl)
            });
        }
        else {
            $('#tableform').show()
            $('#keywordfrom').show()
            $('#task_btn').show()
            $('#select_project').show()
            document.getElementById("apitable_form").style.display="none";
            document.getElementById("select_api").style.display="none";
            document.getElementById("post_btn").style.display="none";
            document.getElementById("apitxt").style.display="none";
            document.getElementById("decode_btn").style.display="none";
            document.getElementById("select_project_post").style.display="none"
        }

});

//post按钮点击
$(function() {
    $("#post_btn").click(function () {
        var reg_curl = RegExp(/curl/);
        var reg_get = RegExp(/http/);
        var apirequest = $("#request").val()
        if(apirequest.match(reg_curl)){
            getresponse(apirequest,apiurl,'curl')
        }
        else if(apirequest.match(reg_get)){
             getresponse(apirequest,apiurl,'get')
        }
        else{
            if(isJSON(apirequest)){
            getresponse(apirequest,apiurl,'nomal')
        }else {
            console.log('not json')
        }
        }
    })
})

//解密点击
$(function(){
    $("#decode_btn").click(function () {
        document.getElementById("jsoncard").style.display="block";
        decrypt();
        vdm_decrypt();
        $("html,body").animate({scrollTop: $("#json").offset().top}, 1000);
    })
})
