class BookmarkSetter:
	def __init__(self,dst,destination,booklines,offsets,output_path):
		# 目的檔案的PdfFileReader實例對象
		self.dst = dst
		# 預備寫入的空白PdfFileWriter實例對象
		self.destination = destination
		# 準備寫入之書籤列對象，來自BookmarkGetter的getbooklines成員方法
		self.booklines = booklines
		# 若有刪除PDF檔案頁數，則以元組方式傳入被刪除頁數的原頁碼
		self.offsets = offsets
		#用來將新的檔案放回到檔案所在路徑的字串
		self.output_path = output_path
		#預設巢狀書籤列最多五層，設置一空數組以儲存父節點，超過五層則不予理睬
		self.par = [None,None,None,None,None]

	"""
	關於PDF檔案的各種公開參數可參考:
	https://pdfobject.com/pdf/pdf_open_parameters_acro8.pdf
	其中以"Parameters for Opening PDF Files"一章以下的"Parameters"部分所公告的內容為準
	"""
	
	# 左方對齊座標參數
	def defineLeft(self,tp,bookmark):
		#對齊縮放方式為/XYZ且帶有對齊座標參數top和left
		if tp=='/XYZ' and len(bookmark)==6:
			leftc = (None if bookmark[5] is None else eval(bookmark[5].split("=")[1]))
		#對齊縮放方式為/FitH，帶有對齊座標參數top
		elif tp=='/FitH' and len(bookmark)==5:
			leftc = None
		#對齊縮放方式為/XYZ不帶對齊座標參數top和left，將兩者設為None
		else:
			leftc = None
		
		return leftc
	
	# 上方座標對齊參數
	def defineTop(self,tp,bookmark):
		#對齊縮放方式為/XYZ且帶有對齊座標參數top和left
		if tp=='/XYZ' and len(bookmark)==6:
			topc = (None if bookmark[4] is None else eval(bookmark[4].split("=")[1]))
		#對齊縮放方式為/FitH，帶有對齊座標參數top
		elif tp=='/FitH' and len(bookmark)==5:
			topc = (None if bookmark[4] is None else eval(bookmark[4].split("=")[1]))
		#對齊縮放方式為/XYZ不帶對齊座標參數top和left，將兩者設為None
		else:
			topc = None
		
		return topc
	
	"""
	此方法與方法內的PdfFileWriter().addbookmark無關，識自定義的方法
	參數為 addbookmark(self, 頁面對齊縮放方式, 書籤標題, 頁碼, 層數, 左方對齊座標參數, 上方座標對齊參數)
	而 PdfFileWriter().addBookmark(書籤標題, 頁碼, 父節點, 顏色, 粗體, 斜體, 頁面對齊縮放方式, 左方對齊座標參數, 上方座標對齊參數, 其他參數)
	"""
	def addBookmark(self,tp,ttl,page,lv,leftc,topc):
		level = (None if lv==0 else self.par[lv-1])
		#依照對齊座標參數決定寫入PDF的方式
		if tp == '/XYZ' and topc is not None and leftc is not None:
			cur = self.destination.addBookmark(ttl,page,level,None,False,False,'/XYZ',leftc,topc,None)
		elif tp == '/XYZ' and topc is None and leftc is None:
			cur = self.destination.addBookmark(ttl,page,level,None,False,False,'/XYZ',leftc,topc,None)
		elif tp == '/FitH':
			cur = self.destination.addBookmark(ttl,page,level,None,False,False,'/FitH',topc)
		elif tp == '/FitV':
			cur = self.destination.addBookmark(ttl,page,level,None,False,False,'/FitV',leftc)
		else:
			#為避免尚未考慮的對齊格式出現的預設處理
			print('Undefined Type '+tp+"!")
			#倘若不是上述的對其格式參數，則一律設置為/Fit，左方對齊座標參數、上方座標對齊參數和其他參數則不設置
			cur = self.destination.addBookmark(ttl,page,level,None,False,False,'/Fit',None,None,None)
		
		return cur
		
	
	def setbooklines(self):
		#將輸入的來源PDF書籤列文件字串以行為單位分割
		booklines = self.booklines.split("\n")
		#去除書籤列文件尾部多餘的"\n"導致的空元素
		booklines.pop()
		
		#開啟PDF檔寫入類
		
		for i in range(self.dst.getNumPages()):
			self.destination.addPage(self.dst.getPage(i))
		
		#輔助函數
		def gct(i):
			il = i.split("=")
			return il[1]
		
		#每一行的內容都以', '分隔，將內容取出後分別轉至合適型別
		for c in booklines:
			bookmark = c.split(", ")
			lv = int(gct(bookmark[0]))
			ttl = gct(bookmark[1])
			#輸出的頁數加過1，在這裡要減回去
			page = int(gct(bookmark[2]))-1
			
			"""
			倘若來源頁數比目標多，計算每個區段頁數的偏移量
			"""
			cursect = 0
			if self.offsets is not None:
				if page+1 in self.offsets:
					continue
				else:
					while page >= self.offsets[cursect]:
						cursect = cursect + 1
					page = page - cursect
					cursect = 0
			
			#取得對齊類型
			leftc = self.defineLeft(gct(bookmark[3]),bookmark)
			topc = self.defineTop(gct(bookmark[3]),bookmark)
			cur = self.addBookmark(gct(bookmark[3]),ttl,page,lv,leftc,topc)
			#將節點按階層加入數組，以儲存父節點
			self.par[lv] = cur
		
		#新的PDF檔以Bookmarked.pdf為名輸出，並輸出至目的檔案所在之目錄
		output_path = '\\'.join(self.output_path.split('\\')[:-1:])
		outputStream = open(output_path + '\\Bookmarked.pdf','wb')
		self.destination.write(outputStream)
		outputStream.close()