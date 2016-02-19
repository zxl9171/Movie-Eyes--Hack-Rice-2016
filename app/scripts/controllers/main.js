'use strict';

/**
 * @ngdoc function
 * @name hackRiceApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the hackRiceApp
 */
angular.module('hackRiceApp')
  .controller('MainCtrl', function ($scope,$http,$timeout) {
  		$scope.show = false;
  		$scope.avatar = "http://ia.media-imdb.com/images/M/MV5BMTYyMTE0NDQwMV5BMl5BanBnXkFtZTcwMDA1NjA1Nw@@._V1_UX214_CR0,0,214,317_AL_.jpg";
  		$scope.pictures = ["http://www.jackchenmd.com/images/meet-dr-jack-chen-image.jpg","https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRAft8FUbUGpcLUD9yo_OxxWJH6X-h8jEqmzDWpQXTYAguY8vJ5xg"];
  		$scope.description = "description description description description description description description description description description description description description description description";
    	$scope.name = "Name";
    	$scope.news = [{title:"oeijgeowijgow;egij", content:"o;eigjewoigja;ogjao;egjao;ewgij"},
    					{title:"oeijgeowijgow;egij", content:"o;eigjewoigja;ogjao;egjao;ewgij"},
    					{title:"oeijgeowijgow;egij", content:"o;eigjewoigja;ogjao;egjao;ewgij"}];
    	$scope.movies = ["http://ia.media-imdb.com/images/M/MV5BMTQ1NzE3MzY0NV5BMl5BanBnXkFtZTYwNTM2MzE5._V1_UX148_CR0,0,148,200_AL_.jpg"];
    	$scope.capture = "Capture";
    	$scope.captureImage = function() {
    		var video = $("#video").get(0);
    		var scale = 0.5;
    	    var canvas = document.createElement("canvas");
    	    video.pause();
    	    canvas.width = video.videoWidth * scale;
			canvas.height = video.videoHeight * scale;
    	    canvas.getContext('2d')
    	          .drawImage(video, 0, 0, canvas.width, canvas.height);
 	
    	    // var img = document.createElement("img");
    	    // img.src = canvas.toDataURL();
    	    // console.log(canvas.toDataURL());
    	    $scope.capture = "Detecting";
    	    $http.post('http://mzpz.me:3000/api/recongize', { "image-data": canvas.toDataURL() })
    	    .then(function(originaldata){
    	    	$scope.capture = "Capture";
    	    	var data=originaldata.data;
    	    	$scope.pictures = data.related_pics;
    	    	$scope.description = data.bio;
    	    	$scope.name = data.name;
    	    	$scope.avatar = data.avatar;
    	    	$scope.birth_date = data.birth_date;
    	    	$scope.news = data.news;
    	    	$scope.show = true;
    	    }, function(err){
    	    	$scope.capture = "Capture";
    	    	$scope.show = false;
    	    	var dialog = $('#dialog').data('dialog');
        		dialog.open();
        		$timeout(function() {
    			    dialog.close();
    			}, 1000);
    	    });
    	};
//     	{name: "Jack Chen", avatar: "http://www.jackchenmd.com/images/meet-dr-jack-chen-image.jpg",…}
// avatar
// :
// "http://www.jackchenmd.com/images/meet-dr-jack-chen-image.jpg"
// birth-date
// :
// "1992-7-19"
// films
// :
// ["A", "B"]
// 0
// :
// "A"
// 1
// :
// "B"
// name
// :
// "Jack Chen"
// related-pics
// :
// ["http://www.jackchenmd.com/images/meet-dr-jack-chen-image.jpg",…]
// 0
// :
// "http://www.jackchenmd.com/images/meet-dr-jack-chen-image.jpg"
// 1
// :
// "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRAft8FUbUGpcLUD9yo_OxxWJH6X-h8jEqmzDWpQXTYAguY8vJ5xg"
  });
