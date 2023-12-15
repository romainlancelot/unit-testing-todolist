import json
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.form import ItemForm
from apps.core.form import UserForm
from apps.core.models import Item


class BaseView(View):
    def get_user(self, user_id: int) -> User | None:
        """Retrieve a user by their ID.

        Args:
            id (int): The ID of the user.

        Returns:
            User | None: The user object if found, None otherwise.
        """

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


@method_decorator(csrf_exempt, name="dispatch")
class TodolistView(BaseView):
    def get(self, request: HttpRequest, user_id: int) -> JsonResponse:
        """Retrieve a user's items.

        Args:
            id (int): The ID of the user.
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing the user's items.
        """

        user: User | None = self.get_user(user_id)
        if user is None:
            return JsonResponse(
                dict(status="error", message="User does not exist"), status=400
            )
        return JsonResponse(
            dict(
                status="success",
                items=[item.to_dict() for item in user.item_set.all()],  # type: ignore
            ),
            status=200,
        )

    def post(self, request: HttpRequest, user_id: int) -> JsonResponse:
        """Handle the HTTP POST request for creating an item.

        Args:
            id (int): The ID of the user.
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: The JSON response indicating the status and message.
        """

        form: ItemForm = ItemForm(json.loads(request.body))
        user: User | None = self.get_user(user_id)
        if user is None:
            return JsonResponse(
                dict(status="error", message="User does not exist"), status=400
            )
        if form.is_valid():
            Item.objects.create(**form.cleaned_data, user=user)
            return JsonResponse(
                dict(status="success", message="Item created successfully"), status=201
            )
        return JsonResponse(
            dict(status="error", message="Form is invalid", errors=form.errors),
            status=400,
        )


@method_decorator(csrf_exempt, name="dispatch")
class UsersView(BaseView):
    def get(self, request: HttpRequest) -> JsonResponse:
        """Handle GET request and return a JSON response containing information about
        users and their to-do lists.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: The JSON response containing the user information.
        """

        users: list[User] = list(User.objects.all())
        return JsonResponse(
            dict(
                status="success",
                users=[
                    dict(
                        id=user.id,  # type: ignore
                        username=user.username,
                        todolist=[item.to_dict() for item in user.item_set.all()],  # type: ignore
                    )
                    for user in users
                ],
            ),
            status=200 if len(users) > 0 else 204,
        )

    def post(self, request: HttpRequest) -> ...:
        """Handle the HTTP POST request to create a new user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: The JSON response indicating the status and message.
        """

        form: UserForm = UserForm(json.loads(request.body))
        if form.is_valid():
            try:
                User.objects.create_user(**form.cleaned_data)
            except Exception as e:
                return JsonResponse(
                    dict(status="error", message="User already exists"), status=400
                )
            return JsonResponse(
                dict(status="success", message="User created successfully"), status=201
            )
        return JsonResponse(
            dict(status="error", message="Form is invalid", errors=form.errors),
            status=400,
        )
