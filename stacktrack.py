#!/usr/bin/env python

# Usage:
# ./stacktrack.py [one or more tags]
# Track fresh python or ruby questions
# ./stacktrack.py python ruby
# Track only questions with tags django and orm
# ./stacktrack.py 'django;orm'

# Author: Alexander Artemenko <svetlyak.40wt@gmail.com>

import sys
import subprocess
import stackexchange
import time
import datetime

_default_tags = [
    'python',
    'django',
    'flask',
    'mongo',
]

def notify(message):
    try:
        subprocess.call('growl "%s"' % message.replace('"', "'"), shell=True)
    except Exception, e:
        pass


def main():
    tags = sys.argv[1:] or _default_tags
    seen_ids = set()

    so = stackexchange.Site(stackexchange.StackOverflow)
    so.be_inclusive()
    query = stackexchange.QuestionsQuery(so)

    while True:
        questions = []
        for tag in tags:
            questions.extend(query.no_answers(pagesize=3, tagged=tag)[:3])

        for question in questions:
            if question.id not in seen_ids:
                notify(question.title)

                print '%s %3d  %3d\t%s [%s] (%s)' % (
                    question.creation_date,
                    question.score,
                    question.view_count,
                    question.title,
                    ', '.join(question.tags),
                    question.url,
                )
                seen_ids.add(question.id)

        time.sleep(10)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
