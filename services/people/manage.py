# services/people/manage.py


import sys
import unittest

import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import People

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


@cli.command('populate_db')
def populate_db():
    """Populate the database with places."""
    db.session.add(People(
        name='Sensei Lamister',
        isAlive=True,
        placeId=1
    ))
    db.session.add(People(
        name='Aiba Stack',
        isAlive=True,
        placeId=3
    ))
    db.session.add(People(
        name='Joaquín Nevado',
        isAlive=True,
        placeId=3
    ))
    db.session.commit()


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
