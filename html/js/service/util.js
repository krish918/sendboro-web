(function(){
	angular.module('util')
	.service('smoothScroll', function() {
		var posY,
			posElemY;
		
		this.scrollTo = function(elem) {
			start = getPositionY();
			end = getPositionElemY(elem);
			var diff = (end>start) ? (end - start) : (start - end),
					speed = Math.round(diff / 100),
					step = Math.round(diff / 50),
					leap = (end > start) ? start+step : start-step; 
			var idx, timer=0;
			if(end > start) {
				for(idx=start; idx<end; idx+=step) {
					setTimeout("window.scrollTo(0,"+leap+")",timer*speed);
					leap += step;
					if(leap > end)
						leap = end;
					timer++;
				}
				return;
			}
			for(idx=start; idx > end; idx -= step) {
				setTimeout("window.scrollTo(0,"+leap+")",timer*speed);
				leap -= step;
				if (leap < end)
					leap = end;
				timer++;
			}
			
		};
		
		function getPositionY() {
			if(self.pageYOffset) return pageYOffset;
			var html = document.documentElement,
				body = document.body;
			
			return html.scrollTop||body.scrollTop;
		};
		
		function getPositionElemY(elem) {
			var node = document.getElementById(elem),
				posY = node.offsetTop;
			while(node.offsetParent && node.offsetParent != document.body) {
				node = node.offsetParent;
				posY += node.offsetTop;
			}
			
			return posY;
		};
			
	});
})();