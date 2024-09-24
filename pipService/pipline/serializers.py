from rest_framework import serializers
from .models import Pipelines

class PipelineInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipelines
        fields = '__all__'  # 或者指定你想要的字段列表
