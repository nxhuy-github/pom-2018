const { spawn } = require('child_process');
const Item = require('../Item');

function connectToPython(link, fileName, dT) {
    return new Promise((resolve, reject) => {
        let str = '';
        let py = spawn('python', [fileName]);
        
        py.stdin.write(JSON.stringify(link));
        py.stdin.end();

        py.stdout.on('data', function(data){
            str += data.toString();
            //dT = JSON.parse(data.toString());
        });   
        py.stdout.on('end', function(){
            dT = JSON.parse(str);
            console.log('Data: ', typeof dT);
            dT = generateItems(dT);
            resolve(dT);
        });
        py.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
    });
}

function generateItems(dT){
    let arrItems = [];
    dT.forEach((element, index) => {
        let item = new Item(index, 
                            element.motif,
                            element.coverage,
                            element.pos_cov, element.neg_cov, 
                            element.length,
                            element.items,
                            element.area,
                            0);
        arrItems.push(item);
    });
    return arrItems;
};

function sendDataToPython(fileName, storedFile, dT){
    return new Promise((resolve, reject) => {
        let py = spawn('python', [fileName]);

        py.stdin.write(JSON.stringify(storedFile + '&' + JSON.stringify(dT)));
        py.stdin.end();

        py.stdout.on('data', function(data){
            console.log(data.toString());
        });   
        py.stdout.on('end', function(){
            resolve('Send successfully');
        });
        
    });
};

module.exports = {connectToPython, generateItems, sendDataToPython};
