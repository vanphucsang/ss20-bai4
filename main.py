import logging

# Thiết lập hệ thống Logging
logging.basicConfig(
    filename='roster_app.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Dữ liệu ban đầu
roster = [
    {"player_id": "P01", "name": "Faker", "role": "Mid Lane", "salary": 5000.0, "status": "Active"},
    {"player_id": "P02", "name": "Oner", "role": "Jungle", "salary": 3500.0, "status": "Active"},
    {"player_id": "P03", "name": "Ruler", "role": "ADC", "salary": 6000.0, "status": "Benched"}
]

def calculate_actual_pay(player_dict):
    """Hàm phụ trợ tính lương thực nhận dựa trên trạng thái thi đấu."""
    salary = player_dict["salary"]
    status = player_dict.get("status", "Unknown")
    if status == "Benched":
        return salary * 0.5
    return salary

def display_roster(roster_list):
    """Chức năng 1: Xem đội hình thi đấu hiện tại."""
    logger.info("Coach viewed the team roster.")
    
    if not roster_list:
        print("Đội hình hiện đang trống.")
        return

    print("\n--- ĐỘI HÌNH RIKKEI ESPORTS ---")
    print(f"{'ID':<8} | {'Tên tuyển thủ':<20} | {'Vị trí':<15} | {'Lương':<12} | {'Trạng thái'}")
    print("-" * 80)
    
    for player in roster_list:
        try:
            p_id = player["player_id"]
            status = player.get("status", "Unknown") # Bẫy lỗi 1: Default 'Unknown' nếu thiếu key
            
            # Xử lý hiển thị tên kèm nhãn DỰ BỊ
            name_display = f"{player['name']} [DỰ BỊ]" if status == "Benched" else player['name']
            
            print(f"{p_id:<8} | {name_display:<20} | {player['role']:<15} | {player['salary']:<12,.1f} | {status}")
        except KeyError as e:
            logger.error(f"Missing key while displaying roster: {e}")
            print(f"Lỗi: Thiếu dữ liệu cấu trúc cho tuyển thủ (Key: {e})")

def sign_player(roster_list):
    """Chức năng 2: Chiêu mộ tuyển thủ mới."""
    print("\n--- CHIÊU MỘ TUYỂN THỦ MỚI ---")
    p_id = input("Nhập mã tuyển thủ: ").strip().upper()
    
    # Kiểm tra trùng ID
    if any(p.get("player_id") == p_id for p in roster_list):
        print(f"\nLỗi: Mã tuyển thủ {p_id} đã tồn tại.")
        logger.warning(f"Failed to sign player - Duplicate player ID {p_id}")
        return

    name = input("Nhập tên tuyển thủ: ").strip()
    role = input("Nhập vị trí thi đấu: ").strip()

    # Nhập lương an toàn (Bẫy Exception)
    while True:
        try:
            salary_input = input("Nhập mức lương hàng tháng: ")
            salary = float(salary_input)
            if salary <= 0:
                print("\nLương phải là số dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("\nLương phải là số. Vui lòng nhập lại.")
            logger.warning("Failed to sign player - Invalid salary input")

    new_player = {
        "player_id": p_id,
        "name": name,
        "role": role,
        "salary": salary,
        "status": "Active"
    }
    roster_list.append(new_player)
    print(f"\nThành công: Đã chiêu mộ tuyển thủ {name}.")
    logger.info(f"Signed new player {name} with salary {salary}")

def update_player_status(roster_list):
    """Chức năng 3: Cập nhật lương & Trạng thái thi đấu."""
    print("\n--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")
    p_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()
    
    target_player = next((p for p in roster_list if p.get("player_id") == p_id), None)
    
    if not target_player:
        print(f"\nKhông tìm thấy tuyển thủ mang mã {p_id}.")
        logger.warning(f"Failed to update player - Player ID {p_id} not found")
        return

    try:
        print(f"\nTuyển thủ: {target_player['name']}")
        print(f"Vị trí: {target_player['role']}")
        print(f"Lương hiện tại: {target_player['salary']:,.1f}")
        print(f"Trạng thái hiện tại: {target_player['status']}")

        print("\nBạn muốn cập nhật:")
        print("1. Cập nhật lương")
        print("2. Cập nhật trạng thái thi đấu")
        choice = input("Chọn chức năng cập nhật (1-2): ").strip()

        if choice == '1':
            while True:
                try:
                    new_salary = float(input("Nhập mức lương mới: "))
                    if new_salary <= 0:
                        print("\nLương phải là số dương. Vui lòng nhập lại.")
                        continue
                    old_salary = target_player['salary']
                    target_player['salary'] = new_salary
                    print(f"\nThành công: Đã cập nhật lương cho tuyển thủ {p_id}.")
                    logger.info(f"Updated player {p_id} salary from {old_salary} to {new_salary}")
                    break
                except ValueError:
                    print("\nLương phải là số. Vui lòng nhập lại.")
        
        elif choice == '2':
            print("\nChọn trạng thái mới:")
            print("1. Active")
            print("2. Benched")
            status_choice = input("Nhập lựa chọn trạng thái (1-2): ").strip()
            
            if status_choice == '1':
                target_player['status'] = "Active"
            elif status_choice == '2':
                target_player['status'] = "Benched"
            else:
                print("Lựa chọn không hợp lệ.")
                return
            
            print(f"\nThành công: Đã cập nhật trạng thái cho tuyển thủ {p_id}.")
            logger.info(f"Updated player {p_id} status to {target_player['status']}")
        else:
            print("Lựa chọn không hợp lệ.")

    except KeyError as e:
        logger.error(f"Data missing for player {p_id}: {e}")
        print("Lỗi: Dữ liệu tuyển thủ bị hỏng.")

def generate_payroll_report(roster_list):
    """Chức năng 4: Báo cáo quỹ lương hàng tháng."""
    print("\n--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")
    
    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        logger.info("Generated monthly payroll report. Total: 0.0")
        return

    print(f"{'ID':<8} | {'Tên tuyển thủ':<15} | {'Trạng thái':<10} | {'Lương gốc':<12} | {'Lương thực nhận'}")
    print("-" * 80)
    
    total_payroll = 0.0
    has_error = False
    
    for player in roster_list:
        try:
            p_id = player["player_id"]
            name = player["name"]
            status = player.get("status", "Unknown")
            base_salary = player["salary"] # Dễ dính KeyError nếu thiếu lương
            
            actual_pay = calculate_actual_pay(player)
            total_payroll += actual_pay
            
            print(f"{p_id:<8} | {name:<15} | {status:<10} | {base_salary:<12,.1f} | {actual_pay:,.1f}")
            
        except KeyError as e:
            logger.error(f"Missing key while generating payroll report: {e}")
            has_error = True
            break
            
    if has_error:
        print("-" * 80)
        print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")
        total_payroll = 0.0

    print("-" * 80)
    print(f"Tổng quỹ lương hàng tháng: {total_payroll:,.1f}")
    
    if not has_error:
        logger.info(f"Generated monthly payroll report. Total: {total_payroll}")

def main():
    while True:
        print("\n===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====")
        print("1. Xem đội hình thi đấu hiện tại")
        print("2. Chiêu mộ tuyển thủ mới")
        print("3. Cập nhật lương & Trạng thái thi đấu")
        print("4. Báo cáo quỹ lương hàng tháng")
        print("5. Thoát hệ thống")
        print("==================================================")
        
        choice = input("Chọn chức năng (1-5): ").strip()

        match choice:
            case '1':
                display_roster(roster)
            case '2':
                sign_player(roster)
            case '3':
                update_player_status(roster)
            case '4':
                generate_payroll_report(roster)
            case '5':
                print("Hệ thống đang tắt... Chào tạm biệt huấn luyện viên!")
                logger.info("System closed safely.")
                break
            case _:
                print("Vui lòng chọn tính năng hợp lệ từ 1-5.")

if __name__ == "__main__":
    main()