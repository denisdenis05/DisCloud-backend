# Discloud
### A personal project: uploads your files to discord
### BACKEND REPO

<br>

#### <code style="color : red">Disclaimer: This is against Discord's ToS. I am building this for learning purposes</code>

<br>

## You will also need the frontend repository
https://github.com/denisdenis05/discloud-frontend

<br>

## How does it work:

<code style="color : red">As stated before, you need the frontend component to run everything smoothly.</code>

### You insert your discord token, preferably a new bot with no access to other discord servers (technically shouldn't matter anyways).
The backend automatically creates a new server and a new channel for the bot to upload your files to. As long as you do not provide the invite link to anyone, the data should be safe and private (under the assumption nobody can randomly access the created Discord server)

### You upload your files to the frontend
The frontend will send the files to the backend, which will then upload them to discord.
![File uploaded](https://imgur.com/c62uTLe.png)


If your file is larger than 24MB (discord's file upload limit is 25MB), the backend will split it into smaller chunks and upload them one by one

![Files uploaded](https://imgur.com/GjBT3mI.png)

### When downloading, the exact opposite happens. The frontend will request the file from the backend, which will then download it from discord, merge it if necessary, and send it back to the frontend.

<code style="color : red">There is no size limit in this project. However, due to network and/or software limitations, the upload/download process may stall. Check your PC specifications and network bandwidth to approximate the maximum size of a file</code>

<code style="color : red">As of the current writing of this information on 2nd of February 2024, Discord keeps files 'untouched' for (at least) 2 years. However, this timespan cannot be guaranteed as changes may always happen on their side </code>

<br>

## Dependencies:

### Python 3
The project was built using python 3.12.0, but it should work with any python 3 version.
https://www.python.org/downloads/

### Flask
> pip install flask
> 
> pip install flask_cors

### Asyncio
> pip install asyncio

### Discord.py
> pip install discord

### gevent
> pip install gevent
