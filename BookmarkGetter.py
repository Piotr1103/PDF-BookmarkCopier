class BookmarkGetter:
	def __init__(self,pdf):
		self.booklines = ''
		self.pdf = pdf
		self.bookmarks = self.pdf.getOutlines()
		self.getbooklines()
		
	def dechainwrite(self,obj,level):
		txt = ''
		if isinstance(obj,list):
			for i in obj:
				txt += self.dechainwrite(i,level+1)
		else:
			txt += ("lv="+str(level))
			txt += (", title="+obj['/Title'])
			txt += (", page="+str(self.pdf.getDestinationPageNumber(obj)+1))
			if obj['/Type'] == '/XYZ':
				txt += ", type=/XYZ"
				if isinstance(obj['/Top'],(float,int)):
					txt += (", top="+str(obj['/Top']))
				if isinstance(obj['/Left'],(float,int)):
					txt += (", left="+str(obj['/Left']))
			elif obj['/Type'] == '/FitH':
				txt += ", type=/FitH"
				txt += (", top="+str(obj['/Top']))
			else:
				txt += ", type=" + obj['/Type']
			txt += "\n"
		return txt
	
	def getbooklines(self):
		for bookmark in self.bookmarks:
			#解析層級從第0層開始
			self.booklines += self.dechainwrite(bookmark,0)