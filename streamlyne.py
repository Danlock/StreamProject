import sys
from pdfconverter import convert_pdf_to_txt

def main():
	path = sys.argv[2]
	plen = len(path)
	

	if sys.argv[1] == "index":
		if path.lower().endswith(".pdf"):
			index(path,".pdf")
		elif path.lower().endswith(".docx"):
			index(path,".docx")
		elif path.lower().endswith(".html"):
			index(path,".html")
		elif path.lower().endswith(".txt"):
			index(path,".txt")
		else:
			print "Error: Only .pdf,.docx,.html or .txt supported."
			sys.exit()
	elif sys.argv[1] == "search":
		search()
	else:
		print "Error: index OR search must be first argument"
		sys.exit()

def index(path,fType):
	if fType == ".txt":
		
def search():


main()