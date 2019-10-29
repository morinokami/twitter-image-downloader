[![CircleCI](https://circleci.com/gh/morinokami/twitter-image-downloader.svg?style=svg)](https://circleci.com/gh/morinokami/twitter-image-downloader)

## What it does

Download all images uploaded by a specified Twitter user.

## What you need

- Python 3

## Setup

First, you need to install `twitter-image-dl`:

```sh
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
$ twt_img foo -c confidentials.json
```

where `confidentials.json` is the json file containing your api keys.
This command creates a directory called `foo` and save images to that
directory.

If you want to save images to a directory other than `foo`, use `-d` or
`--dest` argument to specify the destination.

You can specify which size of images to download using the optional argument
`-s` (or `--size`). There are five values you can specify:

- `large`
- `medium`
- `small`
- `orig`
- `thumb`

If you don't specify this value, images of `large` size will be downloaded
by default.

Using the `--rts` flag, you can also download images contained in retweets.

Provide a number to the `-l` or `--limit` argument (e.g. `-l 25`) to limit how
many tweets are inspected for images (starting with the most recent). Note that
if you're using `--limit` without `--rts`, the number of tweets inspected can
be smaller than the specified limit.

## Testing

Install dependencies for testing and enter `pytest` command like this:

```sh
$ gi clone git@github.com:morinokami/twitter-image-downloader.git
$ cd twitter-image-downloader
$ pipenv install --dev
$ pipenv run test
```

Notice that you have to set `KEY` and `SECRET` environment variables for
testing to work.
