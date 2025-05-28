import tkinter as tk
from tkinter import messagebox, ttk
from DuLieu import Book, ThuThu
from QuanLy_Book import QuanLyBook
from QuanLy_ThuThu import QuanLyThuThu
import re
class GiaoDienNutBam(tk.Frame):
    def __init__(self, parent, mode, ql_book, ql_thuthu, refresh_callback, selected_data=None):
        self.mode = mode
        self.ql_book = ql_book
        self.ql_thuthu = ql_thuthu
        self.refresh_callback = refresh_callback
        self.selected_data = selected_data
        
        # Tạo cửa sổ
        self.win = tk.Toplevel(parent)
        self.win.title("Thông tin sách" if mode == "book" else "Thông tin thủ thư")
        self.win.geometry("340x280" if mode == "book" else "340x340")
        self.win.transient(parent)
        self.win.grab_set()
        
        self.tao_form()
        
        # Nếu có dữ liệu được chọn, điền vào form
        if self.selected_data:
            self.dien_thong_tin(self.selected_data)
        
    def tao_form(self):
        frame = tk.Frame(self.win)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mã
        tk.Label(frame, text="Mã:").grid(row=0, column=0, sticky="w", pady=5)
        self.var_ma = tk.StringVar()
        self.entry_ma = tk.Entry(frame, textvariable=self.var_ma, width=30)
        self.entry_ma.grid(row=0, column=1, pady=5)
        
        # Tên
        tk.Label(frame, text="Tên:").grid(row=1, column=0, sticky="w", pady=5)
        self.var_ten = tk.StringVar()
        tk.Entry(frame, textvariable=self.var_ten, width=30).grid(row=1, column=1, pady=5)
        
        if self.mode == "book":
            if not self.selected_data:
                self.MaTuDong()
            # Tác giả
            tk.Label(frame, text="Tác giả:").grid(row=2, column=0, sticky="w", pady=5)
            self.var_tacgia = tk.StringVar()
            tk.Entry(frame, textvariable=self.var_tacgia, width=30).grid(row=2, column=1, pady=5)
            
            # Thể loại
            tk.Label(frame, text="Thể loại:").grid(row=3, column=0, sticky="w", pady=5)
            self.var_theloai = tk.StringVar()
            self.cb_theloai = ttk.Combobox(frame, textvariable=self.var_theloai, width=27)
            self.cb_theloai['values'] = ["Chung", "Sách giáo khoa", "Sách tham khảo", "Sách kỹ năng sống", "Truyện tranh", "Tiểu thuyết", "Văn học Việt Nam", "Văn học nước ngoài", "Khoa học - Công nghệ", "Lịch sử - Địa lý", "Tâm lý - Tâm linh", "Tâm lý - Giáo dục", "Kinh tế - Quản trị", "Sách Ngoại ngữ", "Tôn Giáo - Tín ngưỡng", "Sách thiếu nhi", "Sách văn học cổ điển", "Truyện dân gian", "Sách nghệ thuật", "Sách du lịch", "Sách nấu ăn", "Sách khoa học xã hội"]
            self.cb_theloai.set("Chung")
            self.cb_theloai.grid(row=3, column=1, pady=5)
            
            # Số lượng
            tk.Label(frame, text="Số lượng:").grid(row=4, column=0, sticky="w", pady=5)
            self.var_soluong = tk.IntVar()
            tk.Entry(frame, textvariable=self.var_soluong, width=30).grid(row=4, column=1, pady=5)
            
        else:  # thuthu
            if not self.selected_data:
                self.MaTuDong()
            
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
            self.cb_ca = ttk.Combobox(frame, textvariable=self.var_ca, width=27)
            self.cb_ca['values'] = ["06:00 - 10:00", "10:00 - 14:00", "14:00 - 18:00", "06:00 - 10:00 & 10:00 - 14:00","06:00 - 10:00 & 14:00 - 18:00","10:00 - 14:00 & 14:00 - 18:00","Toàn thời gian"]
            self.cb_ca.set("06:00 - 10:00")
            self.cb_ca.grid(row=5, column=1, pady=5)
            
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
        tk.Button(btn_frame, text="Sửa", command=self.sua, width=8).pack(side="left", padx=5)
    
    def dien_thong_tin(self, data):
        if self.mode == "book":
            self.var_ma.set(data[0])
            self.var_ten.set(data[1])
            self.var_tacgia.set(data[2])
            self.var_theloai.set(data[3])
            self.var_soluong.set(data[4])
        else:
            self.var_ma.set(data[0])
            self.var_ten.set(data[1])
            self.var_sdt.set(data[2])
            self.var_email.set(data[3])
            self.var_diachi.set(data[4])
            self.var_ca.set(data[5])
            self.var_luong.set(data[6])
    
    def MaTuDong(self):
        if self.mode == "book":
            existing_codes = [book.bookID for book in self.ql_book.BookList]
            count = 1
            while f"MS{count:03d}" in existing_codes:
                count += 1
            self.var_ma.set(f"MS{count:03d}")
        else:  # thuthu
            existing_codes = [tt.staffID for tt in self.ql_thuthu.ThuThuList]
            count = 1
            while f"TT{count:03d}" in existing_codes:
                count += 1
            self.var_ma.set(f"TT{count:03d}")
    
    def them(self):
        try:
            if self.mode == "book":
                if self.var_soluong.get() < 0:
                    messagebox.showerror("Lỗi", "Số lượng không được âm")
                    return
                book = Book(self.var_ma.get(), self.var_ten.get(), 
                        self.var_tacgia.get(), self.var_theloai.get(), 
                        self.var_soluong.get())
                self.ql_book.addBook(book)
                messagebox.showinfo("Thông báo", "Thêm sách thành công")
            else:
                if self.var_luong.get() < 0:
                    messagebox.showerror("Lỗi", "Lương không được âm")
                    return
                if not re.match(r"^\d{10}$", self.var_sdt.get()):
                    messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ")
                    return
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', self.var_email.get()):
                    messagebox.showerror("Lỗi", "Email không hợp lệ")
                    return
                thuthu = ThuThu(self.var_ma.get(), self.var_ten.get(),
                            self.var_sdt.get(), self.var_email.get(),
                            self.var_diachi.get(), self.var_ca.get(),
                            self.var_luong.get())
                self.ql_thuthu.addThuThu(thuthu)
                messagebox.showinfo("Thông báo", "Thêm thủ thư thành công")
            self.moi()
            self.refresh_callback()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def xoa(self):
        ma = self.var_ma.get()
        if not ma:
            messagebox.showerror("Lỗi", "Chọn mã để xóa")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa {ma}?"):
            try:
                if self.mode == "book":
                    self.ql_book.removeBook(ma)
                else:
                    self.ql_thuthu.removeThuThu(ma)
                messagebox.showinfo("Thông báo", "Xóa thành công")
                self.win.destroy()
                self.moi()
                self.refresh_callback()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    
    def moi(self):
        self.MaTuDong()
        self.var_ten.set("")
        if self.mode == "book":
            self.var_tacgia.set("")
            self.var_theloai.set("Chung")
            self.var_soluong.set(0)
        else:
            self.var_sdt.set("")
            self.var_email.set("")
            self.var_diachi.set("")
            self.var_ca.set("06:00 - 10:00")
            self.var_luong.set(0.0)
    
    def sua(self):
        if not self.var_ma.get():
            messagebox.showerror("Lỗi", "Chọn mã để sửa")
            return
        try:
            ma = self.var_ma.get()
            if self.mode == "book":
                if not self.var_ten.get() or not self.var_tacgia.get():
                    messagebox.showerror("Lỗi", "Các thông tin không được để trống")
                    return
                if self.var_soluong.get() < 0:
                    messagebox.showerror("Lỗi", "Số lượng không được âm")
                    return
                book = Book(ma, self.var_ten.get(), 
                            self.var_tacgia.get(), self.var_theloai.get(), 
                            self.var_soluong.get())
                self.ql_book.updateBook(ma, book)
                messagebox.showinfo("Thông báo", "Sửa sách thành công")
                self.win.destroy()
            else:
                if self.var_luong.get() < 0:
                    messagebox.showerror("Lỗi", "Lương không được âm")
                    return
                if not re.match(r"^\d{10}$", self.var_sdt.get()):
                    messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ")
                    return
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', self.var_email.get()):
                    messagebox.showerror("Lỗi", "Email không hợp lệ")
                    return
                if not self.var_ten.get() or not self.var_sdt.get() or not self.var_email.get():
                    messagebox.showerror("Lỗi", "Các thông tin không được để trống")
                    return
                thuthu = ThuThu(ma, self.var_ten.get(),
                            self.var_sdt.get(), self.var_email.get(),
                            self.var_diachi.get(), self.var_ca.get(),
                            self.var_luong.get())
                self.ql_thuthu.updateThuThu(ma, thuthu)
                messagebox.showinfo("Thông báo", "Sửa thủ thư thành công")
                self.win.destroy()
            self.refresh_callback()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

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
    
    def GiaoDien(self):
        # Nút
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Cập nhật Sách", command=self.mo_sach, 
                width=15, height=2).pack(side="left", padx=5)
        if self.user_login.permission:
            # Chỉ quản lý thủ thư nếu có quyền
            tk.Button(btn_frame, text="Cập nhật Thủ thư", command=self.mo_thuthu,
                    width=15, height=2).pack(side="left", padx=5)
        
        # Tìm kiếm sách
        tk.Label(btn_frame, text="Tìm sách:").pack(side="left", padx=(20,5))
        self.var_tim_sach = tk.StringVar()
        tk.Entry(btn_frame, textvariable=self.var_tim_sach, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Tìm", command=self.tim_kiem_sach, width=8).pack(side="left", padx=5)
        
        # Tìm kiếm thủ thư
        tk.Label(btn_frame, text="Tìm thủ thư:").pack(side="left", padx=(20,5))
        self.var_tim_thuthu = tk.StringVar()
        tk.Entry(btn_frame, textvariable=self.var_tim_thuthu, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Tìm", command=self.tim_kiem_thuthu, width=8).pack(side="left", padx=5)
        
        # Bảng sách
        sach_frame = tk.LabelFrame(self, text="Thông tin sách")
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
        
        self.tree_sach.bind("<Double-1>", self.on_sach_double_click)
        self.tree_sach.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bảng thủ thư
        tt_frame = tk.LabelFrame(self, text="Thông tin thủ thư")
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
        self.tree_tt.bind("<Double-1>", self.on_thuthu_double_click)
        self.tree_tt.pack(fill="both", expand=True, padx=5, pady=5)
    
    def on_sach_double_click(self, event):
        selection = self.tree_sach.selection()
        if selection:
            values = self.tree_sach.item(selection[0], 'values')
            GiaoDienNutBam(self.master, "book", self.ql_book, self.ql_thuthu, self.load_data_sach, selected_data=values)
    
    def on_thuthu_double_click(self, event):
        selection = self.tree_tt.selection()
        if selection:
            values = self.tree_tt.item(selection[0], 'values')
            GiaoDienNutBam(self.master, "thuthu", self.ql_book, self.ql_thuthu, self.load_data_thuthu, selected_data=values)
    
    def mo_sach(self):
        GiaoDienNutBam(self.master, "book", self.ql_book, self.ql_thuthu, self.load_data_sach)
    
    def mo_thuthu(self):
        GiaoDienNutBam(self.master, "thuthu", self.ql_book, self.ql_thuthu, self.load_data_thuthu)
    
    def load_data_sach(self):
        for item in self.tree_sach.get_children():
            self.tree_sach.delete(item)
        for book in self.ql_book.BookList:
            self.tree_sach.insert("", "end", values=(
                book.bookID, book.bookName, book.author, book.category, book.quantity))
    
    def load_data_thuthu(self):    
        for item in self.tree_tt.get_children():
            self.tree_tt.delete(item)
        for tt in self.ql_thuthu.ThuThuList:
            self.tree_tt.insert("", "end", values=(
                    tt.staffID, tt.staffName, tt.phone, tt.email, tt.address, tt.shift, tt.salary))
    
    def tim_kiem_sach(self):
        keyword = self.var_tim_sach.get().strip()
        if not keyword:
            self.load_data_sach()
            return
        for item in self.tree_sach.get_children():
            self.tree_sach.delete(item)
        for book in self.ql_book.searchBooks(keyword):
            self.tree_sach.insert("", "end", values=(
                book.bookID, book.bookName, book.author, book.category, book.quantity))
    
    def tim_kiem_thuthu(self):    
        keyword = self.var_tim_thuthu.get().strip()
        if not keyword:
            self.load_data_thuthu()
            return
        if self.user_login.permission:
            for item in self.tree_tt.get_children():
                self.tree_tt.delete(item)
            for tt in self.ql_thuthu.searchThuThu(keyword):
                self.tree_tt.insert("", "end", values=(
                    tt.staffID, tt.staffName, tt.phone, tt.email, tt.address, tt.shift, tt.salary))
