const fs = require('fs');

require('dotenv').config();

function getEnvAsArray() {
  const envArray = [];
  for (let key in process.env) {
    if (process.env.hasOwnProperty(key)) {
      envArray.push(process.env[key]);
    }
  }

  global.console.log(envArray);
  return envArray;
}

function scanSourceCode(directory, staticStrings = [], envVariablesArray = []) {
  if (!staticStrings.length) {
    console.log('No static strings provided.');
  }

  if (!envVariablesArray.length) {
    console.log('No environment variables provided.');
  }

  // const additionalTargetStrings = readTargetStrings(envVariables);
  // Concatenate the two arrays and convert to a Set to remove duplicates
  let targetStrings = [...new Set([...staticStrings, ...envVariablesArray])];

  const foundLines = [];

  const files = fs.readdirSync(directory, { withFileTypes: true });
  files.forEach((file) => {
    const filePath = directory + '/' + file.name;
    const fileContent = fs.readFileSync(filePath, 'utf8').split('\n');
    fileContent.forEach((line, lineNum) => {
      targetStrings.forEach((targetString) => {
        if (line.includes(targetString)) {
          foundLines.push({
            filePath,
            lineNum: lineNum + 1,
            lineContent: line.trim(),
            targetString,
          });
          return; // Once a target string is found in a line, no need to check further
        }
      });
    });
  });

  return foundLines;
}

const directoryToScan = './build';
// const staticStrings = [' react-mount-point-unstable '];
const staticStrings = [];
const envVariablesArray = getEnvAsArray();

const foundLines = scanSourceCode(
  directoryToScan,
  staticStrings,
  envVariablesArray
);

if (foundLines.length > 0) {
  console.log('Found the following strings in the source files:');
  //   foundLines.forEach(({ filePath, lineNum, lineContent, targetString }) => {
  //     console.log(`File: ${filePath}, Line: ${lineNum}, Content: ${lineContent}`);
  //   });
} else {
  console.log('No strings were found in any files.');
}
