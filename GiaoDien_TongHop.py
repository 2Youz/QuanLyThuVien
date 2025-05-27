import tkinter as tk
from tkinter import messagebox, ttk
from DuLieu import Book, ThuThu
from QuanLy_Book import QuanLyBook
from QuanLy_ThuThu import QuanLyThuThu

class GiaoDienNutBam(tk.Frame):
    def __init__(self, parent, mode, ql_book, ql_thuthu, refresh_callback):
        self.mode = mode
        self.ql_book = ql_book
        self.ql_thuthu = ql_thuthu
        self.refresh_callback = refresh_callback
        
        # Tạo cửa sổ
        self.win = tk.Toplevel(parent)
        self.win.title("Quản lý Sách" if mode == "book" else "Quản lý Thủ thư")
        self.win.geometry("400x300" if mode == "book" else "400x400")
        self.win.transient(parent)
        self.win.grab_set()
        
        self.tao_form()
        
    def tao_form(self):
        frame = tk.Frame(self.win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mã
        tk.Label(frame, text="Mã:").grid(row=0, column=0, sticky="w", pady=5)
        self.var_ma = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_ma, width=30).grid(row=0, column=1, pady=5)
        
        # Tên
        tk.Label(frame, text="Tên:").grid(row=1, column=0, sticky="w", pady=5)
        self.var_ten = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_ten, width=30).grid(row=1, column=1, pady=5)
        
        if self.mode == "book":
            # Tác giả
            tk.Label(frame, text="Tác giả:").grid(row=2, column=0, sticky="w", pady=5)
            self.var_tacgia = tk.StringVar()
            tk.Entry(frame, textvariable=self.var_tacgia, width=30).grid(row=2, column=1, pady=5)
            
            # Thể loại
            tk.Label(frame, text="Thể loại:").grid(row=3, column=0, sticky="w", pady=5)
            self.var_theloai = tk.StringVar()
            cb = ttk.Combobox(frame, textvariable=self.var_theloai, width=27)
            cb['values'] = ["Chung", "Sách giáo khoa", "Sách tham khảo", "Sách kỹ năng sống", "Truyện tranh", "Tiểu thuyết", "Văn học Việt Nam", "Văn học nước ngoài", "Khoa học - Công nghệ", "Lịch sử - Địa lý", "Tâm lý - Tâm linh", "Tâm lý - Giáo dục", "Kinh tế - Quản trị", "Sách Ngoại ngữ", "Tôn Giáo - Tín ngưỡng", "Sách thiếu nhi", "Sách văn học cổ điển", "Truyện dân gian", "Sách nghệ thuật", "Sách du lịch", "Sách nấu ăn", "Sách khoa học xã hội"]
            cb.set("Chung")
            cb.grid(row=3, column=1, pady=5)
            
            # Số lượng
            tk.Label(frame, text="Số lượng:").grid(row=4, column=0, sticky="w", pady=5)
            self.var_soluong = tk.IntVar()
            tk.Entry(frame, textvariable=self.var_soluong, width=30).grid(row=4, column=1, pady=5)
            
        else:  # thuthu
            # Auto mã thủ thư
            self.auto_ma_thuthu()
            
            # SĐT
            tk.Label(frame, text="SĐT:").grid(row=2, column=0, sticky="w", pady=5)
            self.var_sdt = tk.StringVar()
            tk.Entry(frame, textvariable=self.var_sdt, width=30).grid(row=2, column=1, pady=5)
            
            # Email
            tk.Label(frame, text="Email:").grid(row=3, column=0, sticky="w", pady=5)
            self.var_email = tk.StringVar()
            tk.Entry(frame, textvariable=self.var_email, width=30).grid(row=3, column=1, pady=5)
            
            # Địa chỉ
            tk.Label(frame, text="Địa chỉ:").grid(row=4, column=0, sticky="w", pady=5)
            self.var_diachi = tk.StringVar()
            tk.Entry(frame, textvariable=self.var_diachi, width=30).grid(row=4, column=1, pady=5)
            
            # Ca làm
            tk.Label(frame, text="Ca làm:").grid(row=5, column=0, sticky="w", pady=5)
            self.var_ca = tk.StringVar()
            cb2 = ttk.Combobox(frame, textvariable=self.var_ca, width=27)
            cb2['values'] = ["06:00 - 10:00", "10:00 - 14:00", "14:00 - 18:00", "06:00 - 10:00 & 10:00 - 14:00","06:00 - 10:00 & 14:00 - 18:00","10:00 - 14:00 & 14:00 - 18:00","Toàn thời gian"]
            cb2.set("06:00 - 10:00")
            cb2.grid(row=5, column=1, pady=5)
            
            # Lương
            tk.Label(frame, text="Lương:").grid(row=6, column=0, sticky="w", pady=5)
            self.var_luong = tk.DoubleVar()
            tk.Entry(frame, textvariable=self.var_luong, width=30).grid(row=6, column=1, pady=5)
        
        # Nút
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=10, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Thêm", command=self.them, width=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Xóa", command=self.xoa, width=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Mới", command=self.moi, width=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Đóng", command=self.win.destroy, width=8).pack(side="left", padx=5)
    
    # Tự động tạo mã thủ thư
    def auto_ma_thuthu(self):
        count = len(self.ql_thuthu.ThuThuList) + 1
        self.var_ma.set(f"TT{count:03d}")
    
    # Thêm sách hoặc thủ thư
    def them(self):
        try:
            if self.mode == "book":
                book = Book(self.var_ma.get(), self.var_ten.get(), 
                        self.var_tacgia.get(), self.var_theloai.get(), 
                        self.var_soluong.get())
                self.ql_book.addBook(book)
                messagebox.showinfo("OK", "Thêm sách thành công")
            else:
                thuthu = ThuThu(self.var_ma.get(), self.var_ten.get(),
                            self.var_sdt.get(), self.var_email.get(),
                            self.var_diachi.get(), self.var_ca.get(),
                            self.var_luong.get())
                self.ql_thuthu.addThuThu(thuthu)
                messagebox.showinfo("OK", "Thêm thủ thư thành công")
            self.moi()
            self.refresh_callback()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    # Xóa sách hoặc thủ thư
    def xoa(self):
        ma = self.var_ma.get()
        if not ma:
            messagebox.showerror("Lỗi", "Nhập mã để xóa")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa {ma}?"):
            try:
                if self.mode == "book":
                    self.ql_book.removeBook(ma)
                else:
                    self.ql_thuthu.removeThuThu(ma)
                messagebox.showinfo("OK", "Xóa thành công")
                self.moi()
                self.refresh_callback()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    # Làm mới form
    def moi(self):
        self.var_ma.set("")
        self.var_ten.set("")
        if self.mode == "book":
            self.var_tacgia.set("")
            self.var_theloai.set("Khác")
            self.var_soluong.set(0)
        else:
            self.auto_ma_thuthu()
            self.var_sdt.set("")
            self.var_email.set("")
            self.var_diachi.set("")
            self.var_ca.set("Sáng")
            self.var_luong.set(0)

