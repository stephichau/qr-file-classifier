# Create Flash app

## First step: Flask module

If flask module is not installed, run `pip3 install flask`

## Second step: 


# Deploy Flask app in Heroku

## First step: Heroku Cli

First of all, you will need the Heroku CLI; If you don't have a Heroku account, sign up in  [this link](https://www.heroku.com/) and then download [Heroku Cli](https://devcenter.heroku.com/articles/heroku-cli).

Having Heroku Cli set up, proceed to *login* into the Heroku Cli by typing `heroku login` in the terminal and type the information needed.

## Second step: Files needed

1. **Procfile**: for more information, consult [Heroku Procfile](https://devcenter.heroku.com/articles/procfile). To create this, run `pip3 install guinicorn` and create a new file named *Procfile* with no extension. Finally, add the following line `web: gunicorn moduleName:appName` to Procfile.

2. **requirements.txt**: sets application dependencies by running `pip3 freeze > requirements.txt`.

## Third step: Deploy

In the application folder, run: `heroku create ${uniqueAppName}-api-heroku`. Once finished, if successful, the output will show the URL where your app is hosted.