import argparse
import base64
import json
import os
import shutil
import sys

import dateutil.parser
import requests


class Downloader:

    def __init__(self, api_key, api_secret):
        self.bearer_token = self.bearer(api_key, api_secret)
        self.last_tweet = None
        self.count = 0

    def download_images(self, user, save_dest):
        '''Download and save images that user uploaded.

        Args:
            user: User ID.
            save_dest: The directory where images will be saved.
        '''

        tweets = self.get_tweets(user, self.last_tweet)
        while len(tweets) > 0:
            for tweet in tweets:
                # create a file name using the timestamp of the image
                timestamp = dateutil.parser.parse(tweet['created_at']).timestamp()
                fname = str(int(timestamp))

                # save the image
                image = self.extract_image(tweet)
                self.save_image(image, save_dest, fname)
                self.last_tweet = tweet['id']
            tweets = self.get_tweets(user, self.last_tweet)

    def bearer(self, key, secret):
        '''Receive the bearer token and return it.

        Args:
            key: API key.
            secret: API string.
        '''

        # setup
        credential = base64.b64encode(bytes('{}:{}'.format(api_key, api_secret), 'utf-8')).decode()
        url = 'https://api.twitter.com/oauth2/token'
        headers = {
            'Authorization': 'Basic {}'.format(credential),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        payload = {'grant_type': 'client_credentials'}

        # post the request
        r = requests.post(url, headers=headers, params=payload)

        # check the response
        if r.status_code == 200:
            return r.json()['access_token']
        else:
            return None

    def get_tweets(self, user, start):
        '''Download user's tweets and return them as a list.

        Args:
            user: User ID.
            start: Tweet ID.
        '''

        # setup
        bearer_token = self.bearer_token
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        headers = {
            'Authorization': 'Bearer {}'.format(bearer_token)
        }
        payload = {'screen_name': user, 'count': 200, 'include_rts': False}
        if start:
            payload['max_id'] = start

        # get the request
        r = requests.get(url, headers=headers, params=payload)

        # check the response
        if r.status_code == 200:
            tweets = r.json()
            if len(tweets) == 1:
                return []
            else:
                print('Got ' + str(len(tweets)) + ' tweets')
                return tweets if not start else tweets[1:]
        else:
            return []

    def extract_image(self, tweet):
        '''Return the url of the image embedded in tweet.

        Args:
            tweet: A dict object representing a tweet.
        '''

        if 'media' in tweet['entities']:
            return tweet['entities']['media'][0]['media_url']
        else:
            return None

    def save_image(self, image, path, timestamp):
        '''Download and save an image to path.

        Args:
            image: The url of the image.
            path: The directory where the image will be saved.
            timestamp: The time that the image was uploaded.
                It is used for naming the image.
        '''

        if image:
            print('Saving ' + image)

            # image's path with a new name
            ext = os.path.splitext(image)[1]
            save_dest = os.path.join(path, timestamp + ext)

            # save the image in the specified directory
            r = requests.get(image + ':large', stream=True)
            if r.status_code == 200:
                with open(save_dest, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
                self.count += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download all images uploaded by a twitter user you specify")
    parser.add_argument('user_id', help='an ID of a twitter user')
    parser.add_argument('dest', help='specify where to put images')
    parser.add_argument('-k', '--key', help='api key')
    parser.add_argument('-s', '--secret', help='api secret')
    parser.add_argument('-c', '--confidentials', help='a json file containing a key and a secret')
    args = parser.parse_args()

    if args.confidentials:
        with open(args.confidentials) as f:
            confidentials = json.loads(f.read())
        api_key = confidentials['api_key']
        api_secret = confidentials['api_secret']
    elif args.key and args.secret:
        api_key = args.key
        api_secret = args.secret
    else:
        sys.exit()

    downloader = Downloader(api_key, api_secret)
    downloader.download_images(args.user_id, args.dest)
