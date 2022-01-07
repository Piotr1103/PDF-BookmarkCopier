from BookmarkCopier import BookmarkCopier

#目標檔案./demo/B.pdf比來源檔案./demo/A.pdf少了第21頁和第258頁
test = BookmarkCopier('./demo/A.pdf','./demo/B.pdf',(21,258))
test.setbooklines()