"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'config.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'config.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for the_voice.
    """
    columns = 2

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Content Portal (CMS)'), '/cms/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        self.children.append(modules.Group(
            title="Core",
            display="tabs",
            children=[
                modules.AppList(
                    title='Context',
                    models=(
                        'metavision.core.*',
                        'django_context.*',
                        'invitations.*',
                        'django_proximity_roles.*',
                    )
                ),
                modules.AppList(
                    title='Performances',
                    models=(
                        'the_voice.performances.*',
                    )
                ),
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 12))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5,
        ))

        self.children.append(modules.Group(
            title="Accounts",
            display="tabs",
            children=[
                modules.AppList(
                    title='Users',
                    models=(
                        'the_voice.users.*',
                        'django_proximity_roles.*',
                    )
                ),
                modules.AppList(
                    title='Accounts',
                    models=(
                        'accounts.*',
                    )
                ),
                modules.AppList(
                    title='Authentication',
                    models=(
                        'allauth.*',
                        'rest_framework.*',
                    )
                ),
                modules.AppList(
                    title='Mailing Lists',
                    models=(
                        'django_common.mailing_list.*',
                    )
                ),
                # modules.AppList(
                #     title='Invitations',
                #     models=(
                #         'the_voice.vsinvitations.*',
                #         'invitations.*',
                #     )
                # ),
                modules.AppList(
                    title='File Resources',
                    models=(
                        'django_common.file.resources.*',
                    )
                ),
            ]
        ))

        self.children.append(modules.Group(
            title="Administration",
            display="tabs",
            children=[
                # modules.AppList(
                #     title='Ticket Tracker',
                #     models=(
                #         'the_voice.tracker.*',
                #     )
                # ),
                modules.AppList(
                    title='Administration',
                    models=(
                        'django.contrib.*',
                    )
                ),
                modules.AppList(
                    title='Users',
                    models=(
                        'the_voice.users.*',
                        'django_proximity_roles.*',
                    )
                ),
                
                modules.AppList(
                    title='Sites',
                    models=(
                        'django.contrib.sites.models.Site',
                    )
                )
            ]
        ))

        self.children.append(modules.Group(
            title="Scheduled Tasks",
            display="tabs",
            children=[
                modules.AppList(
                    title='Scheduled Tasks',
                    models=(
                        'django_celery_beat.*',
                    )

                ),
                modules.AppList(
                    title='Task Results',
                    models=(
                        'django_celery_results.*',
                    )

                )
            ]
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))


        # append an app list module for "Applications"
        # self.children.append(modules.AppList(
        #     _('Applications'),
        #     exclude=('django.contrib.*',),
        # ))

        # append an app list module for "Administration"
        # self.children.append(modules.AppList(
        #     _('Administration'),
        #     models=('django.contrib.*',),
        # ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for the_voice.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
