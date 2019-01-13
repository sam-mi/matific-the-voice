Install
=========

how to set up The Voice test::

    git clone https://github.com/sam-mi/matific-the-voice.git

    mkvirtualenv thevoice -p python3

    createdb the_voice

    pip install -r requirements/local.txt
    pip install -r requirements/test.txt

    ./manage.py migrate
    ./manage.py populate_users


Users generally use the format `username@testuser.com` with password `matifictest`

