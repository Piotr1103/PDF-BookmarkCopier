from BookmarkCopier import BookmarkCopier

#目標檔案./demo/B.pdf比來源檔案./demo/A.pdf少了第21頁和第258頁
#test = BookmarkCopier('./demo/A.pdf','./demo/B.pdf',(21,258))

#在原有頁數後面插入新頁數
# test = BookmarkCopier('./demo/Vue核心篇.pdf','./demo/Vue核心篇-已融合.pdf',None)

src = input("請輸入書籤列來源檔案路徑：")
dst = input("請輸入目的地檔案路徑：")
offsets = input("被刪除的頁數，以空格隔開，沒有則輸入N：")
if not offsets in ("N", "n"):
	try:
		offtup = tuple([int(i) for i in offsets.split()])
	except:
		print("錯誤!請確定輸入是否正確。", offtup, type(offtup))

test = BookmarkCopier(src, dst, offtup)

test.setbooklines()