
notification = " "*4 + "Hệ thống quản lý bãi đỗ xe" + " "*4
gach = "-"*len(notification)

print(gach)
print(notification)
print(gach)

# Khai báo giờ 
from datetime import datetime
danh_sach_xe = []

while True:
    choice = input("""
1. Check-in (Đăng ký xe vào)
2. Báo cáo tồn kho (Hiển thị danh sách)
3. Tìm kiếm xe (Theo biển số)
4. Check--out (Xử lý xe ra & tính phí)
5. Thoát chương trình
Nhập lựa chọn của bạn: """)
    
    if choice == "1":
        bien_so = input("Nhập biển số:")
        if not bien_so:
            print("Không được để trống!")
            continue
        
        trung = False
        for xe in danh_sach_xe:
            if xe["bien_so"] == bien_so:
                trung = True
                break
        if trung:
            print("Error! Biển số xe đã tồn tại.")
            continue
                 
        loai_xe = int(input("Nhập loại xe (Xe máy=1, ô tô=2):"))
        if not loai_xe:
            print("Không được để trống!")
            continue
        
        if len(danh_sach_xe) == 0:
            id_xe = 1
        else:
            id_xe = danh_sach_xe[-1]["id_xe"]+1
        
        # Lấy giờ
        time = datetime.now()
        
        xe = {"id_xe": id_xe,
              "bien_so": bien_so,
              "loai_xe": loai_xe,
              "time": time}
        danh_sach_xe.append(xe) 
        print("Thêm thành công!")
        
    elif choice == "2":
        if len(danh_sach_xe) == 0:
            print("[Thông báo: Bãi xe hiện đang trống!]")
        else:
            header = f"{' ID':<10}|{' Biển số':<15}|{' Loại xe':<10}|{' Time':<10}"
            print("-"*len(header))
            print(header)
            print("-"*len(header))
            for xe in danh_sach_xe:
                loai_xe = "Xe máy" if xe["loai_xe"] == 1 else "Ô tô"
                print(f"{xe['id_xe']:<10}|{xe['bien_so']:<15}|{loai_xe:<10}|{xe['time'].strftime('%H:%M:%S'):<10}")
                
    elif choice == "3":
        find = input("Nhập biển số xe cần tìm: ")
        tim_thay = False
        for xe in danh_sach_xe:
            if xe["bien_so"] == find:
                tim_thay = True
                loai_xe = "Xe máy" if xe["loai_xe"] == 1 else "Ô tô"
                print("\n===== THÔNG TIN XE =====")
                print(f"ID xe       : {xe['id_xe']}")
                print(f"Biển số     : {xe['bien_so']}")
                print(f"Loại xe     : {loai_xe}")
                print(f"Giờ vào     : {xe['time'].strftime('%d/%m/%Y %H:%M:%S')}")
                print("========================")
                break
        if not tim_thay:
            print(f"[Lỗi] không tìm thấy biển số {bien_so} trong hệ thống!")
        
    elif choice == "4":
        bien_so = input("Nhập biển số xe cần ra: ")
        
        tim_thay = False
        
        for xe in danh_sach_xe:
            if xe["bien_so"] == bien_so:
                tim_thay = True
                gio_ra = datetime.now()

                # Tính số giờ
                tg_gui = gio_ra - xe["time"]
                
                so_gio = tg_gui.total_seconds()/3600
                
                # Tính phí
                if xe["loai_xe"] == "1":
                    phi = so_gio * 5000
                else:
                    phi = so_gio * 10_000
                
                print(f"Giờ vào: {xe['time'].strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"Giờ ra: {gio_ra.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"Số giờ gửi: {so_gio:.2f} giờ")
                print(f"Tổng phí: {phi:.2f} VND")
                danh_sach_xe.remove(xe)
                
                print(f"[Thành công] Đã xóa xe ID: {xe['id_xe']} thành công!")
        if not tim_thay:      
            print(f"[Error] Không tìm thấy biển số {bien_so} trong hệ thống!") 
    
    elif choice == "5":  
        break