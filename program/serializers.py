from rest_framework import serializers
from .models import Program, PermittedUserAttributes, Member
from django.contrib.auth.models import User
from user.serializers import UserMinimalSerializer
from location.models import City, Country,Region, LocalArea
from minutes.models import Agenda
from minutes.serializers import AgendaSerializer

from rest_framework.utils import model_meta
from rest_framework.compat import set_many


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-member-detail',
                                             read_only=True)
    user = UserMinimalSerializer(required=False)
    parent_program = serializers.CharField(source='program.parent_program.name', read_only=True)
    program = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name='cell-api-program-detail')
    organization = serializers.CharField(source='program.organization.name', read_only=True)
    agendas = serializers.HyperlinkedRelatedField(view_name='cell-api-agenda-detail', read_only=True,
                                                  many=True)
    create_agendas = AgendaSerializer(many=True, required=False, write_only=True)
    points = serializers.HyperlinkedRelatedField(view_name='cell-api-point-detail', read_only=True,
                                                  many=True)

    class Meta:
        model = Member
        fields = ('url', 'organization', 'parent_program', 'program', 'role', 'user',
                  'agendas', 'points', 'create_agendas')

    def create(self, validated_data):
        agenda_data = None

        try:
            agenda_data = validated_data.pop('create_agendas')
        except KeyError:
            pass # if it is a Keyerror then the add_branchs does not exist

        member = Member.objects.create(**validated_data)

        if agenda_data:
            for datum in agenda_data:
                Agenda.objects.create(author=member, **datum)

        return member

    def update(self, instance, validated_data):
        agenda_data = None
        try:
            agenda_data = validated_data.pop('create_agendas')
        except KeyError:
            pass # pass if the add_branches key does not exist
            #raise KeyError('%s' % str(validated_data))
        try:
            # remove the UserMinimalSerializer as this
            # is not expected by the model of the Member
            validated_data.pop('user')
        except KeyError:
            pass

        if agenda_data:
            for datum in agenda_data:
                agenda = None
                try:
                    purpose = datum.get('purpose')
                    date = datum.get('date')
                    # branch_name and organization are unique together
                    agenda = Agenda.objects.get(author=instance, purpose=purpose, date=date)
                except:
                    pass
                if agenda:
                    info = model_meta.get_field_info(agenda)
                    for attr, value in datum.items():
                        if attr in info.relations and info.relations[attr].to_many:
                            set_many(agenda, attr, value)
                        else:
                            setattr(agenda, attr, value)
                    agenda.save()
                else:
                    agenda = Agenda.objects.create(author=instance, **datum)
                    instance.agendas.add(agenda)
                instance.save()

        return super(MemberSerializer, self).update(instance, validated_data)


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-program-detail',
                                             read_only=True)
    slug = serializers.SlugField(read_only=True)
    organization = serializers.HyperlinkedRelatedField(read_only=True,
                                                       view_name='cell-api-organization-detail')
    parent_program = serializers.HyperlinkedRelatedField(queryset=Program.objects.all(),
                                                       view_name='cell-api-program-detail', required=False)
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='cell-api-member-detail')
    permitteduserattributes = serializers.HyperlinkedRelatedField(read_only=True,
                                                                  view_name='cell-api-permitteduserattributes-detail')
    add_members = serializers.HyperlinkedRelatedField(many=True, write_only=True, required=False,
                                                      view_name='cell-api-user-detail',
                                                      queryset=User.objects.all().filter(is_active=True))

    class Meta:
        model = Program
        fields = ('url', 'organization', 'parent_program', 'name', 'slug', 'description',
                  'members', 'permitteduserattributes', 'add_members')

    def create(self, validated_data):
        member_data = None

        try:
            member_data = validated_data.pop('add_members')
        except KeyError:
            pass # if it is a Keyerror then the add_branchs does not exist

        program = Program.objects.create(**validated_data)

        if member_data:
            for datum in member_data:
                Member.objects.create(program=program, **datum) # expects "user" : "url"
        return program

    def update(self, instance, validated_data):
        member_data = None

        try:
            member_data = validated_data.pop('add_members')
        except KeyError:
            pass # pass if the add_members key does not exist

        if member_data:
            for datum in member_data:
                member = None
                try:
                    member = Member.objects.get(program=instance, user=datum)
                except:
                    pass

                if not member:
                    member = Member.objects.create(program=instance, user=datum)
                    member.save() # this uses an intermediate model thus no add()
                instance.save()

        return super(ProgramSerializer, self).update(instance, validated_data)


class PermittedUserAttributesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(source='pk', view_name='cell-api-permitteduserattributes-detail',
                                             read_only=True)
    program = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name='cell-api-program-detail')
    countries = serializers.HyperlinkedRelatedField(many=True, view_name='cell-api-country-detail',
                                                          queryset=Country.objects.all())
    cities = serializers.HyperlinkedRelatedField(many=True, view_name='cell-api-city-detail',
                                                          queryset=City.objects.all())
    regions = serializers.HyperlinkedRelatedField(many=True, view_name='cell-api-region-detail',
                                                          queryset=Region.objects.all())
    localareas = serializers.HyperlinkedRelatedField(many=True, view_name='cell-api-localarea-detail',
                                                          queryset=LocalArea.objects.all())

    class Meta:
        model = PermittedUserAttributes
        exclude = []

