#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 @sayeed_accesstoken_bot - Complete Telegram Bot
All features from mm.py converted to Telegram Bot
Developer: @sayeed_khxn
"""

import telebot
import requests
import os
import sys
import json
import time
import re
import urllib.parse
import base64
import hashlib
import urllib3
import logging
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# ── Disable SSL warnings ──────────────────────────────────────────
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ── Dependency checks ──────────────────────────────────────────────
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print("[✗] Missing: pycryptodome\nInstall: pip install pycryptodome")
    sys.exit(1)

try:
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import message_factory as _message_factory
except ImportError:
    print("[✗] Missing: protobuf\nInstall: pip install protobuf")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════
#  BOT CONFIG
# ═══════════════════════════════════════════════════════════════════
BOT_TOKEN = "8980229663:AAEobZ5GsAANDnG3f4jQprUN5QxU7SaLavM"
OWNER_ID = "@sayeed_khxn"
OWNER_CHAT_ID = 8029040127  # Your chat ID

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

# ═══════════════════════════════════════════════════════════════════
#  EMBEDDED PROTOBUF DEFINITIONS
# ═══════════════════════════════════════════════════════════════════
_FREEFIRE_PROTO_SERIALIZED = (
    b'\n\x0e\x46reeFire.proto"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t'
    b'\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t'
    b'\x12\x1b\n\x13orign_platform_type\x18c \x01(\t"]\n\x10\x42lacklistInfoRes'
    b'\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason'
    b'\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\r'
    b'"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08'
    b'\x12\x16\n\x0equeue_position\x18\x02 \x01(\r'
    b'\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\r'
    b'\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08'
    b'"\xa0\x03\n\x08LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04'
    b'\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t'
    b'\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t'
    b'\x12\x19\n\x11new_active_region\x18\x06 \x01(\t'
    b'\x12\x19\n\x11recommend_regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t'
    b'\x12\x0b\n\x03ttl\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t'
    b'\x12\x16\n\x0e\x65mulator_score\x18\x0b \x01(\r'
    b'\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.BlacklistInfoRes'
    b'\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueueInfo'
    b'\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18\x0f \x01(\r'
    b'\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city\x18\x11 \x01(\t'
    b'\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t'
    b'*\xa8\x01\n\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00'
    b'\x12\x1b\n\x17\x42\x41N_REASON_IN_GAME_AUTO\x10\x01'
    b'\x12\x15\n\x11\x42\x41N_REASON_REFUND\x10\x02'
    b'\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03'
    b'\x12\x16\n\x12\x42\x41N_REASON_SKINMOD\x10\x04'
    b'\x12 \n\x1b\x42\x41N_REASON_IN_GAME_AUTO_NEW\x10\xf6\x07'
    b'b\x06proto3'
)

_pool = _descriptor_pool.Default()
_pool.AddSerializedFile(_FREEFIRE_PROTO_SERIALIZED)
LoginReq = _message_factory.GetMessageClass(_pool.FindMessageTypeByName("LoginReq"))
LoginRes = _message_factory.GetMessageClass(_pool.FindMessageTypeByName("LoginRes"))

# ═══════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV  = b'6oyZDr22E3ychjM%'

PLATFORM_MAP = {
    3: "Facebook", 4: "Guest", 5: "VK",
    6: "Huawei", 8: "Google", 11: "X (Twitter)", 13: "AppleId",
}

PLATFORM_NAMES = {
    1: "Garena", 3: "Facebook", 4: "Guest", 5: "VK",
    6: "Huawei", 7: "Apple", 8: "Google", 10: "GameCenter / Line",
    11: "X (Twitter)", 13: "Apple ID", 28: "Line", 35: "TikTok",
}

# ═══════════════════════════════════════════════════════════════════
#  USER SESSIONS
# ═══════════════════════════════════════════════════════════════════
user_sessions = {}

def get_session(uid):
    if uid not in user_sessions:
        user_sessions[uid] = {"step": "idle", "data": {}}
    return user_sessions[uid]

def reset_session(uid):
    if uid in user_sessions:
        user_sessions[uid] = {"step": "idle", "data": {}}
    else:
        user_sessions[uid] = {"step": "idle", "data": {}}

# ═══════════════════════════════════════════════════════════════════
#  CRYPTO HELPERS
# ═══════════════════════════════════════════════════════════════════
def aes_encrypt(data):
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        return cipher.encrypt(pad(data, 16))
    except Exception as e:
        logger.error(f"AES Encrypt error: {e}")
        return None

def aes_decrypt(data):
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        return unpad(cipher.decrypt(data), 16)
    except Exception as e:
        logger.error(f"AES Decrypt error: {e}")
        return None

# ═══════════════════════════════════════════════════════════════════
#  PROTOBUF HELPERS
# ═══════════════════════════════════════════════════════════════════
def _read_varint(data, offset):
    result = 0
    shift = 0
    while offset < len(data):
        byte = data[offset]
        offset += 1
        result |= (byte & 0x7f) << shift
        if not (byte & 0x80):
            break
        shift += 7
    return result, offset

def _parse_history_record(data):
    record = {}
    offset = 0
    while offset < len(data):
        tag, offset = _read_varint(data, offset)
        wire_type = tag & 0x07
        field_num = tag >> 3
        if wire_type == 0:
            val, offset = _read_varint(data, offset)
            if field_num == 1: record['ts'] = val
            elif field_num == 2: record['ram'] = val
        elif wire_type == 2:
            length, offset = _read_varint(data, offset)
            val = data[offset:offset + length]
            offset += length
            if field_num == 3: 
                try:
                    record['dev'] = val.decode('utf-8', errors='ignore')
                except:
                    record['dev'] = str(val)
            elif field_num == 4:
                try:
                    record['arch'] = val.decode('utf-8', errors='ignore')
                except:
                    record['arch'] = str(val)
        else:
            break
    return record

def parse_login_history(data):
    records = []
    offset = 0
    while offset < len(data):
        tag, offset = _read_varint(data, offset)
        wire_type = tag & 0x07
        field_num = tag >> 3
        if wire_type == 0:
            _read_varint(data, offset)
        elif wire_type == 2:
            length, offset = _read_varint(data, offset)
            val = data[offset:offset + length]
            offset += length
            if field_num == 1:
                records.append(_parse_history_record(val))
        else:
            break
    return records

def build_login_req(token, open_id, platform_type):
    msg = LoginReq()
    msg.open_id = open_id
    msg.open_id_type = str(platform_type)
    msg.login_token = token
    msg.orign_platform_type = str(platform_type)
    encrypted = aes_encrypt(msg.SerializeToString())
    if encrypted is None:
        return None
    return encrypted

# ═══════════════════════════════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════════════════════════════
def fmt_seconds(s):
    try:
        s = int(s)
        d, h = divmod(s, 86400)
        h, m = divmod(h, 3600)
        m, sec = divmod(m, 60)
        return f"{d}d {h}h {m}m {sec}s"
    except:
        return f"{s}s"

def main_menu_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton("🔍 Cʜᴇᴄᴋ Bɪɴᴅ Iɴꜰᴏ"),
        KeyboardButton("📧 Bɪɴᴅ Eᴍᴀɪʟ"),
        KeyboardButton("❌ Uɴʙɪɴᴅ Eᴍᴀɪʟ"),
        KeyboardButton("🔄 Cʜᴀɴɢᴇ Bɪɴᴅ Eᴍᴀɪʟ"),
        KeyboardButton("🚫 Cᴀɴᴄᴇʟ Bɪɴᴅ"),
        KeyboardButton("🔑 Eᴀᴛ → Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ"),
        KeyboardButton("🗑️ Rᴇᴠᴏᴋᴇ Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ"),
        KeyboardButton("📜 Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ"),
        KeyboardButton("🔗 Cʜᴇᴄᴋ Bᴏᴜɴᴅ Aᴄᴄᴏᴜɴᴛꜱ"),
        KeyboardButton("👤 Oᴡɴᴇʀ Dᴇᴛᴀɪʟꜱ"),
        KeyboardButton("🔄 Rᴇꜱᴇᴛ Sᴇꜱꜱɪᴏɴ"),
    ]
    markup.add(*buttons)
    return markup

def cancel_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("❌ Cᴀɴᴄᴇʟ"))
    return markup

# ═══════════════════════════════════════════════════════════════════
#  CORE API FUNCTIONS (from mm.py)
# ═══════════════════════════════════════════════════════════════════

def get_player_info(access_token):
    try:
        url = f"https://api-otrss.garena.com/support/callback/?access_token={access_token}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(r.url).query)
        return {
            "uid": qs.get("account_id", ["Unknown"])[0],
            "nickname": urllib.parse.unquote(qs.get("nickname", ["Unknown"])[0]),
            "region": qs.get("region", ["Unknown"])[0],
            "success": True
        }
    except Exception as e:
        logger.error(f"get_player_info error: {e}")
        return {"success": False, "error": str(e)}

def get_bind_info(access_token):
    try:
        url = "https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
        params = {'app_id': "100067", 'access_token': access_token}
        headers = {
            'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
        }
        r = requests.get(url, params=params, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return {"success": True, "data": data}
        return {"success": False, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        logger.error(f"get_bind_info error: {e}")
        return {"success": False, "error": str(e)}

def extract_eat(text):
    try:
        text = text.strip()
        if text.startswith("http"):
            parsed = urllib.parse.urlparse(text)
            params = urllib.parse.parse_qs(parsed.query)
            if "eat" in params:
                return params["eat"][0]
        match = re.search(r'eat=([a-f0-9]+)', text)
        if match:
            return match.group(1)
        match = re.search(r'[a-f0-9]{100,}', text)
        if match:
            return match.group(0)
        return None
    except Exception as e:
        logger.error(f"extract_eat error: {e}")
        return None

def eat_to_access(eat_token):
    try:
        url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
        parsed = urllib.parse.urlparse(r.url)
        params = urllib.parse.parse_qs(parsed.query)
        access_token = params.get("access_token", [None])[0]
        account_id = params.get("account_id", ["Unknown"])[0]
        nickname = urllib.parse.unquote(params.get("nickname", ["Unknown"])[0])
        region = params.get("region", ["Unknown"])[0]
        if access_token:
            return {"success": True, "access_token": access_token, "account_id": account_id, "nickname": nickname, "region": region}
        return {"success": False, "error": "Access token not found"}
    except Exception as e:
        logger.error(f"eat_to_access error: {e}")
        return {"success": False, "error": str(e)}

def send_otp(access_token, email):
    try:
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:send_otp",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"email": email, "locale": "en_PK", "region": "PK",
                  "app_id": "100067", "access_token": access_token},
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"send_otp error: {e}")
        return {"success": False, "error": str(e)}

def verify_otp(access_token, email, otp):
    try:
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:verify_otp",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"app_id": "100067", "access_token": access_token, "email": email,
                  "code": otp, "otp": otp, "type": "1"},
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"verify_otp error: {e}")
        return {"success": False, "error": str(e)}

def verify_identity(access_token, email, otp=None, sec_code=None):
    try:
        payload = {"email": email, "app_id": "100067", "access_token": access_token}
        if otp:
            payload["otp"] = otp
        if sec_code:
            payload["secondary_password"] = hashlib.sha256(sec_code.encode()).hexdigest()
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:verify_identity",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data=payload,
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"verify_identity error: {e}")
        return {"success": False, "error": str(e)}

def create_bind_request(access_token, email, verifier_token, sec_code):
    try:
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:create_bind_request",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"email": email, "app_id": "100067",
                  "access_token": access_token, "verifier_token": verifier_token,
                  "secondary_password": sec_code},
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"create_bind_request error: {e}")
        return {"success": False, "error": str(e)}

def create_rebind_request(access_token, identity_token, email, verifier_token):
    try:
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:create_rebind_request",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"identity_token": identity_token, "email": email,
                  "app_id": "100067", "verifier_token": verifier_token,
                  "access_token": access_token},
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"create_rebind_request error: {e}")
        return {"success": False, "error": str(e)}

def create_unbind_request(access_token, identity_token):
    try:
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:create_unbind_request",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"app_id": "100067", "access_token": access_token,
                  "identity_token": identity_token},
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"create_unbind_request error: {e}")
        return {"success": False, "error": str(e)}

def cancel_bind_request(access_token):
    try:
        r = requests.post(
            "https://100067.connect.garena.com/game/account_security/bind:cancel_request",
            headers={
                "User-Agent": "GarenaMSDK/4.0.30",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            data={"app_id": "100067", "access_token": access_token},
            timeout=15
        )
        data = r.json()
        return {"success": data.get("result") == 0, "data": data}
    except Exception as e:
        logger.error(f"cancel_bind_request error: {e}")
        return {"success": False, "error": str(e)}

def revoke_token(access_token):
    try:
        refresh_token = "1380dcb63ab3a077dc05bdf0b25ba4497c403a5b4eae96d7203010eafa6c83a8"
        logout_url = f"https://100067.connect.garena.com/oauth/logout?access_token={access_token}&refresh_token={refresh_token}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(logout_url, headers=headers, timeout=15)
        return {"success": r.status_code == 200 and "error" not in r.text}
    except Exception as e:
        logger.error(f"revoke_token error: {e}")
        return {"success": False, "error": str(e)}

def get_platform_info(access_token):
    try:
        r = requests.get(
            "https://100067.connect.garena.com/bind/app/platform/info/get",
            params={"access_token": access_token},
            headers={
                "User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            },
            timeout=10
        )
        if r.status_code == 200:
            return {"success": True, "data": r.json()}
        return {"success": False, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        logger.error(f"get_platform_info error: {e}")
        return {"success": False, "error": str(e)}

def get_login_history_data(token):
    try:
        jwt_token = None
        open_id = None

        if token.startswith("ey") and "." in token:
            jwt_token = token
        else:
            try:
                r = requests.get(
                    f"https://100067.connect.garena.com/oauth/token/inspect?token={token}",
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=5,
                ).json()
                open_id = r.get("open_id")
            except:
                pass

            if not open_id:
                try:
                    r = requests.get(
                        "https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/",
                        headers={"access-token": token, "user-agent": "Mozilla/5.0"},
                        verify=False, timeout=5,
                    ).json()
                    uid = r.get("uid")
                    if uid:
                        r2 = requests.post(
                            "https://topup.pk/api/auth/player_id_login",
                            json={"app_id": 100067, "login_id": str(uid)},
                            verify=False, timeout=5,
                        ).json()
                        open_id = r2.get("open_id")
                except:
                    pass

            if not open_id:
                return {"success": False, "error": "Failed to extract Open ID"}

            platforms = [8, 3, 4, 6]
            for ptype in platforms:
                payload = build_login_req(token, open_id, ptype)
                if payload is None:
                    continue
                try:
                    r = requests.post(
                        "https://loginbp.ggpolarbear.com/MajorLogin",
                        headers={
                            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
                            "Connection": "Keep-Alive",
                            "Accept-Encoding": "gzip",
                            "Content-Type": "application/octet-stream",
                            "Expect": "100-continue",
                            "X-GA": "v1 1",
                            "X-Unity-Version": "2018.4.11f1",
                            "ReleaseVersion": "OB52",
                        },
                        data=payload, timeout=10, verify=False,
                    )
                    if r.status_code == 200:
                        res = LoginRes()
                        try:
                            res.ParseFromString(aes_decrypt(r.content))
                        except:
                            res.ParseFromString(r.content)
                        if res.token:
                            jwt_token = res.token
                            break
                except:
                    continue

        if not jwt_token:
            return {"success": False, "error": "Failed to get JWT token"}

        player_info = {}
        try:
            b64 = jwt_token.split('.')[1]
            b64 += "=" * ((4 - len(b64) % 4) % 4)
            decoded = json.loads(base64.urlsafe_b64decode(b64).decode())
            player_info = {
                "name": urllib.parse.unquote(decoded.get("nickname", "Unknown")),
                "uid": decoded.get("account_id", "Unknown"),
                "region": decoded.get("lock_region", "Unknown"),
                "platform": PLATFORM_MAP.get(decoded.get("external_type", 0), "Unknown"),
            }
        except:
            pass

        try:
            history_headers = {
                "Expect": "100-continue",
                "Authorization": f"Bearer {jwt_token}",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB52",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
                "Host": "client.ind.freefiremobile.com",
                "Connection": "close",
            }
            r = requests.post(
                "https://client.ind.freefiremobile.com/GetLoginHistory",
                headers=history_headers,
                data=aes_encrypt(b""),
                timeout=15, verify=False,
            )
            if r.status_code != 200:
                return {"success": False, "error": f"HTTP {r.status_code}", "player": player_info}

            try:
                decrypted = aes_decrypt(r.content)
            except:
                decrypted = r.content

            records = parse_login_history(decrypted)
            return {"success": True, "records": records, "player": player_info}
        except Exception as e:
            return {"success": False, "error": str(e), "player": player_info}
    except Exception as e:
        logger.error(f"get_login_history_data error: {e}")
        return {"success": False, "error": str(e)}

# ═══════════════════════════════════════════════════════════════════
#  QUICK CONVERT
# ═══════════════════════════════════════════════════════════════════
def quick_convert(message, text):
    uid = message.chat.id
    eat = extract_eat(text)
    if not eat:
        bot.send_message(uid, "❌ <b>EAT token nahi mila!</b> Sahi format mein bhejo.")
        return

    status = bot.send_message(uid, "⏳ <b>Converting...</b>")
    result = eat_to_access(eat)
    
    try:
        bot.delete_message(uid, status.message_id)
    except:
        pass

    if result["success"]:
        text_msg = f"""<b>✅ EAT → ACCESS TOKEN SUCCESS!</b>

