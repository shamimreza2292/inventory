#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StocketBucket.settings')
import django

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
password = 'admin'
email = 'admin@example.com'

try:
    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.save()
        print('updated')
    else:
        User.objects.create_superuser(username, email, password)
        print('created')
except Exception:
    import traceback
    traceback.print_exc()
    raise
