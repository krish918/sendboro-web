(function () {
	angular.module("init")
		.controller('panelController', ['scroll','smoothScroll','$scope','$timeout', 'Offset', 
		                                function (scroll, smoothScroll,$scope,$timeout,Offset) {
			this.page = 1;
			this.slide = 1;
			this.hideAuthFlag = true;
			this.toggleAuthPanel = function () {
				this.hideAuthFlag = !this.hideAuthFlag;
				if(!this.hideAuthFlag) {
					$scope.shifterClass = "shifted-page";
					document.body.className = 'pigeo-home fix';
					$scope.hideClass = 'show-auth';
					$scope.init();  //to clear the auth-panel form
				}
				else {
					document.body.className = 'pigeo-home';
					$scope.shifterClass = "";
				}
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
			
			this.isAuthShown = function() {
				return !this.hideAuthFlag;
			}
			
			this.toggleComeOverPage = function() {
				if (this.page === 1)
					smoothScroll.scrollTo('co-page');
				else {
					smoothScroll.scrollTo('zero-top');
				}
				
			};
			
			this.wrapUpContent = function(data) {
				
				var nextPageHeight = data.scrollHeight;
				
				if (data.y > nextPageHeight/3)
					this.page = 2;
				else 
					this.page = 1;
				
				//console.log(this.page);
				
				if(data.y == nextPageHeight) {
					
					//showing feature items one by one
					$scope.itemOneClass = 'show-items';
					
					$timeout(function(){
						$scope.itemTwoClass = 'show-items';
					},200);
					
					$timeout(function(){
						$scope.itemThreeClass = 'show-items';
					},400);
				}
				
				if(data.y > nextPageHeight/4) {
					$scope.coverTextAnimateClass = 'departed';
					$scope.alternateEnterClass = 'inception';
				}
				else if(data.y < nextPageHeight/4) {
					$scope.coverTextAnimateClass = '';
					$scope.alternateEnterClass = '';
					$scope.itemOneClass = '';
					$scope.itemTwoClass = '';
					$scope.itemThreeClass = '';
				}
				
			};
		
	}]);
})();