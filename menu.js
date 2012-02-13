var Menu = {
	_channel : { 's': 0, 'zixun': 1, 'chezhan': 2, 'meinv': 3, 'redian': 4, 'xuanche': 5, 'shijia': 6, 'saiche': 7, 'wanche': 8, 'piaoyi': 9, 'guanggao': 10, 'paoche': 11, 'all': 12 },
	nowChannel : 0,
	_oldCss : '',
	_nowID : 0,
	initMunu : function(){
		var urls = window.location.href.split('/');
		if (urls.length > 3) {
			Menu.nowChannel = Menu._channel[urls[3]];
			var val = $('#mynav' + Menu.nowChannel);
			if (val.length > 0) {
				$('#qh_con' + Menu.nowChannel)[0].style.display = "block";
				val[0].className = "nav_on";
			}else{
				$('#qh_con0')[0].style.display = "block";
				$('#mynav0')[0].className = "nav_on";
			}
		}
	},
	moveOver : function(val){
		Menu._nowID = parseInt(val.toString().replace('mynav', ''));
		Menu._oldCss = $("#mynav" + Menu._nowID)[0].className;
		$("#mynav" + Menu._nowID)[0].className = "nav_on";
		for (var id = 0; id <= 12; id++) {
			if (id == Menu._nowID)
				$("#qh_con" + id)[0].style.display = "block";
			else
				$("#qh_con" + id)[0].style.display = "none";
		}
	},
	moveOut : function(val){
		var num = parseInt(val.toString().replace('mynav', ''));
		if (typeof (Menu.nowChannel) == 'undefined') {
			if (Menu._nowID != 0) {
				$("#mynav" + Menu._nowID)[0].className = "";
				$("#mynav0")[0].className = "nav_on";
			}
		}
		else {
			if (Menu._nowID != Menu.nowChannel) {
				$("#mynav" + Menu._nowID)[0].className = "";
				$("#mynav" + Menu.nowChannel)[0].className = "nav_on";
			}
		}
	}
};

$(document).ready(function () {
	Menu.initMunu();
	$('#nav a').each(function () {
		$(this).bind("mouseover", function () {
			Menu.moveOver(this.id);
		});
		$(this).bind("mouseout", function () {
			Menu.moveOut(this.id);
		});
	});
});
