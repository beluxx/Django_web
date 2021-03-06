
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from .drf_views import UserViewSet, GroupViewSet, ArticleListSet, CategoryListSet,  AllArticleRssFeed, ArticleSearchView, test_apiview, test, DepartmentViewSet
from django.conf.urls import include
from apps.index.views import HelloView

router = routers.DefaultRouter()
router.register(r'all_users', UserViewSet)
router.register(r'user_groups', GroupViewSet)
router.register(r'all_categorys', CategoryListSet)
router.register(r'all_articles', ArticleListSet)
router.register(r'all_dapartments', DepartmentViewSet)
# router.register(r'all_tools', ToolLinkListSet)
router.register(r"search", ArticleSearchView, basename="search")

# rest_framework框架
urlpatterns = [
    # path('rest_framework/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("rest_framework/", include(router.urls)),
    url(r"^test/", test_apiview.as_view(), name="RunCase"),  # 执行单个接口下所有用例
    # 执行单个接口下所有用例, name="RunCase"),  # 执行单个接口下所有用例
    url(r"^123", test, name="123")
]

# rss订阅
urlpatterns += [
    url(r'rss/$', AllArticleRssFeed(), name='rss'),
]

# 自定义api
urlpatterns += [
    path('hello', HelloView.as_view()),
]
