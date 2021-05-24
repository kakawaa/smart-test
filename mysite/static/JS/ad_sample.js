var elt = $('#test');
elt.tagsinput({
});



    $('.select2').select2({
            allowClear: true,
            tags: true
        }
    )

    $("select").on("select2:select", function (evt) {
      var element = evt.params.data.element;
      var $element = $(element);
      $element.detach();
      $(this).append($element);
      $(this).trigger("change");
    });
    //
    // // 大表格
    // var table = $('#ad_stat_table').DataTable({
    //     "pageLength": 10,
    //     "paging": true,       <!-- 允许分页 -->
    //     "lengthChange": false, <!-- 允许改变每页显示的行数 -->
    //     "searching": true,    <!-- 允许内容搜索 -->
    //     "ordering": true,     <!-- 允许排序 -->
    //     "info": true,         <!-- 显示信息 -->
    //     "autoWidth": false,    <!-- 固定宽度 -->
    //
    //     "columnDefs": [
    //         {"orderable": false, "targets": -1}
    //     ]
    //
    // });


