from rest_framework import serializers
from userapp.models import Block, User

class BlockSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Block
        fields = ('owner',
                  'num',
                  'pd_id',
                  'batch_id',
                  'timestamp',
                  'product_details',
                  'hash_code',)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password',
                  'mobile',)