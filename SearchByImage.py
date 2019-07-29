import webapp2
import jinja2
import os

from webapp2_extras import auth
from webapp2_extras import sessions
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import images
from Login import *
from posts import Post
from Comment import *
import requests
import requests
import json
from requests_toolbelt.adapters import appengine
import base64

# Pass the image data to an encoding function.

appengine.monkeypatch()

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
def detect_web_uri(image_content):
    params = {
        "requests": [
            {
                "image":{
                  "content":image_content
                 },
                "features": [
                    {
                        "type": "WEB_DETECTION",
                        "maxResults": 5
                    }
                ]
            }
        ]
    }
    keyVision = {"key": "AIzaSyDVscFkNGni1N2XCA8ThkSh0aZr20P_vhQ"}
    r = requests.post("https://vision.googleapis.com/v1/images:annotate", json=params, params=keyVision)
    img_dict = json.loads(r.text)

    list_of_entity_links = []
    urls =[]
    for response in img_dict['responses']:
        for entity in response['webDetection']['webEntities']:
            if 'description' in entity.keys():
                CustomSearchParams = {"key": "AIzaSyAso_n3tH-AGcXaXHBt5YLaHSdV3XoXMvM",
                                      "cx": "006239744188845988923:qyi6wbfdc_g", "q": entity['description'], "num": 5}
                search_query = requests.get("https://www.googleapis.com/customsearch/v1", params=CustomSearchParams)
                search_dict = json.loads(search_query.text)
                entity_link_list =[]
                for search in search_dict['items']:
                    entity_link_list.append((entity['description'],search['link']))
                list_of_entity_links.append(entity_link_list)
        for pages in response['webDetection']['pagesWithMatchingImages']:
            urls.append(pages['url'])

    return (list_of_entity_links,urls)

def detect_web_uri_by_url(image_url):
    params = {
        "requests": [
            {
                "image":{
                  "source":{
                  "imageUri":
                    image_url
                     }
                 },
                "features": [
                    {
                        "type": "WEB_DETECTION",
                        "maxResults": 3
                    }
                ]
            }
        ]
    }
    keyVision = {"key": "AIzaSyDVscFkNGni1N2XCA8ThkSh0aZr20P_vhQ"}
    r = requests.post("https://vision.googleapis.com/v1/images:annotate", json=params, params=keyVision)
    img_dict = json.loads(r.text)
    list_of_entity_links = []
    urls =[]
    for response in img_dict['responses']:
        for entity in response['webDetection']['webEntities']:
            if 'description' in entity.keys():
                CustomSearchParams = {"key": "AIzaSyAso_n3tH-AGcXaXHBt5YLaHSdV3XoXMvM",
                                      "cx": "006239744188845988923:qyi6wbfdc_g", "q": entity['description'], "num": 6}
                search_query = requests.get("https://www.googleapis.com/customsearch/v1", params=CustomSearchParams)
                search_dict = json.loads(search_query.text)
                entity_link_list = []
                for search in search_dict['items']:
                    entity_link_list.append((entity['description'], search['link']))
                list_of_entity_links.append(entity_link_list)
        for pages in response['webDetection']['pagesWithMatchingImages']:
            urls.append(pages['url'])

    return (list_of_entity_links,urls)

class SearchImagePage(BaseHandler):
    @user_required
    def post(self):
        self.response.headers.add_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.response.headers.add_header("Expires", "0")
        image_content = self.request.get('SearchImage')
        image_url = self.request.get('SearchImageUrl')
        if image_url:
            (search_contents,urls) = detect_web_uri_by_url(image_url)
        elif image_content:
            (search_contents,urls) = detect_web_uri(base64.b64encode(image_content))
        template_vars = {
            "search_contents": search_contents,
            "urls":urls
        }
        self.render_template("image-Search.html",template_vars)
