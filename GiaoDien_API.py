import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from DuLieu import Book
from QuanLy_API import APIBook
from QuanLy_Book import QuanLyBook

class GiaoDienAPI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Tìm Kiếm Sách Qua API")
        self.pack(fill="both", expand=True)
        self.ql_api = APIBook()
        self.GiaoDien()
        
    def GiaoDien(self):
        tk.Label(self, text="Từ khóa tìm kiếm:").place(x=20, y=20)
        self.keyword = tk.StringVar()
        self.entry_keyword = tk.Entry(self, textvariable=self.keyword)
        self.entry_keyword.place(x=120, y=20, width=200)
        
        tk.Button(self, text="Tìm kiếm", command=self.search).place(x=330, y=20, width=100)
        tk.Button(self, text="Thêm sách", command=self.add_book).place(x=440, y=20, width=100)
        tk.Button(self, text="Làm mới", command=self.clear).place(x=550, y=20, width=100)
        
        self.tree = ttk.Treeview(self, columns=("bookName", "author", "category"), show="headings")
        self.tree.heading("bookName", text="Tên Sách")
        self.tree.column("bookName", width=250)
        self.tree.heading("author", text="Tác Giả")
        self.tree.column("author", width=200)
        self.tree.heading("category", text="Thể Loại")
        self.tree.column("category", width=180)
        self.tree.place(x=20, y=60, width=630, height=300)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Thêm label để hiển thị kết quả tìm kiếm
        self.lbl_result = tk.Label(self, text="", fg="blue", font=("Arial", 10))
        self.lbl_result.place(x=20, y=370)
        
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            if values:
                self.keyword.set(values[0])  # Set tên sách vào keyword (index 0 vì bỏ bookID)
                
    def search(self):
        keyword = self.keyword.get().strip()
        if not keyword:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm.")
            return

        try:
            # Xóa dữ liệu cũ trong tree
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Reset thông báo
            self.lbl_result.config(text="Đang tìm kiếm...")
            self.update()
                
            # Gọi API tìm kiếm
            results = self.ql_api.tim_kiem_sach(keyword)
            
            if results:
                # Hiển thị kết quả trong tree
                for book in results:
                    self.tree.insert("", "end", values=(
                        book.get('title', ''),
                        book.get('author', ''),
                        book.get('category', '')
                    ))
                self.lbl_result.config(text=f"✅ Tìm thấy {len(results)} kết quả")
            else:
                self.lbl_result.config(text="❌ Không tìm thấy sách nào")
                
        except Exception as e:
            print(f"Search error: {e}")
            self.lbl_result.config(text=f"❌ Có lỗi xảy ra: {e}")
    
    def add_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sách để thêm.")
            return

        item = self.tree.item(selected_item)
        values = item['values']
        if not values:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu sách được chọn.")
            return
            
        # Nhập số lượng
        quantity = tk.simpledialog.askinteger("Số lượng", f"Nhập số lượng cho:\n{values[0]}", initialvalue=1, minvalue=1, maxvalue=999)
        if quantity is None:
            return
            
        # Tự động tạo mã sách
        try:
            ql_book = QuanLyBook()
            
            # Lấy danh sách sách hiện tại
            try:
                current_books = ql_book.getAllBooks()  # Hoặc phương thức tương tự
            except:
                current_books = []
            
            # Kiểm tra sách đã tồn tại chưa (theo tên sách)
            existing_book = None
            for book in current_books:
                if hasattr(book, 'bookName') and book.bookName.lower().strip() == values[0].lower().strip():
                    existing_book = book
                    break
            
            if existing_book:
                # Nếu sách đã tồn tại, cộng dồn số lượng
                existing_book.quantity += quantity
                self.lbl_result.config(text=f"✅ Cộng thêm {quantity} cuốn. Tổng: {existing_book.quantity} cuốn")
            else:
                # Tạo mã sách mới
                book_id = self.generate_book_id(current_books)
                
                new_book = Book(
                    book_id,
                    values[0],  # title
                    values[1],  # author
                    values[2],  # category
                    quantity
                )
                
                ql_book.addBook(new_book)
                self.lbl_result.config(text=f"✅ Thêm sách mới với mã {book_id}, số lượng: {quantity}")
                
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi thêm sách: {e}")
    
    def generate_book_id(self, current_books):
        """Tự động tạo mã sách MS001, MS002, ..."""
        max_id = 0
        for book in current_books:
            if hasattr(book, 'bookID') and book.bookID.startswith("MS") and len(book.bookID) == 5:
                try:
                    num = int(book.bookID[2:])
                    if num > max_id:
                        max_id = num
                except:
                    continue
        
        return f"MS{max_id + 1:03d}"
            
    def clear(self):
        self.keyword.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.lbl_result.config(text="")

# Chạy thử
if __name__ == "__main__":
    root = tk.Tk()
    app = GiaoDienAPI(root)
    app.pack(fill="both", expand=True)
    root.geometry("700x400")
    root.mainloop()