<b>🔑 Access Token:</b>
<code>{result['access_token']}</code>

<b>👤 Account Details:</b>
• <b>ID:</b> <code>{result['account_id']}</code>
• <b>Name:</b> <code>{result['nickname']}</code>
• <b>Region:</b> <code>{result['region']}</code>

⏰ Token valid ~8 hours"""
        bot.send_message(uid, text_msg, reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ <b>Conversion Failed!</b>\n\nError: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())

# ═══════════════════════════════════════════════════════════════════
#  BOT HANDLERS
# ═══════════════════════════════════════════════════════════════════

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.chat.id
    reset_session(uid)
    welcome = f"""<b>╔════════════════════════════════╗
║      🤖 @Sayeedbind_bot      ║
╚════════════════════════════════╝</b>

👋 Wᴇʟᴄᴏᴍᴇ <b>{message.from_user.first_name}</b>!

<b>🔰 Fᴇᴀᴛᴜʀᴇꜱ (ꜰʀᴏᴍ Bɪɴᴅ Iɴꜰᴏ)</b>
━━━━━━━━━━━━━━━━━━━━━━━
• 🔍 Cʜᴇᴄᴋ Bɪɴᴅ Iɴꜰᴏ
• 📧 Bɪɴᴅ Eᴍᴀɪʟ
• ❌ Uɴʙɪɴᴅ Eᴍᴀɪʟ
• 🔄 Cʜᴀɴɢᴇ Bɪɴᴅ Eᴍᴀɪʟ
• 🚫 Cᴀɴᴄᴇʟ Bɪɴᴅ Rᴇǫᴜᴇꜱᴛ
• 🔑 Eᴀᴛ → Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ
• 🗑️ Rᴇᴠᴏᴋᴇ Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ
• 📜 Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ
• 🔗 Cʜᴇᴄᴋ Bᴏᴜɴᴅ Aᴄᴄᴏᴜɴᴛꜱ

