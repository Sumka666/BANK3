import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateView(View):

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({"error": "User oldsongui"}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON buruu baina"}, status=400)

        required_fields = data.get("required_fields", [])
        missing_fields = []

        # Required fields шалгах
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)

        if missing_fields:
            return JsonResponse({
                "missing_fields": missing_fields,
                "message": "Darah talbaruud shaardlagatai"
            }, status=400)

        # Update хийх field-үүд
        updatable_fields = ["username", "email", "first_name", "last_name"]

        updated_data = {}

        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
                updated_data[field] = data[field]

        user.save()

        return JsonResponse({
            "message": "Amjilttai shinechlegdlee",
            "updated": updated_data
        })