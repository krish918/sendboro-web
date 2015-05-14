(function () {

	angular.module("borocasa")
	
	.directive("homeLoader", function($rootScope, mbStatus) {
		var template = '<div class="welcome-container" ng-if="isHomeLoading">'
			+'<div class="quote-container">'
		  +'<div class="quote">'
		  	+'"I know you are tired. But come, this is the way!"'
		  	+'<br />'
			+'<strong>-Rumi</strong>'
		  +'</div>'
		+'</div>'
		+'<div class="logo">'
			+'<img src="static/resource/picture/logo-home-2.png">'
		+'</div>'
		+'<div class="upper-pb" ng-if="isHomeLoading">'
			+'<img src="static/resource/loader/welcome-bar.gif">'
		+'</div>'
		+'<div class="wait-text" ng-hide="isHomeLoadingFailed">'
			+'Almost there! <br />Just setting up things for you.'
		+'</div>'
		+'<div class="wait-text alert-text" ng-if="isHomeLoadingFailed">'
			+'Dayum! Something\'s broken at sendboro.<br />'
			+'Please come back after a moment.'
		+'</div>'
		
		+'<div class="lower-pb" ng-if="isHomeLoading">'
			+'<img src="static/resource/loader/welcome-bar.gif">'
		+'</div>'
	+'</div>';
		 return {
			restrict: 'E',
			template: template,
			link : function(scope, elem, attr) {

				scope.isHomeLoading = true;
				scope.isHomeLoadingFailed = false;

				scope.$on('$stateChangeStart', function() {
					if(mbStatus.resolved)
						return;
					scope.isHomeLoading = true;
				});

				scope.$on('$stateChangeSuccess', function() {
					if(mbStatus.appRunning)
						return;
					scope.isHomeLoading = false;
				});

				scope.$on('$stateChangeError', function() {
					if(mbStatus.appRunning)
						return;
					scope.isHomeLoading = true;
					scope.isHomeLoadingFailed = true;
				});
			}
			};
	});
})();