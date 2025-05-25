import json
import os
from datetime import datetime, timedelta
from DuLieu import MuonTra, Book
from QuanLy_Book import QuanLyBook

class QuanLyMuonTra(QuanLyBook):
    def __init__(self):
        super().__init__()
        # Danh sách mượn trả
        self.MuonTraList = []
        self.MuonTraFile = 'muontra.json'
        self.loadData()
    
    # Tải dữ liệu từ file muontra.json vào danh sách mượn trả
    def loadData(self):
        if not os.path.exists(self.MuonTraFile) or os.path.getsize(self.MuonTraFile) == 0:
            return []
        try: 
            with open(self.MuonTraFile, "r", encoding="utf-8") as file:
                muontraData = json.load(file)
                for mt in muontraData:
                    m = MuonTra(
                        mt['customerID'], 
                        mt['customerName'], 
                        mt['phone'], 
                        mt['email'], 
                        mt['address'], 
                        mt['bookID'], 
                        mt['bookName'], 
                        mt['borrowDate'], 
                        mt['returnDate'], 
                        mt['status'], 
                        mt['fine']
                    )
                    self.MuonTraList.append(m)
        except json.JSONDecodeError as e:
            print(f"Lỗi khi đọc dữ liệu từ file JSON: {e}")
            self.MuonTraList = []
        except FileNotFoundError:
            print(f"File {self.MuonTraFile} không tồn tại.")
            self.MuonTraList = []
        return self.MuonTraList
    
    # Lưu dữ liệu vào file muontra.json
    def saveData(self):
        try:
            with open(self.MuonTraFile, "w", encoding="utf-8") as file:
                muontraData = [mt.to_dict() for mt in self.MuonTraList]
                json.dump(muontraData, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào file JSON: {e}")
    
    # Thêm thông tin mượn sách
    def addMuonTra(self, muontra):
        book = self.getBookByID(muontra.bookID)
        if not book:
            raise ValueError("❌ Mã sách không tồn tại.")
        if book.quantity <= 0:
            raise ValueError("❌ Sách đã hết, không thể mượn.")
        
        # Kiểm tra người mượn đã mượn sách hay chưa
        for mt in self.MuonTraList:
            if (mt.customerID == muontra.customerID and
                mt.bookID == muontra.bookID and
                not mt.status):
                raise ValueError("❌ Người mượn đã mượn sách này, không thể mượn lại.")
        
        self.MuonTraList.append(muontra)
        book.quantity -= 1
        self.saveData()
        super().saveData()
        print("✅ Thêm mượn trả thành công!")
        print(f"📅 Ngày phải trả: {muontra.returnDate}")
    
    # Tính tiền phạt nếu trả sách muộn
    def tinhTienPhat(self, muon_tra_luu, ngay_hien_tai=None):
        if ngay_hien_tai is None:
            ngay_hien_tai = datetime.now().strftime("%d-%m-%Y")
    
        try:
            # Tính từ ngày phải trả (không phải ngày mượn + 14 ngày)
            ngay_phai_tra = datetime.strptime(muon_tra_luu.returnDate, "%d-%m-%Y")
            ngay_tra_thuc_te = datetime.strptime(ngay_hien_tai, "%d-%m-%Y")
        
            if ngay_tra_thuc_te > ngay_phai_tra:
                so_ngay_tre = (ngay_tra_thuc_te - ngay_phai_tra).days
                muon_tra_luu.fine = so_ngay_tre * 5000  # 5000 VND/ngày trễ
                print(f"⚠️ Trả muộn {so_ngay_tre} ngày. Phạt: {muon_tra_luu.fine:,} VND")
                return muon_tra_luu.fine
            else:
                muon_tra_luu.fine = 0
                return 0
        except ValueError as e:
            print(f"Lỗi khi tính tiền phạt: {e}")
            return 0
    
    # Trả sách
    def tra_sach(self, customerID, bookID, Ngay_tra_thuc_te=None):
        if not Ngay_tra_thuc_te:
            Ngay_tra_thuc_te = datetime.now().strftime("%d-%m-%Y")
        
        found = False
        # Xem xét từng mục trong danh sách mượn trả
        for mt in self.MuonTraList:
            if (mt.customerID == customerID and mt.bookID == bookID and not mt.status):
                self.tinhTienPhat(mt, Ngay_tra_thuc_te)
                book = self.getBookByID(bookID)
                if not book:
                    raise ValueError("❌ Mã sách không tồn tại.")
                
                mt.status = True  # Đánh dấu là đã trả sách
                # Thêm thuộc tính actualReturnDate nếu MuonTra class có thuộc tính này
                if hasattr(mt, 'actualReturnDate'):
                    mt.actualReturnDate = Ngay_tra_thuc_te  # Ngày trả thực tế
                book.quantity += 1  # Tăng số lượng sách
                found = True
                break
        
        # Nếu không tìm thấy thông tin mượn sách thì báo lỗi
        if not found:
            raise ValueError("❌ Không tìm thấy thông tin mượn sách.")
        
        self.saveData()
        super().saveData()
        print("✅ Trả sách thành công!")
        if hasattr(mt, 'fine') and mt.fine > 0:
            print(f"💰 Tiền phạt: {mt.fine:,} VND")
    
    # Cập nhật thông tin mượn trả
    def updateMuonTra(self, customerID, bookID, new_muontra):
        found = False
        for mt in self.MuonTraList:
            if mt.customerID == customerID and mt.bookID == bookID:
                mt.customerName = new_muontra.get("customerName", mt.customerName)
                mt.phone = new_muontra.get("phone", mt.phone)
                mt.email = new_muontra.get("email", mt.email)
                mt.address = new_muontra.get("address", mt.address)
                mt.borrowDate = new_muontra.get("borrowDate", mt.borrowDate)
                mt.returnDate = new_muontra.get("returnDate", mt.returnDate)
                found = True
                break
        
        if not found:
            raise ValueError("❌ Không tìm thấy thông tin mượn sách.")
        
        self.saveData()
        print("✅ Cập nhật thông tin mượn trả thành công!")
    
    # Lấy thông tin mượn trả theo mã khách hàng
    def getMuonTraByCustomerID(self, customerID):
        result = []
        for mt in self.MuonTraList:
            if mt.customerID == customerID:
                mt_info = {
                    'customerID': mt.customerID,
                    'customerName': mt.customerName,
                    'phone': mt.phone,
                    'email': mt.email,
                    'address': mt.address,
                    'bookID': mt.bookID,
                    'bookName': mt.bookName,
                    'borrowDate': mt.borrowDate,
                    'returnDate': mt.returnDate,
                    'status': mt.status,
                    'fine': mt.fine
                }
                result.append(mt_info)
        
        return result if result else None
    
    def capNhatTrangThaiQuaHan(self):
        ngay_hien_tai = datetime.now().strftime("%d-%m-%Y")
        # Kiểm tra xem có sách nào quá hạn không
        co_cap_nhat = False
    
        for mt in self.MuonTraList:
            if not mt.status:  # Chỉ xét sách chưa trả
                tien_phat_cu = mt.fine
                self.tinhTienPhat(mt, ngay_hien_tai)
                if mt.fine != tien_phat_cu:
                    co_cap_nhat = True
    
        if co_cap_nhat:
            self.saveData()
            print("✅ Đã cập nhật trạng thái quá hạn.")
    
        return co_cap_nhat
    
    def timKiemMuonTra(self, tu_khoa):
        if not tu_khoa or not tu_khoa.strip():
            return []
    
        tu_khoa_lower = tu_khoa.lower().strip()
        ket_qua = []
    
        for mt in self.MuonTraList:
            if (tu_khoa_lower in mt.customerID.lower() or
                tu_khoa_lower in mt.customerName.lower() or
                tu_khoa_lower in mt.bookID.lower() or
                tu_khoa_lower in mt.bookName.lower()):
                ket_qua.append(mt)
    
        return ket_qua
    
    def thongKeMuonTra(self):
        tong = len(self.MuonTraList)
        dang_muon = len([mt for mt in self.MuonTraList if not mt.status])
        da_tra = len([mt for mt in self.MuonTraList if mt.status])
        qua_han = len([mt for mt in self.MuonTraList if not mt.status and mt.fine > 0])
        tong_phat = sum(mt.fine for mt in self.MuonTraList)
    
        return {
            "tong_muon": tong,
            "dang_muon": dang_muon,
            "da_tra": da_tra,
            "qua_han": qua_han,
            "tong_phat": tong_phat
        }
    
    def getSachQuaHan(self):
        self.capNhatTrangThaiQuaHan()
        return [mt for mt in self.MuonTraList if not mt.status and mt.fine > 0]