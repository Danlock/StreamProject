from __future__ import absolute_import
import sys
import pymongo

from PyPDF2 import PdfFileReader
from celery import Celery
import pika


from tasks import add

app = Celery('streamlyne', broker='amqp://guest@localhost//')
client = pymongo.MongoClient()
db = client.stream_db
dbIndex = db.stream
SEARCH_LIMIT = 10


def main():
    path = sys.argv[2]
    plen = len(path)

    if sys.argv[1] == "index":
        if path.lower().endswith(".pdf"):
            text = convert.delay(path,".pdf")
            index.delay(text)
        elif path.lower().endswith(".docx"):
            text = convert.delay(path,".docx")
            index.delay(text)
        elif path.lower().endswith(".html"):
            text = convert.delay(path, ".html")
            index.delay(text)
        elif path.lower().endswith(".txt"):
            text = convert.delay(path, ".txt")
            index.delay(text)
        else:
            print "Error: Only .pdf,.docx,.html or .txt supported."
            sys.exit()
    elif sys.argv[1] == "search":
        search.delay(path)
    else:
        print "Error: index OR search must be first argument"
        sys.exit()

@app.task
def convert(path,fType):
    text = ""
    f = open(path, 'r')
    text = f.read()

    if fType == ".txt":	
    	return text
    if fType == ".pdf":
        pdf = PdfFileReader(open(path, "rb"))
        for page in pdf.pages:
            text.append(page.extractText())
    if fType == ".docx":
	    pdf = PdfFileReader(open(path, "rb"))
	    for page in pdf.pages:
	        text.append(page.extractText())
	return text

@app.task
def index(text):
	# unicode(text['txt'], errors = 'replace')
	dbIndex.ensure_index([
    ('txt', pymongo.TEXT),
    ('fType', pymongo.TEXT),
    ('path', pymongo.TEXT)
    ],
        weights={
        'path': 100,
        'txt': 25
    	}
    )

    dbIndex.insert({'txt':text, 'fType':fType, 'path':path})
    
    cursor = dbIndex.find()
    for c in cursor:
        print c

    """
    if fType == ".pdf":
        pdf = PdfFileReader(open(path, "rb"))
        for page in pdf.pages:
            text.append(page.extractText())
    print text
	"""

@app.task
def search(query):
    results = db.command('text', 'stream', search=query, limit=SEARCH_LIMIT)
    print results['results']

main()
