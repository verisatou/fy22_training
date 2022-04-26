from django.urls import path
from . import views

app_name = 'feedback' 

urlpatterns = [
    path('mypage/', views.index, name='mypage'), 
    #全体宛
    path('list/', views.FeedbackListView.as_view(), name='list'), 
    path('detail/<int:pk>/', views.FeedbackDetailView.as_view(), name='detail'), #pk問題ok
    #個人宛
    path('private_list/', views.FeedbackPrivateListView.as_view(), name='private_list'), 
    path('private_detail/<int:pk>/', views.FeedbackPrivateReplyDetailView.as_view(), name='private_detail'),#pk問題ok
    #フィードバック投稿
    path('create/', views.FeedbackCreateView.as_view(), name='create'), 
    path('update/<int:pk>/', views.FeedbackUpdateView.as_view(), name='update'),#pk問題ok
    #path('delete/<int:pk>/', views.FeedbackDeleteView.as_view(), name='delete'), #使わない
    #履歴一覧 、詳細
    path('history/', views.FeedbackHistoryListView.as_view(), name='history'),
    path('history_detail/<int:pk>/', views.FeedbackHistoryDetailView.as_view(), name='history_detail'), #pk問題ok
    #返信の作成
    #path('reply_create/<int:pk>/', views.ReplyCreateView.as_view(), name='reply_create'), #使わない
]