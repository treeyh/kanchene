var Search = {
	_searchValue : '',
	searchVideo : function(){
		//var key = $('#txtSearch').val();
		var val = $('#txtSearch').val().toString().replace(/[\%\.\[\]\(\)\{\}]/gi, '');
		if (val.length <= 0)
			alert('请输入搜索条件.');
		else {
			var searchurl = 'http://'+domain+'/s/' + encodeURIComponent(val) + '.htm';
			window.location.href = searchurl;
		}
		return false;
	},
	inputclick : function(event){		
        if (event.keyCode == 13) {
            Search.searchVideo();
        }
	},
	searchF : function(){
		Search._searchValue = $('#txtSearch').val();
        $('#txtSearch').val('');
	},
	searchB : function(){
		var val = $('#txtSearch').val();
		if (val == '') {
            $('#txtSearch').val(Search._searchValue);
        }
	}
};
$(document).ready( function(){
	$('#txtSearch').bind('focus', function(event){ 
		Search.searchF(); }).bind('blur', function(event){ 
		Search.searchB();}).bind('keydown', function(event){ 
		Search.inputclick(event);});
	$('#btsearch').bind('click', function(event){ Search.searchVideo();});
});

function addDefaultPage() {
	var val = window.location;
	if (document.all) {
		document.body.style.behavior = 'url(#default#homepage)';
		document.body.setHomePage(val);
	} else if (window.sidebar) {
		if (window.netscape) {
			try {
				netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
			}
			catch (e) {
				alert("Firefox暂无此功能，请手动设置。");
			}
		}
		var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch);
		prefs.setCharPref('browser.startup.homepage', val);
	}
}
function addFavorite() {
	var surl = window.location;
	var stitle = window.document.title;
	try {
		window.external.addFavorite(surl, stitle);
	}
	catch (e) {
		try {
			window.sidebar.addPanel(stitle, surl, "");
		}
		catch (e) {
			alert("加入收藏失败，请使用Ctrl+D进行添加");
		}
	}
}


