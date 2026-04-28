from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_qr(request):
    if request.method != "POST":
        data = [{"function": "dt_qr"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_qr"}]
        return JsonResponse(sendResponse(request, 1002, data))
    
    required_fields = ["action", "account_token", "amount", "description"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_qr"}]
        return JsonResponse(sendResponse(request, 1003, data))
    action = jsons["action"]
    account_token = jsons["account_token"]
    amount = jsons["amount"]
    description = jsons["description"]
    conn = None
    cur = None
    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            select  account_number from accounts where account_token = %s
        """
        cur.execute(sql, (account_token,))
        rows = cur.fetchall()
        if len(rows) != 1:
            data = []
            return JsonResponse(sendResponse(request, 400, data, action))

        account_number = rows[0][0]
        qrtext = f"dans={account_number}&amount={amount}&description={description}"
        data = [{"qrtext": qrtext}]
       

        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)

