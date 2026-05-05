from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from BankProject.settings import connectDB, sendResponse, disconnectDB


import random, string
from datetime import datetime

@csrf_exempt
def dt_register(request):
    if request.method != "POST":
        data = [{"function": "dt_register"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_register"}]
        return JsonResponse(sendResponse(request, 1002, data))

    required_fields = ["action", "email", "firstname", "lastname", "passwordhash"]

    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_register"}]
        return JsonResponse(sendResponse(request, 1003, data))

    action = jsons["action"]
    email = jsons["email"]
    firstname = jsons["firstname"]
    lastname = jsons["lastname"]
    passwordhash = jsons["passwordhash"]

    conn = None
    cur = None

    try:
        conn = connectDB()
        cur = conn.cursor()

        # 1. email already exists check
        check_sql = "SELECT account_id FROM users WHERE email = %s"
        cur.execute(check_sql, (email,))
        if cur.fetchone():
            data = [{"message": "Email already exists"}]
            return JsonResponse(sendResponse(request, 1008, data, action))

        # 2. insert user
        insert_sql = """
            INSERT INTO users (email, firstname, lastname, passwordhash, status, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW()) RETURNING account_id
        """
        cur.execute(insert_sql, (email, firstname, lastname, passwordhash, 1))
        conn.commit()

        account_id = cur.fetchone()[0]



        # Define the character pool (letters + digits)
        chars = string.ascii_letters + string.digits

        # Generate 20 random characters and join them
        account_token = ''.join(random.choices(chars, k=20))


# 2. insert accout number
        insert_sql = """
            INSERT INTO accounts(
	account_id, balance, currency, created_at, account_token)
	VALUES (%s, %s, %s, %s, %s) RETURNING account_number;
        """
        balance = 100000000.00
        currency = 'MNT'
        cur.execute(insert_sql, (account_id, balance, currency, datetime.now(), account_token))
        conn.commit()

        account_number = cur.fetchone()[0]

        # 3. return success
        data = [{
            "account_number": account_number,
            "balance": balance,
            "currency": currency,
            "account_token": account_token
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