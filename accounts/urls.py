from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers


from .api import (
    ClassroomAPI,
    FramerAPI,
    LoginAPI,
    ProjectViewSet,
    PromotionAPI,
    RegisterAPI,
    SkillViewSet,
    StudentAPI,
    TaskViewSet,
    TeacherAPI,
    UserAPI,
    UsersAPI,
    TaskCommentViewSet,
    DepartmentAPI,
    AttachmentsViewSet,
    ConventionMessageViewSet,
    RapportCommentViewSet,
    NotificationViewSet
)

router = routers.DefaultRouter()
router.register('students', StudentAPI, 'student')
router.register('teachers', TeacherAPI, 'teacher')
router.register('framers', FramerAPI, 'framer')
router.register('skills', SkillViewSet, 'skills')
router.register('classroom', ClassroomAPI, 'classroom')
router.register('task', TaskViewSet, 'task')
router.register('project', ProjectViewSet, 'project')
router.register('attachments', AttachmentsViewSet, 'attachment')
router.register('conv-messages', ConventionMessageViewSet, 'conventionMessage')
router.register('task-comments', TaskCommentViewSet, 'taskComments')
router.register('rapport-comments', RapportCommentViewSet, 'rapportComments')
router.register('notifications', NotificationViewSet, 'notification')

urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/users', UsersAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
    path('promos', PromotionAPI.as_view()),
    path('department', DepartmentAPI.as_view()),
] + router.urls
