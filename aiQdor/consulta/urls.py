from django.urls import path

from django.contrib.auth.decorators import login_required

from . import views

# 'url'/<include>
urlpatterns = [
    path('', views.user_consulta, name='user-consulta'),
    path('consulta/<int:id>', views.EditarConsultaView.as_view(), name='editar-consulta'),
    path('consulta_desmarcar/<int:id>', login_required(views.DesmarcarConsultaView.as_view()), name='desmarcar-consulta'),
]
