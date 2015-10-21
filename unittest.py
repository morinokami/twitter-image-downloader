import os
import shutil
import time

from nose.tools import with_setup, eq_, raises, assert_true

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


def test_save_image():
    os.mkdir('temp')
    now = str(int(time.time()))
    downloader.save_image('http://pbs.twimg.com/media/CRd-x43VAAAV9k2.png', 'temp', now)
    image = os.listdir('temp')
    shutil.rmtree('temp')
    assert_true(len(image) > 0)
