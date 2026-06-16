import os

import requests

DBOSS_API_URL = os.environ.get("DBOSS_API_URL", "https://dboss-backend.onrender.com")


class AuthError(Exception):
    pass


def register(username: str, email: str, password: str) -> dict:
    url = f"{DBOSS_API_URL}/register"
    try:
        resp = requests.post(
            url,
            json={"username": username, "email": email, "password": password},
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        raise AuthError(
            f"Backend'e bağlanılamadı. Sunucu erişilebilir mi? ({DBOSS_API_URL})"
        )
    if resp.status_code == 400:
        detail = _extract_detail(resp)
        raise AuthError(f"Kayıt başarısız: {detail}")
    if not resp.ok:
        raise AuthError(f"Kayıt başarısız (HTTP {resp.status_code}): {resp.text[:200]}")
    return resp.json()


def login(username: str, password: str) -> str:
    url = f"{DBOSS_API_URL}/login"
    try:
        resp = requests.post(
            url,
            json={"username": username, "password": password},
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        raise AuthError(
            f"Backend'e bağlanılamadı. Sunucu erişilebilir mi? ({DBOSS_API_URL})"
        )
    if resp.status_code == 401:
        raise AuthError("Kullanıcı adı veya şifre hatalı.")
    if not resp.ok:
        raise AuthError(f"Giriş başarısız (HTTP {resp.status_code}): {resp.text[:200]}")
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise AuthError("Sunucu geçerli bir token döndürmedi.")
    return token


def get_me(token: str) -> dict:
    url = f"{DBOSS_API_URL}/me"
    try:
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        raise AuthError(
            f"Backend'e bağlanılamadı. Sunucu erişilebilir mi? ({DBOSS_API_URL})"
        )
    if resp.status_code == 401:
        raise AuthError("Oturum süresi dolmuş veya geçersiz token. Tekrar giriş yap.")
    if not resp.ok:
        raise AuthError(f"Kullanıcı bilgisi alınamadı (HTTP {resp.status_code}): {resp.text[:200]}")
    return resp.json()


def _extract_detail(resp: requests.Response) -> str:
    try:
        return resp.json().get("detail", resp.text[:200])
    except Exception:
        return resp.text[:200]
