Description
===========
instagram_simple_post is a simple function to create any type of post with Instagram Graph API

You can post photo, video, and carousel album, with only one method


Requirements
============

* [filestack-python](https://github.com/filestack/filestack-python)

* [requests module](https://pypi.org/project/requests/)


Installation
============

* Complete the config.py with your Instagram Access Token, Instagram user ID and filestack API KEY
    
* You need to setup your Instagram Graph API access, tutorial [here](https://medium.com/gitconnected/automating-instagram-posts-with-python-and-instagram-graph-api-374f084b9f2b)
    
* You also need a free access to the [Filestack API](https://www.filestack.com/)

Examples
========
### From Python
```python
import instagram_simple_post

instagram_simple_post.publish_image('<PATH_TO_IMAGE>', 'Description of my post')
```

### From NodeJs

Requirements : You need to uncomment the last line of instagram_simple_post.py

```js
//Import child process module.
const {spawn} = require('child_process');
//Import PythonShell module.
const {PythonShell} =require('python-shell');

async function postInstagram(listeFichiers, desc){
    let options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: [listeFichiers, desc] //An argument which can be accessed in the script using sys.argv[1]
    };

    // Lancement du code Python
    logs = await new Promise(resolve => {
        PythonShell.run('python/instagram_simple_post.py', options, function (err, result){
            //if (err) throw err;

            // result is an array consisting of messages collected during execution of script.
            return resolve(result);
        })
    }).catch(err => console.log(err));

    // Print python program logs
    console.log(logs);

}

postInstagram('<PATH_TO_IMAGE>', 'Description of my post');
```
# Notes from author

If you don't want to use Filestack storage function, you need to edit **instagram_simple_post.py** to delete code block where the filestack upload append, detect if the media is image or video, and give direct media URLs in parameter

