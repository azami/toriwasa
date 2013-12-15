'use strict';

/* Controllers */

var toriwasaControllers = angular.module('toriwasaControllers', []);

toriwasaControllers.run(
  function($rootScope, $http) {
    $http.get('api/user').success(function(data) {
      $rootScope.user = data;
  });
    $http.get('api/threads').success(function(data) {
      $rootScope.threads = data;
      $rootScope.users = [];
      $.each($rootScope.threads, function(u, t) {
        $rootScope.users.push({name: u, threads: t});
      });
  });
});

toriwasaControllers.controller('CallbackCtrl', ['$scope', '$http', '$routeParams',
  function($scope, $http, $routeParams) {
    $http.get('api/auth/verify', {params: {oauth_verifier: $routeParams.verifier}}).success(function(data) {
      window.location = window.location.origin;
    });
  }]);

toriwasaControllers.controller('IndexCtrl', ['$scope', '$http',
  function($scope, $http) {
    $scope.thread = new Thread($http);
  }]);

toriwasaControllers.controller('ThreadCtrl', ['$scope', '$http', '$routeParams',
  function($scope, $http, $routeParams) {
    $scope.upload = function(thread, file) {
      $('#upload').modal('hide');
      var fd = new FormData();
      fd.append('file', $('input[type=file]')[0].files[0]);
      $.ajax({
        url: 'api/thread/' + thread + '/upload',
        type: 'POST',
        data: fd,
        processData: false,
        contentType: false
        }).done(function() {
          document.location.reload();
      });
    };
    $scope.owner = $routeParams.user;
    $scope.thread = $routeParams.thread;
    $http.get('api/' + $routeParams.user + '/' + $routeParams.thread).success(function(data) {
      $scope.picts = data;
  })}]);


var Init = function($scope, $http, $rootScope) {
  $scope.signin = function() {
    $http.get('api/auth/url').success(function(data) {
      window.location = data;
    });
  }};


var Thread = function($http) {
  this.create = function(name) {
    $http.post('api/thread/' + name + '/create').success(function(data) {
      document.location.reload();
    });
  };
};
