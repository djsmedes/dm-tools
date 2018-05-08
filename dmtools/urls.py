"""dmtools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from base.views import HomepageView, \
    update_effect_list, remove_effect, remove_combatants, \
    update_initiative, poll_for_combatant_updates, \
    update_all_combatants

breadcrumbs = [
    {'href': '/', 'text': 'Home'},
]

ajax_patterns = [
    path('update-effect-list/', update_effect_list, name='ajax-update-effect-list'),
    path('remove-effect/', remove_effect, name='ajax-remove-effect'),
    path('remove-combatants/', remove_combatants, name='ajax-remove-combatants'),
    path('update-initiative/', update_initiative, name='ajax-update-initiative'),
    path('poll/', poll_for_combatant_updates, name='ajax-poll-update-combatants'),
    path('update-all-combatants/', update_all_combatants, name='ajax-update-all-combatants'),
]

accounts_patterns = [
    path('login/', auth_views.LoginView.as_view(template_name='base/accounts/login.html'), name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout')
]

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(extra_context={'breadcrumbs': breadcrumbs}), name='home'),
    path('', include('base.urls')),
    path('', include('people.urls')),
    path('', include('statblocks.urls')),
    path('', include('places.urls')),
    path('plot/', include('plot.urls')),
    path('ajax/', include(ajax_patterns)),
    path('accounts/', include(accounts_patterns)),
    path('api-auth/', include('rest_framework.urls')),
]
