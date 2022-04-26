from django.urls import path
from . import views 

app_name = 'memo' 

urlpatterns = [
    path('list/', views.MemoListView.as_view(), name='list'), 
    path('detail/<int:pk>/', views.MemoDetailView.as_view(), name='detail'), #pkok
    path('create/', views.MemoCreateView.as_view(), name='create'),
    path('subcreate/', views.MemoSUBCreateView.as_view(), name='subcreate'),
    path('subcomplete/',views.subcomplete, name='subcomplete'),
    path('update/<int:pk>/', views.MemoUpdateView.as_view(), name='update'), #pkok
    # path('delete/<int:pk>/', views.MemoDeleteView.as_view(), name='delete'),
]