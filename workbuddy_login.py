#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 WorkBuddy 短信验证码登录工具 (v2 · 插件接口版)
════════════════════════════════════════════════════════════════
输入手机号 → 自动发送验证码 → 输入收到的验证码 → 直接拿到 AT + RT

用法:
  python workbuddy_login.py                    # 交互式登录（推荐）
  python workbuddy_login.py 13800000000        # 指定手机号
  python workbuddy_login.py 13800000000 123456 # 指定手机号和验证码
  python workbuddy_login.py --verify           # 登录后用 RT 试刷新一次，验证可用性

输出格式（可直接用于 WORKBUDDY_REFRESH_TOKEN 环境变量）:
  手机号:AT:RT

说明:
  · 走官方插件登录接口 /v2/plugin/login/*，由服务端直接下发 accessToken / refreshToken，
    无需再解析 Keycloak 登录页表单，稳定可靠。
  · 仅依赖 requests。
"""
import sys, os, json, time, base64, datetime
import requests

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except Exception:
    pass

BASE = "https://www.workbuddy.cn"
SEND_SMS_URL = BASE + "/v2/plugin/login/send-sms"
LOGIN_URL = BASE + "/v2/plugin/login/token"
REFRESH_URL = "https://copilot.tencent.com/v2/plugin/auth/token/refresh"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/138.0.7204.251 Safari/537.36")


def _headers():
    return {"Content-Type": "application/json", "Accept": "application/json, text/plain, */*",
            "Origin": BASE, "Referer": BASE + "/", "User-Agent": UA}


def send_sms(phone):
    """发送短信验证码。返回 (ok, 提示信息)"""
    print("[2/5] 发送短信验证码到 %s ..." % phone)
    try:
        r = requests.post(SEND_SMS_URL, headers=_headers(), json={"phone": phone},
                          timeout=20, verify=False)
        d = r.json()
    except Exception as e:
        print("  ⚠️ 发送请求异常: %s" % str(e)[:80])
        return False, str(e)[:80]
    if d.get("code") == 0:
        exp = (d.get("data") or {}).get("expires_in", 300)
        print("  ✅ 验证码已发送 (有效期 %s 秒)" % exp)
        return True, ""
    msg = d.get("msg", "未知错误")
    print("  ❌ 发送失败: %s" % msg)
    low = str(msg).lower()
    if "keycloak spi" in low or "400" in low:
        print("  💡 手机号可能格式有误，或该号码暂不支持短信登录")
    elif "频繁" in str(msg) or "frequent" in low or "too many" in low:
        print("  💡 发送过于频繁，请稍后再试")
    return False, msg


def login(phone, sms_code):
    """用手机号+验证码登录，返回 dict 或 None"""
    print("[3/5] 提交登录...")
    try:
        r = requests.post(LOGIN_URL, headers=_headers(),
                          json={"login_method": "phone", "phone": phone, "sms_code": sms_code},
                          timeout=30, verify=False)
        d = r.json()
    except Exception as e:
        print("  ❌ 登录请求异常: %s" % str(e)[:80])
        return None
    if d.get("code") != 0:
        msg = d.get("msg", "未知错误")
        print("  ❌ 登录失败: %s" % msg)
        low = str(msg).lower()
        if "code" in low or "验证码" in str(msg) or "expire" in low:
            print("  💡 验证码可能已过期或输入有误，请重新发送后尽快输入")
        return None
    data = d.get("data") or {}
    at = data.get("accessToken") or data.get("access_token") or ""
    rt = data.get("refreshToken") or data.get("refresh_token") or ""
    if not at or not rt:
        print("  ❌ 响应缺少 accessToken / refreshToken: %s" % json.dumps(data, ensure_ascii=False)[:200])
        return None
    print("  ✅ 登录成功!")
    return {"phone": phone, "accessToken": at, "refreshToken": rt, "raw": data}


def _jwt(tok):
    try:
        pay = tok.split(".")[1]
        pay += "=" * (4 - len(pay) % 4)
        return json.loads(base64.urlsafe_b64decode(pay))
    except Exception:
        return {}


def verify_rt(rt):
    """用 RT 调一次刷新接口，验证凭据真的可用"""
    print("[5/5] 验证刷新令牌...")
    try:
        r = requests.post(REFRESH_URL, headers={"X-Refresh-Token": rt,
                                                "X-Auth-Refresh-Source": "plugin",
                                                "Content-Type": "application/json"},
                          json={}, timeout=20, verify=False)
        d = r.json()
        if d.get("code") == 0 and (d.get("data") or {}).get("accessToken"):
            print("  ✅ 刷新令牌可用（已成功换发新 AT）")
            return True
        print("  ⚠️ 刷新验证未通过: %s" % str(d.get("msg", ""))[:80])
    except Exception as e:
        print("  ⚠️ 刷新验证异常: %s" % str(e)[:80])
    return False


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║ 🔐 WorkBuddy 短信验证码登录工具 (插件接口版)   ║")
    print("║ 输入手机号 → 收验证码 → 获取 Token            ║")
    print("╚══════════════════════════════════════════════╝")

    args = [a for a in sys.argv[1:] if a != "--verify"]
    do_verify = "--verify" in sys.argv
    phone = args[0] if len(args) > 0 else ""
    sms_code = args[1] if len(args) > 1 else None

    if not phone:
        phone = input("📱 请输入手机号: ").strip()
    if not phone:
        print("❌ 手机号不能为空")
        return 1

    print("[1/5] 准备登录...")
    print("  ✅ 目标: %s" % BASE)

    if not sms_code:
        ok, _ = send_sms(phone)
        if not ok:
            return 1
        sms_code = input("  📱 请输入收到的验证码: ").strip()
        if not sms_code:
            print("  ❌ 验证码不能为空")
            return 1
    else:
        print("[2/5] 使用命令行提供的验证码")

    res = login(phone, sms_code)
    if not res:
        print("\n❌ 登录失败")
        return 1

    at, rt = res["accessToken"], res["refreshToken"]
    j = _jwt(at)
    exp = j.get("exp", 0)
    exp_str = datetime.datetime.fromtimestamp(exp).strftime("%Y-%m-%d %H:%M") if exp else "?"
    print("[4/5] 解析凭据...")
    print("  ✅ 身份: %s | AT 过期: %s" % (j.get("preferred_username", phone), exp_str))

    if do_verify:
        verify_rt(rt)
    else:
        print("[5/5] 完成!")

    env_line = "%s:%s:%s" % (phone, at, rt)
    print("\n" + "═" * 60)
    print("✅ 将下面的值追加到 WORKBUDDY_REFRESH_TOKEN 变量")
    print("═" * 60)
    print(env_line)
    print("═" * 60)

    result = {"phone": phone, "access_token": at, "refresh_token": rt,
              "env_line": env_line, "login_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    save_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wb_login_result.json")
    results = []
    if os.path.exists(save_file):
        try:
            results = json.load(open(save_file, encoding="utf-8"))
        except Exception:
            results = []
    results.append(result)
    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print("📁 结果已保存到: %s" % save_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
