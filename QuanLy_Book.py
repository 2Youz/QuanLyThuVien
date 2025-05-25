import json
import os
from DuLieu import Book

class QuanLyBook:
    def __init__(self):
        self.BookList = []
        self.BooksFile = 'books.json'
        self.loadData()
    # tải dữ liệu từ file books.json vào danh sách sách
    def loadData(self):
        if not os.path.exists(self.BooksFile) or os.path.getsize(self.BooksFile) == 0:
            return []
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
        except json.JSONDecodeError as e:
            print(f"Lỗi khi đọc dữ liệu từ file JSON: {e}")
            self.BookList = []
        except FileNotFoundError:
            print(f"File {self.BooksFile} không tồn tại.")
            self.BookList = []
        return self.BookList
    # lưu dữ liệu vào file books.json
    def saveData(self):
        try:
            with open(self.BooksFile, "w", encoding= "utf-8") as file:
                booksData = [book.to_dict() for book in self.BookList]
                json.dump(booksData, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào file JSON: {e}")
    # thêm sách mới
    def addBook(self, book):
        for b in self.BookList:
            if b.bookID == book.bookID:
                raise ValueError("❌ Mã sách đã tồn tại.")
        self.BookList.append(book)
        self.saveData()
        print("✅ Thêm sách thành công!")
    # xóa sách theo mã sách
    def removeBook(self, bookID):
        """Xóa sách theo mã sách"""
        before_count	 = len(self.BookList)
        self.BookList = [book for book in self.BookList if book.bookID != bookID]
        
        if len(self.BookList) == before_count:
            raise ValueError("❌ Mã sách không tồn tại.")
        
        self.saveData()
        print("✅ Xóa sách thành công!")
    # cập nhật thông tin sách
    def updateBook(self, bookID, new_book):
        found = False
        for i, book in enumerate(self.BookList):
            if book.bookID == bookID:
                self.BookList[i] = new_book
                found = True
                break
    
        if not found:
            raise ValueError("❌ Mã sách không tồn tại.")
    
        self.saveData()
        print("✅ Cập nhật sách thành công!")
    # lấy thông tin sách theo mã sách
    def getAllBooks(self):
        """Lấy tất cả sách"""
        if not self.BookList:
            raise ValueError("❌ Không có sách nào trong danh sách.")
        return self.BookList
    
    def getBookByID(self, bookID):
        """Lấy sách theo mã sách"""
        for book in self.BookList:
            if book.bookID == bookID:
                return book
        return None
    
    def searchBooks(self, keyword):
        """Tìm kiếm sách theo từ khóa"""
        results = []
        for book in self.BookList:
            if (keyword.lower() in book.bookName.lower() or 
                keyword.lower() in book.author.lower() or 
                keyword.lower() in book.category.lower()):
                results.append(book)
        return results