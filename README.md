# djangoblog

## PythonAnywhere deployment notes

This project can run on PythonAnywhere with the same Django settings module (`BLOG.settings`).

Recommended environment variables for the PythonAnywhere Web app / WSGI file:

```python
import os

os.environ["DJANGO_DEBUG"] = "False"
os.environ["DJANGO_SECRET_KEY"] = "replace-with-a-long-random-secret"
os.environ["DJANGO_ALLOWED_HOSTS"] = "yourusername.pythonanywhere.com"
os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = "https://yourusername.pythonanywhere.com"
```

If these variables are not set, development defaults are used. The default host list includes
`.pythonanywhere.com` so the app can start on PythonAnywhere during initial setup, but production
deployments should still set the exact `DJANGO_ALLOWED_HOSTS` value for their site.

Typical setup commands:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

Configure PythonAnywhere static/media mappings to the project `staticfiles/` and `media/`
directories, then reload the Web app.
