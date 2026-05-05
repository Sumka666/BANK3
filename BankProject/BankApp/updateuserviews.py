from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_update_user(request):
    if request.method != "POST":
        data = [{"function": "dt_update_user"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_update_user"}]
        return JsonResponse(sendResponse(request, 1002, data))

    required_fields = ["action", "account_id", "firstname", "lastname"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_update_user"}]
        return JsonResponse(sendResponse(request, 1003, data))

    action = jsons["action"]
    account_id = jsons["account_id"]
    firstname = jsons["firstname"]
    lastname = jsons["lastname"]

    conn = None
    cur = None
    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            update users
            set firstname = %s, lastname = %s
            where account_id = %s
        """
        cur.execute(sql, (firstname, lastname, account_id))
        conn.commit()

        if cur.rowcount == 0:
            data = [{"msg": "Account not found"}]
            return JsonResponse(sendResponse(request, 1004, data, action))

        data = [{
            "account_id": account_id,
            "firstname": firstname,
            "lastname": lastname,
        }]
        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)
