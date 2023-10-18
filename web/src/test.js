import {PythonShell} from 'python-shell';
let pyshell = new PythonShell('../../src/tst.py');

// sends a message to the Python script via stdin
pyshell.send('hello');

pyshell.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message);
  //decode message from utf8 to utf16
  var str = message;
  var decodedString = String.fromCharCode.apply(null, new Uint16Array(str));
  console.log(decodedString);
  
});

// end the input stream and allow the process to exit
pyshell.end(function (err,code,signal) {
  if (err) throw err;
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('finished');
});