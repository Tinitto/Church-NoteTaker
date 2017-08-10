from rest_framework import viewsets, generics, permissions, status
from django.contrib.auth.models import User
from .serializers import UserUpdateSerializer, UserSerializer, ProfileSerializer
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .permissions import IsUser, IsUserOrReadOnly, IsOwnerOrReadOnly


class SearcheableUserModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        Allows a GET param, 'q', to be used against name.
        """
        queryset = super(SearcheableUserModelViewSet, self).get_queryset()

        if self.request.GET.get('q', None):
            full_queryset = queryset.filter(first_name__icontains=self.request.GET['q'])
            full_queryset += queryset.filter(last_name__icontains=self.request.GET['q'])
            return full_queryset

        return queryset


#creating a new user
#class CreateUserView(CreateAPIView):
class CreateUserView(generics.CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=False)
        user = User.objects.get(username=serializer.validated_data['username'])
        #user.is_active = False
        #user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your CellNotes Account'
        message = render_to_string('user/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)


class ActivateUserViewSet(viewsets.mixins.UpdateModelMixin, viewsets.mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    This is for acitvation of the user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def activate(self, request):
        uidb64 = self.request.GET.get('uidb64', None) # get the query parameter clalled uidb64
        token = self.request.GET.get('token', None)  # get the query parameter called token

        if uidb64 and token:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user = get_object_or_404(User, pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.profile.email_confirmed = True
                user.save()
                login(self.request, user)
                return Response(('activated',), status=status.HTTP_200_OK)
            else:
                return Response(('Not found',), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(('Not acceptable',), status=status.HTTP_406_NOT_ACCEPTABLE)



class ProfileViewSet(SearcheableUserModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


#class AddressViewSet(viewsets.ModelViewSet):
#    """
#    This viewset automatically provides `list`, `create`, `retrieve`,
#    `update` and `destroy` actions.
#    """
#    queryset = Address.objects.all()
#    serializer_class = AddressSerializer
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                          IsOwnerOrReadOnly)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This only allows listing and detail actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUserOrReadOnly)


class UserUpdateViewSet(viewsets.mixins.UpdateModelMixin, viewsets.mixins.DestroyModelMixin,
                        viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    This only allows listing and detail actions
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsUser)

    def perform_update(self, serializer):
        data = self.request.data.copy()
        try:
            user = authenticate(username=self.request.user.username, password=data['current_password'])
        except KeyError:
            raise KeyError('Non-existent data type')
        if user is not None:
            # change password
            if data['new_password']:
                user.set_password(data['new_password'])
                #user.save()
                serializer.save(password=user.password)
            serializer.save()



