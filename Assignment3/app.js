var MongoClient = require('mongodb').MongoClient;
var ObjectId = require('mongodb').ObjectID;
var fs = require('fs');

// The database connection URI
var url = 'mongodb://localhost:27017/w205assignment3';

MongoClient.connect(url, function(err, db) {
  console.log("Connected!");
  global.db = db;
  collection=db.collection("tweets");

	startDay1 = new Date("2015-02-14T09:00:00+01:00");
	endDay1 = new Date("2015-02-14T16:00:00+01:00");
	startDay2 = new Date("2015-02-15T09:00:00+01:00");
	endDay2 = new Date("2015-02-15T16:00:00+01:00");

  //Query 1: get person who tweeted the most
	collection.aggregate(
		[
			{
				$group : {
					_id:{screen_name:"$screen_name"}, //group by city and product
					num_tweets: {$sum:1}
				}
			},
			{
				$sort: {num_tweets:-1}
			}
		],function(err,docs){
			console.log("\nAnswer to Question 1: "+docs[0]['_id']['screen_name']+" tweeted the most with "+docs[0]['num_tweets']+" tweets");
			// console.log(docs);
		}
	);

  // //Query 2: top 10 hashtags used
  setTimeout(function(){  //setting timeout so queries don't happen at the same time
	  // first establish function for counting arrays of hashtags with sorting
	  function count_hashtags(hashtags_mongo) {
	  	var count = {};
	  	for (var key in hashtags_mongo){
	  		hashtags_tweet = hashtags_mongo[key]['hashtags'];
	  		if (hashtags_tweet.length>0){
					for (key2 in hashtags_tweet){
						hashtag = hashtags_tweet[key2];
			  		if (count.hasOwnProperty(hashtag)) count[hashtag]+=1;
			  		else count[hashtag]=1;					
					}  			
	  		}
	  	}
	  	//convert into array for sorting
	  	var sort_array = [];
	  	for (var key in count) {
	    	sort_array.push({hashtag:key,count:count[key]});
			}
			sort_array.sort(function(x,y){return y.count - x.count});
	  	return sort_array;
	  }

	  // perform MongoDB query
	  var hashtags_temp = [];
	  collection.find(
		  {},
		  {hashtags:1}
	  ).toArray(function(err,docs){
	  	hashtags_count = count_hashtags(docs);
	  	console.log("\nAnswer to Question 2: These are the top 10 most used hashtags among all the tweets:");
	  	for (var i=0; i<10; i++) console.log(hashtags_count[i]);
	  })
	},1000);

  //Query 3: tweets produced per hour
  setTimeout(function(){  //setting timeout so queries don't happen at the same time
		var t0 = startDay1;
		var t1 = new Date(t0.getTime()+60*60000); //increment one hour
		day = 1 //set intial day
		endDay = endDay1; //set intial end time for the day to be end of day 1
		
		console.log("\nAnswer to Question 3: Hourly tweets in chronological order:");
		(function loop() {
			collection.aggregate([
				{
					$match : {"created_at" : {$gte:t0,$lt:t1}}
				},
				{
					$group : {
						_id: t0, //group by each hour
						tweets_num: {$sum:1}
					}
				}
			],function(err,docs){

				// convert time into CET based on my local timezone
				var t0_utc = t0.getTime() + (t0.getTimezoneOffset() * 60000);
				var t0_cet = new Date(t0_utc + 3600000);
				var t1_cet = new Date(t0_cet.getTime() + 3600000);

				// create strings for outputing date and time
				date_cet = t0_cet.toLocaleString().slice(4,15);
				t0_cet = t0_cet.toLocaleString().slice(16,-18);
				t1_cet = t1_cet.toLocaleString().slice(16,-18);

				if (docs.length>0){
					console.log("On "+date_cet+" between "+t0_cet+" and "+t1_cet+" (CET), there are "+docs[0]['tweets_num']+" tweets");
				}
				else {
					console.log("On "+date_cet+" between "+t0_cet+" and "+t1_cet+" (CET), there are 0 tweets");
				}

				if (t0<endDay-3600000){	//loop through each hour during the day till end of day
					t0=t1;
					t1=new Date(t0.getTime()+3600000);
					loop();
				}
				else if (day==1) {  //check if it's end of first day or not
					t0=startDay2;
					t1=new Date(t0.getTime()+3600000);
					endDay = endDay2;
					day+=1
					loop();
				}
			});
		}()); 
		//notice that need to implement immediate function for looping each hour
		//this is needed due to asynchrous nature of javascript
	},4000);

});

