To run the app, run the following in the bash:

```
$ git pull https://github.com/MelnNik/django1003 master
$ pipenv install
$ python manage.py runserver
```

Refresh your local git environment with what is on GitHub.

```
$ git fetch
$ git merge
```

To update the model: Add phrases to ./ai/components/intents.json and run ./ai/components/training_model.py before starting the server. Make sure you have NLTK
library locally installed.




