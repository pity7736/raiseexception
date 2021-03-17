import os

env = os.environ['APP_ENVIRONMENT']
print('env', env)

if env == 'dev':
    from .dev import *  # noqa: F401, F403
elif env == 'testing':
    from .testing import *  # noqa: F401, F403
elif env == 'production':
    from .production import *  # noqa: F401, F403
else:
    raise ValueError('env environment not set')
