var elt = $('#test');
elt.tagsinput({});


// $('.select2').select2({
//         allowClear: true,
//         tags: true
//     }
// )
// $("ul.select2-selection__rendered").sortable({
//       containment: 'parent'
//   })

// $("select").on("select2:select", function (evt) {
//   var element = evt.params.data.element;
//   var $element = $(element);
//   $element.detach();
//   $(this).append($element);
//   $(this).trigger("change");
// });

// 大表格
var table = $('#apk_infos_table').DataTable({
    "pageLength": 10,
    "paging": true, <!-- 允许分页 -->
    "lengthChange": false, <!-- 允许改变每页显示的行数 -->
    "searching": true, <!-- 允许内容搜索 -->
    "ordering": false, <!-- 允许排序 -->
    "info": false, <!-- 显示信息 -->
    "autoWidth": false, <!-- 固定宽度 -->
    "pagingType": "full_numbers",
    "language": {
        "paginate": {
            "next": ">",
            "previous": "<"
        },
    },
    "order": [[0, "desc"]],
    dom: 't<"bottom"ip><"clear">',
    "columnDefs": [
        {"orderable": false, "targets": -1}
    ]
});
// 初始化

// 筛选项目
$('#all_apk_name').on('keyup change', function () {
    // console.log(this.value)
    // console.log(table.column(2))
    if (this.value !== "All") {
        table
            .column(0)
            .search(this.value)
            .draw();
    } else {
        table
            .column(0)
            .search("")
            .draw();


    }

});


// 筛选列
$('#search_input').on('keyup change', function search() {
    col = document.getElementById("all_col").value
    keyword = document.getElementById("search_input").value
    if (col == "apk_name") {
        if (keyword == "") {
            table
                .column(1)
                .search("")
                .draw();
        } else {
            table
                .column(1)
                .search(keyword)
                .draw();
        }
    } else if (col == "version") {
        if (keyword == "") {
            table
                .column(2)
                .search("")
                .draw();
        } else {
            table
                .column(2)
                .search(keyword)
                .draw();
        }
    } else if (col == "version_code") {
        if (keyword == "") {
            table
                .column(3)
                .search("")
                .draw();
        } else {
            table
                .column(3)
                .search(keyword)
                .draw();
        }
    } else if (col == "size") {
        if (keyword == "") {
            table
                .column(4)
                .search("")
                .draw();
        } else {
            table
                .column(4)
                .search(keyword)
                .draw();
        }
    } else if (col == "time") {
        if (keyword == "") {
            table
                .column(5)
                .search("")
                .draw();
        } else {
            table
                .column(5)
                .search(keyword)
                .draw();
        }
    }

});

// 筛选列 更换列名时，先清空，再搜索
$('#all_col').on('click', function () {
    document.getElementById("search_input").value = ''
    col = document.getElementById("all_col").value
    keyword = document.getElementById("search_input").value
    if (col == "id") {
        table
            .column(0)
            .search("")
            .draw();
    } else if (col == "build_id") {
        table
            .column(1)
            .search("")
            .draw();

    } else if (col == "apk_name") {
        table
            .column(3)
            .search("")
            .draw();
    } else if (col == "version") {

        table
            .column(4)
            .search("")
            .draw();

    } else if (col == "version_code") {

        table
            .column(5)
            .search("")
            .draw();

    } else if (col == "size") {

        table
            .column(6)
            .search("")
            .draw();

    } else if (col == "time") {

        table
            .column(7)
            .search("")
            .draw();

    }
})


//选择对比版本
$('#apk_infos_table tbody').on('click', '#choose', function () {
    var data = table.row($(this).parents('tr')).data()[1];
    elt.tagsinput('add', data)
    console.log(elt.tagsinput("items"))
    toastr.success('选择版本：' + data);
});

$('#apk_infos_table tbody').on('click', '#delete', function () {
        var apk_name_for_delete = table.row($(this).parents('tr')).data()[1];
        console.log(apk_name_for_delete)
        $("#delete_confirm").on('click', function () {
            $.ajax({
                url: "/delete_data/",
                type: "GET",
                async: false,
                data: {
                    apk_name: apk_name_for_delete
                },
                success: function (data) {
                    $('#modal-danger').modal('hide')
                    if (data['code'] == 200) {
                        toastr.success('删除成功');
                        location.reload()
                    }
                    if (data['code'] == 202) {
                        toastr.error("无删除权限，请联系管理员！")
                        return false
                    }

                }
            });

        })
    }
);


