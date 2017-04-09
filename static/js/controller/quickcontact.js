(function (){
	
	var ctrlFunc = function($scope, $timeout){
		
		var self = this;
		this.addContactFlag = 0;
		this.error = 0;
		
		$scope.init = function() {
			$scope.animateWidget = 'animateWidget';
		};
		
		this.checkAddContactFlag = function(val) {
			return this.addContactFlag === val;
		};
		
		this.checkError = function(val) {
			return this.error === val;
		};
		
		this.showAddContact = function(val) {
			self.addContactFlag = -1;
			$timeout(function() {
				self.addContactFlag = val;
			}, 250);
			$scope.addContactClass = (val == 1) ? "show-add-contact" : "";
		}
		
		this.initAddContact = function() {
			if(!validateAddContactForm())
				return;
		};
		
		this.pristineError = function() {
			if(self.error == 1)
				setError(0);
		};
		
		var validateAddContactForm = function() {
			if(!$scope.contactName || $scope.contactName.trim().length == 0) {
				setError(1);
				$scope.addContactErrorText = "Contact name missing.";
			}
			else if((!$scope.userName || $scope.userName.trim().length == 0) 
					&& (!$scope.phoneNum || $scope.phoneNum.trim().length == 0)) {
				setError(1);
				$scope.addContactErrorText = "Username or Phone is required.";
			}
		};
		
		var setError = function(val) {
			self.error = -1;
			$timeout(function(){
				self.error = val;
			},200);
		};
		
		
		
	};	
	
	angular.module("borocasa")
	
	.controller('quickContactController', ctrlFunc);
	
})()