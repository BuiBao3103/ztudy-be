from django.apps import AppConfig
import threading
import time
import os
import sys


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'
    _task_scheduled = False

    def ready(self):
        # Bỏ qua nếu đang chạy lệnh quản lý khác
        if len(sys.argv) > 1 and sys.argv[1] not in ['runserver', 'gunicorn']:
            return
            
        # Nếu là Django development server, chỉ chạy trong process con
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return
            
        # Cách tiếp cận đơn giản: Đăng ký tín hiệu request_started
        # Chỉ chạy cập nhật sau khi nhận được request đầu tiên
        from django.core.signals import request_started
        
        # Sử dụng biến toàn cục để kiểm soát việc chỉ chạy 1 lần
        # Ngay cả khi có nhiều workers
        self.register_update_signal()
    
    def register_update_signal(self):
        """Đăng ký tín hiệu để chạy cập nhật sau request đầu tiên"""
        from django.core.signals import request_started
        from django.dispatch import receiver
        
        # Dùng biến class để theo dõi việc chạy cập nhật một lần duy nhất
        has_run = False
        
        @receiver(request_started)
        def run_update_once(sender, **kwargs):
            nonlocal has_run
            if has_run:
                return
                
            # Đánh dấu đã chạy để tránh chạy nhiều lần
            has_run = True
            
            # Tạo thread riêng để chạy cập nhật bảng xếp hạng
            thread = threading.Thread(target=self.delayed_update)
            thread.daemon = True
            thread.start()
            
    def delayed_update(self):
        """Chạy cập nhật bảng xếp hạng sau một độ trễ ngắn"""
        # Chờ để đảm bảo ứng dụng đã khởi động hoàn toàn
        time.sleep(3)
        
        try:
            from .leaderboard_tasks import update_leaderboards
            print("=== Running initial leaderboard update ===")
            update_leaderboards()
            print("=== Leaderboard update completed successfully ===")
        except Exception as e:
            print(f"=== Error in leaderboard update: {e} ===")
