const http = require('http');
const express = require('express');
const app = express();

const PORT = 3000;

const routes = require('./routes.js');
routes(app);

http.createServer(app).listen(PORT, function() {
	console.log('Server is bound to port: ', PORT);
});