import asyncio
import csv
import os
from pathlib import Path
from datetime import datetime
from twikit import Client, TooManyRequests
from random import randint, uniform
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.environ['email']
PASSWORD = os.environ['password']
USERNAME = os.environ['username']

# Initialize client
client = Client("en-US")

MINIMUM_TWEETS = 30000
SCREEN_NAME = "NatWestBusiness"
TWEET_TYPE = "Replies"
QUERY = f"(from:{SCREEN_NAME}) until:2025-01-31 since:2020-01-01"

async def get_users(users):
    if users is None:
        users = await client.search_user(QUERY)
    else:
        wait_time = uniform(5, 10)
        asyncio.sleep(wait_time)
        users = await users.next()

    return users

async def get_tweets(tweets):
    if tweets is None:
        tweets = await client.search_tweet(QUERY, product="Top", count=20)
    else:
        wait_time = uniform(5, 10)
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()

    return tweets

async def get_user_tweets(tweets):
    user = await client.get_user_by_screen_name(SCREEN_NAME)
    user_id = user.id
    if tweets is None:
        tweets = await client.get_user_tweets(user_id, tweet_type=TWEET_TYPE, count=40)
    else:
        wait_time = uniform(5, 12)
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
        
    return tweets

async def main():
    if os.path.exists('cookies.json'):
        print('########### logging in...#############')
        await client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)
        client.save_cookies("cookies.json")
    else:
        print("########### loading cookies...########")
        client.load_cookies("cookies.json")

    output_path = Path('./data')
    os.makedirs(output_path, exist_ok=True)
    output_file = output_path / f'{SCREEN_NAME}-{TWEET_TYPE}-tweets.csv'

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'username', 'text', 'thumbnail_title', 'thumbnail_url',
            'tweet_url', 'created_at', 'retweets', 'likes', 'views'
        ])

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:

        try:
            # tweets = await get_tweets(tweets)
            # tweets = await get_users(tweets)
            tweets = await get_user_tweets(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f"{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}")
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f"{datetime.now()} - No more tweets found!")
            break

        if tweets:
            for tweet in tweets:
                tweet_count += 1
                # print([tweet_count, tweet.id, tweet.name, tweet.screen_name])
                tweet_data = [
                    tweet.user.name,
                    tweet.text,
                    tweet.thumbnail_title,
                    tweet.thumbnail_url,
                    tweet.urls,
                    tweet.created_at_datetime,
                    tweet.retweet_count,
                    tweet.favorite_count,
                    tweet.view_count,
                ]

                with open(output_file, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)

            print(f"{datetime.now()} - Got {tweet_count} tweets")

    print(f"{datetime.now()} - Done! Got {tweet_count} tweets found")

asyncio.run(main())
