gach = "="
tieu_de = " "*4 + "Quản Lý Kho Hàng" + " "*4
print(gach* len(tieu_de))
print(tieu_de)
print(gach* len(tieu_de))


def menu():
    print("""
1. Xem danh sách hàng tồn kho
2. Nhập thêm hàng hóa mới
3. Cập nhật số lượng tồn kho theo ID
4. Thoát chương trình
=====================================""")

def nhap_hang():
    while True:
        id = input("Nhập ID: ")
        if id == "":
            print("ID không được để trống!")
        else: 
            break
    
    while True:
        name = input("Nhập tên hàng hóa: ")
        if name == "":
            print("Tên hàng hóa không được để trống!")
        else: break
        
    while True:
        try:
            quanlity = int(input("Nhập số lượng: "))
            if quanlity <= 0:
                print("Số lượng phải > 0!")
            else: break
        except ValueError:
            print("Vui lòng nhập số nguyên!")
    
    item = {"id": id,
            "name": name,
            "quanlity": quanlity}
    
    return item

def nhap_kho():
    kho = []
    while True:
        try:
            n = int(input("Nhập số lượng hàng hóa ban đầu: "))
            if n < 0:
                print("Số lượng không được < 0!")
            else:
                break
        except ValueError:
            print("Vui lòng nhập số nguyên!")
            
    for i in range(n):
        print(f"\n --- Hàng hóa thứ {i+1} ---")
        item = nhap_hang()
        kho.append(item)
    
    return kho

def show_kho(kho):
    print("\n ======= DANH SÁCH HÀNG TỒN KHO =======")
    if len(kho) == 0:
        print("Kho hàng hiện đang trống!")
        return
    
    print(f"{'ID':<10}| {'Tên hàng':<20}| {'SL tồn':<15}")
    print("-"* 50)
    
    for item in kho:
        print(f"{item['id']:<10}|"
              f"{item['name']:<25}|"
              f"{item['quanlity']:<15}")
        
def them_hang(kho):
    print("\n====== NHẬP HÀNG =====")
    item = nhap_hang()
    kho.append(item)
    print("Thêm hàng thành công!")
    
def cap_nhat_hang_ton(kho):
    print("\n===== CẬP NHẬT SỐ LƯỢNG =====")
    id = input("Nhập mã hàng hóa cần sửa: ")
    for item in kho:
        if item['id'] == id:
            print(f"Tìm thấy hàng hóa: {item['name']}\n"
                  f"Số lượng hiện tại: {item['quanlity']}")
            
            while True:
                try:
                    quanlity = int(input("Nhập số lượng mới: "))
                    if quanlity <= 0:
                        print("Số lượng phải > 0!")
                    else: break
                except ValueError:
                    print("Vui lòng nhập số nguyên")
            item['quanlity'] = quanlity
            print("Cập nhật số lượng thành công!")
            return
    print(f"Không tìm thấy hàng hóa có mã [{id}] !")
    
def main():
    kho = nhap_kho()
    while True:
        menu()
        choice = input("Mời bạn chọn chức năng(1-4): ")
        if choice == "1":
            show_kho(kho)
        elif choice == "2":
            them_hang(kho)
        elif choice == "3":
            cap_nhat_hang_ton(kho)
        elif choice == "4":
            print("Cảm ơn bạn đã sử dụng phần nềm!")
            print("[Chương trình kết thúc]")
            break
        else: 
            print("Lựa chọn không hợp kệ!")    
            
main()
