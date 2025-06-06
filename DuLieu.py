class User: #Lớp những tài khoản người dùng:
    def __init__(self, tenDN, matKhau, chucVu, quyen = False):
        self.username = tenDN
        self.password = matKhau
        self.role = chucVu
        self.permission = quyen
class Book: #Lớp những quyển sách:
    def __init__(self, maSach, tenSach, tacGia, theLoai, soLuong):
        self.bookID = maSach
        self.bookName = tenSach
        self.author = tacGia
        self.category = theLoai
        self.quantity = soLuong
    def to_dict(self): #Chuyển đổi đối tượng thành từ điển
        return { 
            'bookID': self.bookID,
            'bookName': self.bookName,
            'author': self.author,
            'category': self.category,
            'quantity': self.quantity
        }
    def from_dict(self, data): #Chuyển đổi từ điển thành đối tượng
        self.bookID = data['bookID']
        self.bookName = data['bookName']
        self.author = data['author']
        self.category = data['category']
        self.quantity = data['quantity']
class ThuThu: #Lớp những thủ thư:
    def __init__(self, maTT, tenTT, soDT, email, diachi, caLam, luong):
        self.staffID = maTT
        self.staffName = tenTT
        self.phone = soDT
        self.email = email
        self.address = diachi
        self.shift = caLam
        self.salary = luong
    def to_dict(self): #Chuyển đổi đối tượng thành từ điển
        return {
            'staffID': self.staffID,
            'staffName': self.staffName,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'shift': self.shift,
            'salary': self.salary
        }
    def from_dict(self, data): #Chuyển đổi từ điển thành đối tượng
        self.staffID = data['staffID']
        self.staffName = data['staffName']
        self.phone = data['phone']
        self.email = data['email']
        self.address = data['address']
        self.shift = data['shift']
        self.salary = data['salary']
        