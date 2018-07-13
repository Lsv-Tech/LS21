from rest_framework.routers import SimpleRouter

from apiscrap.views import RobotModelViewSet, TaskRobotModelViewSet

router = SimpleRouter()

router.register('robot', RobotModelViewSet)
router.register('tasks', TaskRobotModelViewSet)

urlpatterns = router.urls
