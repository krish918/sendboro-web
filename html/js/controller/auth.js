(function () {	
	angular.module("init")
		.controller('authController', ['$scope','$http', '$cookies','$timeout','$window','countries',
		                                  function($scope, $http, $cookies,$timeout,$window,countries) {
			
			this.countryList = countries.fetch();
			
			var self = this;
			
			$scope.init = function() {
				$scope.countryName = '';
				$scope.dialCode = '';
				$scope.phone = '';
				$scope.disableClass = '';
				self.error = 0;
				self.scene = 1;
				self.processingFlag = false;
				self.formSubmittable = true;
			};
			
			$scope.hideErrors = function() {
				self.error = 0;
				$scope.disableClass = '';
			};
			
			//for showing loader while authenticating
			this.isProcessing = function() {
				return this.processingFlag;
			};
			
			//checking which scene is presented
			this.isScenePresented = function(scn) {
				return scn === this.scene;
			};
			
			//changing scene to verification window 
			this.changeScene = function(scn) {
				this.scene = scn;
			};
			
			//fill country code in input box when a country a selected
			this.fillCountryCode = function() {
				$scope.hideErrors();
				$scope.dialCode = $scope.countryName;
			};
			
			//for checking error code showing appropriate message
			this.isErrorCode = function(error) {
				return this.error === error;
			};
			
			this.validateForm = function () {
				var sPhone = $scope.phone.trim(),
				    sDialCode = $scope.dialCode.trim(),
				    reDialCode = new RegExp("^[\+][1-9][0-9]*[ ]?[0-9]*$"),
				    rePhone = new RegExp("[^0-9 ]"),
				    reUserName = new RegExp("^[a-zA-Z][0-9a-zA-Z\.]+$")
				    reAltCredential = new RegExp("[a-zA-Z]");  //for testing if UN is provided instead of phone 
				
				//for hiding submit button
				$scope.disableClass = 'hide-button';
				
				if (sPhone.length === 0) {
					this.error = 1;
				}
				else if(reAltCredential.test(sPhone) && !reUserName.test(sPhone)) {
					this.error = 4;
				} 
				else if(!reAltCredential.test(sPhone) && rePhone.test(sPhone)) {
					this.error = 2;
				}
				else if (!reAltCredential.test(sPhone) && !reDialCode.test(sDialCode)) {
					this.error = 3;
				}
				
				if (this.error !== 0) return false;
				
				this.processingFlag = true;
				return true;
			};
			
			this.sendCredential = function () {
				if (!this.formSubmittable)
					return;
				this.formSubmittable = false;
				console.log('form submitted');
			}
//			this.inProcess = 0;	//request in process flag
//			this.sum = 0;		//sum of phone no.| just for fun
//			this.attempt = 0;   //attempt to verify code 
//			this.phone = '';
//			this.data.siphone = '';
//			this.data.sipass = '';
//			var self = this,
//				request_headers = {
//			   					'Content-Type': 'application/x-www-form-urlencoded',
//			   					'X-CSRFToken' :  $cookies.csrftoken
//			   		 			};
//	
//			this.signup = function (pan) {
//				this.inProcess = 1;
//				this.phone = this.data.tel;
//				$http({
//						url : 'authmod/signup',
//					   data : 'phone='+this.phone+'&ac='+encodeURIComponent(this.areacode),
//					   method: 'POST',
//					   headers: request_headers
//				}).success(function(res) {
//					console.log(res);
//					self.data = {};
//					self.inProcess = 0;
//					//pan.panel = 4;
//					if('success' in res) {
//						self.phone = res.phone;
//						self.areacode = res.areacode;
//						self.flag = 1;
//					}
//					else if(res.error == 1)
//						self.flag = 2; //for showing unknown error
//					else if(res.error == 2)
//						self.flag = 3; //for showing validation error
//					else
//						self.flag = 5;  //user is already registered
//					
//				}).error (function () {
//					self.inProcess = 0;
//					pan.panel = 4;
//					self.flag = 2;
//				});
//			};
//			
//			this.validateSignIn = function () {
//				var rePhone = /^[0-9]{6,13}$/,
//				    rePhrase = /^[0-9]{5}$/,
//				    phone = this.data.siphone,
//				    password = this.data.sipass;
//				
//				if(!phone || !phone.toString().match(rePhone)) {
//					$scope.inputClass1 = 'invalid-input-1';
//					$timeout(function () {
//						$scope.inputClass1 = 'red-border';
//					},1000);
//					return false;
//				}
//				$scope.inputClass1 = '';
//				if(!password || !password.match(rePhrase)) {
//					$scope.inputClass2 = 'invalid-input-1';
//					$timeout(function() {
//						$scope.inputClass2 = 'red-border';
//					},1000);
//					return false;
//				}
//				$scope.inputClass2 = '';
//				return true;
//			};
//			
//			this.signin = function(pan) {
//				$scope.inputClass2 = '';
//				$scope.inputClass1 = '';
//				
//				self.inProcess = 1;
//				var phone = this.data.siphone,
//				    code = this.data.sipass;
//				console.log($scope.areacode);
//				console.log(phone);
//				console.log(code);
//				$http({
//					url : 'authmod/signin',
//				   data : 'phone='+phone+'&ac='+encodeURIComponent($scope.areacode)+'&code='+code,
//				   method: 'POST',
//				   headers: request_headers
//			}).success(function(res) {
//				
//				console.log(res);
//				
//				if('success' in res) {
//					$window.location.href = '/';
//				}
//				else {
//					self.inProcess = 0;
//					if(res.error == 3) {
//						self.data = {};
//						self.flag = 2; //for showing unknown error
//					}
//					else if(res.error == 2) {
//						$scope.inputClass2 = 'invalid-input-1'; //for showing code error
//						$timeout(function () {
//							$scope.inputClass2 = 'red-border';
//						},1000);
//					}
//					else if(res.error == 1) {
//						$scope.inputClass1 = 'invalid-input-1';  //for invalid phone
//						$timeout(function () {
//							$scope.inputClass2 = 'red-border';
//						},1000);
//					}
//				}
//					
//				
//			}).error (function (response) {
//				console.log(response);
//				self.inProcess = 0;
//				pan.panel = 4;
//				self.flag = 2;
//			});
//		};
//			
//			this.checkFlag = function(arg) {
//				return arg === this.flag;
//			}
//			
//			this.checkProcess = function(arg) {
//				return arg === this.inProcess;
//			}
//			
//			this.changeFlag = function (arg) {
//				this.flag = arg;
//			}
//			
//			this.verifyCode = function (frmCtrl,pan) {
//				this.inProcess = 1;
//				var self = this;
//				$http({
//					url : 'authmod/verify',
//					method : 'POST',
//					data : 'code='+self.data.vericode+'&ac='+
//							encodeURIComponent(self.areacode)+'&ph='+self.phone,
//					headers : request_headers
//				}).success(function (res) {
//					if('success' in res) {
//						self.calcsum();
//						self.flag = 4;
//						$window.location.href = '/home';
//					}
//					else if('error' in res ) {
//						self.inProcess = 0;
//						if(res['error']===1) { 
//							frmCtrl.validateForm(undefined);
//							
//							//to close panel after three unsuccessful attempt
//							self.attempt++;
//							if(self.attempt % 4 === 0) {
//								$scope.inv_code_class = 'invalid-entry';
//								$timeout(function(){
//									self.flag=0;
//									pan.showPanel(1);
//									$scope.inv_code_class = '';
//								},1300);
//								
//							}
//						}
//						else if(res['error'] === 2 || res['error']===4)
//							self.flag = 2; //for showing unknown error
//						else if(res['error'] == 3)
//							self.flag = 5;
//					}
//						
//				}).error(function (res) {
//					self.inProcess = 0;
//					self.flag = 2;
//				});
//			};
//			
//			this.calcsum = function () {
//				var sum = i = 0;
//				while(i < this.phone.length) {
//					sum += parseInt(this.phone[i++])
//				}
//				this.sum = sum;
//			}
//			
		}]);
	
})();