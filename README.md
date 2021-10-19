Clone the repo:
---------------
1. Git clone git@github.com:jayakrishnanj/sentiment_api.git
2. Go to sentiment_api folder

Setting up local Environment for notification
---------------------------------------------
1. Create `.env` file in sentiment_api folder
2. Add `EMAIL` and `KEY` for notification: https://support.google.com/mail/answer/185833?hl=en
    Ex.: EMAIL="xyz@gmail.com"
        KEY="abcd"

Create Upload folder
--------------------
Create upload folder in app folder. `Note:` This is temporary, it will be fixed in future release.


There are two ways you can install application:
===============================================

Manual Approach: Install dependecies manually:
----------------------------------------------
Install python3 and pip3 via homebrew

Install all the dependencies:

Run `pip3 install -r requirements.txt`

Run the app.

1. Go to app folder
2. Run `python3 main.py`

Docker Approach: Install and Run using docker:
-----------------------------
1. Make sure docker is install in system and running
2. Go to sentiment_api folder
3. Run `docker build -t sentiment-app:latest .`
4. Run `docker run -it sentiment-app`
5. Run app in docker container `docker run -it -d -p 8000:8000 sentiment-app`
6. Run `docker stop` to exit.


Note: Email notification
------------------------
There is one config available to disable the email notification for actual users. use `DEVELOPMENT_MODE` to `True` if you are using the app in development mode.
