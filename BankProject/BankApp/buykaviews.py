from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_username(request):
    if request.method != "POST":
        data = [{"function": "dt_username"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_username"}]
        return JsonResponse(sendResponse(request, 1002, data))
    
    required_fields = ["action", "account_number"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_username"}]
        return JsonResponse(sendResponse(request, 1003, data))
    action = jsons["action"]
    account_number = jsons["account_number"]
    conn = None
    cur = None

    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            SELECT (users.firstname || ' ' || users.lastname) AS fullname 
            FROM accounts INNER JOIN users ON accounts.account_id = users.account_id 
            WHERE accounts.account_number = %s
        """
        cur.execute(sql, (account_number, ))
        rows = cur.fetchall()
        if len(rows) != 1:
            data = []
            return JsonResponse(sendResponse(request, 303, data, action))

        fullname = rows[0][0]

        
        data = [{"account_number": account_number, "fullname": fullname}]
        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)
