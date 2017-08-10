from rest_framework import serializers
from .models import Reference, Agenda, Minute, Point
from program.models import Member


from rest_framework.utils import model_meta
from rest_framework.compat import set_many


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the reference model
    """
    url_id = serializers.HyperlinkedIdentityField(
        view_name='cell-api-reference-detail'
    )
    id = serializers.IntegerField(source='pk', write_only=True, required=False)

    class Meta:
        model = Reference
        exclude = []
        fields = ('url_id', 'id', 'source', 'book', 'chapter', 'verse', 'url')


class PointSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Point model
    """
    url = serializers.HyperlinkedIdentityField(view_name='cell-api-point-detail')
    minute = serializers.HyperlinkedRelatedField(view_name='cell-api-minute-detail',
                                                 read_only=True)
    author = serializers.HyperlinkedRelatedField(
        view_name='cell-api-member-detail',
        read_only=True
    )
    references = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='cell-api-reference-detail',
        read_only=True
    )
    # add_references
    last_modified = serializers.DateTimeField(read_only=True)
    added_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Point
        exclude = []


class AddMinuteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for addition of a minute by only program editor and above
    """
    url = serializers.HyperlinkedIdentityField(view_name='cell-api-minute-detail')

    class Meta:
        model = Minute
        fields = ('url', 'title')


class MinuteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Minute model
    """
    url = serializers.HyperlinkedIdentityField(view_name='cell-api-minute-detail')
    title = serializers.CharField(read_only=True)
    agenda = serializers.HyperlinkedRelatedField(
        view_name='cell-api-agenda-detail',
        read_only=True
    )
    references = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='cell-api-reference-detail',
        read_only=True
    )
    points = serializers.HyperlinkedRelatedField(read_only=True, many=True,
                                                 view_name='cell-api-point-detail')
    add_points = PointSerializer(many=True, write_only=True, required=False)
#    add_references = ReferenceSerializer(many=True, write_only=True, required=False)
    last_modified = serializers.DateTimeField(read_only=True)
    added_on = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Minute
        fields = ('url', 'agenda', 'title', 'references', 'last_modified',
                  'added_on', 'points', 'add_points')

    def create(self, validated_data):
        point_data = None
        current_user = None

        try:
            point_data = validated_data.pop('add_points')
        except KeyError:
            pass # if it is a Keyerror then the add_branchs does not exist

        try:
            current_user = validated_data.pop('current_user')
        except KeyError:
            pass # if it is a Keyerror then the add_branchs does not exist

        minute = Minute.objects.create(**validated_data)

        if current_user:
            program = minute.agenda.author.program
            author = None
            try:
                author = Member.objects.get(program=program, user=current_user)
            except:
                pass
            if author and point_data:
                for datum in point_data:
                    Point.objects.create(minute=minute, author=author, **datum)

        return minute

    def update(self, instance, validated_data):
        point_data = None
        current_user = None
        author = None

        try:
            point_data = validated_data.pop('add_points')
        except KeyError:
            pass # pass if the add_branches key does not exist
            # raise KeyError('%s' % str(validated_data))

        try:
            current_user = validated_data.pop('current_user')
        except KeyError:
            pass # pass if the add_branches key does not exist
            # raise KeyError('%s' % str(validated_data))

        if current_user:
            program = instance.agenda.author.program
            try:
                author = Member.objects.get(program=program, user=current_user)
            except:
                pass

        if point_data and author:
            for datum in point_data:
                point = None
                try:
                    text_detail = datum.get('text_detail')
                    # text_detail, author and minute are unique together
                    point = Point.objects.get(minute=instance, text_detail=text_detail, author=author)
                except:
                    pass

                if point:
                    info = model_meta.get_field_info(point)
                    for attr, value in datum.items():
                        if attr in info.relations and info.relations[attr].to_many:
                            set_many(point, attr, value)
                        else:
                            setattr(point, attr, value)
                    point.save()
                else:
                    point = Point.objects.create(minute=instance, author=author, **datum)
                    instance.points.add(point)
                instance.save()

        return super(MinuteSerializer, self).update(instance, validated_data)



class AgendaSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Agenda model
    """
    url = serializers.HyperlinkedIdentityField(view_name='cell-api-agenda-detail')
    author = serializers.HyperlinkedRelatedField(
        view_name='cell-api-member-detail',
        read_only=True
    )
    last_modified = serializers.DateTimeField(read_only=True)
    added_on = serializers.DateTimeField(read_only=True)
    minutes = serializers.HyperlinkedRelatedField(view_name='cell-api-minute-detail',
                                                  read_only=True, many=True)
    add_minutes = AddMinuteSerializer(required=False, write_only=True, many=True)

    class Meta:
        model = Agenda
        fields = ('url', 'author', 'purpose', 'privacy', 'date', 'venue', 'last_modified',
                  'added_on', 'minutes', 'add_minutes')

    def create(self, validated_data):
        minute_data = None

        try:
            minute_data = validated_data.pop('add_minutes')
        except KeyError:
            pass # if it is a Keyerror then the add_branchs does not exist

        agenda = Agenda.objects.create(**validated_data)

        if minute_data:
            for datum in minute_data:
                Minute.objects.create(agenda=agenda, **datum)

        return agenda

    def update(self, instance, validated_data):
        minute_data = None
        try:
            minute_data = validated_data.pop('add_minutes')
        except KeyError:
            pass # pass if the add_branches key does not exist
            # raise KeyError('%s' % str(validated_data))

        if minute_data:
            for datum in minute_data:
                minute = None
                try:
                    title = datum.get('title')
                    # branch_name and organization are unique together
                    minute = Minute.objects.get(agenda=instance, title=title)
                except:
                    pass

                if minute:
                    info = model_meta.get_field_info(minute)
                    for attr, value in datum.items():
                        if attr in info.relations and info.relations[attr].to_many:
                            set_many(minute, attr, value)
                        else:
                            setattr(minute, attr, value)
                    minute.save()
                else:
                    minute = Minute.objects.create(agenda=instance, **datum)
                    instance.minutes.add(minute)
                instance.save()

        return super(AgendaSerializer, self).update(instance, validated_data)
