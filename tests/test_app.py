import os
import pytest
import responses
import time

from twt_img import twt_img
from twt_img import exceptions as e


@pytest.fixture
@responses.activate
def downloader():
    responses.add(
        responses.POST,
        "https://api.twitter.com/oauth2/token",
        json={"access_token": "loremipsum"},
        status=200,
    )
    downloader = twt_img.Downloader("key", "secret")

    return downloader


@responses.activate
def test_invalid_confidentials_should_raise():
    responses.add(
        responses.POST,
        "https://api.twitter.com/oauth2/token",
        json={
            "errors": [
                {
                    "code": 99,
                    "message": "Unable to verify your credentials",
                    "label": "authenticity_token_error",
                }
            ]
        },
        status=403,
    )

    with pytest.raises(e.BearerTokenNotFetchedError):
        _ = twt_img.Downloader("my api key", "my api secret")


@responses.activate
def test_get_tweets_as_json(downloader):
    responses.add(
        responses.GET,
        "https://api.twitter.com/1.1/statuses/user_timeline.json",
        json=[{"data": "foo"}, {"data": "bar"}],
        status=200,
    )

    tweets = downloader.get_tweets("BarackObama", rts=True)

    assert len(tweets) == 2


def test_image_extracted(downloader):
    sample_tweet = {
        "entities": {
            "media": [
                {
                    "type": "photo",
                    "media_url": "http://pbs.twimg.com/media/foo.jpg",
                    "sizes": {
                        "medium": {"resize": "fit", "h": 823, "w": 600},
                        "thumb": {"resize": "crop", "h": 150, "w": 150},
                        "large": {"resize": "fit", "h": 1024, "w": 746},
                        "small": {"resize": "fit", "h": 466, "w": 340},
                    },
                }
            ]
        }
    }

    extracted_url = downloader.extract_image(sample_tweet)[0]
    expected = "http://pbs.twimg.com/media/foo.jpg"

    assert extracted_url == expected


def test_should_return_none_if_no_images(downloader):
    dummy_tweet = {"entities": []}
    assert downloader.extract_image(dummy_tweet) is None


@responses.activate
def test_save_image(tmpdir, downloader):
    responses.add(
        responses.GET,
        url="http://pbs.twimg.com/media/test.png:large",
        stream=True,
    )

    now = str(int(time.time()))
    downloader.save_image("http://pbs.twimg.com/media/test.png", tmpdir, now)

    image = os.listdir(tmpdir)
    assert len(image) > 0
    assert image[0] == f"{now}.png"
