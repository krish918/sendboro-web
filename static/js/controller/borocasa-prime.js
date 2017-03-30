(function() {
	
	
	angular.module("borocasa")
		
		.controller('homeFrameController', ['user','$scope','mbStatus','PushBoro',
		    function(user,$scope,mbStatus,PushBoro) {
				this.data = user.data
				var self = this;
				mbStatus.appRunning = true;
				
				$scope.init = function () {
					user.listenUpdate($scope, function (newdata) {
						self.data = user.data;
					});
					
					$scope.dpClass = 'animate-dp';
					pushUserIdentity ();
					$scope.newArrival = false;
				};

				
				var pushUserIdentity = function () {
					if(user.data.username)
						self.data.identity = user.data.username;
					else
						self.data.identity = user.data.countrycode+user.data.phone;
				};
				
				this.cancelSending = function() {
					PushBoro.cancelPush();
				};
				
		}])
		
		.controller('userPanelController', ['$scope','$timeout','$cookies',
		                            '$window','$http', '$location','$metaboro','$poll',
		    function($scope,$timeout,$cookies,$window,$http,$location,$metaboro,$poll) {
				
				var metaboro = $metaboro.$$state.value;
				this.userdata = metaboro.data;
			
				$scope.userPanelClass = [];
				$scope.userPanelIcons = [
		                         'glyphicon-folder-close',
		                         'glyphicon-cog',
		                         'glyphicon-off',
		                         ];
				$scope.logoutMsgToggle = false;
				this.logoutMsg = '';
				this.logoutClickCount = 0;
				this.panel = 0;
				
				
				var loPromise,
					cc = this.userdata.countrycode,
					phone = this.userdata.phone;
				
				this.logoutCtrl = function () {
					$scope.logoutMsgToggle = true;
					this.logoutClickCount++;
					var self = this;
					
					if (this.logoutClickCount === 1) {
						this.logoutMsg = "Click again to confirm logout.";
						loPromise = $timeout(function (){
							$scope.logoutMsgToggle = false;
							self.logoutClickCount = 0;
						},5000);
					}
					else if(this.logoutClickCount === 2) {
						$timeout.cancel(loPromise);
						this.doLogout();
					}
				};
				
				this.doLogout = function() {
					var self = this;
					this.logoutMsg = 'Logging you out...';
					var cleanup = function() {
						$timeout(function() {
							self.logoutClickCount = 0;
							$scope.logoutMsgToggle = false;
						},5000);
					};
					
					$poll.post('/logout',null)
					.then(function(res){
						if ('success' in res) {
							$window.location.href = '/';
						}
						else {
							console.log(res);
							self.logoutMsg = "Sorry! There was an error.";
							cleanup();
						}
					}, function() {
						self.logoutMsg = "Sorry! Server is not responding.";
						cleanup();
					});
				};
				
				
				this.upDispatch = function(idx) {
					if(idx === 2)
						this.logoutCtrl();
					else if(idx === 1)
						$location.url('/settings');
					else if(0 === idx)
						$location.url('/inbox');
				};
				
				this.userPanelAnimate = function (state, idx) {
					if(state===1)
						$scope.userPanelClass[idx] = 'enlarge-icon';
					else if(state===0)
						$scope.userPanelClass[idx] = '';
				};
		}])
		
		.controller('settingsController', ['$scope','$metaboro','FileUploader','$timeout','$cookies',
		    '$http',function($scope, $metaboro, FileUploader, $timeout,$cookies,$http){
				
				var metaboro = $metaboro.$$state.value,
					uploader,
					errorTimeout,
					self = this;
				
				this.panel = 1;
				this.user = metaboro.data;

				
				this.checkPanel = function(arg) {
					return this.panel === arg;
				};
				
				this.setPanel = function(arg) {
					this.panel = arg;
				}
				
				$scope.init = function () {
					document.title = 'General Settings';
					$scope.settingClass = 'animateWidget';
					$scope.unEdit = true;
					$scope.fnEdit = true;
					$scope.loaderUn = false;
					$scope.loaderFn = false;
					$scope.settings_error = false;
					initUploader();
					initSettings();
					metaboro.listenUpdate($scope, function() {
						self.user = metaboro.data
					});
				};
				
				var initSettings = function() {
					
					//setting initial display text for username and fullname
					//  plus injecting the values in input-box models
					//  in case username/fullname is already set by user.
					//  this function will be called again to update model whenever
					//  username/fullname is updated by user.
					if(!self.user.username)
						self.user.username = 'Not Set';
					else
						$scope.username = self.user.username;
					
					if(!self.user.fullname)
						self.user.fullname = 'Not Set';
					else
						$scope.fullname = self.user.fullname;
				};
				
				var initUploader = function () {
					uploader = $scope.uploader = new FileUploader ({
						url:'/api/photo',
						headers: {
							'X-CSRFToken': $cookies.csrftoken
						}
					});
					
					//to reload queue object when selected the same file
					FileUploader.FileSelect.prototype.isEmptyAfterSelection= function() {
						return true;
					}
					
					uploader.filters.push({
						name: 'sizesieve',
						fn: function (item) {
							if(item.size >7000000)
								return false;
							return true;
						}
					});
					
					uploader.filters.push({
						name: 'typesieve',
						fn: function (item) {
							if(item.type.match(/image/))
								return true;
							return false;
						}
					});
				}
				
				var uploadHandler = function (item) {
					item.upload ();
					uploader.onSuccessItem = function(item,response) {
						console.log(response);
						if('error' in response)
							showError(false, response)
						else
							metaboro.update({'photo':response});
					};
					
					uploader.onErrorItem = function(item, response) {
						showError(false, {error:3});
					};
					
					uploader.onProgressItem = function (item, progress) {
						$scope.progress = progress;
					}
					
					uploader.onCompleteItem = function (item, response) {
						$scope.progress = 0;
					}
					
				};
				
				$scope.upHandler = function () {
					uploader.onAfterAddingFile = function (item) {
						uploadHandler (item);
					}
					
					uploader.onWhenAddingFileFailed = function (item, filter) {
						showError (filter,false);
					}
				}
				
				var hideError = function () {
					errorTimeout = $timeout(function () {
						$scope.settings_error = false;
					},10000);
				};
				
				var showError = function (filter, server) {
					if(errorTimeout)
						$timeout.cancel(errorTimeout);
					if((filter && filter.name === 'sizesieve') 
							|| (server && server.error===1)) {
						$scope.errorContent = 'Please make sure the image is'
							+ ' less than 7MB in size.'
					}
					else if((filter && filter.name === 'typesieve')
								||(server && server.error===2)) {
						$scope.errorContent = 'Please make sure the'
							+' file is indeed a JPEG, BMP, GIF or PNG image.';
					}
					else if(server && server.error === 3) {
						$scope.errorContent = 'Our server is '+
						'acting weird. Please try after a moment.';
					}
					$scope.settings_error = true;
					hideError();
				};
				
				this.edit = (function (){
					
					var toggleEdit = function(arg) {
						
						//argument is the name of scope variable
						//  for each input-box and this toggles the truth value of
						//  respective input-box.
						$scope[arg] = !$scope[arg];
					};
					
					//second argument is to exec toggleEdit 
					//if value doesn't qualify to be processed further
					var sendEdit = function(model,target) {
						if(!$scope[model] || 
								($scope[model].length === 0 || 
										$scope[model].toUpperCase() == self.user[model].toUpperCase())) {
									toggleEdit(target);
						}
						else {
							processEdit(model);
						}
						
					};
					
					var processEdit = function (model) {
						var reUserName = /^([a-zA-Z]{1,}[\._\-]?[a-zA-Z0-9]{1,}){1,}$/,
							reFullName = /^[a-zA-Z]{1,}[ ][a-zA-Z]{1,}([ ][a-zA-Z]{2,}){0,}$/,
							
							invalidateInput = function(inptClass) {
							
								$scope[inptClass] = 'invalid-entry red-border';
								$timeout(function () {
									$scope[inptClass] = 'red-border';
								},1000);
								
						};
						
						if(model == 'username') {
							if($scope[model].match(reUserName)) {
								$scope.unEditClass = '';
								$scope.loaderUn = true;
								callApi($scope[model], model);
							}
							else invalidateInput('unEditClass');
						}
						else if(model == 'fullname') {
							if($scope[model].match(reFullName)) {
								$scope.fnEditClass = '';
								$scope.loaderFn = true;
								callApi($scope[model], model);
							}
							else invalidateInput('fnEditClass');
						}
					};
					
					var resetEditPanel = function (model) {
						if(model == 'username') {
							$scope.loaderUn = false;
							$scope.unEdit = true;
						}
						else if(model == 'fullname') {
							$scope.loaderFn = false;
							$scope.fnEdit = true;
						}
					};
					
					var callApi = function (value, model) {
						$http({
							url: '/api/alter',
							data: ''+model+'='+value+'',
							method: 'post',
							headers: {
								'X-CSRFToken': $cookies.csrftoken,
								'Content-Type': 'application/x-www-form-urlencoded',
							},
						})
						
						.success(function(response) {
							// disappear input text-box and tick button to let users
							//  edit again
							resetEditPanel(model);
							console.log(response);
							if('success' in response) {
								//if uname is in response update username/identity
								//  app-wide else do the same with fullname
								if('uname' in response)
									metaboro.update({
										username: response.uname,
										identity: response.uname,
									});
								else if('fname' in response)
									metaboro.update({fullname: response.fname});
							}
							else {
								//if there is an error hide loader and show error msg
								//  corresponding to the code returned
								$scope.settings_error = true
								if(response.error == 1) {
									$scope.loaderUn = false;
									$scope.errorContent = 'Your username is not valid.'
								}
								else if(response.error == 2) {
									$scope.loaderFn = false;
									$scope.errorContent = 'Your full name doesn\'t seem valid.'
								}
								else if(response.error == 3) {
									$scope.loaderUn = false;
									$scope.errorContent = 'This username is already taken.'
								}
								else {
									$scope.loaderUn = false;
									$scope.loaderFn = false;
									$scope.errorContent = 'Please try later.'
								}
							}
							
						})
						
						.error(function(response) {
							
							//to cancel any earlier timeout as this one will
							// again show an error
							$timeout.cancel(errorTimeout);
							
							// disappear input text-box and tick button
							resetEditPanel(model);
							
							//display error and define error content and run timer to 
							//  make it disappear
							$scope.settings_error = true;
							$scope.errorContent = 'Please try later.';
							hideError();
						});
						
					};
					
					return {
						toggle: toggleEdit,
						send: sendEdit
					};
					
				})();
				
				
		}]);
		
})();