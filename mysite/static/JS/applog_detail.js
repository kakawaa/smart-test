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
var logcontent = ''
var log_name_list=[]
var old_log_name_list=[]
function getdata(logname,log_detail_name){
      $.ajax({
          url:"/applog_api/",
          type:'get',
          async: true,
          data: {
                "logname":logname,
                "log_detail_name":log_detail_name
            },
          beforeSend:function () {
              loading();
          },
          success:function(data){
              logcontent=data['data']
              log_name_list = data['filelist']
              for(var i=0;i<log_name_list.length;i+=1){
                  old_log_name_list.push(log_name_list[i])
              }

          },
          complete:function () {
              removeLoading('test');
              document.getElementById("logcontent").innerHTML = logcontent;
              if(old_log_name_list.length==log_name_list.length){
                  for (var i = 0; i < log_name_list.length; i++) {
                      $('#type_log').append('<option>' + log_name_list[i] + '</option>')
                  };
              }
          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }
var logname = document.getElementById("logname").innerText
getdata(logname,'')
document.getElementById("logcontent").innerHTML = logcontent
//$("#logcontent").val(logcontent);

$('#type_log').on('keyup change', function () {
    //$('#type_log').empty()
    getdata(logname,this.value)
    });

//复制文本
$(function(){
    $("#copy_btn").click(function () {
        let url_content = $("#logcontent");
        //选择复制的文本
        url_content.select();
        //执行浏览器复制命令
        document.execCommand("copy");
        toastr.success("Copy Success");
    })
})