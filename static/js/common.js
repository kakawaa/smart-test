'use strict'

/**
 * loading效果
 */
const LOAGDING_TYPE={
	small:120,
    normal:170
}

function loading(action='body',title=null,type=LOAGDING_TYPE.small) {
    $(action).loading({
        loadingWidth:type,
        title:title,
        name:'test',
        discription:'',
        direction:'column',
        type:'origin',
        originBg:'white',
        originDivWidth:40,
        originDivHeight:40,
        originWidth:5,
        originHeight:5,
        smallLoading:true,
        loadingMaskBg:'transparent'
    });
}

/**
 * toast样式
 */
const SPOP_TYPE={
	error:'error',
	success:'success',
	warning:'warning'
}

function Spop(type,msg){
	spop({
		template: msg,
		position  : 'top-center',
		style: type,
		autoclose: 2000
	});
}

/**
 * 获取文件后缀
 */
function  getExtension (name) {
    return name.substring(name.lastIndexOf(".")+1)
}

/**
 * json格式化
 */
function parse(str) {
	return JSON.stringify(JSON.parse(str), null, "\t");
}

/**
 * json格式检查
 */
function isJSON(str) {
	if (typeof str == 'string') {
        try {
            var obj=JSON.parse(str);
            if(typeof obj == 'object' && obj ){
                return true;
            }else{
                return false;
            }

        } catch(e) {
			return false;
        }
    }
    else{
        return false;
    }
}

/**
 * 建表
 */
function maketable({Table=null,pageLength=10,paging=true,lengthChange=true,searching=true,columns=null,data=null}) {
	let table = $(Table).DataTable({
        "destroy": true,
        "pageLength": pageLength,
        "paging": paging, <!-- 允许分页 -->
        "lengthChange": lengthChange, <!-- 允许改变每页显示的行数 -->
        "searching": searching, <!-- 允许内容搜索 -->
        "ordering": false, <!-- 允许排序 -->
        "info": false, <!-- 显示信息 -->
        "autoWidth": false, <!-- 固定宽度 -->
        "pagingType": "full_numbers",
        "order": [[0, "desc"]],
        dom: 't<"bottom"ip><"clear">',
        columns:columns,
        data:data
    });
	return table

}
/**
 * josn美化
 */
function json_viewer(element,input){
    var options = {
        collapsed: $('#collapsed').is(':checked'),
        withQuotes: $('#with-quotes').is(':checked')
    };
    $(element).jsonViewer(input, options);
}


