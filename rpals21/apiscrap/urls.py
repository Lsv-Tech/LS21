from rest_framework.routers import SimpleRouter

from apiscrap.views import RobotModelViewSet, TaskRobotModelViewSet

router_project = SimpleRouter()

router_project.register('robot', RobotModelViewSet)
router_project.register('tasks', TaskRobotModelViewSet)

urlpatterns = router_project.urls
