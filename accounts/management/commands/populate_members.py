from django.core.management.base import BaseCommand
from accounts.models import Member

class Command(BaseCommand):
    help = '填充會員資料'

    def handle(self, *args, **kwargs):
        # 假設頭像圖片為 icons/avatar1.png 到 icons/avatar10.png
        avatars = [f"icons/avatar{i}.png" for i in range(1, 11)]
        members_data = [
            {"username": "member1", "avatar": avatars[0], "address": "台北市中正區忠孝東路一段100號"},
            {"username": "member2", "avatar": avatars[1], "address": "新北市板橋區文化路二段200號"},
            {"username": "member3", "avatar": avatars[2], "address": "台中市西區台灣大道三段300號"},
            {"username": "member4", "avatar": avatars[3], "address": "高雄市前鎮區中山二路400號"},
            {"username": "member5", "avatar": avatars[4], "address": "桃園市中壢區中大路500號"},
            {"username": "member6", "avatar": avatars[5], "address": "台南市東區中華東路一段600號"},
            {"username": "member7", "avatar": avatars[6], "address": "台北市信義區松仁路700號"},
            {"username": "member8", "avatar": avatars[7], "address": "新竹市東區光復路二段800號"},
            {"username": "member9", "avatar": avatars[8], "address": "彰化市中央路900號"},
            {"username": "member10", "avatar": avatars[9], "address": "宜蘭市中山路三段1000號"},
            {"username": "member11", "avatar": avatars[0], "address": "花蓮市國聯一路1100號"},
            {"username": "member12", "avatar": avatars[1], "address": "基隆市仁愛區愛三路1200號"},
        ]

        for data in members_data:
            Member.objects.get_or_create(
                username=data["username"],
                defaults={"avatar": data["avatar"], "address": data["address"]}
            )
        self.stdout.write(self.style.SUCCESS('成功填充 12 個會員資料'))