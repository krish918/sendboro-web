(function () {	
	angular.module("init")
		.controller('authController', ['$scope','$timeout','$window','countries','$parse','$poll',
		                                  function($scope,$timeout,$window,countries,$parse,$poll) {
			
			var TIMER_CONST = 30,
				POLL_ERROR = -1,
				INVALID_CODE = -2,
				VALID_CODE = 1,
				EMPTY_POLL = 3,
				RESOLVED_CODE = -3;
			
			this.countryList = countries.fetch();
			watchTimer();
			$scope.focus = 0;
			
			var self = this,
				timer,
				pollTimer,
				authAttempt = 0,
				usrDialCode = '', 
				usrCountryCode='';  /* for temp storing country info fetched from server
								       will be used to fill up the form again
			                           in case user exits auth window */
			
			/* init() is being initialised every time auth-panel
			   comes in view */
			$scope.init = function() {
				$scope.dialCode = usrDialCode;
				$scope.countryCode = usrCountryCode;
				$scope.phone = '';
				$scope.disableClass = '';
				self.error = 0;
				self.changeScene(1);
				self.processingFlag = false;
				self.formSubmittable = true;
				self.authdata = {};
			};
			
			$scope.incrementFocus = function(e) {
				/* if clicked on some other input element in scene 1
				   focus shouldn't go back to the phone number input */
				if(self.scene == 1 && typeof e !== 'undefined')
					return;
				$scope.focus += 1;
			};
			
			function watchTimer() {
				var model = $parse('resendTimer');
				$scope.$watch(model, function(value) {
					if(value <= TIMER_CONST && value > 0) {
						$scope.resendClass = '';
						timer = $timeout(function() {
								$scope.$apply(model.assign($scope, value-1));
							},1000);
					}
					else if(value === 0){
						$timeout.cancel(timer);
						$scope.resendClass = 'active';
					}
					else {
						$scope.resendClass = '';
					}
				});
			};
						
			/* anonymous function for fetching country from user
			   location once the controller is initialised */
			
			(function() {
				$poll.get('api/country')
				.then(function(res){
					console.log(res);
					if(res.success === true) {
						for(var obj of self.countryList) {
							if(obj.code == res.data.country_code) {
								usrDialCode = $scope.dialCode = obj.dial_code;
								usrCountryCode = $scope.countryCode = obj.code;
								break;
							}
						}
						
					}
				});
			})();
			
			
			$scope.hideErrors = function() {
				if(self.processingFlag)
					return;
				self.error = 0;
				$scope.disableClass = '';
			};
			
			//for changing dialcode input on selecting country
			$scope.syncInputSelect = function() {
				$scope.hideErrors();
				for(var obj of self.countryList) {
					if($scope.countryCode == obj.code) {
						$scope.dialCode = obj.dial_code;
						break;
					}
				}
			};
			
			//for selecting correct country after changing dialCode manually
			$scope.syncInputText = function() {
				$scope.hideErrors();
				$scope.countryCode = '';
				for(var obj of self.countryList) {
					if($scope.dialCode == obj.dial_code) {
						$scope.countryCode = obj.code;
						break;
					}
				}
			};
			
			//for showing loader while authenticating
			this.isProcessing = function() {
				return this.processingFlag;
			};
			
			//checking which scene is presented
			this.isScenePresented = function(scn) {
				return scn === this.scene;
			};
			
			//changing scene of auth-panel 
			this.changeScene = function(scn) {
				/* scn = 0 is called on closing the authpanel. So no more action , just
				   make the scene zero and return. */
				if(scn === 0) {
					this.scene = scn;
					return;
				}
				
				/* we will give an intermediate value to first let the earlier
				   scene disappear and then new one appear. */
				this.scene = -1;
				this.error = 0;
				//to keep track of keyup when entering code
				
				$timeout.cancel(pollTimer);
				
				self.codePressCount = 0;
				if(scn == 1)
					$timeout.cancel(timer);

				$timeout(function(){
					self.scene = scn;
					$scope.incrementFocus();
					// for showing submit-button
					$scope.disableClass = '';
					if(scn == 2) {
						//for truncating all codes
						$scope.code = [];
						//resetting timer to 30 so that it can be watched
						$scope.resendTimer = TIMER_CONST;
					}
				},400);
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
				    reUserName = new RegExp("^[a-zA-Z][0-9a-zA-Z\. ]+$")
				    reAltCredential = new RegExp("[a-zA-Z]");  //for testing if UN is provided instead of phone 
				
				total_length_phone = (sDialCode.replace(' ','').length - 1) + sPhone.replace(' ','').length
				//for hiding submit button
				$scope.disableClass = 'hide-button';
				
				if (sPhone.length === 0) {
					this.error = 1;
				}
				else if(reAltCredential.test(sPhone) && !reUserName.test(sPhone)) {
					this.error = 4;
				} 
				else if(!reAltCredential.test(sPhone) && 
						(rePhone.test(sPhone) || sPhone.length < 4 || total_length_phone > 15)) {
					this.error = 2;
				}
				else if (!reAltCredential.test(sPhone) && 
						(!reDialCode.test(sDialCode)|| $scope.countryCode.trim().length==0)) {
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
				
				var
					phone = cachedPhone = encodeURIComponent($scope.phone),
					dialcode = cachedDc = encodeURIComponent($scope.dialCode),
					countrycode = encodeURIComponent($scope.countryCode),
					data = 'crdntl='+phone+'&dc='+dialcode+'&cc='+countrycode;
				
				$poll.post('authmod/signon',data)
				
				.then(function(res) {
					self.processingFlag = false;
					self.formSubmittable = true;
					if(res.success == false) {
						self.error = res.errorcode;
					}
					else {
						
						self.changeScene(2);
						
						self.authdata = res;
						
						if ('uname' in self.authdata)
							$scope.username = self.authdata.uname;
						else
							$scope.username = '';
						$scope.codeTarget = self.authdata.dialcode+' '+self.authdata.phone
						initiateChallengePolling();
					}
				}).catch(function(res) {
					self.formSubmittable = true;
					self.processingFlag = false;
					self.error = res.errorcode;
				});
			};
			
			function initiateChallengePolling() {
				$poll.get('authmod/challenge')
				
				.then(function(res) {
					console.log(res);
					if(res.status == POLL_ERROR || res.status == RESOLVED_CODE)
						self.error = POLL_ERROR;
					else if(res.status == EMPTY_POLL)
						pollTimer = $timeout(initiateChallengePolling, 3000);
					else if(res.status == INVALID_CODE) {
						self.error = res.status;
						resetCodeInputView();
						$timeout.cancel(pollTimer);
						authAttempt++;
						if (authAttempt > 3) {
							$timeout(function(){
								self.changeScene(1);
							},2000);
							authAttempt = 0;
							return;
						}
						pollTimer = $timeout(initiateChallengePolling, 3000);
					}
					else if(res.status == VALID_CODE) {
						var idx, data = '';
						for(idx=0; idx<5; idx++)
							$scope.code[idx] = '#';
						self.codePressCount = 5;
						self.processingFlag = true;
						if ('return' in self.authdata)
							data += 'mode=i&uid='+self.authdata.userid;
						else {
							data += 'mode=u';
							data += '&dc='+encodeURIComponent(self.authdata.dialcode);
							data += '&ph='+self.authdata.phone;
							data += '&cc='+self.authdata.countrycode
						}
						$poll.post('authmod/authent',data)
						.then(function(res){
							if (res.success == false) {
								resetCodeInputView();
								self.error = res.errorcode;
							}
							else {
								$window.location.href = '/';
							}
						});
					}
				}).catch(function(res){
					self.error = res.errorcode;
				});
			};
			
			function resetCodeInputView() {
				$scope.resendTimer = 0;
				self.processingFlag = false;
				$scope.code = [];
				self.codePressCount = 0;
			};
			
			this.resendCode = function() {
				if ($scope.resendTimer !== 0)
					return;
				//a negative value for timer makes sure there's no re-submission 
				// and this value won't be even watched by scope watcher
				
				$scope.resendTimer = -1;
				var data;
				
				if ('return' in this.authdata)
					data = 'type=i&id='+this.authdata.userid;
				else
					data = 'type=u&dc='+self.authdata.dialcode+'&ph='+self.authdata.phone;
				
				$poll.post('authmod/resend', data)
				
				.then(function(res){
					if(res.success == false) {
						throw res;
					}
					else {
						/* if successful restart timer so that if code is not received again
						   user can try again */
						$scope.resendTimer = TIMER_CONST;
					}
				}).catch(function(res){
					self.error = res.errorcode;
					
					/* timer set to zero so that no countdown occurs and
					   resend button activated so that user can try again */
					$scope.resendTimer = 0;
					
					//to make error disappear after 5 sec.
					$timeout(function(){
						self.error = 0;
					},5000);
					
					console.log(res);
				});
			};
			
			$scope.fillCodeInput = function(event) {
				var key = event.keyCode,
					keyValue;
				console.log(key);
				//for stopping backspace from going back in history in some browsers
				if(key === 8)
					event.preventDefault();
					
				if (self.codePressCount > 4)
					return;
				
				if((key >= 48 && key <=57) || (key >= 96 && key <= 105)) {
					self.error = 0;
					keyValue = key % 48;
					$scope.code[self.codePressCount] = keyValue;
					self.codePressCount += 1
					if(self.codePressCount > 4) {
						self.processingFlag = true;
						sendCode();
					}
				}
				//backspace should delete previous entry until every
				// code input box is filled up
				else if(key == 8 && self.codePressCount != 0) {
					self.codePressCount -= 1;
					$scope.code[self.codePressCount] = '';
				}
			};
			
			function sendCode() {
				var endpoint = '/';
				$scope.code.forEach(function(value){
					endpoint += value;
				});
				$poll.post(endpoint, null)
				.then(function(res){
					console.log(res);
					if(res.success == false) {
						throw 'UNKNOWN ERROR';
					}
				}).catch(function(res) {
					self.processingFlag = false;
					$scope.code = [];
					self.codePressCount = 0;
					self.error = -1;
				});
			};
			
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