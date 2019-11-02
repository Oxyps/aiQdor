# Admin
from django.contrib import admin
# Autenticação
from django.contrib.auth import views as auth_views
# Para Os Caminhos
from django.urls import path, include

# Views
from user import views as user_views
from dentista import views as dentista_views
from consulta import views as consulta_views

# 'url'/<include>
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cadastro/', user_views.register, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('consulta/', include('consulta.urls'), name='consulta'),
    path('perfil/', user_views.perfil, name='perfil'),
    path('perfil_edit/', user_views.perfil_edit, name='perfil-edit'),
    path('lista_dentistas/', dentista_views.listaDentista, name='lista-dentistas'),
    path('agendar_consulta', consulta_views.AgendarConsultaView.as_view(), name='agendar-consulta'),
    #path('consulta/<int:id>', consulta_views.consulta_edit, name='editar-consulta/<int:id>'),
]

