from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB


@csrf_exempt
def dt_account(request):
    if request.method != "POST":
        data = [{"function": "dt_account"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_account"}]
        return JsonResponse(sendResponse(request, 1002, data))

    required_fields = ["action", "account_id"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_account"}]
        return JsonResponse(sendResponse(request, 1003, data))

    action = jsons["action"]
    account_id = jsons["account_id"]

    conn = None
    cur = None

    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            SELECT account_id, account_number, balance
            FROM accounts
            WHERE account_id = %s
        """
        cur.execute(sql, (account_id,))
        rows = cur.fetchall()

        if not rows:
            data = []
            return JsonResponse(sendResponse(request, 1007, data, action))

        data = []
        for row in rows:
            data.append({
                "account_id": row[0],
                "account_number": row[1],
                "balance": row[2],
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