class ChuyenXe:
    def __init__(self, ten, quang_duong, gio, loai_xe, mua):
        self.ten = ten
        self.quang_duong = quang_duong
        self.gio = gio
        self.loai_xe = loai_xe
        self.mua = mua
        
    def kiem_tra(self):
        if self.ten == "":
            return False
        
        if self.quang_duong <= 0:
            return False
        
        if self.gio < 0 or self.gio > 23:
            return False
        
        if self.loai_xe != "4 cho" and self.loai_xe != "7 cho":
            return False
        
        return True
    
    def tinh_cuoc(self):
        #Đơn giá
        if self.loai_xe == "4 cho":
            gia = 12000
        else:
            gia = 15000
            
        #Cước cơ bản
        cuoc_co_ban = self.quang_duong * gia
        
        # Phụ thu giờ cao điểm
        phu_thu_gio_cd = 0
        if (6 <= self.gio <= 8 ) or (17 <= self.gio <= 19):
            phu_thu_gio_cd = cuoc_co_ban * 0.10
        
        # Phụ thu trời mưa
        phu_thu_mua = 0
        if self.mua == "co":
            phu_thu_mua = self.quang_duong * 5000
            
        tong_cuoc = cuoc_co_ban + phu_thu_gio_cd + phu_thu_mua
        
        return cuoc_co_ban,phu_thu_gio_cd,phu_thu_mua,tong_cuoc
    
    def phan_loai(self):
        if self.quang_duong < 5:
            return "Chuyến ngắn"
        
        elif self.quang_duong <= 15:
            return "Chuyến trung bình"
        else:
            return "Chuyến dài"
        
    def uu_tien(self):
        cao_diem = (6 <= self.gio <= 8) or (17 <= self.gio <= 19)
        if cao_diem:
            if self.phan_loai() == "Chuyến dài":
                return "Ưu tiên tài xế nhiều kinh nghiệm"
            else:
                return "Ưu tiên tài xế gần nhất"
        else:
            return "Bình thường"
        
    def muc_cuoc(self, tong_cuoc):
        return "Cao" if tong_cuoc > 150000 else "Thấp"
    
ten = input("Nhập tên khách hàng: ")
quang_duong = float(input("Nhập quãng đường (km): "))
gio = int(input("Nhập giờ xuất phát (0- 23): "))
loai_xe = input("Nhập loại xe (4 cho/ 7 cho): ")
mua = input("Trời có mưa không? (co/khong): ")

xe = ChuyenXe(ten, quang_duong, gio, loai_xe, mua)

if not xe.kiem_tra():
    print("Dữ liệu không hợp lệ!")
else:
    cuoc_co_ban, phu_thu_gio, phu_thu_mua, tong_cuoc = xe.tinh_cuoc()
    
    print("\n ---Kết Quả---")
    print("Khách hàng:",xe.ten)
    print("Quãng đường:",xe.quang_duong,"km")
    print("Loại xe:",xe.loai_xe)
    
    print("Cước cơ bản:", cuoc_co_ban,"VND")
    print("Phụ thu giờ cao điểm:",phu_thu_gio,"VND")
    print("Phụ thu trời mưa:", phu_thu_mua, "VND")
    print("Tổng cước:", tong_cuoc,"VND")
    
    print("Loai chuyến đi:",xe.phan_loai())
    print("Ưu tiên điều xe:",xe.uu_tien())
    print("Mức cước:",xe.muc_cuoc(tong_cuoc))
    