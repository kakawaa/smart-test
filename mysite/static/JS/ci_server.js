var action_type=''
var action_role1= ''
var action_role2= ''
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
// 切换类型
$('#action_type').on('keyup change', function () {
        action_type = this.value
        if (this.value === "Upload File") {
            document.getElementById("select1").style.display="block"
            document.getElementById("select0").style.display="none";
            document.getElementById("select3").style.display="none"
            document.getElementById("select2").style.display="none"
            document.getElementById("gradle").style.display="block";

        } else if(this.value === "Restart Service") {
            $('#commandtxt').val('')
            document.getElementById("select2").style.display="block"
            document.getElementById("select0").style.display="none";
            document.getElementById("select1").style.display="none";
            document.getElementById("select3").style.display="none"
            document.getElementById("gradle").style.display="none";

        }
        else if(this.value === "Server") {
            $('#commandtxt').val('')
            document.getElementById("select3").style.display="block"
            document.getElementById("select2").style.display="none"
            document.getElementById("select0").style.display="none";
            document.getElementById("select1").style.display="none";
            document.getElementById("gradle").style.display="none";

        }
        else {
            $('#commandtxt').val('')
            document.getElementById("select0").style.display="block"
            document.getElementById("select1").style.display="none";
            document.getElementById("select2").style.display="none";
            document.getElementById("select3").style.display="none"
            document.getElementById("gradle").style.display="none";
        }

    });

$('#type_1').on('keyup change', function () {
        action_role1 = this.value
        if (this.value === "Gradle") {
            getcontent('Upload File','Gradle','1')
            $("#commandtxt").val(lscontent)
            //document.getElementById("commandtxt").innerHTML = lscontent

        } else {
            //document.getElementById("commandtxt").innerHTML = ''
            $("#commandtxt").val('')
        }

    });



var lscontent = ''
var process = ''
function getcontent(action,type,ls){
      $.ajax({
          url:"/ci_server_api/",
          type:'get',
          async: false,
          data: {
                "action":action,
                "type":type,
                "ls":ls
            },
          success:function(data){
              lscontent= data['content']
          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }

function downloadfile(action,type,filelink){
      $.ajax({
          url:"/ci_server_api/",
          type:'get',
          async: true,
          data: {
                "action":action,
                "type":type,
                "filelink":filelink
            },
          beforeSend:function () {
              loading();
          },
          success:function(data){
              var result= data['result']
              if(result=='success'){

                  //getcontent('Gradle','1')
                  //document.getElementById("commandtxt").innerHTML = lscontent
                  toastr.success("Download Success");
                  //document.getElementById("commandtxt").innerHTML = 'Success'
              }
          },
          complete:function () {
              removeLoading('test');
              getcontent('Upload File','Gradle','1');
              $("#commandtxt").val(lscontent);
          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }
function getprocess(action,type,Sprocess){
      $.ajax({
          url:"/ci_server_api/",
          type:'get',
          async: true,
          data: {
                "action":action,
                "type":type,
                "Sprocess":Sprocess
            },
          success:function(data){
              var result= data['result']
              process = result
          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }
function restart_server(action,type,Sprocess){
      $.ajax({
          url:"/ci_server_api/",
          type:'get',
          async: true,
          data: {
                "action":action,
                "type":type,
                "Sprocess":Sprocess
            },
          beforeSend:function () {
              loading();
          },
          success:function(data){
              var result= data['result']
              process = result
              if (Sprocess){
                  console.log(process)
              }else{
                  if(result==1){
                  toastr.success("Restart Success");
                  }else {
                      toastr.success("Restart Fail");
                  }
              }

          },
          complete:function () {
              removeLoading('test');
              $("#commandtxt").val(process);
          },
          error:function(XMLHttpRequest, textStatus, errorThrown) {
              alert(XMLHttpRequest.status);
              alert(XMLHttpRequest.readyState);
              alert(textStatus);
          }});
  }



//console.log(filelink)
$('#type_2').on('keyup change', function () {
    action_role2 = this.value
    if (action_role2){
        restart_server('Restart Service',action_role2,1)
    }else {
        $("#commandtxt").val('');
    }

    });

$(function(){
    $("#summit_btn").click(function () {
        var filelink = $("#filelink").val().trim()
        //download file
        if (action_type=='Upload File'){
            if(filelink && action_role1=='Gradle'){
                downloadfile('Upload File','Gradle',filelink);
            }else{
                $("#commandtxt").val('no file');
            }
        }else {
            if(action_role2){
                restart_server('Restart Service',action_role2,'')
            }else{
                $("#commandtxt").val('Please select restart type');
            }
        }
    })
})