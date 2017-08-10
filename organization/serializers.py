from rest_framework import serializers
from .models import Organization, Category, Branch
from django.contrib.auth.models import User
from rest_framework.utils import model_meta
from rest_framework.compat import set_many

from location.serializers import LocalAreaSerializer
from location.models import LocalArea
from program.serializers import ProgramSerializer
from program.models import Program


class BranchSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(source='pk',
                                               view_name='cell-api-org-branch-detail',
                                               read_only=True)
    organization = serializers.HyperlinkedRelatedField(read_only=True,
                                                       view_name='cell-api-organization-detail')
    localarea = serializers.HyperlinkedRelatedField( required=False,
        view_name='cell-api-localarea-detail', queryset=LocalArea.objects.all())
    other_address = LocalAreaSerializer(required=False, write_only=True)
    city = serializers.CharField(source='localarea.city.name', read_only=True)
    region = serializers.CharField(source='localarea.city.region.name', read_only=True)
    country = serializers.CharField(source='localarea.city.country.name', read_only=True)

    class Meta:
        model = Branch
        fields = ('url', 'organization', 'name', 'localarea', 'other_address',
                  'city', 'region', 'country')

    def create(self, validated_data):
        address_data = None
        try:
            address_data = validated_data.pop('other_address')
        except:
            pass
        branch = Branch.objects.create(**validated_data)

        # Only associate a new address to the user is none is selected
        if address_data:
            LocalArea.objects.create(branch=branch, **address_data)
        return branch

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
                localarea = LocalArea.objects.get(branch=instance, area_name=area_name)
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

        return super(BranchSerializer, self).update(instance, validated_data)


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    #copy from the restframework3 of cities_light
    url = serializers.HyperlinkedIdentityField(view_name='cell-api-organization-detail',
                                             read_only=True, source='pk')
    user = serializers.HyperlinkedRelatedField(view_name='cell-api-userprofile-detail', read_only=True)
    admins = serializers.HyperlinkedRelatedField(many=True, view_name='cell-api-userprofile-detail', required=False,
                                                 queryset=User.objects.all().filter(profile__email_confirmed=True))
    slug = serializers.SlugField(read_only=True)
    category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), required=False,
                                                   view_name='cell-api-org-category-detail')
    approved = serializers.BooleanField(read_only=True)
    branches = serializers.HyperlinkedRelatedField( many=True,
        view_name='cell-api-org-branch-detail', read_only=True)
    add_branches = BranchSerializer(many=True, required=False, write_only=True)
    programs = serializers.HyperlinkedRelatedField(many=True,view_name='cell-api-program-detail', read_only=True)
    add_programs = ProgramSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Organization
        fields = ('url', 'user', 'name', 'slug', 'emblem', 'category', 'admins', 'branches',
                  'add_branches', 'approved', 'programs', 'add_programs')

    def create(self, validated_data):
        branch_data = None
        program_data = None
        try:
            branch_data = validated_data.pop('add_branches')
        except KeyError:
            pass # if it is a Keyerror then the add_branchs does not exist
        try:
            program_data = validated_data.pop('add_programs')
        except KeyError:
            pass # means that the add_programs key is non-existent

        organization = Organization.objects.create(**validated_data)

        if branch_data:
            for datum in branch_data:
                Branch.objects.create(organization=organization, **datum)

        if program_data:
            for datum in program_data:
                Program.objects.create(organization=organization, **datum)

        return organization

    def update(self, instance, validated_data):
        branch_data = None
        program_data = None
        try:
            branch_data = validated_data.pop('add_branches')
        except KeyError:
            pass # pass if the add_branches key does not exist

        try:
            program_data = validated_data.pop('add_programs')
        except KeyError:
            pass # pass if the add_programs key does not exist

        if branch_data:
            for datum in branch_data:
                branch = None
                try:
                    branch_name = datum.get('name')
                    # branch_name and organization are unique together
                    branch = Branch.objects.get(organization=instance, name=branch_name)
                except:
                    pass
                if branch:
                    info = model_meta.get_field_info(branch)
                    for attr, value in datum.items():
                        if attr in info.relations and info.relations[attr].to_many:
                            set_many(branch, attr, value)
                        else:
                            setattr(branch, attr, value)
                    branch.save()
                else:
                    branch = Branch.objects.create(organization=instance, **datum)
                    instance.branches.add(branch)
                instance.save()

        if program_data:
            for datum in program_data:
                program = None
                try:
                    program_name = datum.get('name')
                    # name and organization are unique together in Program model
                    program = Program.objects.get(organization=instance, name=program_name)
                except:
                    pass
                if program:
                    info = model_meta.get_field_info(program)
                    for attr, value in datum.items():
                        if attr in info.relations and info.relations[attr].to_many:
                            set_many(program, attr, value)
                        else:
                            setattr(program, attr, value)
                    program.save()
                else:
                    program = Program.objects.create(organization=instance, **datum)
                    instance.programs.add(program)
                instance.save()

        return super(OrganizationSerializer, self).update(instance, validated_data)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(source='pk',
                                               view_name='cell-api-org-category-detail',
                                               read_only=True)
    slug = serializers.SlugField(read_only=True)
    organizations = serializers.HyperlinkedRelatedField(view_name='cell-api-organization-detail',
                                                        many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'slug', 'organizations')


