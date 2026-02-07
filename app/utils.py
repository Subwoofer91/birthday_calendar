from datetime import date, timedelta
from lunarcalendar import Converter, Solar, Lunar
import smtplib
from email.mime.text import MIMEText
import os
import requests

import requests
import uuid

# WeCom Webhook URL (Get from env or leave empty to be filled by user)
WECOM_WEBHOOK_URL = os.getenv("WECOM_WEBHOOK_URL", "")

def calculate_next_birthday(birthday_obj):
    today = date.today()
    birth_date = birthday_obj.date
    
    if birthday_obj.is_lunar:
        # Convert stored Gregorian birth date to Lunar to get the Lunar day/month
        solar_birth = Solar(birth_date.year, birth_date.month, birth_date.day)
        lunar_birth = Converter.Solar2Lunar(solar_birth)
        
        # Calculate next lunar birthday in current or next Gregorian year
        try:
            lunar_next = Lunar(today.year, lunar_birth.month, lunar_birth.day, lunar_birth.isleap)
            solar_next = Converter.Lunar2Solar(lunar_next)
            next_bday = date(solar_next.year, solar_next.month, solar_next.day)
        except:
             lunar_next = Lunar(today.year + 1, lunar_birth.month, lunar_birth.day, lunar_birth.isleap)
             solar_next = Converter.Lunar2Solar(lunar_next)
             next_bday = date(solar_next.year, solar_next.month, solar_next.day)

        if next_bday < today:
             lunar_next = Lunar(today.year + 1, lunar_birth.month, lunar_birth.day, lunar_birth.isleap)
             solar_next = Converter.Lunar2Solar(lunar_next)
             next_bday = date(solar_next.year, solar_next.month, solar_next.day)
             
        return next_bday

    else:
        # Gregorian
        try:
            next_bday = date(today.year, birth_date.month, birth_date.day)
        except ValueError:
            # Leap year born on Feb 29
            next_bday = date(today.year, 3, 1) 

        if next_bday < today:
            try:
                next_bday = date(today.year + 1, birth_date.month, birth_date.day)
            except ValueError:
                next_bday = date(today.year + 1, 3, 1)
        
        return next_bday

def send_notification(birthday_obj, days_left):
    if not WECOM_WEBHOOK_URL:
        print("WeCom Webhook URL not set. Skipping notification.")
        return

    calendar_type = "农历" if birthday_obj.is_lunar else "公历"
    note_content = birthday_obj.note if birthday_obj.note else "无"
    
    # Markdown content for WeCom
    content = f"""### 🎂 生日提醒 
> **{birthday_obj.name}** ({calendar_type}) 
> 还有 **{days_left}** 天过生日 
> <font color="comment">备注：{note_content}</font>"""
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    print(f"Sending WeCom notification to {WECOM_WEBHOOK_URL}: {content}")
    
    try:
        response = requests.post(WECOM_WEBHOOK_URL, json=payload)
        response.raise_for_status() # Raise error for bad status codes
        print(f"WeCom notification sent successfully. Response: {response.text}")
    except Exception as e:
        print(f"Failed to send WeCom notification: {e}")
