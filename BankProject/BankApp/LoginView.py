from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_login(request):
    if request.method != "POST":
        data = [{"function": "dt_login"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_login"}]
        return JsonResponse(sendResponse(request, 1002, data))

    required_fields = ["action", "email", "passwordhash"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_login"}]
        return JsonResponse(sendResponse(request, 1003, data))
    action = jsons["action"]
    email = jsons["email"]
    passwordhash = jsons["passwordhash"]
    conn = None
    cur = None
    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            select  account_id, email, firstname, lastname, status, created_at from users
            where email = %s and passwordhash = %s
        """
        cur.execute(sql, (email, passwordhash))
        rows = cur.fetchall()
        if len(rows) != 1:
            data = []
            return JsonResponse(sendResponse(request, 1007, data, action))

        data = []
        for row in rows:
            data.append({
                "account_id": row[0],
                "email": row[1],
                "firstname": row[2],
                "lastname": row[3],
                "status": row[4],
                "created_at": row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None
            })

        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)
