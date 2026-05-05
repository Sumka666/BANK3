from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_status(request):
    if request.method != "POST":
        return JsonResponse(sendResponse(request, 1001, [{"function": "dt_status"}]))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(sendResponse(request, 1002, [{"function": "dt_status"}]))

    required_fields = ["action", "account_id", "status"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        return JsonResponse(sendResponse(request, 1003, [{"function": "dt_status"}]))

    action = jsons["action"]
    account_id = jsons["account_id"]
    status = jsons["status"]

    ALLOWED_STATUS = ["suspended", "active", "banned"]


    if status not in ALLOWED_STATUS:
        return JsonResponse(
            sendResponse(
                request,
                1005,
                [{"error":"Aldaa zaalaa. Hereglegchiin tulviin songolt : suspended, active, banned"}],
                action
            )
        )

    conn = None
    cur = None

    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            UPDATE users
            SET status = %s
            WHERE account_id = %s
        """
        cur.execute(sql, (status, account_id))
        conn.commit()

        if cur.rowcount == 0:
            return JsonResponse(sendResponse(request, 1004, [{"msg": "Account not found"}], action))

        data = [{"account_id": account_id, "status": status}]
        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        return JsonResponse(sendResponse(request, 1006, [{"error": str(e)}], action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)