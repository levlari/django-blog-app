===============
django-blog-app
===============
django-blog-app is a simple blogging app with the following features:

   - user authentication
   - user registration with email confirmation
   - dynamic preview while creating posts

Instructions
------------

1. Install the django-crispy-forms by following the installation guide at
   http://django-crispy-forms.readthedocs.io/en/latest/

2. Add "blog" app to your installed apps like::

    INSTALLED_APPS = [
        ...
        'blog',
    ]

3. Include the blog URLconf in your project's urls.py::

    url(r'^blog/', include('blog.urls')),

4. User uploaded files such as images in blog posts should be stored separately
   from static files for security reasons. Provide the appropriate values for the
   following settings in your project's settings.py::

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

5. Some models require ``Pillow`` (http://pillow.readthedocs.io/en/latest/) to be installed.
   Install it using pip::

    pip install Pillow

6. Some of the views require urls for logging to which unauthorised users are
   redirected to. Add the following settings to your project's settings.py (you
   can change them if you want)::

    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/blog/'

7. This app uses ``Bootstrap 3`` with ``django-crispy-forms``.
   So, add the following setting to your projects settings.py::

    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    CRISPY_FAIL_SILENTLY = not DEBUG    # raise exception in development.

8. To send email (required when registering new users), the following settings
   need to be included. You have to use your own SMTP server and provide the details
   accordingly::

    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.example.com'
    EMAIL_PORT = 000
    EMAIL_HOST_USER = 'email@example.com'
    EMAIL_HOST_PASSWORD = "password"
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

9. Run ``python manage.py migrate`` to create the necessary tables for the blog
   models.

10. The required bootstrap and jquery files are included in the static/blog
    directory.
