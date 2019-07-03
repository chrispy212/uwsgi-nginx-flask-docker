from flask import make_response, abort
import json

from flask import make_response, abort
from requests.auth import HTTPBasicAuth
import json
import uuid
import gzip
import io
import requests
import base64
import inspect
import sys

username = "chrispy_212@hotmail.com"
password = "l87j82iok"
filename = 'myfile.json.gz'
api_url = "https://www.paprikaapp.com/api/v1/sync/groceries/"

try:
    from StringIO import StringIO
except ModuleNotFoundError:
    # Python 3.
    from io import StringIO

def create(grocery):
	title = grocery.get("title", None)

	#Form JSON object
	groceryJson = createJsonWithTitle(title)

	#GZIP compress JSON
	compressedJson = compress(groceryJson)

	#This is just to test that it encodes/decodes properly
	#decompressedJson = uncompress(compressedJson)

	#post the finalised compressed JSON data
	result = sendGzippedJson(compressedJson)

	if result == 200:
		return make_response("{title} successfully created".format(title=title), 201)
	else:
		return make_response("{title} failed to be created".format(title=title), 404)

def createJsonWithTitle(_title):
	#Open JSON template file
	template = open("/home/chrispy212/groceries/templates/grocery.json", "r").read()
	#parse json template into python list groceryItem
	groceryItem = json.loads(template)

	#generate uuid
	newUid = str(uuid.uuid4())

	#replace dynamic list uid with generated uuid
	groceryItem[0]["uid"] = newUid
	#groceryItem[0]["uid"] = 'A422CB82-6081-41AB-974A-F0FE9C823D44-45934-0001EA461E778F6E'

	#replace dynamic list name with passed _title
	groceryItem[0]["name"] = str(_title)
	groceryItem[0]["ingredient"] = str(_title)
	#print(json.dumps(groceryItem[0], indent=4))

	#return dynamic json
	return json.dumps(groceryItem, indent=4)


def compress(text):
	'''
	Compress data and base64 encode data.
	'''

	sfp = StringIO()
	gfp = gzip.GzipFile(filename='internal.txt', fileobj=sfp, mode='wb', compresslevel=9)
	gfp.write(text)
	gfp.close()
	data = sfp.getvalue()
	sfp.close()

	#compressed = base64.b64encode(data)
	return data


def uncompress(data):
	'''
	Base64 decode and uncompress data.
	'''
	#data = base64.b64decode(data)

	sfp = StringIO()
	sfp.write(data)
	sfp.seek(0)
	gfp = gzip.GzipFile(fileobj=sfp, mode='rb')
	uncompressed = gfp.read()
	sfp.close()
	gfp.close()

	return uncompressed

def sendGzippedJson(_gz):

	files = {'data':StringIO(_gz)}
	# sending post request and saving response as response object
	r = requests.post(url = api_url, files = files, auth = (username, password))
	return r

