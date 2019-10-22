import os
import time

import pytest

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


def test_invalid_confidentials_should_fail():
    with pytest.raises(BearerTokenNotFetchedError):
        invalid_downloader = Downloader('my api key', 'my api secret')


def test_get_tweets():
    tweets = downloader.get_tweets('BarackObama', rts=True)
    assert len(tweets) ==  200


def test_image_properly_extracted():
    assert downloader.extract_image(tweet)[0] == "http://pbs.twimg.com/media/foo.jpg"


def test_should_fail_if_no_images():
    dummy_tweet = {'entities': []}
    assert downloader.extract_image(dummy_tweet) == None


def test_save_image(tmpdir):
    now = str(int(time.time()))
    downloader.save_image('http://pbs.twimg.com/media/CRd-x43VAAAV9k2.png', tmpdir, now)
    image = os.listdir(tmpdir)
    assert len(image) > 0
