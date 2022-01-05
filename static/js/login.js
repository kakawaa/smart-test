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
            Spop(SPOP_TYPE['error'],'帐号或密码不能为空')
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
                        window.location.href = "/builder/home";
                        return false
                    }
                    else{
                        Spop(SPOP_TYPE['error'],'帐号或密码错误')
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
                Spop(SPOP_TYPE['error'],'帐号或密码不能为空')
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
                            window.location.href = "/builder/home";
                            return false
                        }
                        else{
                            Spop(SPOP_TYPE['error'],'帐号或密码错误')
                        }
                    }
                });
            }
        }
    })

    $('#create_account').on('click', function () {
        let new_account = document.getElementById("new_account").value
        let new_password = document.getElementById("new_password").value
        let confirm_password = document.getElementById("confirm_password").value
        if (new_account == '' || new_password == '') {
            Spop(SPOP_TYPE['error'],'帐号或密码不能为空')
            return false
        }else if (confirm_password != new_password){
            Spop(SPOP_TYPE['error'],'密码不一致')
        }else {
            $.ajax({
                url: "/sign_up_api/",
                type: "POST",
                async: false,
                data: {
                    username: new_account,
                    password: new_password
                },
                success: function (data) {
                    if (data['code'] == 200) {
                        window.location.href = "/builder/home";
                        return false
                    }
                    else{
                        Spop(SPOP_TYPE['warning'],'账户已经存在')
                    }
                }
            });
        }
    });

    $("#new_password").keypress(function (event) {
        if (event.which === 13) {
            let new_account = document.getElementById("new_account").value
            let new_password = document.getElementById("new_password").value
            let confirm_password = document.getElementById("confirm_password").value
            if (new_account == '' || new_password == '') {
                Spop(SPOP_TYPE['error'],'帐号或密码不能为空')
            }
            else if (confirm_password != new_password){
                Spop(SPOP_TYPE['error'],'密码不一致')
            } else {
                $.ajax({
                    url: "/sign_up_api/",
                    type: "POST",
                    async: false,
                    data: {
                        username: new_account,
                        password: new_password
                    },
                    success: function (data) {
                        if (data['code'] == 200) {
                            window.location.href = "/builder/home";
                            return false
                        }
                        else{
                            Spop(SPOP_TYPE['warning'],'账户已经存在')
                        }
                    }
                });
            }
        }
    })

    var login_api_url = encodeURIComponent('http://0.0.0.0:5656/scan_login_api');
    var goto = encodeURIComponent('https://oapi.dingtalk.com/connect/oauth2/sns_authorize?appid=xxxx&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=' + login_api_url)

    var obj = DDLogin({
        id: "login_container",
        goto: goto,
        style: "border:none;background-color:#FFFFFF;",
        width: "300",
        height: "310"
    });

    var hanndleMessage = function (event) {
        var origin = event.origin;
        if (origin == "https://login.dingtalk.com") {
            var loginTmpCode = event.data;
            console.log("loginTmpCode", loginTmpCode);
            var url2 = "https://oapi.dingtalk.com/connect/oauth2/sns_authorize?appid=xxxxx" +
                "&response_type=code&scope=snsapi_login_api&state=STATE&redirect_uri=" + login_api_url + "&loginTmpCode=" + loginTmpCode;
            $.ajax({
                url: "/scan_login/",
                type: "POST",
                async: false,
                data: {
                    ding_url: url2,
                },
                success: function (data) {
                    console.log(data)
                    if (data['code'] == 200) {
                        Spop(SPOP_TYPE['success'],'登录成功')
                        window.location.href = "/builder/home";
                        return false
                    }
                    if (data['code'] == 202) {
                        Spop(SPOP_TYPE['error'],'登录失败')
                        return false
                    }
                }
            });
            return false;
        }};

    if (typeof window.addEventListener != 'undefined') {
        window.addEventListener('message', hanndleMessage, false);
    } else if (typeof window.attachEvent != 'undefined') {
        window.attachEvent('onmessage', hanndleMessage);
    };
});














