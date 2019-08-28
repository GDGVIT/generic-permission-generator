from django.urls import path
from . import views
urlpatterns = [
    path('upload/', views.UploadDocument.as_view()),
    path('pdf/', views.GeneratePDF.as_view()),
    path('mytemplates/', views.AvailableTemplateViewsForUser.as_view()),
]
