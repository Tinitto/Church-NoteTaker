from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from rest_framework.utils import model_meta
from rest_framework.compat import set_many
from location.serializers import LocalAreaSerializer
from location.models import LocalArea


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-userprofile-detail',
                                             read_only=True)
    user = serializers.HyperlinkedRelatedField(view_name='cell-api-user-detail',
                                             read_only=True)
    #address = serializers.HyperlinkedIdentityField(source='address', view_name='cell-api-useraddress-detail',
    #                                            read_only=True)
    localarea = serializers.HyperlinkedRelatedField(required=False,
        view_name='cell-api-localarea-detail', queryset=LocalArea.objects.all())
    other_address = LocalAreaSerializer(required=False)
    city = serializers.CharField(source='localarea.city.name', read_only=True)
    region = serializers.CharField(source='localarea.city.region.name', read_only=True)
    country = serializers.CharField(source='localarea.city.country.name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)

    class Meta:
        model = Profile
        fields = ('url', 'user', 'first_name', 'last_name', 'profile_photo', 'telephone',
                  'birthday', 'gender', 'localarea', 'other_address', 'city', 'region', 'country',)

    def create(self, validated_data):
        address_data = None
        try:
            address_data = validated_data.pop('other_address')
        except:
            pass
        profile = Profile.objects.create(**validated_data)

        if address_data:
            LocalArea.objects.create(user=profile, **address_data)
        return profile

    def update(self, instance, validated_data):
        try:
            localarea_data = validated_data.pop('other_address')
        except:
            raise KeyError('Invalid local area input')
        if localarea_data:
            # remove any input to the localarea field
            try:
                validated_data.pop('localarea')
            except KeyError:
                pass
            localarea = None
            try:
                area_name = localarea_data.get('area_name')
                localarea = LocalArea.objects.get(user=instance, area_name=area_name)
            except:
                pass
            if localarea:
                info = model_meta.get_field_info(localarea)
                for attr, value in localarea_data.items():
                    if attr in info.relations and info.relations[attr].to_many:
                        set_many(instance, attr, value)
                    else:
                        setattr(instance, attr, value)
                    localarea.save()
            else:
                localarea = LocalArea.objects.create(**localarea_data)
                instance.localarea = localarea
                instance.save()

        return super(ProfileSerializer, self).update(instance, validated_data)



class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    This is only for write. To view user details, go to the profile
    """
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-user-detail',
                                             read_only=True)
    edit = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-userupdate-detail',
                                             read_only=True)
    profile = serializers.HyperlinkedRelatedField(view_name='cell-api-userprofile-detail',
                                                read_only=True)
    email = serializers.EmailField(max_length=254, help_text='Required. inform \
                              a valid email address', write_only=True)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True) # will not be readable
    created_organizations = serializers.HyperlinkedRelatedField(view_name='cell-api-organization-detail',
                                                                many=True, read_only=True)
    administered_organizations = serializers.HyperlinkedRelatedField(view_name='cell-api-organization-detail',
                                                                many=True, read_only=True)
    programs = serializers.HyperlinkedRelatedField(view_name='cell-api-member-detail',
                                                                many=True, read_only=True)

    #override to save password
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('url', 'edit', 'username', 'first_name', 'last_name', 'email', 'password', 'profile',
                  'created_organizations', 'administered_organizations', 'programs')


class UserMinimalSerializer(serializers.HyperlinkedModelSerializer):
    """
    This is only for write. To view user details, go to the profile
    """
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-user-detail',
                                             read_only=True)
    edit = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-userupdate-detail',
                                             read_only=True)
    profile = serializers.HyperlinkedRelatedField(view_name='cell-api-userprofile-detail',
                                                read_only=True)

    class Meta:
        model = User
        fields = ('url', 'edit', 'profile')




class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """
    This is only for write. To view user details, go to the profile
    """
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-userupdate-detail',
                                             read_only=True)
    profile = serializers.HyperlinkedRelatedField(view_name='cell-api-userprofile-detail',
                                                read_only=True)
    email = serializers.EmailField(max_length=254, help_text='Required. inform \
                              a valid email address', read_only=True)
    username = serializers.CharField(read_only=True) # will not be readable
    current_password = serializers.CharField(write_only=True, allow_blank=False, required=True,
                                             allow_null=True, help_text='Required for any change to succeed')
    new_password = serializers.CharField(write_only=True, allow_blank=True,
                                         allow_null=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email',  'profile',
                  'new_password', 'current_password',)
