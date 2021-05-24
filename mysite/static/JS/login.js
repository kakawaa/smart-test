$(function () {
    // tabSwicth
    let phoneTabcont = $(".tabContentPhone");
    let accountTabcont = $(".tabContentAccount");
    $("ul.tabBoxSwitchUl").on('click', 'li', function () {
        let i = $(this).index();
        // $(this).attr("data-id",i);
        // console.log(i);
        $(this).addClass("tab-active").siblings('li').removeClass("tab-active");
        $("div.tabcont").eq(i).addClass("active").siblings().removeClass("active");

        // let module;//smsFrom accountFrom
        formType(i);
    });


    $("button.selectBtn").click(function (e) {
        if ($(".selectConentent").is(':hidden')) {
            $(".selectConentent").show();

        } else {
            $(".selectConentent").hide();
        }
        $(document).one('click', function () {
            $(".selectConentent").hide();
        });
        e.stopPropagation();
    });
    $(".selectConentent").on('click', function (e) {
        e.stopPropagation();
    })

    function chooseBtn() {
        $("button[data-type='option']").each(function () {
            $(this).click(function () {
                let txt = $(this).text();
                $("button[data-type='selected']").attr("data-fid", $(this).index());
                $("button[data-type='selected'] span").text(txt);
                $(".selectConentent").hide();
                $(".selectOptions").scrollTop($(this).index() * 40);
            });
            $(this).hover(function () {
                $(this).css("background-color", "#f6f6f6");
            }, function () {
                $(this).css("background-color", "#ffffff");
            });
        });
    };


    // ercode tab
    $(".swicth-ercode").click(function (e) {
        e.preventDefault();
        $("form#form_key").hide();
        $(".ercodeSignBox").show();
        makeCode();
    });
    $(".switch-input").click(function (e) {
        e.preventDefault();
        $("form#form_key").show();
        $(".ercodeSignBox").hide();
    });


});