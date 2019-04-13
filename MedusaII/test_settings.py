#  Developed by Vinicius José Fritzen
#  Last Modified 13/04/19 14:48.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        'TEST_NAME': os.path.join(BASE_DIR, 'test_sqlite.db'),
    }
}
# DATABASES = {
#     "default": {
#         # TEST_NAME is absolutely CRITICAL for getting django-nose-selenium
#         # going with sqlite3. The default in-memory breaks everything.
#         'TEST_NAME': os.path.join(project_path, 'test_sqlite.db'),
#     }
# }

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'