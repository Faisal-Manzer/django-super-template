# Django Super Template
Focus on code not on configuration.  

Out of the box production ready setup for:
- REST Api ([django-rest-framework])
- JWT Authentication ([djangorestframework-simplejwt])
- WebSocket ([channels])
- Background task execution ([celery])

# Installation
### Step 1: Clone and install
```shell script
git clone https://github.com/Faisal-Manzer/django-super-template.git
mv django-super-template server
cd server
cp secrets.example.json secrets.json
chmod +x install.sh
./install.sh
```

### Step 2: Secure
Obtain RSA key pair from: https://travistidwell.com/jsencrypt/demo/ and paste them in __config__/keys/private.key and __config__/keys/public.key

### Step 3: Edit `secrets.json`
- `DJANGO`:
    - `SECRET_KEY`: Secret key used by django. Generate new secret key (here)[https://djecrety.ir].
    - `DEBUG`, `PRODUCATION`: [See modes](#modes)
    - `ALLOWED_HOST`: For development is always `['*']` regardless of the settings. 
    For production chose two host `api.YOUR_DOMAIN.com` amd `admin.YOUR_DOMAIN.com`. If you want you can change sub-domains in `__config__/hosts.py`.
- `CLIENTS`: Regex pattern for your API Client base url. This is CORS whitelist.
- `DB`: Postgres database settings
- `TEST_USER`: Create a test user by `./manage.py create-test-user` with credentials provided here.
- `TASK_QUEUE`: Celery task broker message queue, [redis] is preferred as message broker but you can customise according to requirements.
- `CHANNEL_DB`: Temporary data base used by channels to store messages. [Redis][redis] is preferred.
- `AWS`:
    - `S3`:
        - `BUCKET_NAME`: S3Bucket name where media and static file will be stored in production.
        - `REGION`: S3Bucket Region
        - `STATIC_FOLDER`: Key prefix for storing static files in S3
        - `MEDIA_FOLDER`: Key prefix for storing media files in S3
    - `USER`:
        - `ACCESS_KEY_ID`, `SECRET_ACCESS_KEY`: respective key provide by AWS IAM user for programmatic access.
    - `CDN`: Cloud front domains for S3 bucket
        - `PRIMARY`: Custom domain name for Cloudfront CDN
        - `SECONDARY`: Another domain name for Cloudfront CDN. NOTE: SECONDARY will not be used any where.
        
### Step 4: Run servers
Run these server in *separate* terminals
- Postgres
- Django `./manage.py runserver 0.0.0.0:8000`
- Redis `redis-server`
- Celery `celery worker -l info -A __config__`

### Step 5: Test
There are total 9 passing test with 0 errors and 0 failure.
```shell script
./manage.py test
```
Also open [WebSocket browser test](http://localhost:8000/example/ws-browser-test/) to confirm that websocket is running correctly.  


If all the tests are not passing then there is some configuration issue in `secrets.json` or some server has not been started.

## Modes
There are three modes in the project:
- Development: Used for development environment (`DEBUG=True`, `PRODUCTION=False`)
- Staging: When testing deployment to AWS. You can see logs and trails of project (`DEBUG=True`, `PRODUCTION=True`)
- Production: When deploying final production application.

## Secrets in CI/CD
Normally any CI/CD will need all the `secrets` defined in `secrets.json` but coming 
this file to version control is not safe. We created a utility for commit secrets to version control in safe way.  
A dump file will be created with AES encryption to protect secrets.

```shell script
./encrypt.py -g
```

Save `DJANGO_CONFIG_PRIVATE_KEY` and `DJANGO_CONFIG_PUBLIC_KEY` with respective value.  
You can use `--generate` to generate random keys.

```text
usage: encrypt.py [-h] [-i INPUT] [-o OUTPUT] [-e] [-g]
                  [--public-key PUBLIC_KEY] [--private-key PRIVATE_KEY]

Creates encrypted secrets file which can be committed to repo or can be used
in CI/CD.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file path to be encrypted
  -o OUTPUT, --output OUTPUT
                        Output file path
  -e, --use-env         Use environment variable
  -g, --generate        Generate random strong Public key and Private key
  --public-key PUBLIC_KEY
                        Public key of 16 character
  --private-key PRIVATE_KEY
                        Private key which can be of 16, 24, 32 character
```

---
[django-rest-framework]: https://www.django-rest-framework.org
[djangorestframework-simplejwt]: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
[channels]: https://channels.readthedocs.io/en/latest/
[celery]: https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
[redis]: https://redis.io
