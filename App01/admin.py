from django.contrib import admin
from App01.models import Articles  # 导入文章表
from App01.models import Tags  # 导入标签表
from App01.models import Cover  # 导入封面表
from App01.models import Comment  # 导入封面表
from App01.models import Avatars  # 导入头像表
from App01.models import UserInfo  # 导入头像表

# Register your models here.
# 注册
admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)
