from pipline.models import PipelinesConifg
from django.core.exceptions import ObjectDoesNotExist

    
def set_property(name, value):
    config, created = PipelinesConifg.objects.update_or_create(
        name=name,
        defaults={'value': value}
    )
    return created  # 返回是否是新创建的

def get_property(name):
    try:
        config = PipelinesConifg.objects.get(name=name)
        return config.value
    except ObjectDoesNotExist:
        return None  # 或者返回一个默认值

# 使用示例
# properties.set_property('example_name', 'example_value')
# value = properties.get_property('example_name')
