# How to deploy your pytorch model on heroku

```bash
cd path/with/Dockerfile

heroku login
# pass init "Name"  # if you use "credsStore": "pass" in ~/.docker/config.json
heroku container:login

heroku create
heroku container:push web -a your_app_name
heroku container:release web -a your_app_name
heroku logs --tail -a your_app_name
```

Open <https://your_app_name.herokuapp.com/static/test.html> in a browser
