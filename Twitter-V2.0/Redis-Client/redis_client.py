import redis
import redis_login
import json

# Connect to the Server
r = redis.Redis(
    host = redis_login.HOSTNAME,
    port = redis_login.PORT,
    password = redis_login.PASSWORD
)

# Open tweets file and store it as a dictionary in a variable
file = open('streamed_tweets.json')
tweets_json = json.load(file)

# Set variable object as the json object in Redis Server
r.execute_command('JSON.SET', 'object', '.', json.dumps(tweets_json))

# Get object variable from the Redis Server
reply = json.loads(r.execute_command('JSON.GET', 'object'))