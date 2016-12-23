import os

# Import default settings for the project
from xwing_rulebook.conf.default import *

# We use an environmental variable to indicate the, erm, environment
# This block writes all settings to the local namespace
module_path = os.environ.get('DJANGO_CONF', 'xwing_rulebook.conf.environment')

try:
    module = __import__(module_path, globals(), locals(), ['*'])
except ImportError:
    module = None

if module:
    for k in dir(module):
        if not k.startswith("__"):
            locals()[k] = getattr(module, k)

    # Add any additional apps only required locally
    if 'EXTRA_APPS' in locals():
        INSTALLED_APPS = INSTALLED_APPS + EXTRA_APPS

    if 'EXTRA_MIDDLEWARE_CLASSES' in locals():
        MIDDLEWARE = MIDDLEWARE + EXTRA_MIDDLEWARE

