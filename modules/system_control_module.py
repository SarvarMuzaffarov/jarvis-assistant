"""
JARVIS - Tizim Boshqaruvi Moduli
Dasturlar, fayllar, ekran, ovoz, Wi-Fi, screenshot va boshqalar
"""

import os
import subprocess
import psutil
import pyautogui
import time
from datetime import datetime
from config import APP_PATHS, SCREENSHOT_DIR


class SystemControl:
    def __init__(self):
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        pyautogui.FAILSAFE = True
    
    # ==================== DASTURLAR ====================
    
    def open_app(self, app_name):
        app_name_lower = app_name.lower().strip()
        
        if app_name_lower in APP_PATHS:
            path = APP_PATHS[app_name_lower].replace("{user}", os.getlogin())
            if os.path.exists(path):
                subprocess.Popen(path)
                return f"✅ {app_name} ochildi."
        
        try:
            os.startfile(app_name_lower)
            return f"✅ {app_name} ochildi."
        except:
            pass
        
        try:
            subprocess.Popen(f"start {app_name_lower}", shell=True)
            return f"✅ {app_name} ochildi."
        except Exception as e:
            return f"❌ {app_name} ni ochib bo'lmadi: {e}"
    
    def close_app(self, app_name):
        app_name_lower = app_name.lower()
        closed = False
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if app_name_lower in proc.info['name'].lower():
                    proc.terminate()
                    closed = True
            except:
                continue
        return f"✅ {app_name} yopildi." if closed else f"❌ {app_name} topilmadi."
    
    def list_running_apps(self):
        apps = set()
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name']
                if name and not name.startswith('_'):
                    apps.add(name)
            except:
                continue
        return sorted(list(apps))
    
    # ==================== FAYLLAR ====================
    
    def search_file(self, filename, directory=None):
        if directory is None:
            directory = os.path.expanduser("~")
        results = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if filename.lower() in file.lower():
                    results.append(os.path.join(root, file))
                    if len(results) >= 10:
                        return results
        return results
    
    def open_file(self, filepath):
        try:
            os.startfile(filepath)
            return f"✅ Fayl ochildi: {filepath}"
        except Exception as e:
            return f"❌ Faylni ochib bo'lmadi: {e}"
    
    def create_file(self, filepath, content=""):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ Fayl yaratildi: {filepath}"
        except Exception as e:
            return f"❌ Fayl yaratib bo'lmadi: {e}"
    
    # ==================== EKRAN ====================
    
    def take_screenshot(self, region=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath
    
    def set_brightness(self, level):
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return f"✅ Yorqinlik {level}% ga o'rnatildi."
        except Exception as e:
            return f"❌ Yorqinlikni o'zgartirib bo'lmadi: {e}"
    
    # ==================== OVOZ ====================
    
    def set_volume(self, level):
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume_db = -65.25 * (1 - level / 100)
            volume.SetMasterVolumeLevel(volume_db, None)
            return f"✅ Ovoz balandligi {level}% ga o'rnatildi."
        except Exception as e:
            return f"❌ Ovozni o'zgartirib bo'lmadi: {e}"
    
    def mute_volume(self):
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            return "✅ Ovoz o'chirildi (mute)."
        except Exception as e:
            return f"❌ Xato: {e}"
    
    def unmute_volume(self):
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)
            return "✅ Ovoz yoqildi."
        except Exception as e:
            return f"❌ Xato: {e}"
    
    # ==================== TARMOQ ====================
    
    def toggle_wifi(self, enable=True):
        try:
            action = "enable" if enable else "disable"
            subprocess.run(f'netsh interface set interface "Wi-Fi" {action}', shell=True, capture_output=True)
            status = "yoqildi" if enable else "o'chirildi"
            return f"✅ Wi-Fi {status}."
        except Exception as e:
            return f"❌ Wi-Fi ni o'zgartirib bo'lmadi: {e}"
    
    # ==================== TIZIM ====================
    
    def lock_computer(self):
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        return "✅ Kompyuter bloklandi."
    
    def restart_computer(self, delay=30):
        subprocess.run(f"shutdown /r /t {delay}", shell=True)
        return f"⚠️ Kompyuter {delay} soniyadan keyin qayta yuklanadi."
    
    def shutdown_computer(self, delay=30):
        subprocess.run(f"shutdown /s /t {delay}", shell=True)
        return f"⚠️ Kompyuter {delay} soniyadan keyin o'chadi."
    
    def cancel_shutdown(self):
        subprocess.run("shutdown /a", shell=True)
        return "✅ O'chirish bekor qilindi."
    
    def get_system_info(self):
        import platform
        return {
            "os": platform.system() + " " + platform.release(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 1),
            "ram_used_percent": psutil.virtual_memory().percent,
            "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 1),
            "disk_used_percent": round(psutil.disk_usage('/').used / psutil.disk_usage('/').total * 100, 1),
            "battery": self._get_battery_info(),
            "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 1)
        }
    
    def _get_battery_info(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {"percent": battery.percent, "charging": battery.power_plugged}
        except:
            pass
        return None
