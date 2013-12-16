'use strict';

/* App Module */

var toriwasaApp = angular.module('toriwasaApp', [
  'ngRoute',
  'toriwasaControllers',
]);

toriwasaApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/toriwasa', {
        templateUrl: 'partials/index.html',
        controller: 'IndexCtrl'
      }).
      when('/callback/:verifier', {
        templateUrl: 'partials/index.html',
        controller: 'CallbackCtrl'
      }).
      when('/:user/:thread', {
        templateUrl: 'partials/thread.html',
        controller: 'ThreadCtrl'
      }).
      otherwise({
        redirectTo: '/toriwasa'
      });
  }]);
