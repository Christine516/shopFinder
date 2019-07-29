from google.appengine.ext import ndb


class UploadedFile(ndb.Model):
    url = ndb.StringProperty(indexed=False)