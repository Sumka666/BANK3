from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests, json

from BankProject.settings import connectDB, sendResponse, disconnectDB
import qrcode
import base64
from io import BytesIO

def text_to_qrbase64(qrtext):
    img = qrcode.make(qrtext)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    base64_data = base64.b64encode(img_bytes).decode('utf-8')
    return base64_data

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
            select  account_number, account_id from accounts where account_token = %s
        """
        cur.execute(sql, (account_token,))
        rows = cur.fetchall()
        if len(rows) != 1:
            data = []
            return JsonResponse(sendResponse(request, 400, data, action))

        account_number = rows[0][0]
        account_id = rows[0][1]

        qrtext = f"dans={account_number}&amount={amount}&description={description}"
        base64_data = text_to_qrbase64(qrtext)
        
        sql = """
            INSERT INTO qr_codes (account_id, account_number, qr_text, created_at, amount, description) VALUES (%s, %s, %s, NOW(), %s, %s) RETURNING qr_id
        """
        cur.execute(sql, (account_id, account_number, qrtext, amount, description))
        qr_id = cur.fetchone()[0]
        conn.commit()

        data = [{"qrtext": qrtext, "qr_id": qr_id, "qr_image": base64_data}]
        return JsonResponse(sendResponse(request, 200, data, action))

    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)
