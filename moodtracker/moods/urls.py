from django.urls import path
from . import views


urlpatterns = [
    path('', views.log_mood, name='log_mood'),
    path('summary/', views.mood_summary, name='summary'),
    path('filter/', views.filter_logs, name='filter_logs'),
    path('insights/', views.advanced_insights, name='advanced_insights'),
    path('chart-data/', views.mood_chart_data, name='chart_data'),
    path('swing-chart-data/', views.swing_chart_data, name='swing_chart_data'),
]