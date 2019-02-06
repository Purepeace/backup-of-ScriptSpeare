//Author: Mustafa Kurugollu 2288113k
//Function that returns List of Adaptations given the Category and Play names a user has selected

const AWS = require('aws-sdk');
const s3 = new AWS.S3();


exports.handler = async (event) => {
  //category and play will both be inputted via API to this lambda function
  const category = event.category;
  const play = event.play_name;
  
  //This is the directory of the folder to choose from
  const folder = category + "/" + play + "/";
  const folder_name_length = folder.length;
  
  const requiredKeys = [];
  const allKeys = [];
  await getAllKeys({ Bucket: 'scriptspeare-media-files' }, allKeys);
  
  
  await allKeys.forEach(function(element){
      if (element.substr(0, folder_name_length) === folder && element.substr(element.length - 4, element.length) === ".mp4") {
          requiredKeys.push(element.slice(folder_name_length, (element.length - 4)));
      }
  });
  
  return requiredKeys;
};

//returns all keys in bucket
async function getAllKeys(params, keys){
  const response = await s3.listObjectsV2(params).promise();
  response.Contents.forEach(obj => keys.push(obj.Key));

  if (response.IsTruncated) {
    const newParams = Object.assign({}, params);
    newParams.ContinuationToken = response.NextContinuationToken;
    await getAllKeys(newParams, keys); // RECURSIVE CALL
  }
}