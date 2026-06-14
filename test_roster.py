import unittest
# Import hàm tính lương từ file main (giả định file ở trên đặt tên là main.py)
from main import calculate_actual_pay

class TestPayrollLogic(unittest.TestCase):
    
    def test_actual_pay_active_player(self):
        """Test Case 1: Tuyển thủ Active -> Nhận 100% lương gốc"""
        player = {
            "player_id": "P01", 
            "name": "Faker", 
            "role": "Mid", 
            "salary": 5000.0, 
            "status": "Active"
        }
        # Kì vọng 5000.0 == 5000.0
        self.assertEqual(calculate_actual_pay(player), 5000.0)

    def test_actual_pay_benched_player(self):
        """Test Case 2: Tuyển thủ Benched -> Nhận 50% lương gốc"""
        player = {
            "player_id": "P03", 
            "name": "Ruler", 
            "role": "ADC", 
            "salary": 6000.0, 
            "status": "Benched"
        }
        # Kì vọng 6000.0 * 0.5 == 3000.0
        self.assertEqual(calculate_actual_pay(player), 3000.0)

if __name__ == '__main__':
    unittest.main()