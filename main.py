from BookmarkCopier import BookmarkCopier

#目標檔案./demo/B.pdf比來源檔案./demo/A.pdf少了第21頁和第258頁
#test = BookmarkCopier('./demo/A.pdf','./demo/B.pdf',(21,258))

#在原有頁數後面插入新頁數
test = BookmarkCopier('./demo/Vue核心篇.pdf','./demo/Vue核心篇-已融合.pdf',None)

test.setbooklines()