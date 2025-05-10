from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('comptes/inscription/', views.inscription, name='inscription'),
    path('comptes/logout/', views.logout_view, name='logout'),

    path('comptes/login/', CustomLoginView.as_view(), name='login'),
    # les pages de equipment ###############################################################
    path('comptes/equipments/', views.equipment_list, name='equipments'),
    path('comptes/equipments/add/', views.add_equipment, name='add_equipment'),
    path('comptes/equipments/edit/<int:N>/', views.edit_equipment, name='edit_equipment'),
    path('comptes/equipments/delete/<int:N>/', views.delete_equipment, name='delete_equipment'),
    path('pareto/', views.pareto_chart, name='pareto'),
    ###### page personnel ##################################################################
    path('comptes/personnel/', views.personnel_avec_radar,name='personnel_list'),
    #path('personnel/radar/', views.radar_plot, name='radar_plot'),
    path('personnel/ajouter/', views.add_personnel, name='add_personnel'),
    path('personnel/modifier/<int:N>/', views.edit_personnel, name='edit_personnel'),
    path('personnel/supprimer/<int:N>/', views.delete_personnel, name='delete_personnel'),
    #### page de historique #################################################################
    path('comptes/historique/', views.Historique, name='historique'),

    #########################################################################################
    path('pareto/', views.pareto_chart, name='pareto'),

    #### page de PDR ########################################################################
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    #### page de planning ###################################################################
    path('comptes/planning/', views.planning_view, name='planning'),
    path('save-planning/', views.save_planning, name='save_planning'),
    #### page de bon de travail ############################################################
    path('comptes/Bon_travail/', views.bon_form_view, name='bon_form'),
    path('bon/<int:pk>/pdf/', views.bon_pdf_view, name='bon_pdf'),
    ##### page de declaration de panne #####################################################
    path('comptes/declarer_panne',views.declarer_panne,name='declarer_panne'),
    path('success/', views.success_page, name='success_page'),
]