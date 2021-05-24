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


function loading_actions() {
    $('#actionsmanager').loading({
        loadingWidth:120,
        title:'',
        name:'test1',
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
};


var request_num='100'

//切换num
$('#num').on('keyup change', function () {
    request_num = this.value
    });

var bitable
$(document).ready(function () {
    document.getElementById("summit_btn").click();
});


$('#summit_btn').click(function () {
        // $('#keyword_txt').val('')
        var ad_source_list = 1
        var anm = $('#ANM').val()
        console.log(anm)
        var filter = $('#Filter').val()
        var keyword = $('#keyword_txt').val()
        // var num = request_num
        $.ajax({
            url: "/offline_log_search/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                anm: anm,
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
                var columns = [{
                    field: 'anm',
                    title: '<strong>ANM</strong>',
                    sortable: true
                }, {
                    field: 'subanm',
                    title: '<strong>SUBANM</strong>',
                    sWidth:"80px",
                    sortable: true
                },{
                    field: 'action',
                    title: '<strong>ACTION</strong>',
                    sortable: true,
                    sWidth:"150px",
                    className:"text-center"

                }, {
                    field: 'did',
                    title: '<strong>DID</strong>',
                    sortable: true,
                    sWidth:"200px",
                    className:"text-center"
                }, {
                    field: 'brd',
                    title: '<strong>BRD</strong>',
                    sortable: true,
                    className:"text-center"
                }, {
                    field: 'version',
                    title: '<strong>VERSION</strong>',
                    sortable: true,
                    sWidth:"100px",
                    className:"text-center"
                }, {
                    field: 'content',
                    title: '<strong>CONTENT</strong>',
                    sortable: true,
                    className:"text-center"
                },  {
                    field: 'logtime',
                    title: '<strong>LOGTIME</strong>',
                    sortable: true,
                    sWidth:"90px",
                    className:"text-center"
                }];
                bitable = $('#apploginfo_table').DataTable({
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
                    "columnDefs":[{
                        "targets": [6],
                        render: function (data, type, full, meta) {
                            if (data) {
                                if (data.length > 20) {
                                    return data.substr(0, 10) + "<a id='test' href = 'javascript:void(0);' onclick = 'javascript:searchBtn3(\""+data+"\")' data-toggle=\"modal\" data-target=\"#ModalLong\" >...more</a> ";
                                }else{
                                    return data;
                                }
                            }else {
                                return "";
                            }
                        }
                    }],
                    data: data['logdata']
                });


            }
        })
    })

// //搜索表
// $('#keyword_txt').on('keyup change', function search() {
//     var keyword = document.getElementById("keyword_txt").value
//     var filed = document.getElementById("Filed").value
//     console.log(keyword)
//     if (keyword == "") {
//        bitable.column(0).search("").draw();
//        bitable.column(1).search("").draw();
//        bitable.column(2).search("").draw();
//        bitable.column(3).search("").draw();
//        bitable.column(4).search("").draw();
//        bitable.column(6).search("").draw();
//        bitable.column(7).search("").draw();
//     } else {
//         if(filed=='ALL') {
//             bitable.column(0).search("").draw();
//             bitable.column(1).search("").draw();
//             bitable.column(2).search("").draw();
//             bitable.column(3).search("").draw();
//             bitable.column(4).search("").draw();
//             bitable.column(6).search("").draw();
//             bitable.column(7).search("").draw();
//         }
//         else if(filed=='ANM'){
//             bitable.column(0).search(keyword).draw();
//         }
//         else if(filed=='ACTION'){
//             bitable.column(1).search(keyword).draw();
//          }
//         else if(filed=='DID'){
//             bitable.column(2).search(keyword).draw();
//          }
//         else if(filed=='BRD'){
//             bitable.column(3).search(keyword).draw();
//          }
//         else if(filed=='VERSION'){
//             bitable.column(4).search(keyword).draw();
//          }
//          else if(filed=='PROJECT'){
//             bitable.column(6).search(keyword).draw();
//          }
//          else if(filed=='TYPE'){
//             bitable.column(7).search(keyword).draw();
//          }
//
//         }
// });

// //切换Filed
// $('#Filed').on('keyup change', function () {
//     $('#keyword_txt').val('')
//      bitable.column(0).search("").draw();
//      bitable.column(1).search("").draw();
//      bitable.column(2).search("").draw();
//      bitable.column(3).search("").draw();
//      bitable.column(4).search("").draw();
//      bitable.column(6).search("").draw();
//      bitable.column(7).search("").draw();
//
//     });

function searchBtn3(data) {

    // console.log(id)
    // // id = id.replace(/`/g, "\n")
    // // console.log(id)
    // swal({
    //     title:'Log',
    //      text:  id
    // }
    data = data.replace(/`/g,"\n").replace(/{/g,"\n    {\n        ").replace(/,/g,",\n        ").replace(/}/g,"\n    }").replace(/=/g," = ")
    $('#ModalLong').on('show.bs.modal', function () {
  var button = $(event.relatedTarget) // Button that triggered the modal
  //注意这里的whatever对应前面html代码中button标签下data-whatever属性的后半段
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  //此处即为修改modal的标题
    modal.find('#content').text(data)
    });
    };
    $(function() {
    $(".daterange input").each(function() {
        var $this = $(this);

        $this.daterangepicker({
            locale : {
                "format" : "YYYY-MM-DD",// 显示格式
                "separator" : " / ",// 两个日期之间的分割线
                "applyLabel" : "确定",
                "cancelLabel" : "取消",
                "fromLabel" : "开始",
                "toLabel" : "结束",
                "daysOfWeek" : [ "日", "一", "二", "三", "四", "五", "六" ],
                "monthNames" : [ "一月", "二月", "三月", "四月", "五月", "六", "七月", "八月", "九月", "十月", "十一月", "十二月" ],
                "firstDay" : 1,
                "days":7
            },
            startDate: moment().subtract(0, 'days'),
            endDate: moment()

        }, function(start, end, label) {
            // 点击确定后的事件，下面是为了bootstrap validate得校验，
            // 若未使用，可忽视
            if ($this.parents("form.required-validate").length > 0) {
                var $form = $this.parents("form.required-validate");

                var name = $this.attr("name");
                if ($form.length > 0) {
                    var data = $form.data('bootstrapValidator');
                    data.updateStatus(name, 'NOT_VALIDATED', null)
                    // Validate the field
                    .validateField(name);
                }
            }
        // 设置最小宽度，否则显示不全
        }).css("min-width", "210px").next("i").click(function() {
            // 对日期的i标签增加click事件，使其在鼠标点击时可以拉出日期选择
            $(this).parent().find('input').click();
        });
    });
});