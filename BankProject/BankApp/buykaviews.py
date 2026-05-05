from django.http import JsonResponse
from django.db import connection

def get_user_by_account(request):
    account_number = request.GET.get('account_number')

    if not account_number:
        return JsonResponse({'error': 'account_number required'}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.firstname, u.lastname
            FROM accounts a
            JOIN users u ON a.account_id = u.account_id
            WHERE a.account_number = %s
        """, [account_number])

        row = cursor.fetchone()

    if row:
        return JsonResponse({
            'firstname': row[0],
            'lastname': row[1]
        })
    else:
        return JsonResponse({'error': 'Account not found'}, status=404)