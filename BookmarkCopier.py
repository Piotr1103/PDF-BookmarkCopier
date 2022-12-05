from PyPDF2 import PdfFileWriter,PdfFileReader
from BookmarkGetter import BookmarkGetter
from BookmarkSetter import BookmarkSetter

class BookmarkCopier:
	def __init__(self,src,dst,offsets):
		self.src = PdfFileReader(open(src,'rb'))
		self.srcPages = self.src.getNumPages()
		self.dst = PdfFileReader(open(dst,'rb'))
		self.dstPages = self.dst.getNumPages()
		self.offsets = offsets
		self.getter = BookmarkGetter(self.src)
		self.booklines = self.getter.booklines
		self.setter = BookmarkSetter(self.dst,PdfFileWriter(),self.booklines,self.offsets,dst)
		self.compare_pages()
	
	def compare_pages(self):
		if self.srcPages > self.dstPages:
			self.copy_mode = 'deleted'
		elif self.srcPages < self.dstPages:
			self.copy_mode = 'inserted'
		else:
			self.copy_mode = 'equal'
		
		if self.offsets != None and abs(self.srcPages-self.dstPages)!=len(self.offsets):
			print("The length of offsets doesn't add up!")
			print("Please check up the offset pages!")
	
	def setbooklines(self):
		self.setter.setbooklines()