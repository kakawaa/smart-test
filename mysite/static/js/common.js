'use strict'

//loading效果

const LOAGDING_TYPE={
	small:130,
    normal:170
}

function loading_actions(action=null,title=null,type=LOAGDING_TYPE.small) {
    $(action).loading({
        loadingWidth:type,
        title:title,
        name:'loading',
        discription:'',
        direction:'column',
        type:'origin',
        originDivWidth:40,
        originDivHeight:40,
        originWidth:6,
        originHeight:6,
        smallLoading:true,
        loadingMaskBg:'rgba(0,0,0,0.2)'
    });
    setTimeout(function(){},3000);
};

function loading(title=null,type=LOAGDING_TYPE.small) {
    $('body').loading({
        loadingWidth:type,
        title:title,
        name:'test',
        discription:'',
        direction:'column',
        type:'origin',
        originBg:'white',
        originDivWidth:40,
        originDivHeight:40,
        originWidth:6,
        originHeight:6,
        smallLoading:true,
        loadingMaskBg:'rgba(0,0,0,0.2)'
    });
    setTimeout(function(){},3000);
}

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
		autoclose: 1000
	});
}

 //获取后缀
function  getExtension (name) {
    return name.substring(name.lastIndexOf(".")+1)
}

//json格式化
function parse(str) {
	return JSON.stringify(JSON.parse(str), null, "\t");
}

//json格式检查
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
        	Spop(SPOP_TYPE['error'],'not json , please check request and case!')
			return false;
        }
    }
    else{
    	Spop(SPOP_TYPE['error'],'not string!')
        return false;
    }
}

//table
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