<b>⚡ Qᴜɪᴄᴋ Cᴏᴍᴍᴀɴᴅ:</b>
• <code>/Tᴏᴋᴇɴ &lt;Eᴀᴛ&gt;</code> — Dɪʀᴇᴄᴛ Cᴏɴᴠᴇʀᴛ

<b>👤 Dᴇᴠʟᴏᴘᴇʀ:</b> {OWNER_ID}
<b>📢 Cʜᴀɴɴᴇʟ:</b> @apissayeed

<i>Sᴇʟᴇᴄᴛ Aɴ Oᴘᴛɪᴏɴ Bᴇʟᴏᴡ 👇</i>"""
    bot.send_message(uid, welcome, reply_markup=main_menu_markup())

@bot.message_handler(commands=['token'])
def token_command(message):
    uid = message.chat.id
    text = message.text.replace('/token', '').strip()
    if not text:
        bot.send_message(uid, "❌ <b>Usage:</b>\n<code>/token &lt;EAT_TOKEN_OR_URL&gt;</code>")
        return
    quick_convert(message, text)

@bot.message_handler(func=lambda m: m.text == "❌ Cᴀɴᴄᴇʟ")
def cancel_handler(message):
    uid = message.chat.id
    reset_session(uid)
    bot.send_message(uid, "❌ Cᴀɴᴄᴇʟʟᴇᴅ! Sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ:", reply_markup=main_menu_markup())

@bot.message_handler(func=lambda m: m.text == "🔄 Rᴇꜱᴇᴛ Sᴇꜱꜱɪᴏɴ")
def reset_handler(message):
    uid = message.chat.id
    reset_session(uid)
    bot.send_message(uid, "🔄 Sᴇꜱꜱɪᴏɴ ʀᴇꜱᴇᴛ! Sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ:", reply_markup=main_menu_markup())

# ═══════════════════════════════════════════════════════════════════
#  🔍 Cʜᴇᴄᴋ Bɪɴᴅ Iɴꜰᴏ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "🔍 Cʜᴇᴄᴋ Bɪɴᴅ Iɴꜰᴏ")
def check_bind_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "check_bind_token"
    bot.send_message(uid, "🔍 <b>Cʜᴇᴄᴋ Bɪɴᴅ Iɴꜰᴏ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "check_bind_token")
def check_bind_process(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    msg = bot.send_message(uid, "⏳ Fetching bind information...")
    player = get_player_info(token)
    bind = get_bind_info(token)

    text = "<b>🔍 BIND INFORMATION</b>\n\n"
    if player.get("success"):
        text += f"<b>👤 Player:</b>\n• UID: <code>{player['uid']}</code>\n• Nick: <b>{player['nickname']}</b>\n• Region: <code>{player['region']}</code>\n\n"
    if bind.get("success"):
        data = bind["data"]
        email = data.get("email", "")
        email_to_be = data.get("email_to_be", "")
        countdown = data.get("request_exec_countdown", 0)
        text += f"<b>📧 Bind Status:</b>\n• Current: <code>{email or 'None'}</code>\n• Pending: <code>{email_to_be or 'None'}</code>\n"
        if email_to_be:
            text += f"• Countdown: <code>{fmt_seconds(countdown)}</code>\n"
    else:
        text += f"❌ Bind info fetch failed\n"

    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass
    
    bot.send_message(uid, text, reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  📧 Bɪɴᴅ Eᴍᴀɪʟ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "📧 Bɪɴᴅ Eᴍᴀɪʟ")
def bind_email_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "bind_email_token"
    bot.send_message(uid, "📧 <b>Bɪɴᴅ Eᴍᴀɪʟ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "bind_email_token")
def bind_email_token(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    session = get_session(uid)
    session["data"]["token"] = token
    session["step"] = "bind_email_email"
    bot.send_message(uid, "📧 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Eᴍᴀɪʟ</b> Tᴏ Bɪɴᴅ:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "bind_email_email")
def bind_email_email(message):
    uid = message.chat.id
    email = message.text.strip()
    if email == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    session = get_session(uid)
    token = session["data"]["token"]
    msg = bot.send_message(uid, f"⏳ Sending OTP to <code>{email}</code>...")
    result = send_otp(token, email)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        bot.send_message(uid, f"✅ OTP sent to <code>{email}</code>!\n\n📩 Enter the OTP:", reply_markup=cancel_markup())
        session["data"]["email"] = email
        session["step"] = "bind_email_otp"
    else:
        bot.send_message(uid, f"❌ Failed to send OTP: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
        reset_session(uid)

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "bind_email_otp")
def bind_email_otp(message):
    uid = message.chat.id
    otp = message.text.strip()
    if otp == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    session = get_session(uid)
    token = session["data"]["token"]
    email = session["data"]["email"]
    msg = bot.send_message(uid, "⏳ Verifying OTP...")
    result = verify_otp(token, email, otp)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        verifier = result["data"].get("verifier_token", "")
        if verifier:
            session["data"]["verifier"] = verifier
            bot.send_message(uid, "✅ OTP verified!\n\n🔐 Set a <b>6-digit Security Code</b>:", reply_markup=cancel_markup())
            session["step"] = "bind_email_sec"
        else:
            bot.send_message(uid, "❌ No verifier token received!", reply_markup=main_menu_markup())
            reset_session(uid)
    else:
        bot.send_message(uid, f"❌ OTP verification failed!\nError: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
        reset_session(uid)

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "bind_email_sec")
def bind_email_sec(message):
    uid = message.chat.id
    sec = message.text.strip()
    if sec == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    if len(sec) != 6 or not sec.isdigit():
        bot.send_message(uid, "⚠️ Please enter exactly 6 digits!", reply_markup=cancel_markup())
        return

    session = get_session(uid)
    token = session["data"]["token"]
    email = session["data"]["email"]
    verifier = session["data"]["verifier"]
    msg = bot.send_message(uid, "⏳ Creating bind request...")
    result = create_bind_request(token, email, verifier, sec)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        bot.send_message(uid, f"✅ <b>Email Bound Successfully!</b>\n\n📧 Email: <code>{email}</code>\n🔐 Security Code: <code>{sec}</code>", reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ Bind failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  ❌ Uɴʙɪɴᴅ Eᴍᴀɪʟ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "❌ Uɴʙɪɴᴅ Eᴍᴀɪʟ")
def unbind_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "unbind_token"
    bot.send_message(uid, "❌ <b>Uɴʙɪɴᴅ Eᴍᴀɪʟ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "unbind_token")
def unbind_token(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    session = get_session(uid)
    session["data"]["token"] = token

    # Get current email
    bind = get_bind_info(token)
    email = ""
    if bind.get("success"):
        email = bind["data"].get("email", "")

    if not email:
        bot.send_message(uid, "❌ No bound email found! Cannot unbind.", reply_markup=main_menu_markup())
        reset_session(uid)
        return

    session["data"]["email"] = email

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📧 Via OTP"),
        KeyboardButton("🔐 Via Security Code"),
        KeyboardButton("❌ Cᴀɴᴄᴇʟ")
    )
    bot.send_message(uid, f"📧 Current Email: <code>{email}</code>\n\n<b>Choose verification method:</b>", reply_markup=markup)
    session["step"] = "unbind_method"

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "unbind_method")
def unbind_method(message):
    uid = message.chat.id
    method = message.text.strip()
    session = get_session(uid)

    if method == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    token = session["data"]["token"]
    email = session["data"]["email"]

    if method == "📧 Via OTP":
        msg = bot.send_message(uid, f"⏳ Sending OTP to <code>{email}</code>...")
        result = send_otp(token, email)
        try:
            bot.delete_message(uid, msg.message_id)
        except:
            pass

        if result["success"]:
            bot.send_message(uid, f"✅ OTP sent!\n\n📩 Enter the OTP:", reply_markup=cancel_markup())
            session["data"]["method"] = "otp"
            session["step"] = "unbind_verify"
        else:
            bot.send_message(uid, f"❌ Failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
            reset_session(uid)

    elif method == "🔐 Via Security Code":
        bot.send_message(uid, "🔐 Enter your <b>6-digit Security Code</b>:", reply_markup=cancel_markup())
        session["data"]["method"] = "sec"
        session["step"] = "unbind_verify"
    else:
        bot.send_message(uid, "⚠️ Invalid option!", reply_markup=main_menu_markup())
        reset_session(uid)

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "unbind_verify")
def unbind_verify(message):
    uid = message.chat.id
    code = message.text.strip()
    session = get_session(uid)

    if code == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    token = session["data"]["token"]
    email = session["data"]["email"]
    method = session["data"]["method"]

    msg = bot.send_message(uid, "⏳ Verifying identity...")

    if method == "otp":
        result = verify_identity(token, email, otp=code)
    else:
        result = verify_identity(token, email, sec_code=code)

    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        identity_token = result["data"].get("identity_token", "")
        if identity_token:
            msg2 = bot.send_message(uid, "⏳ Creating unbind request...")
            result2 = create_unbind_request(token, identity_token)
            try:
                bot.delete_message(uid, msg2.message_id)
            except:
                pass

            if result2["success"]:
                bot.send_message(uid, f"✅ <b>Email Unbound Successfully!</b>\n\n📧 Email: <code>{email}</code> has been removed.", reply_markup=main_menu_markup())
            else:
                bot.send_message(uid, f"❌ Unbind failed: {result2.get('error', 'Unknown')}", reply_markup=main_menu_markup())
        else:
            bot.send_message(uid, "❌ Identity verification failed!", reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ Verification failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  🔄 Cʜᴀɴɢᴇ Bɪɴᴅ Eᴍᴀɪʟ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "🔄 Cʜᴀɴɢᴇ Bɪɴᴅ Eᴍᴀɪʟ")
def change_bind_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "change_token"
    bot.send_message(uid, "🔄 <b>Cʜᴀɴɢᴇ Bɪɴᴅ Eᴍᴀɪʟ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "change_token")
def change_token(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    session = get_session(uid)
    session["data"]["token"] = token

    bind = get_bind_info(token)
    email = ""
    if bind.get("success"):
        email = bind["data"].get("email", "")

    if not email:
        bot.send_message(uid, "❌ No bound email found! Cannot change.", reply_markup=main_menu_markup())
        reset_session(uid)
        return

    session["data"]["old_email"] = email

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("📧 Via OTP"),
        KeyboardButton("🔐 Via Security Code"),
        KeyboardButton("❌ Cᴀɴᴄᴇʟ")
    )
    bot.send_message(uid, f"📧 Current Email: <code>{email}</code>\n\n<b>Choose verification method:</b>", reply_markup=markup)
    session["step"] = "change_method"

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "change_method")
def change_method(message):
    uid = message.chat.id
    method = message.text.strip()
    session = get_session(uid)

    if method == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    token = session["data"]["token"]
    old_email = session["data"]["old_email"]

    if method == "📧 Via OTP":
        msg = bot.send_message(uid, f"⏳ Sending OTP to <code>{old_email}</code>...")
        result = send_otp(token, old_email)
        try:
            bot.delete_message(uid, msg.message_id)
        except:
            pass

        if result["success"]:
            bot.send_message(uid, f"✅ OTP sent!\n\n📩 Enter the OTP from <code>{old_email}</code>:", reply_markup=cancel_markup())
            session["data"]["method"] = "otp"
            session["step"] = "change_old_verify"
        else:
            bot.send_message(uid, f"❌ Failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
            reset_session(uid)

    elif method == "🔐 Via Security Code":
        bot.send_message(uid, "🔐 Enter your <b>6-digit Security Code</b>:", reply_markup=cancel_markup())
        session["data"]["method"] = "sec"
        session["step"] = "change_old_verify"
    else:
        bot.send_message(uid, "⚠️ Invalid option!", reply_markup=main_menu_markup())
        reset_session(uid)

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "change_old_verify")
def change_old_verify(message):
    uid = message.chat.id
    code = message.text.strip()
    session = get_session(uid)

    if code == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    token = session["data"]["token"]
    old_email = session["data"]["old_email"]
    method = session["data"]["method"]

    msg = bot.send_message(uid, "⏳ Verifying old email identity...")

    if method == "otp":
        result = verify_identity(token, old_email, otp=code)
    else:
        result = verify_identity(token, old_email, sec_code=code)

    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        identity_token = result["data"].get("identity_token", "")
        if identity_token:
            session["data"]["identity_token"] = identity_token
            bot.send_message(uid, "✅ Identity verified!\n\n📧 Enter the <b>NEW Email</b>:", reply_markup=cancel_markup())
            session["step"] = "change_new_email"
        else:
            bot.send_message(uid, "❌ No identity token received!", reply_markup=main_menu_markup())
            reset_session(uid)
    else:
        bot.send_message(uid, f"❌ Verification failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
        reset_session(uid)

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "change_new_email")
def change_new_email(message):
    uid = message.chat.id
    new_email = message.text.strip()
    session = get_session(uid)

    if new_email == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    token = session["data"]["token"]

    msg = bot.send_message(uid, f"⏳ Sending OTP to <code>{new_email}</code>...")
    result = send_otp(token, new_email)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        bot.send_message(uid, f"✅ OTP sent to <code>{new_email}</code>!\n\n📩 Enter the OTP:", reply_markup=cancel_markup())
        session["data"]["new_email"] = new_email
        session["step"] = "change_new_otp"
    else:
        bot.send_message(uid, f"❌ Failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
        reset_session(uid)

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "change_new_otp")
def change_new_otp(message):
    uid = message.chat.id
    otp = message.text.strip()
    session = get_session(uid)

    if otp == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    token = session["data"]["token"]
    new_email = session["data"]["new_email"]

    msg = bot.send_message(uid, "⏳ Verifying new email OTP...")
    result = verify_otp(token, new_email, otp)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        verifier = result["data"].get("verifier_token", "")
        if verifier:
            msg2 = bot.send_message(uid, "⏳ Creating rebind request...")
            result2 = create_rebind_request(
                token,
                session["data"]["identity_token"],
                new_email,
                verifier
            )
            try:
                bot.delete_message(uid, msg2.message_id)
            except:
                pass

            if result2["success"]:
                bot.send_message(uid, f"✅ <b>Email Changed Successfully!</b>\n\n📧 Old: <code>{session['data']['old_email']}</code>\n📧 New: <code>{new_email}</code>", reply_markup=main_menu_markup())
            else:
                bot.send_message(uid, f"❌ Rebind failed: {result2.get('error', 'Unknown')}", reply_markup=main_menu_markup())
        else:
            bot.send_message(uid, "❌ No verifier token received!", reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ OTP verification failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  🚫 Cᴀɴᴄᴇʟ Bɪɴᴅ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "🚫 Cᴀɴᴄᴇʟ Bɪɴᴅ")
def cancel_bind_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "cancel_token"
    bot.send_message(uid, "🚫 <b>Cᴀɴᴄᴇʟ Bɪɴᴅ Rᴇǫᴜᴇꜱᴛ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "cancel_token")
def cancel_bind_process(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    msg = bot.send_message(uid, "⏳ Cancelling bind request...")
    result = cancel_bind_request(token)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        bot.send_message(uid, "✅ <b>Bind Request Cancelled!</b>", reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ Cᴀɴᴄᴇʟ failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  🔑 Eᴀᴛ → Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "🔑 Eᴀᴛ → Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ")
def eat_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "eat_input"
    bot.send_message(uid, "🔑 <b>Eᴀᴛ → Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Eᴀᴛ Tᴏᴋᴇɴ</b> or <b>Uʀʟ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "eat_input")
def eat_process(message):
    uid = message.chat.id
    inp = message.text.strip()
    if inp == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return
    quick_convert(message, inp)
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  🗑️ Rᴇᴠᴏᴋᴇ Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "🗑️ Rᴇᴠᴏᴋᴇ Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ")
def revoke_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "revoke_token"
    bot.send_message(uid, "🗑️ <b>Rᴇᴠᴏᴋᴇ Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b> Tᴏ Rᴇᴠᴏᴋᴇ:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "revoke_token")
def revoke_process(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    msg = bot.send_message(uid, "⏳ Checking token and revoking...")

    player = get_player_info(token)
    if not player.get("success"):
        try:
            bot.delete_message(uid, msg.message_id)
        except:
            pass
        bot.send_message(uid, "❌ Token is already invalid or expired!", reply_markup=main_menu_markup())
        reset_session(uid)
        return

    result = revoke_token(token)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        text = f"""<b>✅ TOKEN REVOKED</b>

