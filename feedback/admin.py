from django.contrib import admin

from .models import Feedback
from .models import Reply

admin.site.register(Feedback)
admin.site.register(Reply)