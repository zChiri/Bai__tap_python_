class SanPham:
    def ___init__(self):
        self.TenHang =""
        self.DonGia = 0
        self.soluong = 0
    
    def nhap(self, stt):
        print(f"\n--- Nhập sản phẩm {stt} ---")
        self.TenHang = input("Tên sản phẩm:")
        self.DonGia = int(input("Đơn giá:"))
        self.soluong = int(input("Số lượng:"))
        
    def ThanhTien(self):
        return self.DonGia * self.soluong
    
    def Xuat(self):
        tien = self.ThanhTien()
        if tien >= 100000:
            DanhGia = "Sản phẩm có giá trị cao"
        elif tien >= 50000:
            DanhGia = "Sản phẩm có giá trị trung bình"
        else: 
            DanhGia = "Sản phẩm có giá trị thấp"
        
        print(
            f"{self.TenHang} | "
            f"{self.DonGia} x {self.soluong} = "
            f"{tien} | {DanhGia}"
        )

class DonHang:
    def __init__(self):
        self.TenKhachHang =""
        self.SLSanPham = 0
        self.DanhSach = []
        
        self.TongTien = 0
        self.GiamGia = 0
        self.TienGiam = 0
        self.TienThanhToan = 0
        
    def Nhap(self):
        print("\n========== NHẬP ĐƠN HÀNG ==========")
        self.TenKhachHang = input("Tên khách hàng:")
        
        # KT số lượng sp
        while self.SLSanPham <= 0:
            self.SLSanPham = int(input("Nhập SL Sản Phẩm:"))
            if self.SLSanPham <= 0:
                print("Số lượng sản phẩm phải > 0")
        
        for i in range(self.SLSanPham):
            sp = SanPham()
            sp.nhap(i + 1)
            self.DanhSach.append(sp)
        
    def TinhTong(self):
        self.TongTien = 0
        for sp in self.DanhSach:
            self.TongTien += sp.ThanhTien()

    def TinhGiamGia(self):
        if self.TongTien >= 500000:
            self.GiamGia = 10
        elif self.TongTien >= 300000:
            self.GiamGia = 5
        else:
            self.GiamGia = 0
        self.TienGiam = self.TongTien * self.GiamGia / 100
        self.TienThanhToan = self.TongTien - self.TienGiam
        
    def CheckGift(self):
        if self.TongTien >= 300000 and self.SLSanPham >= 3:
            return "Được tặng quà"
        else:
            return "Không được tặng quà"
    def  xuat(self):
        print(("\n======== HÓA ĐƠN ========"))
        print("Khách hàng: ",self.TenKhachHang)
        print("\n --- Danh sách sản phẩm ---")
        for sp in self.DanhSach:
            sp.Xuat()
        print("Tổng tiền: ",self.TongTien)
        print("Giảm giá: ",self.GiamGia,"%")
        print("Tiền được giảm: ",self.TienGiam)
        print("Tiền thanh toán: ",self.TienThanhToan)
        print("Quà tặng: ",self.CheckGift())
    
# =====================
# Chương trình chính 

while True:
    don_hang = DonHang()
    don_hang.Nhap()
    don_hang.TinhTong()
    don_hang.TinhGiamGia()
    don_hang.xuat()
    
    while True:
        choose = input("\nBạn có muốn tiếp tục tạo đơn hàng không? (y/n):").lower()
        if choose == "y":
            break
        elif choose == "n":
            print("Chương trình kết thúc!")
            exit()
        else:
            print("Lựa chọn không hợp lệ!\nVui lòng nhập y hoặc n")
