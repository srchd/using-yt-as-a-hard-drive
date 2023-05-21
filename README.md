Using YouTube as a hard drive.
==============================

About
-----

YTHD (or Using YouTube as a Hard Drive) is an app, which lets you to upload almost any files to the video sharing platform, and store it there, without losing any kind of information. You don't have to worry about some stealing your precious data, as every encoded file (video) are unlisted, which means that only the people, who have the link can access it.

Prerequisites
-------------

 - A google account
 - Anaconda with `python>=3.9` [Download here](https://www.anaconda.com/download)
 - Internet connection

Getting your credentials
------------------------

 - **Method one:** Follow all the steps on [how to get your credentials](https://github.com/srchd/using-yt-as-a-hard-drive/tree/main/src/youtube/credentials#readme) and put them inside `src\youtube\credentials` folder
 - **Method two:** Use our [chrome extension](https://github.com/srchd/using-yt-as-a-hard-drive/tree/main/src/chrome_ext_create_project) for creating credentials.json files

How to use it (maybe there will be pictures too)
-------------

 - If everything is set up correctly, start the application via `start_application.bat` file. This will take some minutes, due to conda *extremely fast* speed.
 - From here you can either upload or download a file.

**NOTE:** When the application opens up a browser, directing you to the google sign in surface, just follow their steps, it is an intended behaviour. If you do not allow the application those rights, it just simply won't work :c

Uploading a file
----------------

 - Select your file via the file selector
 - Click on `Upload file` button
 - You can enter your custom title and custom description for your file.
 - Click on `OK`
 - Wait for the process to finish. This will encode your file, and then will upload it to YouTube.

If everything went as intended, you should see an `UPLOAD SUCCESSFUL` text in the bottom right corner of the application

**NOTE:** The videos are unlsited, which means that only the people with the link can access them, so unless you share your credentials with others, your files are kept in secret.

Downloading a file
------------------

If your credentials are correct, you can see all your uploaded files inside the `Listbox` widget.

 - Select the file you want to download
 - Click on `Download File` button
 - Wait for the process to finish. This will decode the video, then will create your original file, and will place it *somewhere*