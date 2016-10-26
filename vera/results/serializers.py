from rest_framework import serializers
from wq.db.patterns import serializers as patterns

import swapper
Result = swapper.load_model('results', 'Result')


class SettableField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, value):
        return value


class ResultSerializer(patterns.TypedAttachmentSerializer):
    value = SettableField()

    def to_representation(self, obj):
        result = super(ResultSerializer, self).to_representation(obj)
        if getattr(obj.type, 'units', None) is not None:
            result['units'] = obj.type.units
        return result

    class Meta(patterns.TypedAttachmentSerializer.Meta):
        exclude = ('report', 'value_text', 'value_numeric')
        model = Result

        object_field = 'report'


class EventResultSerializer(serializers.Serializer):
    site = serializers.ReadOnlyField(
        source='event_site.slug',
    )
    date = serializers.ReadOnlyField(
        source='event_date'
    )
    parameter = serializers.ReadOnlyField(
        source='result_type.slug',
    )
    units = serializers.ReadOnlyField(
        source='result_type.units'
    )
    value = serializers.ReadOnlyField(
        source='result_value'
    )

    class Meta:
        pandas_index = ['date']
        pandas_unstacked_header = ['site', 'parameter', 'units']
        pandas_scatter_coord = ['units', 'parameter']
        pandas_scatter_header = ['site']
        pandas_boxplot_group = 'site'
        pandas_boxplot_date = 'date'
        pandas_boxplot_header = ['units', 'parameter']