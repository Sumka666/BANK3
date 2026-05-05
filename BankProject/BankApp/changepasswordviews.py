from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_changepassword(request):
    if request.method != "POST":
        data = [{"function": "dt_changepassword"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_changepassword"}]
        return JsonResponse(sendResponse(request, 1002, data))
    
    required_fields = ["action", "account_id", "old_password", "new_password"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_changepassword"}]
        return JsonResponse(sendResponse(request, 1003, data))
    
    action = jsons["action"]
    account_id = jsons["account_id"]
    old_password = jsons["old_password"]
    new_password = jsons["new_password"]

    conn = None
    cur = None

    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            UPDATE public.users
            SET passwordhash = %s
            WHERE account_id = %s
              AND passwordhash = %s
        """
        cur.execute(sql, (new_password, account_id, old_password))
        conn.commit()

        if cur.rowcount == 0:
            data = []
            return JsonResponse(sendResponse(request, 303, data, action))

        data = [{"account_id": account_id, "message": "Password updated successfully"}]
        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)