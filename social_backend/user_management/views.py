from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .serializers import FriendRequestSerializer
from django.db import transaction
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db import transaction
from .models import *
from .serializers import UserSerializer,UserDetailSerializer
from django.db.models import Q



class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, **kwargs):
        """
        Api used to check the login state of a user.
        """

        status = False
        if request.user.is_authenticated:
            status = True
        return Response({"status": status})

    def post(self, request, **kwargs):
        """
        Api used when a user tries to login.
        ----
        parameters:
            - email
            - password
        """
        data = request.data
        user = authenticate(username=data["email"], password=data["password"])
        status = False
        token = ""
        message = ""
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            token = token.key
            status = True
            resp = Response({"status": status, "token": token, "message": message})
            resp.set_cookie("AUTHORIZATION", token)
        else:
            message = "Invalid email or password"
            resp = Response({"status": status, "message": message})
        return resp


class UserSignupView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        request_data = request.data
        if request_data.get("email"):
            request_data["email"] = request_data.get("email").lower()
            email_exist = User.objects.filter(email=request_data.get("email").lower())
            if email_exist:
                return Response(status=200,data={"status":"failure","error":"email already exist"})
            request_data["username"] = request_data.get("email").lower()
        user_details = UserSerializer(data=request_data)
        if user_details.is_valid():
            user = User(**user_details.data)
            user.password = make_password(request.data["password"])
            user.save()
            # Contact.objects.create(contact_no=user.phone_number, user_account=user)
            return Response({"message": "user created!"}, status=200)
        else:
            return Response(user_details.errors, status=400)


class FindUser(APIView):
    def get(self, request):
        search_keyword = request.query_params.get('keyword', '')  # Get the search keyword from query parameters
        page_number = request.query_params.get('page', 1) 

        search_query = Q(email__iexact=search_keyword) | Q(name__icontains=search_keyword)

        # Filter the users based on the search query
        users = User.objects.filter(search_query)
        # Paginate the results
        paginator = Paginator(users, 10)  # Show 10 results per page
        try:
            page_users = paginator.page(page_number)
        except EmptyPage:
            return Response({'status': 'failure',"errors":"no result found"}, status=200)

        # Serialize the results and return the response
        serializer = UserDetailSerializer(page_users, many=True)
        return Response(serializer.data, status=200)


class SendFriendRequest(APIView):
    def post(self, request,receiver_id):
        if not receiver_id:
            return Response(status=400,data={"status":"failure","errors":"reciever_id is mandatory"})
        sender = request.user
        receiver = User.objects.get(pk=receiver_id)

        # Check if the sender has exceeded the request limit within a minute
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        try:
            FriendRequest.objects.get(sender=sender, receiver=receiver)
            return Response({"status":"failure",'message': 'Friend request already sent'}, status=200)
        except FriendRequest.DoesNotExist:
            request_limit, created = FriendRequestLimit.objects.get_or_create(
                user=sender, last_request_time__gte=one_minute_ago
            )
            if request_limit.requests_count >= 3:
                return Response({'status': 'failure',"errors":"request limit exceeded"}, status=400)

            with transaction.atomic():
                friend_request = FriendRequest(sender=sender, receiver=receiver)
                friend_request.save()

                # Increase the request count and update the last request time
                request_limit.requests_count += 1
                request_limit.last_request_time = now
                request_limit.save()

            return Response({"status":"success",'message': 'Friend request sent successfully.'}, status=201)

class AcceptRejectFriendRequest(APIView):
    def post(self, request, friend_request_id, action):
        try:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
        except Exception as e:
            return Response(status=400,data={"errors":e})
        if action == 'accept':
            friend_request.accepted = True
            sender = friend_request.sender
            receiver = friend_request.receiver
            sender.friends_list.add(sender)
            receiver.friends_list.add(receiver)
            friend_request.save()
        elif action == 'reject':
            friend_request.delete()

        return Response({"status":"success",'message': f'Friend request {action}ed.'}, status=200)

class ListFriends(APIView):
    def get(self, request):
        user = request.user
        friends = user.friends_list
        serializer = UserDetailSerializer(friends, many=True)
        return Response(serializer.data, status=200)

class ListPendingFriendRequests(APIView):
    def get(self, request):
        user = request.user
        pending_requests = FriendRequest.objects.filter(receiver=user, accepted=False)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=200)
