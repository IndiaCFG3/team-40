/* eslint-disable promise/always-return */
/* eslint-disable prefer-arrow-callback */
const functions = require('firebase-functions');
const firebase = require('firebase');
const firestore = require('firebase/firestore');
const express = require('express');
const cors = require('cors')
const admin = require('firebase-admin');
var bodyParser = require('body-parser');
const fs = require('fs');
const Busboy = require('busboy');
const path = require('path');
const os = require('os');
//const uuidv4 = require('uuid/v4');
const { v4: uuidv4 } = require('uuid');
const uuid = uuidv4();

var serviceAccount = require("./permissions.json");
storageBucket= "solidarieta-b44e3.appspot.com";
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://solidarieta-b44e3.firebaseio.com",
  storageBucket: storageBucket
});

const db = admin.firestore();
const storage = admin.storage().bucket();

const app = express();
app.use(bodyParser.urlencoded({ limit: '500mb', extended: true, parameterLimit: 1000000 }));
app.use(bodyParser.json());
app.use(cors({ origin: true }));

const runtimeOpts = {
    timeoutSeconds: 120,
    memory: '1GB'
}
exports.widgets = functions.runWith(runtimeOpts).region('asia-east2').https.onRequest(app);

app.post('/python', async (req, res) => {
  console.log(req.body);

  // Add a new document with a generated id.
  db.collection("searches").add({
    name: req.body.somevalue
}).then(function(docRef) {
    console.log("Document written with ID: ", docRef.id);
})
.catch(function(error) {
    console.error("Error adding document: ", error);
});

  res.status(200).send({message: "hello from server"});
})

app.post('/mobilizerindb', async (req, res) => {
  console.log(req.body);

  // Add a new document with a generated id.
  db.collection("mobilizer").add({
    name: req.body.name,
    emailaddress:req.body.emailaddress
}).then(function(docRef) {
    console.log("Document written with ID: ", docRef.id);
})
.catch(function(error) {
    console.error("Error adding document: ", error);
});
})



