"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'the_voice.menu.CustomMenu'
"""

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for The Voice admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            items.AppList(
                _('ALL'),
            ),
            items.AppList(
                _('Accounts'),
                models=(
                    'the_voice.users.*',
                    'the_voice.performances.*',
                    'the_voice.accounts.*',
                    'allauth.*',
                    'rest_framework.*',
                )
            ),

            items.AppList(
                _('Administration'),
                models=(
                    'django.contrib.*',
                )
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
