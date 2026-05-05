import email
from random import randint
from urllib import request

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from BankProject.settings import connectDB, sendResponse, disconnectDB
from django.core.mail import send_mail


@csrf_exempt
def dt_forgotpassword(request):
    if request.method != "POST":
        data = [{"function": "dt_forgotpassword"}]
        return JsonResponse(sendResponse(request, 1001, data))

    try:
        jsons = json.loads(request.body)
    except json.JSONDecodeError:
        data = [{"function": "dt_forgotpassword"}]
        return JsonResponse(sendResponse(request, 1002, data))
    
    required_fields = ["action", "email"]
    if not all(field in jsons and jsons[field] != "" for field in required_fields):
        data = [{"function": "dt_forgotpassword"}]
        return JsonResponse(sendResponse(request, 1003, data))
    action = jsons["action"]
    email = jsons["email"]
    conn = None
    cur = None

    try:
        conn = connectDB()
        cur = conn.cursor()

        sql = """
            select account_id from users where email = %s
        """
        cur.execute(sql, (email,))
        rows = cur.fetchall()
        if len(rows) != 1:
            data = []
            return JsonResponse(sendResponse(request, 400, data, action))

        account_id = rows[0][0]

        # Generate a verification code and store it in the database

        n = 6
        verification_code = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
        sql = """
            UPDATE users SET reset_code = %s, reset_code_expiry = NOW() + INTERVAL '15 minutes' WHERE account_id = %s
        """
        cur.execute(sql, (verification_code, account_id))
        conn.commit()

        # send_mail(
        #     'Password Reset Verification Code',
        #     f'Your password reset verification code is: {verification_code}',
        #     'from@example.com',
        #     [email],
        #     fail_silently=False,
        #     )

        data = [{"email": email}]
        return JsonResponse(sendResponse(request, 200, data, action))
    except Exception as e:
        data = [{"error": str(e)}]
        return JsonResponse(sendResponse(request, 1006, data, action))

    finally:
        if cur:
            cur.close()
        if conn:
            disconnectDB(conn)
            

@csrf_exempt
def dt_verifyuser(request):    
    if request.method != "POST":        
        return JsonResponse(sendResponse(request, 1001, [{"function": "dt_verifyuser"}]))    
    try:        
        jsons = json.loads(request.body)    
    except json.JSONDecodeError:        
        return JsonResponse(sendResponse(request, 1002, [{"function": "dt_verifyuser"}]))    
    required_fields = ["action", "reset_code"]    
    if not all(field in jsons and jsons[field] != "" for field in required_fields):        
        return JsonResponse(sendResponse(request, 1003, [{"function": "dt_verifyuser"}]))    
    action = jsons["action"]      
    reset_code = jsons["reset_code"]    
    conn = None    
    cur = None 

    try:        
        conn = connectDB()        
        cur = conn.cursor()        
        cur.execute("SELECT account_id, email FROM users WHERE reset_code = %s AND reset_code_expiry > NOW()",            
        (reset_code,))
        rows = cur.fetchall()        
        if len(rows) != 1:            
            return JsonResponse(sendResponse(request, 400, [], action))        
        account_id = rows[0][0]   
        email = rows[0][1]

        data = [{            
            "account_id": account_id,            
            "email": email,            
            "verified": True        
            }]        
        return JsonResponse(sendResponse(request, 200, data, action))    
    except Exception as e:        
        return JsonResponse(sendResponse(request, 1006, [{"error": str(e)}], action))    
    finally:        
        if cur:            
            cur.close()        
            if conn:            
                disconnectDB(conn)

def dt_newpassword(request):
    pass