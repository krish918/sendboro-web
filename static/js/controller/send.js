(function () {
	angular.module('borocasa')
	
	.controller('shareController', ['$scope','$metaboro','PushBoro','$timeout','$cookies',
	       '$http','$rootScope',function($scope, $metaboro, PushBoro, $timeout,$cookies,$http, rootScope){
			
			 //variable to store timeout promise; used
			 //  to cancel timeout when another error occurs
			 //  within the timeout lifespan
			 var errorPromise,
			 	 recipient;
			 
			 $scope.init = function () {
				//document.title = 'Send File';
				$scope.animateWidget = 'animateWidget';
				$scope.blockSelect = true;
				$scope.errorHide = true;
				$scope.dialogHide = true;
				$scope.verifying = false;
				upload.init();
			 };

			 /*$scope.$watch('recipient', function(newVal, oldVal){
				if(newVal && newVal.trim().length != 0)
					$scope.blockSelect = false;
				else
					$scope.blockSelect = true;
			 });*/
			 
			 // for displaying inability to select file
			 rootScope.showInability = function () {
				 $scope.inptErrorClass = 'invalid-entry red-border';
				 
				 //Removes the invalid-entry class after 1 sec.
				 // to allow re-shake on next click
				 $timeout(function () {
					 $scope.inptErrorClass = 'red-border';
				 },1000);
			 };
			 
			 //closes the confirm blind-send dialog box and resets recipient
			 this.closeDialog = function () {
				$scope.dialogHide = true;
				$scope.recipient = '';
			 };
			 
			//if sender wants to send file blindly
			 // resume the sending process
			 this.resumeProcess = function () {
				//start pushing file with an extra flag: blind
				PushBoro.pushFile({
						recipient: recipient,
						blind: 1
					}); 
				$scope.dialogHide = true;
			 };
			 
			 this.checkRecipient = function () {
				 var reUsername = /^([a-zA-Z]{1,}[\._\-]?[a-zA-Z0-9]{1,}){1,}$/,
				 	 rePhone = /^\+[1-9][0-9]{6,14}$/;
				 
				 //checks whether the recipient is a valid username or phone
				 // and provides ability to select file afterwards.
				 if($scope.recipient.match(reUsername) || $scope.recipient.match(rePhone)) {
					 $scope.blockSelect = false;
					 $scope.inptErrorClass = '';
				 }
				 else $scope.blockSelect = true;
			 };
			 
			 this.cancel = function () {
				 PushBoro.cancelPush();
			 }
			 
			 var upload = (function () {
				
				var uploader;
				
				//initializes uploader object
				var init = function () {
					//setting local uploader and scope uploader
					// to uploader object
					uploader = $scope.uploader = PushBoro.returnObject();
					
				};
				
				var nativeHandler = function (arg1, arg2) {
					PushBoro.handler({
						scope: rootScope,
						onFilterChoke: addingError,
						houseKeeping: arg1 ? verifyRecipient: false,
						onSuccess: showSuccess,
						onError: showFailure,
						onCancel: showCancelled,
						recipient: $scope.recipient,
						blind: $scope.blind,
						uploadAllowed: arg2,
					});
				};
				
				var addingError = function (item, filter) {
					showError(2);
				};
				
				var showCancelled = function(item, response) {
					$scope.showProgress = false;
					showError(3);
				}
				
				var showSuccess = function (item, response) {
					//console.log(response);
					if('error' in response) {
						if(response.error === 1)
							showError(2);
						else showError(0);
					}
					
					else if('success' in response)
						$scope.showSuccess = rootScope.showSuccess = true;
						$timeout(function () {
							$scope.showSuccess = rootScope.showSuccess = false;
						},9000);
				};
				
				var showFailure = function (item, response) {
					//console.log(response);
					showError(0);
				};
				
				var verifyRecipient = function () {
					//showing small loader while verifying recipient
					$scope.verifying = true;
					//sends a http request to verify the recipient
					// value is being url-encoded so as to transmit '+' character
					// successfully to server
					//console.log($scope.recipient);
					$http({
						url: '/api/verify',
						data: 'rcpnt='+encodeURIComponent($scope.recipient),
						method: 'post',
						headers: {
							'X-CSRFToken': $cookies.csrftoken,
							'Content-Type' : 'application/x-www-form-urlencoded',
						}
					}) 
					
					.success(function(response) {
						$scope.verifying = false;
						if('error' in response)
							showError(0);
						else if('nouser' in response) {
							//displays user doesn't exist 
							showError(1);
						}
						else {
							
							if('blind' in response) {
								//asks confirmation for blind-send by showing a dialog-box.
								recipient = response.phone
								$scope.dialogHide = false;
							}
							else if('success' in response) {
								//fill up the recipient array with verified 
								//  UIDs from server
								//recipient = response.uid;
								PushBoro.pushFile({recipient: $scope.recipient});
							}
						}
							
					})
					.error(function(response) {
						$scope.verifying = false;
						showError(0);
					});
				 };
				
				
				return {
					init: init,
					handle: nativeHandler
				};
				
			 })();
			  
			 $scope.initPushEngine = function () {
				 var uploadAllowed,
				 	 housekeeping;

				if(arguments.length == 2) {
					housekeeping = arguments[0];
					uploadAllowed = arguments[1];
				}
				else {
					housekeeping = true;
					uploadAllowed = !$scope.blockSelect;
				}

				upload.handle(housekeeping, uploadAllowed);
			 };
			 
			 var showError = function(arg) {
				 //if errorPromise is unresolved yet, cancel it
				 if(errorPromise)
					 $timeout.cancel(errorPromise);
				 $scope.errorHide = false;
				 rootScope.showError = true;
				 
				 if(arg===0)
					 $scope.errorMessage = rootScope.errorMessage =
					  	'Sorry! We encountered some error. Please try later.';
				 else if(1 === arg)
					 $scope.errorMessage = rootScope.errorMessage = 
					 	"Recipient's username is invalid.";
				 else if(2 === arg)
						 $scope.errorMessage = rootScope.errorMessage = 
						 		"File size shouldn't exceed 6GB.";
				 else if(3 === arg)
					 	 $scope.errorMessage = rootScope.errorMessage = 
						  	"File sending was interrupted.";
							 
				 errorPromise = $timeout(function () {
					 $scope.errorHide =  true;
					 rootScope.showError = false;
				 },6000);
			 };
			 
	}])
	
	
	.controller('inboxController', ['$scope','user','PushBoro','$timeout','$cookies',
	       '$http',function($scope, metaboro, PushBoro, $timeout,$cookies,$http){
				
				this.user = metaboro.data;
				$scope.isEmpty = false;
				
				var self = this;
		
				$scope.init =  function () {
					//document.title = 'Inbox';
					$scope.animateWidget="animateWidget";
					metaboro.listenUpdate($scope, function() {
						self.user = metaboro.data
					});
					
					if(!self.user.file.senderlist.length)
						$scope.isEmpty = true;
					
					//resetAlerts();
				};
				
				//now new files nnotification will
				//reset when user navigates to sender view
				/*var resetAlerts = function () {
					$http({
						url: '/file/changestate',
						method: 'post',
						headers: {
							'X-CSRFToken': $cookies.csrftoken,
							'Content-Type' : 'application/x-www-form-urlencoded',
						}
					})
					.success(function (response) {
						console.log(response);
						if('success' in response) {
							metaboro.update({'file': {'newcount': 0}});
						}
					})
					.error(function (response) {
						console.log(response);
					});

				};*/
				
				this.initDownload = function (file) {
					
										
				};
	}])

	.controller('senderController', ['$scope','user','$poll','$stateParams', 
		   function($scope, metaboro, $poll, $stateParams){
				
				this.user = metaboro.data;
				$scope.isEmpty = false;
				
				var self = this;
		
				$scope.init =  function () {
					//document.title = 'Inbox';
					self.files = [];
					$scope.animateWidget="animateWidget";
					metaboro.listenUpdate($scope, function() {
						self.user = metaboro.data
					});
					
					if(!self.user.file.senderlist.length)
						$scope.isEmpty = true;

					if($stateParams['sender']) {
						self.sender = $stateParams['sender'];
					}

					welcomeSender();
					if(self.new_files)
						resetAlerts();
				};

				var welcomeSender = function() {
					for(var sender of self.user.file.senderlist) {
						if(sender.identity == self.sender 
						|| sender.identity == '+'+self.sender) {
							self.sender_id = sender._id;
							self.files = sender.files;
							self.sender_pic = sender.pic;
							self.silh = sender.silh;
							//self.piclarge = sender.piclarge;
							self.new_files = sender.new;
						}
					}
					if(self.files.length == 0)
						$scope.isEmpty = true;

				}
				
				var resetAlerts = function () {
					var endpoint = '/file/changestate';
					var data = 'aid='+encodeURIComponent(self.sender_id);
					$poll.post(endpoint, data)
					
					.then(function (response) {
						//console.log(response);
						if('success' in response) {
							metaboro.update({'file': {
								'newcount': 
							(self.user.file.newcount - self.new_files)}});
						}
					}, function (response) {
						//console.log(response);
					});

				};
				
				this.initDownload = function (file) {
					
										
				};
	}]);
	
	
	
})();