import os

from nose.tools import with_setup, eq_, raises

from twt_img import Downloader
from exceptions import *

api_key = os.environ['KEY']
api_secret = os.environ['SECRET']
downloader = Downloader(api_key, api_secret)
tweet = {
    "entities": {
        "media": [
            {
                "type": "photo",
                "media_url": "http://pbs.twimg.com/media/foo.jpg",
                "sizes": {
                    "medium": {
                        "resize": "fit",
                        "h": 823,
                        "w": 600
                    },
                    "thumb": {
                        "resize": "crop",
                        "h": 150,
                        "w": 150
                    },
                    "large": {
                        "resize": "fit",
                        "h": 1024,
                        "w": 746
                    },
                    "small": {
                        "resize": "fit",
                        "h": 466,
                        "w": 340
                    }
                }
            }
        ]
    }
}


@raises(BearerTokenNotFetchedError)
def test_invalid_confidentials_should_fail():
    invalid_downloader = Downloader('my api key', 'my api secret')


def test_get_tweets():
    tweets = downloader.get_tweets('BarackObama', rts=True)
    eq_(len(tweets), 200)


def test_image_properly_extracted():
    eq_(downloader.extract_image(tweet), "http://pbs.twimg.com/media/foo.jpg")


def test_should_fail_if_no_images():
    dummy_tweet = {'entities': []}
    eq_(downloader.extract_image(dummy_tweet), None)
