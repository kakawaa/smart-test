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



var applog_table
$(document).ready(function () {
    document.getElementById("summit_btn").click();
});


$('#summit_btn').click(function () {
        var date = $('#datetext').val().toString()
        startdate = date.split("/")[0].trim()
        enddate = date.split("/")[1].trim()
        console.log(date)
        var project = $('#project').val()
        console.log(project)
        var filter = $('#Filter').val()
        var keyword = $('#keyword_txt').val()
        $.ajax({
            url: "/applog_search_api/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                project: project,
                filter: filter,
                keyword: keyword,
                sdate:startdate,
                edate:enddate
            },

            beforeSend: function () {
                loading();

            },
            complete: function () {
                removeLoading('test');
            },
            success: function (data) {
                console.log(data)
                var columns = [{
                    field: 'id',
                    title: '<strong>ID</strong>',
                    sortable: true,
                    className:"text-center"
                },{
                    field: 'project',
                    title: '<strong>PROJECT</strong>',
                    sortable: true,
                    className:"text-center",
                    sWidth:"160px",
                }, {
                    field: 'version',
                    title: '<strong>VERSION</strong>',
                    sortable: true,
                    className:"text-center"
                }, {
                    field: 'logname',
                    title: '<strong>LOGNAME</strong>',
                    sortable: true,
                    className:"text-center",
                    sWidth:"150px"
                }, {
                    field: 'did',
                    title: '<strong>DID</strong>',
                    sortable: true,
                    className:"text-center",
                    sWidth:"150px",
                }, {
                    field: 'remark',
                    title: '<strong>REMARK</strong>',
                    sortable: true,
                    className:"text-center",
                    sWidth:"150px",

                }, {
                    field: 'ctime',
                    title: '<strong>CTIME</strong>',
                    sortable: true,
                    className:"text-center",
                    sWidth:"100px",
                }, {
                    field: 'more',
                    title: '<strong>MORE</strong>',
                    sortable: true,
                    className:"text-center",
                    sWidth:"60px",
                    defaultContent:"<a class=\"btn btn-success btn-xs\" style=\"color: white;cursor:pointer;\" id=\"view_btn\">\n" +
                        "           <i class=\"fa fa-eye\">\n" +
                        "           </i>\n" +
                        "           View\n" +
                        "           </a>\n" +
                        "<a class=\"btn btn-danger btn-xs\" style=\"color: white;cursor:pointer;\" id=\"file_btn\">\n" +
                        "           <i class=\"fa fa-download\">\n" +
                        "           </i>\n" +
                        "           File\n" +
                        "           </a>\n"
                }
                ];
                applog_table = $('#applog_table').DataTable({
                    "destroy": true,
                    "pageLength": 10,
                    "paging": true,
                    "lengthChange": false,
                    "searching": true,
                    "ordering": false,
                    "info": false,
                    "autoWidth": false,
                    "order": [[0, "desc"]],
                    dom: 't<"bottom"ip><"clear">',
                    columns: columns,
                    data: data['logdata']
                });

                //view_btn点击
                $('#applog_table tbody').on('click', '#view_btn', function () {
                    var logname =applog_table.row($(this).parents('tr')).data()[3];
                    //window.location.href="http://0.0.0.0:8887/test_report/"+id
                    window.location.href="http://ti.flatincbr.com:8887/applog_detail/"+logname
                });

                $('#applog_table tbody').on('click', '#file_btn', function () {
                    var logname =applog_table.row($(this).parents('tr')).data()[3];
                    window.location.href="http://47.106.194.167:8181/nemo/TI/applog/"+logname
                });


            }
        })
    })