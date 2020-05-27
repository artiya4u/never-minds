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

### Run the web hook service on your server.
- Install Python 3.5+
- Install required library `pip install -r requirements.txt`
- Export env `export MIND_USERNAME=myuser; export MIND_PASSWORD=mypassword`
- python3 app.py

### Setup the webhook
Paste your webhook URL in the URL box.
Select Post in method, and application/json in content type.
Paste the following snippet into the Body field and modify it to your liking. You should at least set the icon_url. (You can add other details like the post time, click the Add ingredient button to see what is available)
```
{
  "username":"{{UserName}}",
  "text":"{{Text}}",
  "content":{{LinkToTweet}}"
}
```