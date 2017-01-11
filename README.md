
Useful commands
```
$ sudo su - postgres
$ pg_dump -U postgres rulebookdb -f rulebookdb-`date -u +"%Y-%m-%dT%H:%M:%SZ"`.sql

$ sudo mv /var/lib/postgresql/rulebookdb-2016-12-30T20:03:56Z.sql /home/lvisintini/src/xwing-rulebook/backups/rulebookdb-2016-12-30T20:03:56Z.sql
$ sudo chown lvisintini:lvisintini /home/lvisintini/src/xwing-rulebook/backups/rulebookdb-2016-12-30T20:03:56Z.sql

$ python xwing_rulebook/manage.py book_markdown --book URR-SWX > outputs/urr-swx.md
$ python xwing_rulebook/manage.py rules_json > outputs/rules.json

& git submodule update --recursive --remote
```