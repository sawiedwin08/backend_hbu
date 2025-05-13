from apps.activities.models import *
from rest_framework import serializers

class DimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        exclude = ('state','created_date','modified_date','deleted_date',)

    # def to_representation(self, instance):

class ProgramDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramDimension
        exclude = ('state','created_date','modified_date','deleted_date',)

class SubprogramDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubprogramDimension
        exclude = ('state','created_date','modified_date','deleted_date',)