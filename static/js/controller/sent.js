(function (){
	
	var ctrlFunc = function($scope){

		$scope.init = function() {
			$scope.animateWidget = 'animateWidget';
		};
		
		
	};	
	
	angular.module("borocasa")
	
	.controller('sentController', ctrlFunc);
	
})()