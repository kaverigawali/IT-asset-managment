from django.contrib import admin
from django.urls import path
from asset import views


urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Home
    path("", views.home, name="home"),

    # Login
    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register_view, name="register"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    path("assets/<int:id>/assign/", views.assign_asset, name="assign_asset"),
    path("assets/<int:id>/return/", views.return_asset, name="return_asset"),  

    

    # Employees
    path("employees/", views.employees, name="employees"),
    path(
        "employees/<int:id>/",
        views.employee_detail,
        name="employee_detail"
    ),
    path(
        "employees/add/",
        views.employee_add,
        name="employee_add"
    ),

    # Assets
    path("assets/", views.assets, name="assets"),
    path(
        "assets/<int:id>/",
        views.asset_detail,
        name="asset_detail"
    ),
    path(
        "assets/add/",
        views.asset_add,
        name="asset_add"
    ),
    path(
        "assets/<int:id>/edit/",
        views.asset_edit,
        name="asset_edit"
    ),

    path(
    "assets/<int:id>/delete/",
    views.asset_delete,
    name="asset_delete"
    ),

    # Assign Asset
    path(
        "assets/<int:id>/assign/",
        views.assign_asset,
        name="assign_asset"
    ),

    # Profile
    path("profile/", views.profile, name="profile"),

    # Activity
    path("activity/", views.activity, name="activity"),
]