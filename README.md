[![Build Status](https://travis-ci.org/morinokami/twitter-image-downloader.svg?branch=master)](https://travis-ci.org/morinokami/twitter-image-downloader)

### About
With this program, you can download all images uploaded by a specific twitter user.

### Setup
First, before downloading images, you have to install dependencies using pip:
```
$ pip install -r requirements.txt
```
Of course, you need your api key and api secret as well. if you don't have them, consult [Twitter Developers](https://dev.twitter.com/) and create your application. After you get your api key and api secret, create a json file which should look like:
```
{
  "api_key": "your api key",
  "api_secret": "your api secret"
}
```

### Usage
To download the images the user of id "foo" has uploaded, enter the command below in the command line:
```
$ python3 twt_img.py foo dest_path -c confidentials.json
```
where ```dest_path``` is the directory where images will be downloaded, and ```confidentials.json``` is a json file containing your api key and api secret.

You can specify which size of images to download using the optional argument ```-s``` (or ```--size```). There are four values you can use for it: ```large```, ```medium```, ```small```, or ```thumb```. If you don't specify this value, images of large size will be downloaded by default.

Using the ```--rts``` flag, you can also download images contained in retweets.
