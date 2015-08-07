import StringIO
import json
import logging
import random
import urllib
import urllib2
import time

# parsing plex data from xml api results
from xml.dom import minidom
from xml.etree.ElementTree import *

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = 'TELEGRAM BOT API HERE!'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    #'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)


        #I CUSTOMISED FROM HERE!!!


        if '/tv' in text:
            purl = urllib2.Request(url='http://plex_server_address_or_IP_address_here:32400/library/sections/1/newest?X-Plex-Token=YOUR_PLEX_TOKEN_HERE')
            f = urllib2.urlopen(purl)
            tree = ElementTree()
            tree.parse(f)
            root = tree.getroot()
            shows = root.findall('./Video')
            for s in shows[:10]:
                title = s.attrib['grandparentTitle']
                season = s.attrib['title']
                #added = s.attrib['addedAt'] wanted to add the date and time but not sure how to convert Epoch time format.
                reply(title +' - '+ season)


        if '/movies' in text:
            purl = urllib2.Request(url='http://plex_server_address_or_IP_address_here:32400/library/sections/2/recentlyAdded?X-Plex-Token=YOUR_PLEX_TOKEN_HERE')
            f = urllib2.urlopen(purl)
            tree = ElementTree()
            tree.parse(f)
            root = tree.getroot()
            shows = root.findall('./Video')
            for s in shows[:5]:
                title = s.attrib['title']
                summary = s.attrib['summary']
                reply(title +' - '+ summary)

        if '/anime' in text:
            purl = urllib2.Request(url='http://plex_server_address_or_IP_address_here:32400/library/sections/6/newest?X-Plex-Token=YOUR_PLEX_TOKEN_HERE')
            f = urllib2.urlopen(purl)
            tree = ElementTree()
            tree.parse(f)
            root = tree.getroot()
            shows = root.findall('./Video')
            for s in shows[:5]:
                title = s.attrib['grandparentTitle']
                season = s.attrib['title']
                reply(title +' - '+ season) 
  
                    
app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
