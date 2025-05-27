import json
import os
from DuLieu import Book

class QuanLyBook:
    def __init__(self):
        self.BookList = []
        self.BooksFile = 'books.json'
        self.loadData()
    
    def loadData(self):
        if not os.path.exists(self.BooksFile) or os.path.getsize(self.BooksFile) == 0:
            return
        try: 
            with open(self.BooksFile, "r", encoding="utf-8") as file:
                booksData = json.load(file)
                for book in booksData:
                    b = Book(
                        book['bookID'], 
                        book['bookName'], 
                        book['author'], 
                        book['category'], 
                        book['quantity']
                    )
                    self.BookList.append(b)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Lỗi khi đọc file: {e}")
            self.BookList = []
    
    def saveData(self):
        try:
            with open(self.BooksFile, "w", encoding="utf-8") as file:
                booksData = [book.to_dict() for book in self.BookList]
                json.dump(booksData, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {e}")
    
    def addBook(self, book):
        for b in self.BookList:
            if b.bookID == book.bookID:
                raise ValueError("Mã sách đã tồn tại.")
        self.BookList.append(book)
        self.saveData()
    
    def removeBook(self, bookID):
        before_count = len(self.BookList)
        self.BookList = [book for book in self.BookList if book.bookID != bookID]
        
        if len(self.BookList) == before_count:
            raise ValueError("Mã sách không tồn tại.")
        
        self.saveData()
    
    def updateBook(self, bookID, new_book):
        for i, book in enumerate(self.BookList):
            if book.bookID == bookID:
                self.BookList[i] = new_book
                self.saveData()
                return
        raise ValueError("Mã sách không tồn tại.")
    
    def getBookByID(self, bookID):
        for book in self.BookList:
            if book.bookID == bookID:
                return book
        return None
    
    def searchBooks(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        for book in self.BookList:
            if (keyword_lower in book.bookName.lower() or 
                keyword_lower in book.author.lower() or 
                keyword_lower in book.category.lower()):
                results.append(book)
        return results
    def getAllBooks(self):
        return self.BookList