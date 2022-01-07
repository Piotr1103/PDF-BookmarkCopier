PDF書籤複製器
===============

## 用途

這個工具是專門用來複製PDF檔案中的書籤列的。

## 用法

程式的用法如在main.py中所示的那樣：

假設我們的檔案./demo/A.pdf透過網路上的工具刪除了第21頁和第258頁，生成了./demo/B.pdf。然而，./demo/A.pdf中所有的書籤列並未被複製到./demo/B.pdf中去。如果一個檔案有數十條甚至數百條書籤，那工作量將會十分驚人。目前在網路上還沒有PDF網站提供複製書籤列的功能。

本工具已經把PDF中相關的設定都納入到程式中，要想複製書籤列，先實例化一個BookmarkCopier物件：

~~~
	BookmarkCopier(src,dst,offsets):
		"src" 書籤列來源檔案名稱
		"dst" 目標檔案名稱
		"offsets" 目標檔案減少的頁數，以tuple的形式傳入
~~~

舉個例子，宣告一個變數test，把BookmarkCopier實例傳入：
~~~
	test = BookmarkCopier('./demo/A.pdf', './demo/B.pdf', (21,258))
~~~

然後調用BookmarkCopier類別的setbooklines()方法：
~~~
	test.setbooklines()
~~~

這樣，就可以在main.py所在的目錄中得到一個bookmarked.pdf的成品檔案。