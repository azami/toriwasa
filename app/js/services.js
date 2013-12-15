var toriwasaServices = angular.module('toriwasaServices', ['ngResource']);

toriwasaServices.factory('user', ['$http',
  function($http){
    return $http.get('api/user', {
      query: {method:'GET'}
    });
  }]);
