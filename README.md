# Never Minds - Tweet to Minds
Tweet to Minds by connect to IFTTT Twitter -> Minds Post.

## Getting start
### Set up IFTTT for tweet
- Go to https://ifttt.com/ and create an account (if you don't already have one).
- Click on you profile icon in the top right corner
- Click on Create
- Click on `This`
- Search for Twitter
- Click on the Twitter square
- Select a trigger like New tweet by you or New tweet by a specific user
- Set the options for the selected trigger (depending on which you selected)
- Click on `That`
- Search for Webhook
- Select the Webhook square
- Select the Make a web request action

### Run the web hook service on Heroku.
- Clone this repo `git clone https://github.com/artiya4u/never-minds.git`
- Go to the code. `cd never-minds`
- Login to your Heroku account `heroku login`
- Create new Heroku apps to run this webhook `heroku create`
- Config username and password for the apps. 
```
heroku config:set MINDS_USERNAME="myusername"
heroku config:set MINDS_PASSWORD="mypassword"
```
- Commit this code to Heroku
```
git add .
git commit -m "Committing all the directory files to Heroku"
git push heroku master
heroku open
```



### Setup the webhook
Paste your webhook URL (`https://my-app.herokuapp.com/post`) in the URL box.
Select Post in method, and application/json in content type.
Paste the following snippet into the Body field and modify it to your liking. You should at least set the icon_url. (You can add other details like the post time, click the Add ingredient button to see what is available)
```
{
    "username":"<<<{{UserName}}>>>",
    "text":"<<<{{Text}}>>>",
    "content":"<<<{{LinkToTweet}}>>>"
}
```
