import tweepy
import schedule
import time

# Twitter API keys (Replace with your own keys)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to follow back users
def follow_back():
    print("Checking for new followers...")
    for follower in tweepy.Cursor(api.get_followers).items():
        if not follower.following:
            follower.follow()
            print(f"Followed back: {follower.screen_name}")

# Function to unfollow non-followers
def unfollow_non_followers():
    print("Checking for non-followers to unfollow...")
    friends = api.get_friends()
    followers = api.get_followers()
    
    follower_ids = {f.id for f in followers}
    for friend in friends:
        if friend.id not in follower_ids:
            api.destroy_friendship(friend.id)
            print(f"Unfollowed: {friend.screen_name}")

# Schedule tasks
schedule.every(10).minutes.do(follow_back)  # Check every 10 minutes
schedule.every().day.at("12:00").do(unfollow_non_followers)  # Run daily at 12 PM

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
 
