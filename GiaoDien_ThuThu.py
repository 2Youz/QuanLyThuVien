import tkinter as tk
from tkinter import messagebox, ttk
from DuLieu import ThuThu
from QuanLy_ThuThu import QuanLyThuThu

class GiaoDienThuThu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self.ql_thuthu = QuanLyThuThu()
        self.GiaoDien()
        self.tailaiDuLieu()
        self.capNhatMaThuThuTiepTheo()
    
    def capNhatMaThuThuTiepTheo(self):
        """Tự động tạo mã thủ thư tiếp theo theo format TT001, TT002, ..."""
        if not self.ql_thuthu.ThuThuList:
            # Nếu chưa có thủ thư nào, bắt đầu từ TT001
            ma_moi = "TT001"
        else:
            # Tìm số lớn nhất trong danh sách mã thủ thư
            max_so = 0
            for thuthu in self.ql_thuthu.ThuThuList:
                if thuthu.staffID.startswith("TT") and len(thuthu.staffID) == 5:
                    try:
                        so = int(thuthu.staffID[2:])  # Lấy phần số từ vị trí thứ 3
                        if so > max_so:
                            max_so = so
                    except ValueError:
                        continue
            
            # Tạo mã mới với số tiếp theo
            ma_moi = f"TT{(max_so + 1):03d}"
        
        self.maThuThu.set(ma_moi)
    
    def GiaoDien(self):
        # Khung chính
        self.KhungChinh = tk.Frame(self, bg="white")
        self.KhungChinh.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Khung cho nhập liệu thủ thư
        self.KhungNhapLieu = tk.Frame(self.KhungChinh, bg="white")
        self.KhungNhapLieu.pack(fill="x", pady=(0, 10))
        
        # Mã thủ thư và tên thủ thư nằm ở dòng 1
        Row_1 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_1.pack(fill="x", pady=5)
        
        tk.Label(Row_1, text="Mã thủ thư:", bg="white", font=("Arial", 10)).pack(side="left")
        self.maThuThu = tk.StringVar()
        self.entryMaThuThu = tk.Entry(Row_1, textvariable=self.maThuThu, width=15, font=("Arial", 10), 
                                     state="readonly", bg="#f0f0f0")  # Chỉ đọc, không cho phép chỉnh sửa
        self.entryMaThuThu.pack(side="left", padx=(5,20))
        
        tk.Label(Row_1, text="Tên thủ thư:", bg="white", font=("Arial", 10)).pack(side="left")
        self.tenThuThu = tk.StringVar()
        tk.Entry(Row_1, textvariable=self.tenThuThu, width=35, font=("Arial", 10)).pack(side="left", padx=(5,0))
        
        # Số điện thoại và email nằm ở dòng 2
        Row_2 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_2.pack(fill="x", pady=5)
        
        tk.Label(Row_2, text="Số điện thoại:", bg="white", font=("Arial", 10)).pack(side="left")
        self.soDienThoai = tk.StringVar()
        tk.Entry(Row_2, textvariable=self.soDienThoai, width=15, font=("Arial", 10)).pack(side="left", padx=(5,20))
        
        tk.Label(Row_2, text="Email:", bg="white", font=("Arial", 10)).pack(side="left")
        self.email = tk.StringVar()
        tk.Entry(Row_2, textvariable=self.email, width=30, font=("Arial", 10)).pack(side="left", padx=(5,0))
        
        # Địa chỉ nằm ở dòng 3
        Row_3 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_3.pack(fill="x", pady=5)
        
        tk.Label(Row_3, text="Địa chỉ:", bg="white", font=("Arial", 10)).pack(side="left")
        self.diaChi = tk.StringVar()
        tk.Entry(Row_3, textvariable=self.diaChi, width=60, font=("Arial", 10)).pack(side="left", padx=(5,0))
        
        # Ca làm việc và lương nằm ở dòng 4
        Row_4 = tk.Frame(self.KhungNhapLieu, bg="white")
        Row_4.pack(fill="x", pady=5)
        
        tk.Label(Row_4, text="Ca làm việc:", bg="white", font=("Arial", 10)).pack(side="left")
        self.caLamViec = tk.StringVar()
        self.cbCaLamViec = ttk.Combobox(Row_4, textvariable=self.caLamViec, width=15, font=("Arial", 10))
        self.cbCaLamViec['values'] = ["06:00 - 10:00", "10:00 - 14:00", "14:00 - 18:00", "06:00 - 10:00 & 10:00 - 14:00","06:00 - 10:00 & 14:00 - 18:00","10:00 - 14:00 & 14:00 - 18:00","Toàn thời gian"]
        self.cbCaLamViec.set("Sáng")
        self.cbCaLamViec.pack(side="left", padx=(5,20))
        
        tk.Label(Row_4, text="Lương:", bg="white", font=("Arial", 10)).pack(side="left")
        self.luong = tk.DoubleVar()
        tk.Entry(Row_4, textvariable=self.luong, width=20, font=("Arial", 10)).pack(side="left", padx=(5,0))
        
        # Khung cho các nút
        self.KhungNut = tk.Frame(self.KhungNhapLieu, bg="white")
        self.KhungNut.pack(fill="x", pady=(10,10))
        
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
        self.KhungTimKiem.pack(fill="x", expand=True, pady=(0, 10))
        
        tk.Label(self.KhungTimKiem, text="Tìm kiếm:", bg="white", font=("Arial", 10)).pack(side="left", padx=5)
        self.tuKhoaTimKiem = tk.StringVar()
        self.entryTimKiem = tk.Entry(self.KhungTimKiem, textvariable=self.tuKhoaTimKiem, font=("Arial", 10))
        self.entryTimKiem.pack(side="left", padx=(5,20))
        self.entryTimKiem.bind("<Return>", lambda event: self.timKiem())
        tk.Button(self.KhungTimKiem, text="Tìm kiếm", command=self.timKiem, bg="#9C27B0", fg="white", 
                font=("Arial", 10, "bold"), width=10, height=2).pack(side="left")
        
        # Khung cho hiển thị danh sách thủ thư
        tree_Khung = tk.Frame(self.KhungChinh, bg="white")
        tree_Khung.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.tree = ttk.Treeview(tree_Khung, columns=("maThuThu", "tenThuThu", "soDienThoai", "email", "diaChi", "caLamViec", "luong"), show="headings")
        self.tree.heading("maThuThu", text="Mã thủ thư")
        self.tree.heading("tenThuThu", text="Tên thủ thư")
        self.tree.heading("soDienThoai", text="Số điện thoại")
        self.tree.heading("email", text="Email")
        self.tree.heading("diaChi", text="Địa chỉ")
        self.tree.heading("caLamViec", text="Ca làm việc")
        self.tree.heading("luong", text="Lương")
        
        self.tree.column("maThuThu", width=80, minwidth=80, stretch=False)
        self.tree.column("tenThuThu", width=120, minwidth=100,stretch=False)
        self.tree.column("soDienThoai", width=90, minwidth=92)
        self.tree.column("email", width=170, minwidth=150)
        self.tree.column("diaChi", width=120, minwidth=150)
        self.tree.column("caLamViec", width=200, minwidth=80)
        self.tree.column("luong", width=120, minwidth=100)
        
        # Thanh cuộn
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
        # Tải lại dữ liệu từ danh sách thủ thư
        for thuthu in self.ql_thuthu.ThuThuList:
            self.tree.insert("", "end", values=(thuthu.staffID, thuthu.staffName, thuthu.phone, 
                            thuthu.email, thuthu.address, thuthu.shift, f"{thuthu.salary:,.0f}"))
    
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            self.maThuThu.set(values[0])
            self.tenThuThu.set(values[1])
            self.soDienThoai.set(values[2])
            self.email.set(values[3])
            self.diaChi.set(values[4])
            self.caLamViec.set(values[5])
            # Xử lý lương (loại bỏ dấu phẩy nếu có)
            luong_str = str(values[6]).replace(',', '')
            try:
                self.luong.set(float(luong_str))
            except ValueError:
                self.luong.set(0.0)
    
    def add(self):
        try:
            ma_thuthu = self.maThuThu.get().strip()
            ten_thuthu = self.tenThuThu.get().strip()
            so_dien_thoai = self.soDienThoai.get().strip()
            email = self.email.get().strip()
            dia_chi = self.diaChi.get().strip()
            ca_lam_viec = self.caLamViec.get().strip()
            luong = self.luong.get()
            
            if not all([ten_thuthu, so_dien_thoai, email, dia_chi, ca_lam_viec]) or luong <= 0:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin và lương > 0.")
                return
            
            # Kiểm tra định dạng email đơn giản
            if "@" not in email or "." not in email:
                messagebox.showerror("Lỗi", "Email không hợp lệ.")
                return
            
            # Kiểm tra số điện thoại (chỉ chứa số)
            if not so_dien_thoai.isdigit():
                messagebox.showerror("Lỗi", "Số điện thoại chỉ được chứa số.")
                return
            
            thuthu = ThuThu(ma_thuthu, ten_thuthu, so_dien_thoai, email, dia_chi, ca_lam_viec, luong)
            self.ql_thuthu.addThuThu(thuthu)
            messagebox.showinfo("Thông báo", "Thêm thủ thư thành công!")
            self.clear()
            self.tailaiDuLieu()
            self.capNhatMaThuThuTiepTheo()  # Cập nhật mã tiếp theo sau khi thêm
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm thủ thư: {e}")
    
    def remove(self):
        maThuThu = self.maThuThu.get().strip()
        if not maThuThu:
            messagebox.showerror("Lỗi", "❌ Vui lòng chọn thủ thư để xóa.")
            return
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa thủ thư '{maThuThu}'?"):
            try:
                self.ql_thuthu.removeThuThu(maThuThu)
                messagebox.showinfo("Thông báo", "✅ Xóa thủ thư thành công!")
                self.clear()
                self.tailaiDuLieu()
                self.capNhatMaThuThuTiepTheo()  # Cập nhật mã tiếp theo sau khi xóa
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))
            except Exception as e:
                messagebox.showerror("Lỗi", f"❌ Lỗi khi xóa thủ thư: {e}")
    
    def update(self):
        maThuThu = self.maThuThu.get().strip()
        if not maThuThu:
            messagebox.showerror("Lỗi", "❌ Vui lòng chọn thủ thư để cập nhật.")
            return
        
        try:
            # Kiểm tra dữ liệu trước khi cập nhật
            ten_thuthu = self.tenThuThu.get().strip()
            so_dien_thoai = self.soDienThoai.get().strip()
            email = self.email.get().strip()
            dia_chi = self.diaChi.get().strip()
            ca_lam_viec = self.caLamViec.get().strip()
            luong = self.luong.get()
            
            if not all([ten_thuthu, so_dien_thoai, email, dia_chi, ca_lam_viec]) or luong <= 0:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin và lương > 0.")
                return
            
            # Kiểm tra định dạng email đơn giản
            if "@" not in email or "." not in email:
                messagebox.showerror("Lỗi", "Email không hợp lệ.")
                return
            
            # Kiểm tra số điện thoại (chỉ chứa số)
            if not so_dien_thoai.isdigit():
                messagebox.showerror("Lỗi", "Số điện thoại chỉ được chứa số.")
                return
            
            updated_thuthu = ThuThu(
                maThuThu,
                ten_thuthu,
                so_dien_thoai,
                email,
                dia_chi,
                ca_lam_viec,
                luong
            )
            self.ql_thuthu.updateThuThu(maThuThu, updated_thuthu)
            messagebox.showinfo("Thông báo", "✅ Cập nhật thủ thư thành công!")
            self.clear()
            self.tailaiDuLieu()
            self.capNhatMaThuThuTiepTheo()  # Cập nhật mã tiếp theo sau khi cập nhật
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"❌ Lỗi khi cập nhật thủ thư: {e}")
    
    def timKiem(self):
        tuKhoa = self.tuKhoaTimKiem.get().strip()
        if not tuKhoa:
            self.tailaiDuLieu()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        results = self.ql_thuthu.searchThuThu(tuKhoa)
        if not results:
            messagebox.showinfo("Thông báo", "🔍 Không tìm thấy thủ thư nào khớp với từ khóa.")
            return
        
        for thuthu in results:
            self.tree.insert("", "end", values=(thuthu.staffID, thuthu.staffName, thuthu.phone, 
                            thuthu.email, thuthu.address, thuthu.shift, f"{thuthu.salary:,.0f}"))
    
    def clear(self):
        self.tenThuThu.set("")
        self.soDienThoai.set("")
        self.email.set("")
        self.diaChi.set("")
        self.caLamViec.set("Sáng")
        self.luong.set(0.0)
        self.tuKhoaTimKiem.set("")
        self.capNhatMaThuThuTiepTheo()  # Cập nhật mã mới khi làm mới form

# Chạy thử giao diện
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý Thủ thư")
    app = GiaoDienThuThu(root)
    app.pack(fill="both", expand=True)
    root.geometry("1000x700")
    root.mainloop()