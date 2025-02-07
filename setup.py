#!/usr/bin/env python
"""
sentry-plugins
==============

All of the plugins for Sentry (https://github.com/getsentry/sentry)

:copyright: 2018 by the Sentry Team
:license: Apache, see LICENSE for more details.
"""
from __future__ import absolute_import

from distutils.command.build import build as BuildCommand
from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as SDistCommand
from setuptools.command.develop import develop as DevelopCommand

from sentry.utils.distutils import (BuildAssetsCommand)

VERSION = '10.0.0.dev0'

tests_require = [
    'exam',
    'flake8>=3.5.0<3.6.0',
    'sentry-flake8>=0.0.1',
    'pycodestyle>=2.3.1<2.4.0',
    'responses',
    'sentry>=8.9.0',
    'pytest-cov>=2.5.1,<2.6.0',
    'pyjwt>=0.3.2',
]

install_requires = [
    'BeautifulSoup>=3.2.1',
    # sentry also requires this, so we're just enforcing that it needs to exist
    'boto3>=1.4.4,<1.5.0',
    'cached-property',
    'mistune',
    'phabricator>=0.6.0,<1.0',
    'python-dateutil',
    'PyJWT',
    'requests-oauthlib>=0.3.0',
    'unidiff>=0.5.4'
]


class BuildAssetsCommand(BuildAssetsCommand):
    def get_dist_paths(self):
        return [
            'src/sentry_plugins/jira/static/jira/dist',
            'src/sentry_plugins/sessionstack/static/sessionstack/dist',
        ]


class SentrySDistCommand(SDistCommand):
    sub_commands = SDistCommand.sub_commands + \
        [('build_assets', None)]

    def run(self):
        cmd_obj = self.distribution.get_command_obj('build_assets')
        cmd_obj.asset_json_path = 'sentry_plugins/assets.json'
        SDistCommand.run(self)


class SentryBuildCommand(BuildCommand):
    def run(self):
        BuildCommand.run(self)
        cmd_obj = self.distribution.get_command_obj('build_assets')
        cmd_obj.asset_json_path = 'sentry_plugins/assets.json'
        self.run_command('build_assets')


class SentryDevelopCommand(DevelopCommand):
    def run(self):
        DevelopCommand.run(self)
        cmd_obj = self.distribution.get_command_obj('build_assets')
        cmd_obj.asset_json_path = 'sentry_plugins/assets.json'
        self.run_command('build_assets')


cmdclass = {
    'sdist': SentrySDistCommand,
    'develop': SentryDevelopCommand,
    'build': SentryBuildCommand,
    'build_assets': BuildAssetsCommand,
}

setup(
    name='sentry-plugins',
    version=VERSION,
    author='Sentry',
    author_email='hello@sentry.io',
    url='https://github.com/getsentry/sentry-plugins',
    description='A collection of Sentry extensions',
    long_description=__doc__,
    license='Apache',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    cmdclass=cmdclass,
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'jira_ac = sentry_plugins.jira_ac',
            'jira = sentry_plugins.jira',
            'sessionstack = sentry_plugins.sessionstack',
        ],
        'sentry.plugins': [
            'amazon_sqs = sentry_plugins.amazon_sqs.plugin:AmazonSQSPlugin',
            'asana = sentry_plugins.asana.plugin:AsanaPlugin',
            'bitbucket = sentry_plugins.bitbucket.plugin:BitbucketPlugin',
            'clubhouse = sentry_plugins.clubhouse.plugin:ClubhousePlugin',
            'github = sentry_plugins.github.plugin:GitHubPlugin',
            'gitlab = sentry_plugins.gitlab.plugin:GitLabPlugin',
            'heroku = sentry_plugins.heroku.plugin:HerokuPlugin',
            'jira = sentry_plugins.jira.plugin:JiraPlugin',
            'jira_ac = sentry_plugins.jira_ac.plugin:JiraACPlugin',
            'pagerduty = sentry_plugins.pagerduty.plugin:PagerDutyPlugin',
            'phabricator = sentry_plugins.phabricator.plugin:PhabricatorPlugin',
            'pivotal = sentry_plugins.pivotal.plugin:PivotalPlugin',
            'pushover = sentry_plugins.pushover.plugin:PushoverPlugin',
            'segment = sentry_plugins.segment.plugin:SegmentPlugin',
            'sessionstack = sentry_plugins.sessionstack.plugin:SessionStackPlugin',
            'slack = sentry_plugins.slack.plugin:SlackPlugin',
            'splunk = sentry_plugins.splunk.plugin:SplunkPlugin',
            'victorops = sentry_plugins.victorops.plugin:VictorOpsPlugin',
            'vsts = sentry_plugins.vsts.plugin:VstsPlugin',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers', 'Intended Audience :: System Administrators',
        'Operating System :: OS Independent', 'Topic :: Software Development'
    ],
)
