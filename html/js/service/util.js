(function(){
	angular.module('util')
	
	.factory('Offset', function() {
		return {
			getY : function() {
				if(self.pageYOffset) return pageYOffset;
				var html = document.documentElement,
					body = document.body;
				
				return html.scrollTop||body.scrollTop;
			},
			
			getElemY : function(elem) {
				var node = document.getElementById(elem),
				posY = node.offsetTop;
				while(node.offsetParent && node.offsetParent != document.body) {
					node = node.offsetParent;
					posY += node.offsetTop;
				}
			
				return posY;
			}
		};
	})
	
	.service('smoothScroll', ['Offset', function(Offset) {
		var posY,
			posElemY;
		
		this.scrollTo = function(elem) {
			start = Offset.getY();
			end = Offset.getElemY(elem);
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
			
	}]);
})();