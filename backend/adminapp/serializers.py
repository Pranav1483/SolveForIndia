from rest_framework import serializers
from userapp.models import Reports

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = ('id',
                  'username',
                  'loc',
                  'report',)