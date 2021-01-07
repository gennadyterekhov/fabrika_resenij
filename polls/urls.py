from django.urls import path, include


from polls import views




app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/post_answer/', views.post_answer, name='post_answer'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),

    path('generate_token/', views.generate_token, name='generate_token'),
]
