# PDF-BookmarkCopier
A tool for copying booklines from one pdf file to another.

The usage is shown in the "main.py".

Assume that we have a pdf file deleted two pages: 21, 258.
The new file is fine, but the bookmarks wasn't copied for that no pdf websites provides the function that copies the bookmarks.

To copy bookmarks from a pdf file to another, create an instance of the BookmarkCopier class:

	BookmarkCopier(src,dst,offsets):
		"src" means the path of the pdf file that has the bookmarks you want to copy from.
		"dst" means the path of the pdf file that you want to copy the bookmarks to.
		"offsets" means the pages deleted, sent in a tuple.

So, it would be like this:
	test = BookmarkCopier('./demo/A.pdf','./demo/B.pdf',(21,258))

Like operating a copy machine, now we have the book on the scanning glass, we have the paper loaded in the tray. And then, the key point: Press the start button to activate the copying sequence.

To press the button, use the "setbooklines" function:
	test.setbooklines()

Finally, you'll a pdf file named "bookmarked.pdf" in the same directory where you put "main.py".

Note that these classes use PyPDF2, the BookmarkCopier can't work if you don't install it.