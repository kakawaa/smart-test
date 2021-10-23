/*
 * Author: rafa
 * Date:  11 Jan 2019
 * Description:修改账户密码
 **/

$(function () {
    'use strict'

    $('#sign_in').on('click', function () {
        var account = document.getElementById("account").value
        var password = document.getElementById("password").value
        if (account == '' || password == '') {
            alert('Username or password cannot be empty!')
            return false
        } else {
            $.ajax({
                url: "/login_api/",
                type: "POST",
                async: false,
                data: {
                    username: account,
                    password: password
                },
                success: function (data) {
                    if (data['code'] == 200) {
                        alert('登录成功')
                        //window.location.href = "/dashboard/";
                        return false
                    }
                    else{
                        alert("account or password wrong！")
                    }
                }
            });
        }
    });

    $("#password").keypress(function (event) {
        if (event.which === 13) {
            //点击回车要执行的事件
            var account = document.getElementById("account").value
            var password = document.getElementById("password").value
            if (account == '' || password == '') {
                alert('帐号或密码不能为空！');
            } else {
                $.ajax({
                    url: "/login_api/",
                    type: "POST",
                    async: false,
                    data: {
                        username: account,
                        password: password
                    },
                    success: function (data) {
                        if (data['code'] == 200) {
                            alert('登录成功');
                            //window.location.href = "/dashboard/";
                            return false
                        }
                        else{
                            alert("帐号或密码错误！")
                        }
                    }
                });
            }
        }
    })
});