👤 <b>Nickname:</b> <code>{player['nickname']}</code>
🆔 <b>Account ID:</b> <code>{player['uid']}</code>
🌍 <b>Region:</b> <code>{player['region']}</code>

🔒 <b>Status:</b> Logged out & Revoked"""
        bot.send_message(uid, text, reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ Revoke failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  📜 Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "📜 Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ")
def history_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "history_token"
    bot.send_message(uid, "📜 <b>Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b> or <b>JWT Token</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "history_token")
def history_process(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    msg = bot.send_message(uid, "⏳ Fetching Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ...\n(This may take 10-15 seconds)")
    result = get_login_history_data(token)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result.get("player"):
        p = result["player"]
        bot.send_message(uid, f"""<b>👤 Player Info</b>
• Name: <code>{p.get('name', 'Unknown')}</code>
• UID: <code>{p.get('uid', 'Unknown')}</code>
• Platform: <code>{p.get('platform', 'Unknown')}</code>
• Region: <code>{p.get('region', 'Unknown')}</code>""")

    if result["success"]:
        records = result["records"]
        if not records:
            bot.send_message(uid, "📭 No Lᴏɢɪɴ Hɪꜱᴛᴏʀʏ records found.", reply_markup=main_menu_markup())
        else:
            for i, rec in enumerate(records[:10], 1):
                ts = rec.get('ts', 0)
                try:
                    date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date_str = "Invalid"
                dev = rec.get('dev', 'Unknown')
                arch = rec.get('arch', 'Unknown')
                ram = rec.get('ram', 0)

                text = f"""<b>📜 Record #{i}</b>
