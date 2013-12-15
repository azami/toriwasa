# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import tweepy
import ConfigParser
from flask import Flask, session, request, abort, json

config = ConfigParser.ConfigParser()
config.read('app.ini')

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             'uploads')
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = config.get('api', 'secret_key')
app.debug = bool(int(config.get('api', 'debug')))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


consumer_key = config.get('api', 'consumer_key')
consumer_secret = config.get('api', 'consumer_secret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)


@app.route('/user')
def user():
    user = dict(session) if 'name' in session else {}
    return json.dumps(user)


@app.route('/auth/url')
def authorization_url():
    return auth.get_authorization_url()


@app.route('/auth/verify')
def verify():
    try:
        token = auth.get_access_token(request.args['oauth_verifier'])
        if not token:
            return abort(401)
        auth.set_access_token(token.key, token.secret)
        user = tweepy.API(auth).me()
    except tweepy.TweepError:
        return abort(401)
    session['name'] = user.screen_name
    session['image'] = user.profile_image_url
    return 'authorized'


@app.route('/auth/unauth')
def unauth():
    session.pop('name')
    session.pop('image')
    return ('', 204)


@app.route('/thread/<thread>/create', methods=['POST'])
def create_thread(thread):
    upload_dir = os.path.join(
        app.config['UPLOAD_FOLDER'], session['name'], thread)
    if os.path.exists(upload_dir):
        return abort(400)
    os.mkdir(upload_dir)
    return (thread, 201)


@app.route('/thread/<thread>/upload', methods=['POST'])
def upload(thread):
    pict = request.files['file']
    ext = os.path.splitext(pict.filename)[1]
    if ext not in ['.jpg', '.gif', '.png']:
        return abort(400)
    upload_dir = os.path.join(
        app.config['UPLOAD_FOLDER'], session['name'], thread)
    if not os.path.exists(upload_dir):
        return abort(400)
    pict_name = '%d%s' % (time.time(), ext)
    pict.save(os.path.join(upload_dir, pict_name))
    return (pict_name, 201)


@app.route('/threads')
def threads():
    users = os.listdir(app.config['UPLOAD_FOLDER'])
    threads = {user: os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],
                                             user))
               for user in users}
    return json.dumps(threads)


@app.route('/<user>/<thread>')
def pictures(user, thread):
    return json.dumps(os.listdir(
        os.path.join(app.config['UPLOAD_FOLDER'], user, thread)))


if app.debug:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))


if __name__ == '__main__':
    app.run(port=9494, host='0.0.0.0')
