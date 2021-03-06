from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'genetic_tac_toe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^move/(\d{1})$', 'genetic_tac_toe.core.views.render_move'),
    url(r'^restart/', 'genetic_tac_toe.core.views.restart'),
    url(r'^$', 'genetic_tac_toe.core.views.interface'),

)