• Timestamp: <code>{ts}</code>
• Last Login: <code>{date_str}</code>
• Device: <code>{dev}</code>
• Architecture: <code>{arch}</code>
• RAM: <code>{ram} MB</code>"""
                bot.send_message(uid, text)

            if len(records) > 10:
                bot.send_message(uid, f"📊 <i>...and {len(records) - 10} more records</i>")

        bot.send_message(uid, "✅ Done!", reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ Failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  🔗 Cʜᴇᴄᴋ Bᴏᴜɴᴅ Aᴄᴄᴏᴜɴᴛꜱ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "🔗 Cʜᴇᴄᴋ Bᴏᴜɴᴅ Aᴄᴄᴏᴜɴᴛꜱ")
def bound_start(message):
    uid = message.chat.id
    session = get_session(uid)
    session["step"] = "bound_token"
    bot.send_message(uid, "🔗 <b>Cʜᴇᴄᴋ Bᴏᴜɴᴅ Aᴄᴄᴏᴜɴᴛꜱ</b>\n\n📋 Sᴇɴᴅ Mᴇ Tʜᴇ <b>Aᴄᴄᴇꜱꜱ Tᴏᴋᴇɴ</b>:", reply_markup=cancel_markup())

@bot.message_handler(func=lambda m: get_session(m.chat.id).get("step") == "bound_token")
def bound_process(message):
    uid = message.chat.id
    token = message.text.strip()
    if token == "❌ Cᴀɴᴄᴇʟ":
        reset_session(uid)
        bot.send_message(uid, "❌ Cancelled.", reply_markup=main_menu_markup())
        return

    msg = bot.send_message(uid, "⏳ Fetching platform bind data...")
    result = get_platform_info(token)
    try:
        bot.delete_message(uid, msg.message_id)
    except:
        pass

    if result["success"]:
        data = result["data"]
        bounded = data.get("bounded_accounts", [])
        available = data.get("available_platforms", [])

        text = "<b>🔗 PLATFORM BIND INFORMATION</b>\n\n"
        text += "<b>✅ Bound Accounts:</b>\n"
        if not bounded:
            text += "  • No third-party platforms bound.\n"
        else:
            for pid in bounded:
                name = PLATFORM_NAMES.get(pid, f"Unknown ({pid})")
                text += f"  • {name}\n"

        text += "\n<b>📋 Available Platforms:</b>\n"
        if not available:
            text += "  • None\n"
        else:
            for pid in available:
                name = PLATFORM_NAMES.get(pid, f"Unknown ({pid})")
                text += f"  • {name}\n"

        bot.send_message(uid, text, reply_markup=main_menu_markup())
    else:
        bot.send_message(uid, f"❌ Failed: {result.get('error', 'Unknown')}", reply_markup=main_menu_markup())
    reset_session(uid)

# ═══════════════════════════════════════════════════════════════════
#  👤 Oᴡɴᴇʀ Dᴇᴛᴀɪʟꜱ
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text == "👤 Oᴡɴᴇʀ Dᴇᴛᴀɪʟꜱ")
def owner_details(message):
    text = f"""<b>👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ</b>

