const functions = require('firebase-functions');
var nodemailer = require('nodemailer');
const admin = require('firebase-admin');
admin.initializeApp(functions.config().firebase);

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
exports.helloWorld = functions.database.ref('/Names/{id}/{name}').onWrite((snap, context) => {
      console.log("Send email");
	  let name = snap.after.val()
	  console.log(name)
	  
	var transporter = nodemailer.createTransport({
	  service: 'gmail',
	  auth: {
		user: 'pifacetester@gmail.com',
		pass: 'Test1234!'
	  }
	});

	var mailOptions = {
		  from: 'pifacetester@gmail.com',
		  to: 'phvallabh@gmail.com',
		  subject: 'DVT entrance',
		  text: name + ' entered the building'
	};

	transporter.sendMail(mailOptions, function(error, info){
	  if (error) {
		console.log(error);
	  } else {
		console.log('Email sent: ' + info.response);
	  }
	});
	console.log("Email done")
    });

