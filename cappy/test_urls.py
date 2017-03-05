from cappy.core.urls import URL

urlpatterns = [
    URL(r'^(?P<slug>[-\w]+)/(?P<slug_b>[-\w]+)/$','cappy.test_views.generic_view',name='generic-view'),
    URL(r'^(?P<slug>[-\w]+)/(?P<slug_b>[-\w]+)/b/$','cappy.test_views.cool_view',name='generic-view-b'),
]