from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from BankProject.settings import connectDB, sendResponse, disconnectDB


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

    action = jsons.get("action", "")

    # ---------------- GET REGISTER ----------------
    if action == "get_register":

        data = [{
            "email": "",
            "firstname": "",
            "lastname": ""
        }]

        return JsonResponse(sendResponse(request, 200, data, action))

    # ---------------- REGISTER ----------------
    elif action == "register":

        required_fields = [
            "email",
            "firstname",
            "lastname",
            "passwordhash"
        ]

        if not all(field in jsons and jsons[field] != "" for field in required_fields):
            data = [{"function": "dt_register"}]
            return JsonResponse(sendResponse(request, 1003, data, action))

        email = jsons["email"]
        firstname = jsons["firstname"]
        lastname = jsons["lastname"]
        passwordhash = jsons["passwordhash"]

        conn = None
        cur = None

        try:
            conn = connectDB()
            cur = conn.cursor()

            # email давхардсан эсэх шалгах
            check_sql = """
                SELECT account_id
                FROM users
                WHERE email = %s
            """

            cur.execute(check_sql, (email,))
            exist = cur.fetchone()

            if exist:
                data = [{"email": "Already exists"}]
                return JsonResponse(sendResponse(request, 1008, data, action))

            # insert
            insert_sql = """
                INSERT INTO users
                (
                    email,
                    firstname,
                    lastname,
                    passwordhash,
                    status,
                    created_at
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    NOW()
                )
            """

            cur.execute(insert_sql, (
                email,
                firstname,
                lastname,
                passwordhash,
                1
            ))

            conn.commit()

            data = [{
                "email": email,
                "firstname": firstname,
                "lastname": lastname
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

    else:
        data = [{"function": "dt_register"}]
        return JsonResponse(sendResponse(request, 1004, data, action))