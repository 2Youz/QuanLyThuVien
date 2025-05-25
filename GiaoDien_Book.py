import tkinter as tk
from tkinter import messagebox, ttk
from DuLieu import Book
from QuanLy_Book import QuanLyBook
class GiaoDienBook(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.ql_book = QuanLyBook()
        self.GiaoDien()
        self.tailaiDuLieu()
    def GiaoDien(self):
        #Khung chính
        self.KhungChinh = tk.Frame(self, bg="white")
        self.KhungChinh.pack(fill="both", expand=True, padx=10, pady=10)
        #Khung cho nhập liệu sách
        self.KhungNhapLieu = tk.Frame(self.KhungChinh, bg="white")
        self.KhungNhapLieu.pack(fill="x", pady=(0, 10))
        # Mã sách và tên sách nằm ở dòng 1
        Row_1 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_1.pack(fill="x", pady=5)
        
        tk.Label(Row_1, text="Mã sách:", bg="white", font=("Arial", 10)).pack(side="left")
        self.maSach = tk.StringVar()
        tk.Entry(Row_1, textvariable=self.maSach, width=15, font=("Arial", 10)).pack(side="left", padx=(5,20) )
        
        tk.Label(Row_1, text="Tên sách:", bg="white", font=("Arial", 10)).pack(side="left")
        self.tenSach = tk.StringVar()
        tk.Entry(Row_1, textvariable=self.tenSach, width=35, font=("Arial", 10)).pack(side="left", padx=(5,0))
        # Tác giả và thể loại nằm ở dòng 2
        Row_2 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_2.pack(fill="x", pady=5)
        
        tk.Label(Row_2, text="Tác giả:", bg="white", font=("Arial", 10)).pack(side="left")
        self.tacGia = tk.StringVar()
        tk.Entry(Row_2, textvariable=self.tacGia,width=20 ,font=("Arial", 10)).pack(side="left", padx=(5,20))
        
        tk.Label(Row_2, text="Thể loại:", bg="white", font=("Arial", 10)).pack(side="left")
        self.theLoai = tk.StringVar()
        self.cbtheLoai = ttk.Combobox(Row_2, textvariable=self.theLoai, width= 25, font=("Arial", 10))
        self.cbtheLoai['values']= ["Sách giáo khoa", "Sách tham khảo", "Sách kỹ năng sống", "Truyện tranh", "Tiểu thuyết", "Văn học Việt Nam", "Văn học nước ngoài", "Khoa học - Công nghệ", "Lịch sử - Địa lý", "Tâm lý - Tâm linh", "Tâm lý - Giáo dục", "Kinh tế - Quản trị", "Sách Ngoại ngữ", "Tôn Giáo - Tín ngưỡng", "Sách thiếu nhi", "Sách văn học cổ điển", "Truyện dân gian", "Sách nghệ thuật", "Sách du lịch", "Sách nấu ăn", "Sách khoa học xã hội"]
        self.cbtheLoai.set("Chung")
        self.cbtheLoai.pack(side="left", padx=(5,0))
        # Số lượng nằm ở dòng 3
        Row_3 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_3.pack(fill="x", pady=5)
        tk.Label(Row_3, text="Số lượng:", bg="white", font=("Arial", 10)).pack(side="left")
        self.soLuong = tk.IntVar()
        tk.Entry(Row_3, textvariable=self.soLuong,width=15, font=("Arial", 10)).pack(side="left", padx=(5,20))
        # Khung cho các nút
        self.KhungNut = tk.Frame(self.KhungNhapLieu, bg="white")
        self.KhungNut.pack(fill="x", pady=(0,10))
        # Nút Thêm, Sửa, Xóa, Làm mới
        tk.Button(self.KhungNut, text="Thêm", command=self.add, bg="#4CAF50", fg="white", 
                font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=(0, 5))
        tk.Button(self.KhungNut, text="Sửa", command=self.update, bg="#2196F3", fg="white", 
                font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=5)
        tk.Button(self.KhungNut, text="Xóa", command=self.remove, bg="#f44336", fg="white", 
                font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=5)
        tk.Button(self.KhungNut, text="Làm mới", command=self.clear, bg="#FF9800", fg="white", 
                font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=5)
        # Khung tìm kiếm
        self.KhungTimKiem = tk.Frame(self.KhungChinh, bg="white")
        self.KhungTimKiem.pack(fill="x", expand=True, pady= (0, 10))
        tk.Label(self.KhungTimKiem, text="Tìm kiếm:", bg="white", font=("Arial", 10)).pack(side="left", padx=5)
        self.tuKhoaTimKiem = tk.StringVar()
        self.entryTimKiem = tk.Entry(self.KhungTimKiem, textvariable=self.tuKhoaTimKiem, font=("Arial", 10))
        self.entryTimKiem.pack(side="left", padx=(5,20))
        self.entryTimKiem.bind("<Return>", lambda event: self.timKiem())
        tk.Button(self.KhungTimKiem, text="Tìm kiếm", command=self.timKiem, bg="#9C27B0", fg="white", 
                font=("Arial", 10, "bold"), width=10, height=2).pack(side="left")
        # Khung cho hiển thị danh sách sách
        tree_Khung = tk.Frame(self.KhungChinh, bg="white")
        tree_Khung.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.tree = ttk.Treeview(tree_Khung, columns=("maSach", "tenSach", "tacGia", "theLoai", "soLuong"), show="headings")
        self.tree.heading("maSach", text="Mã sách")
        self.tree.heading("tenSach", text="Tên sách")
        self.tree.heading("tacGia", text="Tác giả")
        self.tree.heading("theLoai", text="Thể loại")
        self.tree.heading("soLuong", text="Số lượng")
        
        self.tree.column("maSach", width=100, minwidth=80)
        self.tree.column("tenSach", width=300, minwidth=200)
        self.tree.column("tacGia", width=150, minwidth=100)
        self.tree.column("theLoai", width=120, minwidth=100)
        self.tree.column("soLuong", width=100, minwidth=80)
        # Thanh Cuộn
        v_scrollbar = ttk.Scrollbar(tree_Khung, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_Khung, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack các thành phần
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Cấu hình lưới
        tree_Khung.grid_rowconfigure(0, weight=1)
        tree_Khung.grid_columnconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    def tailaiDuLieu(self):
        # Xóa tất cả các mục hiện tại trong cây
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Tải lại dữ liệu từ danh sách sách
        for book in self.ql_book.BookList:
            self.tree.insert("", "end", values=(book.bookID, book.bookName, book.author, book.category, book.quantity))
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            self.maSach.set(values[0])
            self.tenSach.set(values[1])
            self.tacGia.set(values[2])
            self.theLoai.set(values[3])
            self.soLuong.set(values[4])
    def add(self):
        try:
            ma_sach = self.maSach.get().strip()
            ten_sach = self.tenSach.get().strip()
            tac_gia = self.tacGia.get().strip()
            the_loai = self.theLoai.get().strip()
            so_luong = self.soLuong.get()
            if not all([ma_sach, ten_sach, tac_gia, the_loai]) or so_luong <= 0:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            book = Book(ma_sach, ten_sach, tac_gia, the_loai, so_luong)
            self.ql_book.addBook(book)
            messagebox.showinfo("Thông báo", "Thêm sách thành công!")
            self.clear()
            self.tailaiDuLieu()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm sách: {e}")
    def remove(self):
        maSach = self.maSach.get().strip()
        if not maSach:
            messagebox.showerror("Lỗi", "❌ Vui lòng chọn sách để xóa.")
            return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách '{maSach}'?"):
            try:
                self.ql_book.removeBook(maSach)
                messagebox.showinfo("Thông báo", "✅ Xóa sách thành công!")
                self.clear()
                self.tailaiDuLieu()
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))
            except Exception as e:
                messagebox.showerror("Lỗi", f"❌ Lỗi khi xóa sách: {e}")
    def update(self):
        maSach = self.maSach.get().strip()
        if not maSach:
            messagebox.showerror("Lỗi", "❌ Vui lòng chọn sách để cập nhật.")
            return
        try:
            updated_book = Book(
                maSach,
                self.tenSach.get().strip(),
                self.tacGia.get().strip(),
                self.theLoai.get().strip(),
                self.soLuong.get()
            )
            self.ql_book.updateBook(maSach, updated_book)
            messagebox.showinfo("Thông báo", "✅ Cập nhật sách thành công!")
            self.clear()
            self.tailaiDuLieu()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"❌ Lỗi khi cập nhật sách: {e}")
    def timKiem(self):
        tuKhoa = self.tuKhoaTimKiem.get().strip()
        if not tuKhoa:
            self.tailaiDuLieu()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        results = self.ql_book.searchBooks(tuKhoa)
        if not results:
            messagebox.showinfo("Thông báo", "🔍 Không tìm thấy sách nào khớp với từ khóa.")
            return
        for book in results:
            self.tree.insert("", "end", values=(book.bookID, book.bookName, book.author, book.category, book.quantity))
    def clear(self):
        self.maSach.set("")
        self.tenSach.set("")
        self.tacGia.set("")
        self.theLoai.set("Chung")
        self.soLuong.set(0)
        self.tuKhoaTimKiem.set("")
# Chạy thử giao diện
if __name__ == "__main__":
    root = tk.Tk()
    app = GiaoDienBook(root)
    app.pack(fill="both", expand=True)
    root.geometry("800x600")
    root.mainloop()