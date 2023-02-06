from rest_framework import viewsets, permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import LimitOffsetPagination

from .models import Achievement, Cat, User
from .permissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle
from .pagination import CatsPagination

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,) # подключаем разрешения
    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle) # Подключили класс AnonRateThrottle
    # А далее применится лимит low_request
    # Для любых пользователей установим кастомный лимит 1 запрос в минуту
    throttle_scope = 'low_request'
    # Для PageNumberPagination, установленного в классе, параметр PAGE_SIZE 
    # будет взят из словаря REST_FRAMEWORK в settings.py.
    # Если пагинация установлена на уровне проекта, то для отдельного класса 
    # её можно отключить, установив для атрибута pagination_class значение None.
    # pagination_class = PageNumberPagination
    # Даже если на уровне проекта установлен PageNumberPagination
    # Для котиков будет работать LimitOffsetPagination
    # pagination_class = LimitOffsetPagination
    # Вот он наш собственный класс пагинации с page_size=20
    pagination_class = CatsPagination

    def get_permissoins(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернем обновленный перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer