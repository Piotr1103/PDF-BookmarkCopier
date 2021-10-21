class BookmarkSetter:
	def __init__(self,dst,destination,booklines,offsets):
		self.dst = dst
		self.destination = destination
		self.booklines = booklines
		self.offsets = offsets
		#預設朝狀書籤列最多五層，設置一空數組以儲存父節點
		self.par = [None,None,None,None,None]
	
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
		#為避免尚未考慮的對齊格式出現的預設處理
		else:
			print('Undefined Type '+tp+"!")
			cur = None
		
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
		
		#新的PDF檔以bookmarked.pdf為名輸出
		outputStream = open('bookmarked.pdf','wb')
		self.destination.write(outputStream)
		outputStream.close()