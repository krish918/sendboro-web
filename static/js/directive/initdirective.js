(function () {
  angular.module("init")
	.directive('authPanel', function() {
		return {
			restrict: 'E',
			templateUrl: '/decorator/auth-panel',
			controller: 'authController',
			controllerAs: 'authCtrl'
		};
		
	})
	
	.directive('featurePanel', function(){
		return {
			restrict: 'E',
			templateUrl: '/decorator/feature-panel'
		};
	});
	
})();