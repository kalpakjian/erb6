"""
create_users.py
Script to create multiple users with avatars and Hong Kong addresses for Gundam Store.
Run this script in Django shell: python manage.py shell < create_users.py
"""

from django.contrib.auth.models import User
from accounts.models import UserProfile
import random

# 假設頭像檔案位於 /static/icons，文件名列表
AVATARS = [
    'icons/avatar1.png',
    'icons/avatar2.png',
    'icons/avatar3.png',
    'icons/avatar4.png',
    'icons/avatar5.png',
]

# 香港地址生成資料
DISTRICTS = ['中西區', '灣仔區', '東區', '南區', '油尖旺區', '深水埗區', '九龍城區', '黃大仙區', '觀塘區']
ESTATES = ['嘉輝大廈', '怡景花園', '海濱苑', '麗都大樓', '寶馬山莊']
ROADS = ['皇后大道中', '軒尼詩道', '英皇道', '德輔道西', '彌敦道']

# 用戶資料
USERS = [
    {'username': 'user1', 'first_name': '陳偉明', 'email': 'user1@example.com'},
    {'username': 'user2', 'first_name': '李嘉欣', 'email': 'user2@example.com'},
    {'username': 'user3', 'first_name': '張志強', 'email': 'user3@example.com'},
    {'username': 'user4', 'first_name': '黃美玲', 'email': 'user4@example.com'},
    {'username': 'user5', 'first_name': '林子豪', 'email': 'user5@example.com'},
    {'username': 'user6', 'first_name': '吳曉雯', 'email': 'user6@example.com'},
    {'username': 'user7', 'first_name': '劉俊傑', 'email': 'user7@example.com'},
    {'username': 'user8', 'first_name': '何麗華', 'email': 'user8@example.com'},
    {'username': 'user9', 'first_name': '鄭家輝', 'email': 'user9@example.com'},
    {'username': 'user10', 'first_name': '馮詠詩', 'email': 'user10@example.com'},
    {'username': 'user11', 'first_name': '梁浩然', 'email': 'user11@example.com'},
    {'username': 'user12', 'first_name': '蔡靜怡', 'email': 'user12@example.com'},
    {'username': 'user13', 'first_name': '周啟明', 'email': 'user13@example.com'},
    {'username': 'user14', 'first_name': '馬曉晴', 'email': 'user14@example.com'},
    {'username': 'user15', 'first_name': '楊志遠', 'email': 'user15@example.com'},
]

def create_users():
    for user_data in USERS:
        try:
            # 檢查用戶是否已存在
            if User.objects.filter(username=user_data['username']).exists():
                print(f"用戶 {user_data['username']} 已存在，跳過。")
                continue
            
            # 創建用戶
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='1234',
                first_name=user_data['first_name']
            )
            
            # 隨機生成香港地址
            district = random.choice(DISTRICTS)
            estate = random.choice(ESTATES)
            road = random.choice(ROADS)
            building = f"第{random.randint(1, 10)}座 {random.choice(['A', 'B', 'C'])}單位"
            address = f"香港{district}{road}{estate}{building}"
            
            # 隨機選擇頭像
            avatar = random.choice(AVATARS)
            
            # 創建 UserProfile
            UserProfile.objects.create(
                user=user,
                address=address,
                avatar=avatar
            )
            
            print(f"已創建用戶 {user_data['username']}，地址：{address}，頭像：{avatar}")
            
        except Exception as e:
            print(f"創建用戶 {user_data['username']} 失敗：{str(e)}")

if __name__ == '__main__':
    print("開始創建用戶...")
    create_users()
    print("用戶創建完成！")
