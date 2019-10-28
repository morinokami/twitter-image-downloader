[![CircleCI](https://circleci.com/gh/morinokami/twitter-image-downloader.svg?style=svg)](https://circleci.com/gh/morinokami/twitter-image-downloader)


## What it does
With this program, you can download all images uploaded by a specific twitter
user.


## What you need
* Python 3


## Setup
First, you need to install `twitter-image-dl`:

```
$ pip install twitter-image-dl
```

Next, you need to generate your api key and api secret key.
If you don't have them, go to [Twitter Developers](https://dev.twitter.com/)
and create your application.
After you get your api key and api secret key, create a json file like this:

```
{
  "api_key": "your api key",
  "api_secret": "your api secret key"
}
```


## Usage
To download the images the user of id "foo" has uploaded, enter the command
like the following on the command line:

```
$ twt_img foo dest_path -c confidentials.json
```

where `dest_path` is the directory where images will be downloaded, and
`confidentials.json` is a json file containing your api key and api secret.

You can specify which size of images to download using the optional argument
`-s` (or `--size`). There are five values you can specify:

* `large`
* `medium`
* `small`
* `orig`
* `thumb`

If you don't specify this value, images of `large` size will be downloaded
by default.

Using the `--rts` flag, you can also download images contained in retweets.

Provide a number to the `-l` or `--limit` argument (e.g. `-l 25`) to limit how
many tweets are inspected for images (starting with the most recent). Note that
if you're using `--limit` without `--rts`, the number of tweets inspected can
be smaller than the specified limit.


## Testing
Install dependencies for testing and enter `pytest` command like this:

```
$ pipenv install --dev
$ pytest
```

Notice that you have to set `KEY` and `SECRET` environment variables for
testing to work.

