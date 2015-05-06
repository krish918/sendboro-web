(function (){
	
	var ctrlFunc = function($scope){
		this.hover = 0;
		$scope.init = function() {
			$scope.animateContacts = 'animate-contacts';
			$scope.animateBlocks = 'animate-blocks';
		};
		
		this.isHover = function(arg) {
			return this.hover === arg % 2;
		};
		
		this.setHover = function(arg) {
			this.hover = arg;
		};
	};	
	
	angular.module("borocasa")
	
	.controller('quickContactController', ctrlFunc);
	
})()