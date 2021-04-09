from rest_framework import generics, status, mixins, permissions, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from . import models
from . import serializers


@api_view(['GET'])
def top(request, format=None):
    return Response({
        'home': reverse('home', request=request),
        'api_v1': reverse('review_api:course_list', request=request),
        'api_v2': reverse('apiv2:api-root', request=request),
    })


class CourseApi(APIView):
    def get(self, request, format=None):
        courses = models.Course.objects.all()
        serializer = serializers.CourseSerializer(courses, many=True,
                                                  context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()  # 省略
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        # 省略
        pass

    def delete(self, request, format=None):
        # 省略
        pass


class ListCourse(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    # "UnorderedObjectListWarning" on Paginating


class RetrieveCourse(generics.RetrieveAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        course = get_object_or_404(
            models.Course, pk=self.kwargs.get('course_pk'))
        serializer.save(course=course)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            course_id=self.kwargs.get('course_pk'),
            pk=self.kwargs.get('pk')
        )


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class CourseViewSet(viewsets.ModelViewSet):
    """Create, Retrieve, Update, Delete, List"""
    permission_classes = (
        IsSuperUser,
        permissions.DjangoModelPermissions,
    )  # "AND"
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('id', 'title',)  # OrderingFilter
    ordering = ('title',)  # UnorderedObjectListWarning

    @action(methods=['get'], detail=True)
    def reviews(self, request, pk=None):
        """
        /courses/2/reviews/
        ネストに対しては、default paginatorは適用されないので、カスタムで行う必要がある
        """
        self.pagination_class.page_size = 1
        reviews = models.Review.objects.filter(course_id=pk).order_by('-created_at')

        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = serializers.ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Create, Retrieve, Update, Delete, except List (405 Method not allowed)"""
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
