$('#change_btn').on('click', function () {
        var old_pwd = document.getElementById("old_pwd").value
        var new_pwd1 = document.getElementById("new_pwd").value
        var new_pwd2 = document.getElementById("confirm").value
        if (new_pwd1 =='' || old_pwd=='' || new_pwd2=='') {
            toastr.error('密码不能为空！');
            return false
        }else{
            if(new_pwd1 != new_pwd2){
                toastr.warning('新密码不一致！');
                document.getElementById("new_pwd").value = ''
                document.getElementById("confirm").value = ''
                return  false
            }else {
                $.ajax({
                    url: "/change_password_api/",
                    type: "POST",
                    async: false,
                    data: {
                        old_pwd: old_pwd,
                        new_pwd: new_pwd1
                    },
                    success: function (data) {
                        if (data['code']==200){
                            toastr.success('修改成功！');
                            document.getElementById("new_pwd").value = ''
                            document.getElementById("confirm").value = ''
                            document.getElementById("old_pwd").value = ''
                            return  false
                        }if (data['code']==202) {
                            toastr.error ("密码修改失败，原密码错误！")
                            document.getElementById("old_pwd").value = ''
                            return  false
                        }

                    }
                });return false;
        }
        }
    })