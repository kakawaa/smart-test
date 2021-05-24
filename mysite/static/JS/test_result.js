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


var result_table
$(document).ready(function () {
    document.getElementById("summit_btn").click();
});


$('#summit_btn').click(function () {
        var project = $('#project').val()
        var filter = $('#Filter').val()
        var keyword = $('#keyword_txt').val()
        $.ajax({
            url: "/test_result_api/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                project: project,
                filter: filter,
                keyword: keyword
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
                    className:"text-center"
                }, {
                    field: 'env',
                    title: '<strong>ENV</strong>',
                    sortable: true,
                    className:"text-center"
                }, {
                    field: 'task',
                    title: '<strong>TASK</strong>',
                    sortable: true,
                    className:"text-center"
                }, {
                    field: 'status',
                    title: '<strong>STATUS</strong>',
                    sortable: true,
                    className:"text-center"
                }, {
                    field: 'ctime',
                    title: '<strong>CTIME</strong>',
                    sortable: true,
                    className:"text-center"
                }, {
                    field: 'more',
                    title: '<strong>MORE</strong>',
                    sortable: true,
                    className:"text-center",
                    defaultContent:"<a class=\"btn btn-success btn-sm\" style=\"color: white;cursor:pointer;\" id=\"report_btn\">\n" +
                        "           <i class=\"fa fa-eye\">\n" +
                        "           </i>\n" +
                        "           Report\n" +
                        "           </a>\n"
                }
                ];
                result_table = $('#testresult_table').DataTable({
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
                    data: data['resultdata']
                });

                //report_btn点击
                $('#testresult_table tbody').on('click', '#report_btn', function () {
                    var id =result_table.row($(this).parents('tr')).data()[0];
                    //window.location.href="http://0.0.0.0:8887/test_report/"+id
                    window.location.href="/test_report/"+id
                });


            }
        })
    })