class GiaoDienSachVaThuThu(tk.Frame):
    def __init__(self, master, user_login):
        super().__init__(master)
        self.user_login = user_login
        self.pack(fill="both", expand=True)
        
        self.ql_book = QuanLyBook()
        self.ql_thuthu = QuanLyThuThu()
        
        self.GiaoDien()
        self.load_data_sach()
        self.load_data_thuthu()
    # Tạo giao diện chính
    def GiaoDien(self):
        # Nút
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Quản lý Sách", command=self.mo_sach, 
                width=15, height=2).pack(side="left", padx=5)
        
        if self.user_login.permission:
            tk.Button(btn_frame, text="Quản lý Thủ thư", command=self.mo_thuthu,
                    width=15, height=2).pack(side="left", padx=5)
        
        # Tìm kiếm
        tk.Label(btn_frame, text="Tìm sách:").pack(side="left", padx=(20,5))
        self.var_tim = tk.StringVar()
        tk.Entry(btn_frame, textvariable=self.var_tim, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Tìm", command=self.tim_kiem_sach, width=8).pack(side="left", padx=5)
        
        tk.Label(btn_frame, text="Tìm thủ thư:").pack(side="left", padx=(20,5))
        self.var_tim = tk.StringVar()
        tk.Entry(btn_frame, textvariable=self.var_tim, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Tìm", command=self.tim_kiem_thuthu, width=8).pack(side="left", padx=5)
        
        # Bảng sách
        sach_frame = tk.LabelFrame(self, text="Danh sách sách")
        sach_frame.pack(fill="both", expand=True, padx=10, pady=(0,5))
        
        self.tree_sach = ttk.Treeview(sach_frame, columns=("ma","ten","tacgia","theloai","sl"), 
                                    show="headings", height=6)
        self.tree_sach.heading("ma", text="Mã")
        self.tree_sach.heading("ten", text="Tên sách")
        self.tree_sach.heading("tacgia", text="Tác giả")
        self.tree_sach.heading("theloai", text="Thể loại")
        self.tree_sach.heading("sl", text="SL")
        
        self.tree_sach.column("ma", width=80)
        self.tree_sach.column("ten", width=250)
        self.tree_sach.column("tacgia", width=150)
        self.tree_sach.column("theloai", width=100)
        self.tree_sach.column("sl", width=50)
        
        self.tree_sach.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bảng thủ thư
        if self.user_login.permission:
            tt_frame = tk.LabelFrame(self, text="Danh sách thủ thư")
            tt_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            self.tree_tt = ttk.Treeview(tt_frame, columns=("ma","ten","sdt","email","diachi","ca","luong"), 
                                    show="headings", height=5)
            self.tree_tt.heading("ma", text="Mã")
            self.tree_tt.heading("ten", text="Tên")
            self.tree_tt.heading("sdt", text="SĐT")
            self.tree_tt.heading("email", text="Email")
            self.tree_tt.heading("diachi", text="Địa chỉ")
            self.tree_tt.heading("ca", text="Ca")
            self.tree_tt.heading("luong", text="Lương")
            
            self.tree_tt.column("ma", width=70)
            self.tree_tt.column("ten", width=120)
            self.tree_tt.column("sdt", width=90)
            self.tree_tt.column("email", width=150)
            self.tree_tt.column("diachi", width=150)
            self.tree_tt.column("ca", width=80)
            self.tree_tt.column("luong", width=80)
            
            self.tree_tt.pack(fill="both", expand=True, padx=5, pady=5)
    # Mở giao diện quản lý sách
    def mo_sach(self):
        GiaoDienNutBam(self.master, "book", self.ql_book, self.ql_thuthu, self.load_data_sach)
    # Mở giao diện quản lý thủ thư
    def mo_thuthu(self):
        GiaoDienNutBam(self.master, "thuthu", self.ql_book, self.ql_thuthu, self.load_data_thuthu)
    # Tải dữ liệu sách và thủ thư
    def load_data_sach(self):
        # Xóa data cũ
        for item in self.tree_sach.get_children():
            self.tree_sach.delete(item)
        
        # Load sách
        for book in self.ql_book.BookList:
            self.tree_sach.insert("", "end", values=(
                book.bookID, book.bookName, book.author, book.category, book.quantity))
    def load_data_thuthu(self):    
        # Load thủ thư
        if self.user_login.permission:
            for item in self.tree_tt.get_children():
                self.tree_tt.delete(item)
            for tt in self.ql_thuthu.ThuThuList:
                self.tree_tt.insert("", "end", values=(
                    tt.staffID, tt.staffName, tt.phone, tt.email, tt.address, tt.shift, tt.salary))
    # Tìm kiếm sách và thủ thư
    def tim_kiem_sach(self):
        keyword = self.var_tim.get().strip()
        if not keyword:
            self.load_data_sach()
            return
        
        # Tìm sách
        for item in self.tree_sach.get_children():
            self.tree_sach.delete(item)
        for book in self.ql_book.searchBooks(keyword):
            self.tree_sach.insert("", "end", values=(
                book.bookID, book.bookName, book.author, book.category, book.quantity))
    def tim_kiem_thuthu(self):    
        keyword = self.var_tim.get().strip()
        if not keyword:
            self.load_data_thuthu()
            return
        if self.user_login.permission:
            for item in self.tree_tt.get_children():
                self.tree_tt.delete(item)
            for tt in self.ql_thuthu.searchThuThu(keyword):
                self.tree_tt.insert("", "end", values=(
                    tt.staffID, tt.staffName, tt.phone, tt.email, tt.address, tt.shift, tt.salary))

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý thư viện")
    root.geometry("800x600")
    
    user = type('User', (), {'username': 'admin', 'permission': True})()
    app = GiaoDienSachVaThuThu(root, user)
    root.mainloop()