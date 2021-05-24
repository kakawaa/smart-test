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

function parse(str) {
        return JSON.stringify(JSON.parse(str), null, "\t");
    }

var options = {
    collapsed: $('#collapsed').is(':checked'),
    withQuotes: $('#with-quotes').is(':checked')
};
function getdata(opdetail, cb){
  $.ajax({
     url:"http://14.23.91.210:5907/coder/"+opdetail,
     dataType:'jsonp',
     processData: false,
     type:'get',
     success:function(data){
      cb(data)
     },
     error:function(XMLHttpRequest, textStatus, errorThrown) {
       alert(XMLHttpRequest.status);
       alert(XMLHttpRequest.readyState);
       alert(textStatus);
     }});
 }

function decrypt(){
      var val = $("#tb_decrypt").val()
      try{
        json_val = JSON.parse(val);
        getdata("decrypt?data="+encodeURIComponent(json_val['data']), function(val) {
        $('#tb_decrypt').val(parse(val));
        //jsonview
        try {
        var input = eval('(' + $('#tb_decrypt').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
        $('#tb_decrypt_json').jsonViewer(input, options);
      });}
      catch{
        getdata("decrypt?data="+encodeURIComponent(val), function(val) {
        $('#tb_decrypt').val(val);
        $('#tb_decrypt').val(parse(val));
        $('#tb_decrypt').val(parse(val));
        //jsonview
        try {
        var input = eval('(' + $('#tb_decrypt').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
        $('#tb_decrypt_json').jsonViewer(input, options);
      });}
      return false;
    }

function encrypt(){
    var val = $("#tb_decrypt").val();
      getdata("encrypt?data="+encodeURIComponent(val), function(val) {
        $("#tb_decrypt").val(val);

      });
      return false;
  }

function tranit_decrypt(){
    var val = $("#tb_tranit_decrypt").val();
      getdata("decrypt_custt?anm="+$("#tb_decrypt_cust_anm").val()+"&data="+encodeURIComponent(val), function(val) {
        $("#tb_tranit_decrypt").val(val);
      });
      return false;
  }
function vdm_decrypt(){
      var val = $("#tb_vdm_decrypt").val();
      try{
        json_val = JSON.parse(val);
        getdata("vdm_decrypt?data="+encodeURIComponent(json_val['data']), function(val) {
        $('#tb_vdm_decrypt').val(parse(val));
        //jsonview
        try {
        var input = eval('(' + $('#tb_vdm_decrypt').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
        $('#tb_vdm_decrypt_json').jsonViewer(input, options);
      });}
      catch{
        getdata("vdm_decrypt?data="+encodeURIComponent(val), function(val) {
        $('#tb_vdm_decrypt').val(parse(val));
        //jsonview
        try {
        var input = eval('(' + $('#tb_vdm_decrypt').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
        $('#tb_vdm_decrypt_json').jsonViewer(input, options);
      });}
      return false;
    }
function vdm_encrypt(){
    var val = $("#tb_vdm_decrypt").val();
      getdata("vdm_encrypt?data="+encodeURIComponent(val), function(val) {
        $("#tb_vdm_decrypt").val(val);
      });
      return false;
  }
function vdm_decrypt_new(){
      var val = $("#tb_vdm_decrypt_new").val();
      console.log(val)
      var crypt = $("#tb_vdm_decrypt_new_crypt").val();
      getdata("vdm_decrypt_new?crypt="+crypt+"&data="+encodeURIComponent(val), function(val) {
        $("#tb_vdm_decrypt_new").val(parse(val));
        //jsonview
        try {
        var input = eval('(' + $('#tb_vdm_decrypt_new').val() + ')');
        }
        catch (error) {
		      return alert("Cannot eval JSON: " + error);
		    }
        $('#tb_vdm_decrypt_new_json').jsonViewer(input, options);
      });

      return false;
}
function vdm_encrypt_new(){
    var val = $("#tb_vdm_decrypt_new").val();
    var crypt = $("#tb_vdm_decrypt_new_crypt").val();
      getdata("vdm_encrypt_new?crypt="+crypt+"&data="+encodeURIComponent(val), function(val) {
        $("#tb_vdm_decrypt_new").val(val);
      });
      return false;
  }

//edit_checkboxSuccess按钮切换
$('#edit_checkboxSuccess').on('keyup change', function () {
        if (this.checked ===true) {
            $("#tb_decrypt_json").show();
            $("#tb_vdm_decrypt_json").show();
            $("#tb_vdm_decrypt_new_json").show();
            document.getElementById("tb_decrypt").style.display="none";
            document.getElementById("tb_vdm_decrypt").style.display="none";
            document.getElementById("tb_vdm_decrypt_new").style.display="none";
        }
        else {
            $("#tb_decrypt").show();
            $("#tb_vdm_decrypt").show();
            $("#tb_vdm_decrypt_new").show();
            document.getElementById("tb_decrypt_json").style.display="none";
            document.getElementById("tb_vdm_decrypt_json").style.display="none";
            document.getElementById("tb_vdm_decrypt_new_json").style.display="none";
        }

    });

var user_id = $('#uid').val()
var score = $('#score').val()

//user_id
$('#uid').on('keyup change', function () {
    user_id = this.value
    });

//user_id
$('#score').on('keyup change', function () {
    score = this.value
    });

//更新分数
$('#update_score').click(function () {
        $.ajax({
            url: "/galo_test/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                action: 'update',
                user_id: user_id,
                score: score
            },

            beforeSend: function () {
                $('#galo_result').val('updating...')
            },
            complete: function () {
                var result
                $.ajax({
                    url: "/galo_test/",
                    type: "POST",
                    async:true,
                    cache: false,
                    data: {
                        action: 'search',
                        user_id: user_id
                    },

                    beforeSend: function () {},
                    complete: function () {
                        //$('#galo_result').val(result)
                    },
                    success: function (re) {
                        result = re
                        console.log(re)
                        try{
                            $('#galo_result').val("修改之后的分数："+re['data'][0]['score'].toString())
                        }catch (e) {
                            $('#galo_result').val('没有查到记录')
                        }

                    }
        })
            },
            success: function (data) {
                console.log(data)
                //$('#galo_result').val(data['status'])
            }
        })
    })

//刷新缓存
$('#refresh_redis').click(function () {
        $.ajax({
            url: "/galo_test/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                action: 'redis',
                user_id: user_id
            },

            beforeSend: function () {
                $('#galo_result').val('refreshing...')
            },
            complete: function () {
            },
            success: function (data) {
                console.log(data)
                $('#galo_result').val("offline:\n"+data['offline']+'\n'+"online:\n"+data['online'])
            }
        })
    })

//审核提现
$('#review').click(function () {
        $.ajax({
            url: "/galo_test/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                action: 'review',
                user_id: user_id,
                flag: 'true'
            },

            beforeSend: function () {
                $('#galo_result').val('reviewing...')
            },
            complete: function () {

            },
            success: function (data) {
                console.log(data)
                $('#galo_result').val("审核状态："+data['wd_status'].toString())
            }
        })
    })

//拒绝提现
$('#reject').click(function () {
        $.ajax({
            url: "/galo_test/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                action: 'review',
                user_id: user_id,
                flag: 'false'
            },

            beforeSend: function () {
                $('#galo_result').val('rejecting...')
            },
            complete: function () {

            },
            success: function (data) {
                console.log(data)
                $('#galo_result').val("审核状态："+data['wd_status'].toString())
            }
        })
    })


$('#get_phone').click(function () {
        var anm = $('#anm option:selected').val()
        var prefix = $('#phone_type option:selected').val()

        console.log(prefix)

        $.ajax({
            url: "/make_phone/",
            type: "POST",
            async:true,
            cache: false,
            data: {
                anm: anm,
                prefix:prefix.replace('+','')
            },

            beforeSend: function () {
                $('#phone_list').val('waiting...')
            },
            complete: function () {

            },
            success: function (data) {
                var reg = new RegExp(",","g")
                console.log(data)
                $('#phone_list').val(String(data['data']).replace(reg,'\n'))
            }
        })
    })