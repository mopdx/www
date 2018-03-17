from __future__ import print_function
from builtins import str
from users.models import *
from grants.models import *
from django.utils.text import slugify

import json
import markdown

# Speaker JSON dumper

full = Resource.objects.get(name='30 minute talk')
thunder = Resource.objects.get(name='Thunderstorm talk')
panel = Resource.objects.get(name='Panel')

to_json = []

all_talks = full.allocations.all() | thunder.allocations.all()

use_email = False
use_json = True

# JSON Output

if use_json:

    for source in all_talks:
        app = source.applicant
        to_json.append({
            'slug': slugify(app.name),
            'name': app.name,
            'title': app.answers.get(question__question='Talk Title').answer.encode('utf-8'),
            'abstract': markdown.markdown(str(
                app.answers.get(question__question='Talk Abstract').answer.encode('utf-8'), 'utf-8'
            )),
            'details': '',
        })

    print(json.dumps(to_json, indent=4))

# Speaker List in email

if use_email:

    for source in all_talks:
        app = source.applicant
        print("* {name} - [{title}](/conf/na/2016/speakers/#speaker-{slug})".format(**{
            'slug': slugify(app.name),
            'name': app.name,
            'title': app.answers.get(question__question='Talk Title').answer.encode('utf-8'),
        }))
