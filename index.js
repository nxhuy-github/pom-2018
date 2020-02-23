const express = require('express');
const bodyParser = require('body-parser');
const parser = bodyParser.urlencoded({extended: false});
const Item = require('./Item');
const { connectToPython, generateItems, sendDataToPython } = require('./js/helper');

const app = express();
app.listen(3000, () => console.log('Server started...!'));
app.set('view engine', 'ejs');
app.set('views', './views');
app.use(express.static('public'));


let dataTable;

app.get('/', (req, res) => {
    let dT;
    let link = './public/data.csv';
    let fileName = './mypython.py';
    connectToPython(link, fileName, dT)
    .then(result => {
        dataTable = result;
        res.render('home', { dataTable, storedfile: './public/stored.csv' })
    })
    .catch(err => console.log('An error has occured...',err));
});

app.get('/mushrooms', (req, res) => {
    let dT;
    let link = './public/mushrooms.csv';
    let fileName = './mypython.py';
    dataTable = null;
    connectToPython(link, fileName, dT)
    .then(result => {
        dataTable = result;
        res.render('home', { dataTable, storedfile: './public/mushrooms_stored.csv' })
    })
    .catch(err => console.log('An error has occured...',err));
})

app.get('/accidents', (req, res) => {
    let dT;
    let link = './public/accidents.csv';
    let fileName = './mypython.py';
    dataTable = null;
    connectToPython(link, fileName, dT)
    .then(result => {
        dataTable = result;
        res.render('home', { dataTable, storedfile: './public/accidents_stored.csv' })
    })
    .catch(err => console.log('An error has occured...',err));
})

app.post('/finish', parser, (req, res) => {
    let fileName = './mypython.py';
    let storedFile = req.body.storedfile;
    let url = ''
    if (storedFile === './public/stored.csv'){
        url = '/';
    } 
    if (storedFile === './public/mushrooms_stored.csv') {
        url = '/mushrooms'
    }
    if (storedFile === './public/accidents_stored.csv') {
        url = '/accidents'
    }
    dataTable.forEach(element => {
        if(parseInt(req.body[element.id]) === 1){
            element.likeItem();
        }
        if(parseInt(req.body[element.id]) === 0){
            element.dislikeItem();
        }
    });
    //console.log(JSON.stringify(dataTable));
    sendDataToPython(fileName, storedFile, dataTable)
    .then(result => console.log('Result: ', result))
    .catch(err => console.log(err))
    res.render('success', {message: 'Feedback successfully', url});
});
