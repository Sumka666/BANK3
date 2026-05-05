from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB

@csrf_exempt
def dt_statement(request):
    if request.method != "POST":
        data = [{"function": "get_account_statement"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "get_account_statement"}]
        return JsonResponse(sendResponse(request, 1002, data))
    
    required_fields = ["action", "account_id", "account_number"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "get_account_statement"}]
        return JsonResponse(sendResponse(request, 1003, data))
    action = jsons["action"]
    account_id = jsons["account_id"]
    account_number = jsons["account_number"]
   
    conn = None
    cur = None


    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            SELECT transaction_id, account_id, default_account_id, secondary_account_id
                    , amount, currency, transaction_type, status
                    , description, balance, created_at
	        FROM transactions
                WHERE account_id = %s and default_account_id = %s 
        """
        cur.execute(sql, (account_id, account_number))
        rows = cur.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "transaction_id": row[0],
                "account_id": row[1],
                "default_account_id": row[2],
                "secondary_account_id": row[3],
                "amount": row[4],
                "currency": row[5],
                "transaction_type": row[6],
                "status": row[7],
                "description": row[8],
                "balance": row[9],
                "created_at": row[10].strftime('%Y-%m-%d %H:%M:%S') if row[10] else None
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
