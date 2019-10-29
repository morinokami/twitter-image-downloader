import argparse
import base64
import json
import os
import shutil

import dateutil.parser
from datetime import datetime
import requests

from . import exceptions as e


class Downloader:
    def __init__(self, api_key, api_secret):
        self.bearer_token = self.bearer(api_key, api_secret)
        self.last_tweet = None
        self.count = 0

    def download_images(self, user, save_dest, size="large", limit=3200, rts=False):
        """Download and save images that user uploaded.

        Args:
            user: User ID.
            save_dest: The directory where images will be saved.
            size: Which size of images to download.
            rts: Whether to include retweets or not.
        """

        if not os.path.isdir(save_dest):
            raise e.InvalidDownloadPathError()

        num_tweets_checked = 0
        tweets = self.get_tweets(user, self.last_tweet, limit, rts)
        if not tweets:
            print("Got an empty list of tweets")

        while len(tweets) > 0 and num_tweets_checked < limit:
            for tweet in tweets:
                # create a file name using the timestamp of the image
                timestamp = dateutil.parser.parse(tweet["created_at"]).timestamp()
                timestamp = int(timestamp)
                value = datetime.fromtimestamp(timestamp)
                fname = value.strftime("%Y-%m-%d-%H-%M-%S")

                # save the image
                images = self.extract_image(tweet)
                if images is not None:
                    counter = 0
                    for image in images:
                        if counter == 0:
                            self.save_image(image, save_dest, fname, size)
                        else:
                            self.save_image(
                                image, save_dest, fname + "_" + str(counter), size
                            )
                        counter += 1
                num_tweets_checked += 1
                self.last_tweet = tweet["id"]

            tweets = self.get_tweets(user, self.last_tweet, count=limit)

    def bearer(self, key, secret):
        """Receive the bearer token and return it.

        Args:
            key: API key.
            secret: API string.
        """

        # setup
        credential = base64.b64encode(
            bytes("{}:{}".format(key, secret), "utf-8")
        ).decode()
        url = "https://api.twitter.com/oauth2/token"
        headers = {
            "Authorization": "Basic {}".format(credential),
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        payload = {"grant_type": "client_credentials"}

        # post the request
        r = requests.post(url, headers=headers, params=payload)

        # check the response
        if r.status_code == 200:
            return r.json()["access_token"]
        else:
            raise e.BearerTokenNotFetchedError()

    def get_tweets(self, user, start=None, count=200, rts=False):
        """Download user's tweets and return them as a list.

        Args:
            user: User ID.
            start: Tweet ID.
            rts: Whether to include retweets or not.
        """

        # setup
        bearer_token = self.bearer_token
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        payload = {
            "screen_name": user,
            "count": count,
            "include_rts": rts,
            "tweet_mode": "extended",
        }
        if start:
            payload["max_id"] = start

        # get the request
        r = requests.get(url, headers=headers, params=payload)

        # check the response
        if r.status_code == 200:
            tweets = r.json()
            if len(tweets) == 1:
                return []
            else:
                print("Got " + str(len(tweets)) + " tweets")
                return tweets if not start else tweets[1:]
        else:
            print(
                "An error occurred with the request, status code was "
                + str(r.status_code)
            )
            return []

    def extract_image(self, tweet):
        """Return a list of url(s) which represents the image(s) embedded in tweet.

        Args:
            tweet: A dict object representing a tweet.
        """

        if "media" in tweet["entities"]:
            urls = [x["media_url"] for x in tweet["entities"]["media"]]
            if "extended_entities" in tweet:
                extra = [x["media_url"] for x in tweet["extended_entities"]["media"]]
                urls = set(urls + extra)
            return urls
        else:
            return None

    def save_image(self, image, path, timestamp, size="large"):
        """Download and save an image to path.

        Args:
            image: The url of the image.
            path: The directory where the image will be saved.
            timestamp: The time that the image was uploaded.
                It is used for naming the image.
            size: Which size of images to download.
        """

        if image:

            # image's path with a new name
            ext = os.path.splitext(image)[1]
            save_dest = os.path.join(path, timestamp + ext)

            # save the image in the specified directory (or don't)
            if not (os.path.exists(save_dest)):
                print("Saving " + image)

                r = requests.get(image + ":" + size, stream=True)
                if r.status_code == 200:
                    with open(save_dest, "wb") as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    self.count += 1

            else:
                print("Skipping " + image + " because it was already dowloaded")


def main():
    parser = argparse.ArgumentParser(
        description="Download all images uploaded by a twitter user you specify"
    )
    parser.add_argument("user_id", help="an ID of a twitter user")
    parser.add_argument("dest", help="specify where to put images")
    parser.add_argument(
        "-c", "--confidentials", help="a json file containing a key and a secret"
    )
    parser.add_argument(
        "-s",
        "--size",
        help="specify the size of images",
        default="large",
        choices=["large", "medium", "small", "thumb", "orig"],
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help="the maximum number of tweets to check (most recent first)",
        default=3200,
    )
    parser.add_argument(
        "--rts", help="save images contained in retweets", action="store_true"
    )
    args = parser.parse_args()

    if args.confidentials:
        with open(args.confidentials) as f:
            confidentials = json.loads(f.read())
        if "api_key" not in confidentials or "api_secret" not in confidentials:
            raise e.ConfidentialsNotSuppliedError()
        api_key = confidentials["api_key"]
        api_secret = confidentials["api_secret"]
    else:
        raise e.ConfidentialsNotSuppliedError()

    downloader = Downloader(api_key, api_secret)
    downloader.download_images(args.user_id, args.dest, args.size, args.limit, args.rts)