$("#pk_btn").click(function () {
    $('#pk_table').empty()
    var str = "\n" +
        "<div class='table-responsive\'><table border=\"1\" class='table text-nowrap'\n" +
        "                          >\n" +
        "                        <thead>\n" +
        "                        <tr style='background-color: #404553;color: white'>\n" +
        "                            <th>apk_name</th>\n" +
        "                            <th>size</th>\n" +
        "                            <th>dex</th>\n" +
        "                            <th>so</th>\n" +
        "                            <th>xml</th>\n" +
        "                            <th>arsc</th>\n" +
        "                            <th>jar</th>\n" +
        "                            <th>SF</th>\n" +
        "                            <th>MF</th>\n" +
        "                            <th>kotlin_metadata</th>\n" +
        "                            <th>jpg</th>\n" +
        "                            <th>gz</th>\n" +
        "                            <th>png</th>\n" +
        "                            <th>gif</th>\n" +
        "                            <th>web</th>\n" +
        "                            <th>mp4</th>\n" +
        "                            <th>properties</th>\n" +
        "                            <th>kotlin_module</th>\n" +
        "                            <th>kotlin_builtins</th>\n" +
        "                        </tr>\n" +
        "                        </thead>\n" +
        "                        <tbody>";
    // var selected_options=document.getElementById('apk_size_pk').getElementsByTagName('option');
    if (elt.val() != '') {
        var all = elt.val().split(",")
        var size = 0
        var dex = 0
        var so = 0
        var xml = 0
        var arsc = 0
        var jar = 0
        var SF = 0
        var MF = 0
        var kotlin_metadata = 0
        var jpg = 0
        var gz = 0
        var png = 0
        var webp = 0
        var gif =0
        var mp4 = 0
        var properties = 0
        var kotlin_module = 0
        var kotlin_builtins = 0
        var reg = /[a-zA-Z]/g;
        if (all.length != 0) {
            for (var i = 0; i < all.length; i++) {
                $.ajax({
                    url: "/get_size/",
                    type: "GET",
                    async: false,
                    data: {
                        apk_name: all[i]
                    },
                    success: function (json) {
                        var data = eval("(" + json + ")");
                        if (i == 0) {
                            size = Number(data["size"].replace(reg, ""))
                            dex = Number(data["dex"].replace(reg, ""))
                            so = Number(data["so"].replace(reg, ""))
                            xml = Number(data["xml"].replace(reg, ""))
                            arsc = Number(data["arsc"].replace(reg, ""))
                            jar = Number(data["jar"].replace(reg, ""))
                            SF = Number(data["SF"].replace(reg, ""))
                            MF = Number(data["MF"].replace(reg, ""))
                            kotlin_metadata = Number(data["kotlin_metadata"].replace(reg, ""))
                            jpg = Number(data["jpg"].replace(reg, ""))
                            gz = Number(data["gz"].replace(reg, ""))

                            png = Number(data["png"].replace(reg, ""))
                            gif = Number(data["gif"].replace(reg, ""))
                            webp = Number(data["webp"].replace(reg, ""))
                            mp4 = Number(data["mp4"].replace(reg, ""))
                            properties = Number(data["properties"].replace(reg, ""))
                            kotlin_module = Number(data["kotlin_module"].replace(reg, ""))
                            kotlin_builtins = Number(data["kotlin_builtins"].replace(reg, ""))

                            str += "<tr>" +
                                "<td>" + data["apk_name"] + "</td>" +
                                "<td>" + data["size"] + "</td>" +
                                "<td>" + data["dex"] + "</td>" +
                                "<td>" + data["so"] + "</span></td>" +
                                "<td>" + data["xml"] + "</td>" +
                                "<td>" + data["arsc"] + "</td>" +
                                "<td>" + data["jar"] + "</td>" +
                                "<td>" + data["SF"] + "</td>" +
                                "<td>" + data["MF"] + "</td>" +
                                "<td>" + data["kotlin_metadata"] + "</td>" +
                                "<td>" + data["jpg"] + "</td>" +
                                "<td>" + data["gz"] + "</td>" +

                                "<td>" + data["png"] + "</td>" +
                                "<td>" + data["gif"] + "</td>" +
                                "<td>" + data["webp"] + "</td>" +
                                "<td>" + data["mp4"] + "</td>" +
                                "<td>" + data["properties"] + "</td>" +
                                "<td>" + data["kotlin_module"] + "</td>" +
                                "<td>" + data["kotlin_builtins"] + "</td>" +
                                "</tr>"
                        } else {
                            str += "<tr>" +
                                "<td>" + data["apk_name"] + "</td>"
                            var size_diff = (Number(data["size"].replace(reg, "")) - size).toFixed(2)
                            var dex_diff = (Number(data["dex"].replace(reg, "")) - dex).toFixed(2)
                            var so_diff = (Number(data["so"].replace(reg, "")) - so).toFixed(2)
                            var xml_diff = (Number(data["xml"].replace(reg, "")) - xml).toFixed(2)
                            var arsc_diff = (Number(data["arsc"].replace(reg, "")) - arsc).toFixed(2)
                            var jar_diff = (Number(data["jar"].replace(reg, "")) - jar).toFixed(2)
                            var SF_diff = (Number(data["SF"].replace(reg, "")) - SF).toFixed(2)
                            var MF_diff = (Number(data["MF"].replace(reg, "")) - MF).toFixed(2)
                            var kotlin_metadata_diff = (Number(data["kotlin_metadata"].replace(reg, "")) - kotlin_metadata).toFixed(2)
                            var jpg_diff = (Number(data["jpg"].replace(reg, "")) - jpg).toFixed(2)
                            var gz_diff = (Number(data["gz"].replace(reg, "")) - gz).toFixed(2)

                            var png_diff = (Number(data["png"].replace(reg, "")) - png).toFixed(2)
                            var gif_diff = (Number(data["gif"].replace(reg, "")) - gif).toFixed(2)
                            var webp_diff = (Number(data["webp"].replace(reg, "")) - webp).toFixed(2)
                            var mp4_diff = (Number(data["mp4"].replace(reg, "")) - mp4).toFixed(2)
                            var properties_diff = (Number(data["properties"].replace(reg, "")) - properties).toFixed(2)
                            var kotlin_module_diff = (Number(data["kotlin_module"].replace(reg, "")) - kotlin_module).toFixed(2)
                            var kotlin_builtins_diff = (Number(data["kotlin_builtins"].replace(reg, "")) - kotlin_builtins).toFixed(2)

                            if (size_diff > 0) {
                                str += "<td>" + data["size"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(size_diff) + "</span>" + "</td>"
                            }
                            if (size_diff == 0) {
                                str += "<td>" + data["size"] + "</td>"
                            }
                            if (size_diff < 0) {
                                str += "<td>" + data["size"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(size_diff) + "</span>" + "</td>"
                            }


                            if (dex_diff > 0) {
                                str += "<td>" + data["dex"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(dex_diff) + "</span>" + "</td>"
                            }
                            if (dex_diff == 0) {
                                str += "<td>" + data["dex"] + "</td>"
                            }
                            if (dex_diff < 0) {
                                str += "<td>" + data["dex"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(dex_diff) + "</span>" + "</td>"
                            }

                            if (so_diff > 0) {
                                str += "<td>" + data["so"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(so_diff) + "</span>" + "</td>"
                            }
                            if (so_diff == 0) {
                                str += "<td>" + data["so"] + "</td>"
                            }
                            if (so_diff < 0) {
                                str += "<td>" + data["so"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(so_diff) + "</span>" + "</td>"
                            }

                            if (xml_diff > 0) {
                                str += "<td>" + data["xml"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(xml_diff) + "</span>" + "</td>"
                            }
                            if (xml_diff == 0) {
                                str += "<td>" + data["xml"] + "</td>"
                            }
                            if (xml_diff < 0) {
                                str += "<td>" + data["xml"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(xml_diff) + "</span>" + "</td>"
                            }

                            if (arsc_diff > 0) {
                                str += "<td>" + data["arsc"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(arsc_diff) + "</span>" + "</td>"
                            }
                            if (arsc_diff == 0) {
                                str += "<td>" + data["arsc"] + "</td>"
                            }
                            if (arsc_diff < 0) {
                                str += "<td>" + data["arsc"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(arsc_diff) + "</span>" + "</td>"
                            }

                            if (jar_diff > 0) {
                                str += "<td>" + data["jar"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(jar_diff) + "</span>" + "</td>"
                            }
                            if (jar_diff == 0) {
                                str += "<td>" + data["jar"] + "</td>"
                            }
                            if (jar_diff < 0) {
                                str += "<td>" + data["jar"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(jar_diff) + "</span>" + "</td>"
                            }

                            if (SF_diff > 0) {
                                str += "<td>" + data["SF"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(SF_diff) + "</span>" + "</td>"
                            }
                            if (SF_diff == 0) {
                                str += "<td>" + data["SF"] + "</td>"
                            }
                            if (SF_diff < 0) {
                                str += "<td>" + data["SF"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(SF_diff) + "</span>" + "</td>"
                            }

                            if (MF_diff > 0) {
                                str += "<td>" + data["MF"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(MF_diff) + "</span>" + "</td>"
                            }
                            if (MF_diff == 0) {
                                str += "<td>" + data["MF"] + "</td>"
                            }
                            if (MF_diff < 0) {
                                str += "<td>" + data["MF"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(MF_diff) + "</span>" + "</td>"
                            }

                            if (kotlin_metadata_diff > 0) {
                                str += "<td>" + data["kotlin_metadata"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(kotlin_metadata_diff) + "</span>" + "</td>"
                            }
                            if (kotlin_metadata_diff == 0) {
                                str += "<td>" + data["kotlin_metadata"] + "</td>"
                            }
                            if (kotlin_metadata_diff < 0) {
                                str += "<td>" + data["kotlin_metadata"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(kotlin_metadata_diff) + "</span>" + "</td>"
                            }

                            if (jpg_diff > 0) {
                                str += "<td>" + data["jpg"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(jpg_diff) + "</span>" + "</td>"
                            }
                            if (jpg_diff == 0) {
                                str += "<td>" + data["jpg"] + "</td>"
                            }
                            if (jpg_diff < 0) {
                                str += "<td>" + data["jpg"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(jpg_diff) + "</span>" + "</td>"
                            }

                            if (gz_diff > 0) {
                                str += "<td>" + data["gz"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(gz_diff) + "</span>" + "</td>"
                            }
                            if (gz_diff == 0) {
                                str += "<td>" + data["gz"] + "</td>"
                            }
                            if (gz_diff < 0) {
                                str += "<td>" + data["gz"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(gz_diff) + "</span>" + "</td>"
                            }
                            //new
                            if (png_diff > 0) {
                                str += "<td>" + data["png"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(png_diff) + "</span>" + "</td>"
                            }
                            if (png_diff == 0) {
                                str += "<td>" + data["png"] + "</td>"
                            }
                            if (png_diff < 0) {
                                str += "<td>" + data["png"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(png_diff) + "</span>" + "</td>"
                            }

                            if (gif_diff > 0) {
                                str += "<td>" + data["gif"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(gif_diff) + "</span>" + "</td>"
                            }
                            if (gif_diff == 0) {
                                str += "<td>" + data["gif"] + "</td>"
                            }
                            if (gif_diff < 0) {
                                str += "<td>" + data["gif"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(gif_diff) + "</span>" + "</td>"
                            }

                            if (webp_diff > 0) {
                                str += "<td>" + data["webp"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(webp_diff) + "</span>" + "</td>"
                            }
                            if (webp_diff == 0) {
                                str += "<td>" + data["webp"] + "</td>"
                            }
                            if (webp_diff < 0) {
                                str += "<td>" + data["webp"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(webp_diff) + "</span>" + "</td>"
                            }

                            if (mp4_diff > 0) {
                                str += "<td>" + data["mp4"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(mp4_diff) + "</span>" + "</td>"
                            }
                            if (mp4_diff == 0) {
                                str += "<td>" + data["mp4"] + "</td>"
                            }
                            if (mp4_diff < 0) {
                                str += "<td>" + data["mp4"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(mp4_diff) + "</span>" + "</td>"
                            }

                            if (properties_diff > 0) {
                                str += "<td>" + data["properties"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(properties_diff) + "</span>" + "</td>"
                            }
                            if (properties_diff == 0) {
                                str += "<td>" + data["properties"] + "</td>"
                            }
                            if (properties_diff < 0) {
                                str += "<td>" + data["properties"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(properties_diff) + "</span>" + "</td>"
                            }

                            if (kotlin_module_diff > 0) {
                                str += "<td>" + data["kotlin_module"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(kotlin_module_diff) + "</span>" + "</td>"
                            }
                            if (kotlin_module_diff == 0) {
                                str += "<td>" + data["kotlin_module"] + "</td>"
                            }
                            if (kotlin_module_diff < 0) {
                                str += "<td>" + data["kotlin_module"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(kotlin_module_diff) + "</span>" + "</td>"
                            }

                            if (kotlin_builtins_diff > 0) {
                                str += "<td>" + data["kotlin_builtins"] + "<span style='margin-left:15px' class='up'>↑" + Math.abs(kotlin_builtins_diff) + "</span>" + "</td>"
                            }
                            if (kotlin_builtins_diff == 0) {
                                str += "<td>" + data["kotlin_builtins"] + "</td>"
                            }
                            if (kotlin_builtins_diff < 0) {
                                str += "<td>" + data["kotlin_builtins"] + "<span style='margin-left:15px' class='down'>↓" + Math.abs(kotlin_builtins_diff) + "</span>" + "</td>"
                            }

                            str += "</tr>"
                        }
                    }, error: function () {
                        alert("There Is Error！");
                    }
                })
            }
        }
        $("#pk_table").append(str).append("</tbody></table></div>")

    }
})

// var returninfo = data.result.list
// for (var i = 0; i < returninfo.length; i++) {
//     $("tbody").append("<tr><td>" + returninfo[i].datetime + "</td> <td>" + returninfo[i].remark + "</td></tr>")
// }

