from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # LOGIN
    path("", views.requisition_list, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # ADMIN XODÓ (área interna)
    path("xodo-admin/login/", views.admin_login_view, name="admin_login"),
    path("xodo-admin/", views.admin_home, name="admin_home"),
    path("xodo-admin/pedidos/", views.order_list, name="order_list"),
    path("xodo-admin/pedidos/pdf/<int:id>/", views.generate_pdf, name="generate_pdf"),
    path("xodo-admin/dashboard/", views.dashboard, name="dashboard"),

    # USUÁRIO COMUM
    path("requisicoes/", views.requisition_list, name="requisition_list"),
    path("requisicao/<int:id>/", views.requisition_detail, name="requisition_detail"),
    path("requisicao/<int:id>/enviar/", views.send_order, name="send_order"),
    path("meus-pedidos/", views.user_orders, name="user_orders"),
    path("pedido-enviado/", views.order_sent, name="order_sent"),

    # DJANGO ADMIN ORIGINAL
    path("admin/", admin.site.urls),
]
