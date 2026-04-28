

from urllib import request

from django.http import JsonResponse
from httpcore import request
from streamlit import json

from BankProject.BankProject.settings import connectDB, sendResponse, disconnectDB


def dt_login(request):
    if request.method != "POST":
        data = [{"function": "dt_login"}]
        return JsonResponse(sendResponse("dt_login", 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_login"}]
        return JsonResponse(sendResponse("dt_login", 1002, data))

    required_fields = ["action", "email", "passwordhash"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_login"}]
        return JsonResponse(sendResponse("dt_login", 1003, data))

    conn = None
    cur = None
    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            SELECT id, title, content, mood, created_at
            FROM appback_gratitudeentry
            ORDER BY id ASC
        """
        cur.execute(sql)
        rows = cur.fetchall()

        data = []
        for row in rows:
            data.append({
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "mood": row[3],
                "created_at": row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None
            })

        return JsonResponse(sendResponse("get_entries", 1000, data))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse("get_entries", 1006, data))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)
