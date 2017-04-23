(function (){
	
	var ctrlFunc = function($scope, $timeout, $poll, $metaboro) {
		
		var self = this,
			ERROR_INVALID_USER = 'invalid_username',
			ERROR_CONTACT_EXIST = 'already_exist';

		this.addContactFlag = 0;
		this.error = 0;
		this.mainContactList = [];
		
		$scope.init = function() {
			$scope.animateWidget = 'animateWidget';
			this.contact_error = false;
			this.contacts_empty = true;
			this.processing = false;
			this.contactlist = [];
			this.contactAdded = false;
			$scope.dialCode = $metaboro.$$state.value.data.dialcode;
			loadContacts();
		};

		this.hasErrorInFetchingContact = function() {
			return this.contact_error;
		}

		this.isProcessing = function() {
			return this.processing;
		}

		this.isContactsEmpty = function() {
			return this.contacts_empty;
		}

		this.isContactAdded = function() {
			return this.contactAdded;
		}

		var loadContacts = function() {
			self.processing = true;
			var endpoint = 'contact/getlist'
			$poll.get(endpoint)

			.then(function(response) {
				console.log(response);
				self.processing = false;
				self.contacts_empty = false;
				if(response.status != $poll.STATUS_OK)
					throw $poll.SERVER_ERROR
				
				if(response.contacts.length == 0) {
					self.contacts_empty = true;
					return;
				}
				self.mainContactList = self.contactlist = response.contacts;
				
			})

			.catch(function(response) {
				self.contact_error = true;
				self.processing = false;
			});
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
			if(val == 0)
				AddContact.clearForm();
		}
		
		this.initAddContact = function() {
			if(!AddContact.validateData())
				return;
			AddContact.sendData();
		};

		this.makePristine = function() {
			AddContact.makePristine();
		};
	
		var AddContact = (function() {

			var validateAddContactForm = function() {
				if(!$scope.contactName || $scope.contactName.trim().length == 0) {
					setError(1);
					$scope.addContactErrorText = "Contact name missing.";
					return false;
				}

				if((!$scope.userName || $scope.userName.trim().length == 0) 
						&& (!$scope.phoneNum || $scope.phoneNum.trim().length == 0 || 
						!$scope.dialCode || $scope.dialCode.trim().length == 0)) {
					setError(1);
					$scope.addContactErrorText = "Username or Phone is required.";
					return false;
				}
				
				if($scope.phoneNum && $scope.phoneNum.trim().length != 0 
					&& isNaN($scope.phoneNum)) {
						setError(1);
						$scope.addContactErrorText = "Invalid Phone Number";
						return false;
				}

				return true;
			};

			var sendNewContactsData = function() {
				if(self.isAddingContact)
					return;
				toggleAddingContactProcessing(true);

				var data = 'cn='+encodeURIComponent($scope.contactName);
				if($scope.userName) {
					data += "&cu="+encodeURIComponent($scope.userName);
				}
				else {
					data += "&cd="+encodeURIComponent($scope.dialCode);
					data += "&cp="+encodeURIComponent($scope.phoneNum);
				}

				var endpoint = 'contact/put';
				$poll.post(endpoint,data)

				.then(function(res) {
					toggleAddingContactProcessing(false);

					if(ERROR_INVALID_USER in res) {
						setError(1);
						$scope.addContactErrorText = "Invalid Username";
						return;
					}

					if(ERROR_CONTACT_EXIST in res) {
						setError(1);
						$scope.addContactErrorText = "Contact already exists.";
						return;
					}

					if(res.status != $poll.STATUS_OK)
						throw $poll.STATUS_FAILED;
					
					self.contactAdded = true;
					clearAddContactForm();
					$timeout(function(){
						self.contactAdded = false;
					}, 4000);
					loadContacts();
				})

				.catch(function(res) {
					toggleAddingContactProcessing(false);
					setError(1);
					$scope.addContactErrorText = "Error in adding contact.";
					$timeout(function() {
						setError(0);
					}, 4000);
				});
			};

			var toggleAddingContactProcessing = function(val) {
				self.isAddingContact = val;
				$scope.addingContactClass = val ? 'adding-contact': '';
			}

			var pristineError = function() {
				if(self.error == 1)
					setError(0);
			};
		
			var setError = function(val) {
				self.error = -1;
				$timeout(function(){
					self.error = val;
				},200);
			};

			var clearAddContactForm = function() {
				$scope.contactName = '';
				$scope.userName = '';
				$scope.phoneNum = '';
				setError(0);
			}

			return {
				validateData: validateAddContactForm,
				sendData: sendNewContactsData,
				makePristine: pristineError, 
				clearForm: clearAddContactForm,
			};
		})();

		this.searchContacts = function() {
			var query = $scope.searchContactQuery;
			if(!query || query.trim().length == 0) {
				self.contactlist = self.mainContactList;
				return;
			}

			self.contactlist = [];

			for(var contact of self.mainContactList) {
				if(contact.contact_name.indexOf(query.trim()) != -1) {
					self.contactlist.push(contact);
				}
			}

		};

		this.setRecipient = function(username, phone,native) {
			var recipient;
			$scope.blind = (native == 1) ? false : true;
			if(typeof username !== 'undefined') {
				$scope.recipient = username;
				return;
			}

			$scope.recipient = phone;
		};

		$scope.getRecipient = function(e) {
			var node = e.currentTarget;
			var username = node.querySelector('.recipient-candidate.username'),
				phone = node.querySelector('.recipient-candidate.phone'),
				native = node.querySelector('.native-info');
			
			$scope.blind = (native.value == 1) ? false : true;
			if(username.innerHTML.trim().length != 0) {
				$scope.recipient = username.innerHTML.trim();
				return true;
			}

			$scope.recipient = phone.innerHTML.trim();
			$scope.blind = true;
			return true;
		};
		
	};	
	
	angular.module("borocasa")
	
	.controller('quickContactController', ctrlFunc);
	
})()