├─ 🕷️ Nᴀᴍᴇ : Sᴀʏᴇᴇᴅ Kʜᴀɴ
├─ 📩 Tᴇʟᴇɢʀᴀᴍ : @sayeed_khxn
├─ 📢 Cʜᴀɴɴᴇʟ : @apissayeed
├─ 🛡️ Vᴇʀꜱɪᴏɴ : v2.0 • Pʀᴇᴍɪᴜᴍ Eᴅɪᴛɪᴏɴ
└─ 💬 Sᴜᴘᴘᴏʀᴛ : @sayeedapis"""
    bot.send_message(message.chat.id, text, reply_markup=main_menu_markup())

# ═══════════════════════════════════════════════════════════════════
#  FALLBACK HANDLER
# ═══════════════════════════════════════════════════════════════════
@bot.message_handler(func=lambda m: True)
def fallback(message):
    text = message.text.strip()
    if text.startswith('/'):
        bot.send_message(message.chat.id, "⚠️ Invalid command! Use /start", reply_markup=main_menu_markup())
        return
    eat = extract_eat(text)
    if eat:
        quick_convert(message, text)
    else:
        bot.send_message(message.chat.id, "⚠️ Please select an option from the menu below:", reply_markup=main_menu_markup())

# ═══════════════════════════════════════════════════════════════════
#  START BOT
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 @sayeedbind_bot - Telegram Bot Started!")
    print("✅ All features from mm.py converted!")
    print(f"👤 Owner: {OWNER_ID}")
    print("=" * 50)
    
    try:
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0, timeout=60)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        time.sleep(5)
        os.execv(sys.executable, ['python'] + sys.argv)