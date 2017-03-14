
Useful commands
```
$ sudo su - postgres
$ pg_dump -U postgres rulebookdb -f rulebookdb-`date -u +"%Y-%m-%dT%H:%M:%SZ"`.sql
$ exit
$ sudo mv /var/lib/postgresql/rulebookdb-201 /home/lvisintini/src/xwing-rulebook/backups/
$ sudo chown lvisintini:lvisintini /home/lvisintini/src/xwing-rulebook/backups/*

$ psql rulebookdb < /home/lvisintini/src/xwing-rulebook/backups/rulebookdb-2017-03-13T12\:20\:00Z.sql

$ python xwing_rulebook/manage.py book_markdown URR-SWX > outputs/urr-swx.md
$ python xwing_rulebook/manage.py rules_json > outputs/rules.json
$ python xwing_rulebook/manage.py sources_json > outputs/sources.json

& git submodule update --recursive --remote

$ python xwing_rulebook/manage.py book_alpha_order URR-SWX

$ git tag -a AlanTuring-20170301 -m "Release rc_20170227"
$ git push origin AlanTuring-20170301
```

[Link to mermaid graph](http://knsv.github.io/mermaid/live_editor/#/edit/Z3JhcGggVEIKU1RBUlQtLT5BCkEtLT5CCnN1YmdyYXBoIEF0dGFja2VyCiAgICBCLS0-QwplbmQKQy0tPkQKc3ViZ3JhcGggRGVmZW5kZXIKICAgIEQtLT5GCmVuZApGLS0-RwpHLS0-SApILS0gWWVzIC0tPkkKSC0tIE5vIC0tPkoKSS0tPkoKSi0tIFllcyAtLT5CCkogLS0gTm8gLS0-SwpLLS0-TApMLS0-TQpNLS1ZZXMtLT5OCk0tLU5vLS0-QQpOLS0-RU5E)