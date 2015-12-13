(function () {
	angular.module("init")
		.controller('panelController', ['scroll','smoothScroll','$scope','$timeout', 
		                                function (scroll, smoothScroll,$scope,$timeout) {
			this.page = 1;
			this.slide = 1;
			this.hideAuthFlag = true;
			this.toggleAuthPanel = function () {
				this.hideAuthFlag = !this.hideAuthFlag;
			};
			
			
			this.slideFeature = function(dir) {
				var classArr = ['','show-slide-2', 'show-slide-3', 'show-slide-4'];
				if (dir === 1)
					this.slide += 1;
				else 
					this.slide -= 1;
				
				$scope.featureClass = classArr[this.slide-1];
				
			};
			
			this.isSlideShown = function(slide) {
				return this.slide === slide;
			};
			
			this.isPageShown = function(page) {
				return this.page === page;
			};
			
			this.toggleComeOverPage = function() {
				if (this.page === 1)
					smoothScroll.scrollTo('co-page');
				else {
					smoothScroll.scrollTo('zero-top');
				}
				
			};
			
			this.wrapUpContent = function(data) {
				$scope.dictWordsClass = 'hide-meaning';
				
				if (data.y == 0) {
					$scope.dictWordsClass = '';
					this.page = 1;
				}
				else 
					this.page = 2;
				
				
				if(data.y == data.scrollHeight) {
					//showing the dictionary word on next page
					$scope.dictWordsClass = 'bring-on-next';
					
					//showing feature items one by one
					$scope.itemOneClass = 'show-items';
					$timeout(function(){
						$scope.itemTwoClass = 'show-items';
					},200);
					$timeout(function(){
						$scope.itemThreeClass = 'show-items';
					},400);
				}
				
				if(data.y > 300) {
					$scope.mainTextClass = 'skew-text';
					$scope.enterButtonClass = 'translate-to-bottom';
				}
				else if(data.y < 300) {
					$scope.mainTextClass = '';
					$scope.enterButtonClass = '';
					$scope.itemOneClass = '';
					$scope.itemTwoClass = '';
					$scope.itemThreeClass = '';
				}
				
			};
		
	}]);
})();