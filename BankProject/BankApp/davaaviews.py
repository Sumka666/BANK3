from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from BankProject.settings import connectDB, sendResponse, disconnectDB


@csrf_exempt
def dt_account(request):
    if request.method != "POST":
        return JsonResponse(
            sendResponse(request, 1001, [{"function": "dt_account"}])
        )

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            sendResponse(request, 1002, [{"function": "dt_account"}])
        )

    required_fields = ["action", "account_id"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        return JsonResponse(
            sendResponse(request, 1003, [{"function": "dt_account"}])
        )

    action = jsons["action"]
    account_id = jsons["account_id"]

    if action != "getAccountNumber":
        return JsonResponse(
            sendResponse(request, 400, [{"error": "Invalid action"}], action)
        )

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
            return JsonResponse(
                sendResponse(request, 1004, [{"msg": "Account not found"}], action)
            )

        data = []

        for row in rows:
            data.append({
                "account_id": row[0],
                "account_number": row[1],
                "balance": row[2],
            })

        return JsonResponse(
            sendResponse(request, 200, data, action)
        )

    except Exception as e:
        return JsonResponse(
            sendResponse(request, 1006, [{"error": str(e)}], action)
        )

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)