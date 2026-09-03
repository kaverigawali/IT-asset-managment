from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Employee, Asset, Activity


# =========================================================
# HOME
# =========================================================

def home(request):

    total_assets = Asset.objects.count()
    total_employees = Employee.objects.count()

    assigned_assets = Asset.objects.filter(
        status="Assigned"
    ).count()

    available_assets = Asset.objects.filter(
        status="Available"
    ).count()

    repair_assets = Asset.objects.filter(
        status="Repair"
    ).count()

    context = {
        "total_assets": total_assets,
        "total_employees": total_employees,
        "assigned_assets": assigned_assets,
        "available_assets": available_assets,
        "repair_assets": repair_assets,
    }

    return render(
        request,
        "home.html",
        context
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        role = request.POST.get(
            "role",
            "employee"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            messages.error(
                request,
                "Invalid username or password."
            )

            return render(
                request,
                "login.html"
            )

        # =================================================
        # EMPLOYEE LOGIN
        # =================================================

        if role == "employee":

            employee = Employee.objects.filter(
                employee_id=username
            ).first()

            if employee is None:

                messages.error(
                    request,
                    "This account is not linked to an employee."
                )

                return render(
                    request,
                    "login.html"
                )

            login(
                request,
                user
            )

            request.session["role"] = "employee"

            request.session["employee_id"] = (
                employee.employee_id
            )

            return redirect("dashboard")

        # =================================================
        # IT SUPPORT LOGIN
        # =================================================

        elif role == "it_support":

            if not user.is_staff:

                messages.error(
                    request,
                    "This account is not authorized as IT Support."
                )

                return render(
                    request,
                    "login.html"
                )

            login(
                request,
                user
            )

            request.session["role"] = "it_support"

            return redirect("dashboard")

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("login")


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        role = request.POST.get("role")

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "register.html"
            )

        # =================================================
        # EMPLOYEE REGISTRATION
        # =================================================

        if role == "employee":

            employee_id = request.POST.get(
                "employee_id",
                ""
            ).strip()

            name = request.POST.get(
                "name",
                ""
            ).strip()

            email = request.POST.get(
                "email",
                ""
            ).strip()

            phone = request.POST.get(
                "phone",
                ""
            ).strip()

            department = request.POST.get(
                "department",
                ""
            ).strip()

            employee_role = request.POST.get(
                "employee_role",
                ""
            ).strip()

            joining_date = request.POST.get(
                "joining_date"
            )

            if Employee.objects.filter(
                employee_id=employee_id
            ).exists():

                messages.error(
                    request,
                    "Employee ID already exists."
                )

                return render(
                    request,
                    "register.html"
                )

            if Employee.objects.filter(
                email=email
            ).exists():

                messages.error(
                    request,
                    "Email already exists."
                )

                return render(
                    request,
                    "register.html"
                )

            if User.objects.filter(
                username=employee_id
            ).exists():

                messages.error(
                    request,
                    "An account with this Employee ID already exists."
                )

                return render(
                    request,
                    "register.html"
                )

            User.objects.create_user(
                username=employee_id,
                password=password
            )

            Employee.objects.create(
                employee_id=employee_id,
                name=name,
                email=email,
                phone=phone,
                department=department,
                role=employee_role,
                joining_date=joining_date
            )

            messages.success(
                request,
                "Employee account created successfully. Please login using your Employee ID."
            )

            return redirect("login")

        # =================================================
        # IT SUPPORT REGISTRATION
        # =================================================

        elif role == "it_support":

            username = request.POST.get(
                "username",
                ""
            ).strip()

            if User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return render(
                    request,
                    "register.html"
                )

            User.objects.create_user(
                username=username,
                password=password,
                is_staff=True
            )

            messages.success(
                request,
                "IT Support account created successfully. Please login."
            )

            return redirect("login")

        else:

            messages.error(
                request,
                "Please select a valid account type."
            )

    return render(
        request,
        "register.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    # =====================================================
    # LOGIN PROTECTION
    # =====================================================

    if not request.user.is_authenticated:
        return redirect("login")

    role = request.session.get("role")

    if role not in ["employee", "it_support"]:
        return redirect("login")

    # =====================================================
    # DASHBOARD DATA
    # =====================================================

    total_employees = Employee.objects.count()

    total_assets = Asset.objects.count()

    assigned_assets = Asset.objects.filter(
        status="Assigned"
    ).count()

    available_assets = Asset.objects.filter(
        status="Available"
    ).count()

    repair_assets = Asset.objects.filter(
        status="Repair"
    ).count()

    assigned_percentage = (
        assigned_assets / total_assets * 100
        if total_assets else 0
    )

    available_percentage = (
        available_assets / total_assets * 100
        if total_assets else 0
    )

    repair_percentage = (
        repair_assets / total_assets * 100
        if total_assets else 0
    )

    context = {
        "total_employees": total_employees,
        "total_assets": total_assets,
        "assigned_assets": assigned_assets,
        "available_assets": available_assets,
        "repair_assets": repair_assets,
        "assigned_percentage": assigned_percentage,
        "available_percentage": available_percentage,
        "repair_percentage": repair_percentage,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


# =========================================================
# PROFILE
# =========================================================

def profile(request):

    if not request.user.is_authenticated:
        return redirect("login")

    role = request.session.get("role")

    if role not in ["employee", "it_support"]:
        return redirect("login")

    employee = None

    assigned_assets = Asset.objects.none()

    if role == "employee":

        employee_id = request.session.get(
            "employee_id"
        )

        employee = Employee.objects.filter(
            employee_id=employee_id
        ).first()

        if employee:

            assigned_assets = Asset.objects.filter(
                assigned_employee=employee
            ).order_by("-updated_at")

    return render(
        request,
        "profile.html",
        {
            "user": request.user,
            "role": role,
            "employee": employee,
            "assigned_assets": assigned_assets,
        }
    )


# =========================================================
# ACTIVITY
# IT SUPPORT ONLY
# =========================================================

def activity(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("dashboard")

    activities = Activity.objects.select_related(
        "employee",
        "asset",
        "performed_by"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "activity.html",
        {
            "activities": activities
        }
    )


# =========================================================
# =========================================================
# CRUD OPERATIONS
# =========================================================
# =========================================================


# =========================================================
# CREATE - ADD EMPLOYEE
# IT SUPPORT ONLY
# =========================================================

def employee_add(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("dashboard")

    if request.method == "POST":

        employee_id = request.POST.get(
            "employee_id"
        )

        name = request.POST.get(
            "name"
        )

        email = request.POST.get(
            "email"
        )

        phone = request.POST.get(
            "phone"
        )

        department = request.POST.get(
            "department"
        )

        role = request.POST.get(
            "role"
        )

        joining_date = request.POST.get(
            "joining_date"
        )

        employee = Employee.objects.create(
            employee_id=employee_id,
            name=name,
            email=email,
            phone=phone,
            department=department,
            role=role,
            joining_date=joining_date
        )

        # REAL ACTIVITY

        Activity.objects.create(
            employee=employee,
            action="Employee Added",
            description=(
                f"Employee {employee.name} "
                f"({employee.employee_id}) was added."
            ),
            performed_by=request.user
        )

        messages.success(
            request,
            f"Employee {name} added successfully."
        )

        return redirect(
            "employees"
        )

    return render(
        request,
        "employee_form.html"
    )


# =========================================================
# CREATE - ADD ASSET
# IT SUPPORT ONLY
# =========================================================

def asset_add(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("assets")

    employees = Employee.objects.all()

    if request.method == "POST":

        assigned_employee_id = request.POST.get(
            "assigned_employee"
        )

        employee = None

        if assigned_employee_id:

            employee = get_object_or_404(
                Employee,
                id=assigned_employee_id
            )

        asset = Asset.objects.create(
            asset_name=request.POST.get(
                "asset_name"
            ),

            asset_id=request.POST.get(
                "asset_id"
            ),

            asset_tag=request.POST.get(
                "asset_tag"
            ),

            asset_type=request.POST.get(
                "asset_type"
            ),

            brand=request.POST.get(
                "brand"
            ),

            model=request.POST.get(
                "model"
            ),

            serial_number=request.POST.get(
                "serial_number"
            ),

            purchase_date=request.POST.get(
                "purchase_date"
            ),

            price=request.POST.get(
                "price"
            ),

            status=request.POST.get(
                "status"
            ),

            assigned_employee=employee,

            description=request.POST.get(
                "description"
            )
        )

        # REAL ACTIVITY

        Activity.objects.create(
            asset=asset,
            action="Asset Added",
            description=(
                f"Asset {asset.asset_id} "
                f"({asset.asset_name}) was added."
            ),
            performed_by=request.user
        )

        messages.success(
            request,
            "Asset added successfully."
        )

        return redirect(
            "assets"
        )

    return render(
        request,
        "asset_form.html",
        {
            "employees": employees
        }
    )


# =========================================================
# READ - EMPLOYEES
# IT SUPPORT ONLY
# =========================================================

def employees(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("dashboard")

    employees = Employee.objects.all()

    employees_with_assets = Employee.objects.filter(
        assets__isnull=False
    ).distinct().count()

    context = {
        "employees": employees,
        "employees_with_assets": employees_with_assets,
    }

    return render(
        request,
        "employees.html",
        context
    )


# =========================================================
# READ - EMPLOYEE DETAIL
# IT SUPPORT ONLY
# =========================================================

def employee_detail(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("dashboard")

    employee = get_object_or_404(
        Employee,
        id=id
    )

    return render(
        request,
        "employee_detail.html",
        {
            "employee": employee
        }
    )


# =========================================================
# READ - ASSETS
# =========================================================

def assets(request):

    if not request.user.is_authenticated:
        return redirect("login")

    role = request.session.get("role")

    # =====================================================
    # ASSETS BASED ON LOGIN ROLE
    # =====================================================

    if role == "it_support":

        assets = Asset.objects.all()

    elif role == "employee":

        employee_id = request.session.get(
            "employee_id"
        )

        employee = Employee.objects.filter(
            employee_id=employee_id
        ).first()

        if employee:

            assets = Asset.objects.filter(
                assigned_employee=employee
            )

        else:

            assets = Asset.objects.none()

    else:

        return redirect("login")

    # =====================================================
    # ACTUAL ASSET COUNTS
    # =====================================================

    total_assets = assets.count()

    assigned_assets = assets.filter(
        status="Assigned"
    ).count()

    available_assets = assets.filter(
        status="Available"
    ).count()

    repair_assets = assets.filter(
        status="Repair"
    ).count()

    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        assets = assets.filter(
            asset_name__icontains=search
        ) | assets.filter(
            asset_id__icontains=search
        ) | assets.filter(
            serial_number__icontains=search
        )

    # =====================================================
    # ASSET TYPE FILTER
    # =====================================================

    asset_type = request.GET.get(
        "asset_type",
        ""
    )

    if asset_type:

        assets = assets.filter(
            asset_type=asset_type
        )

    # =====================================================
    # STATUS FILTER
    # =====================================================

    status = request.GET.get(
        "status",
        ""
    )

    if status:

        assets = assets.filter(
            status=status
        )

    # =====================================================
    # SEND DATA TO TEMPLATE
    # =====================================================

    return render(
        request,
        "assets.html",
        {
            "assets": assets,

            "search": search,

            "selected_type": asset_type,

            "selected_status": status,

            "total_assets": total_assets,

            "assigned_assets": assigned_assets,

            "available_assets": available_assets,

            "repair_assets": repair_assets,
        }
    )


# =========================================================
# READ - ASSET DETAIL
# =========================================================

def asset_detail(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    asset = get_object_or_404(
        Asset,
        id=id
    )

    role = request.session.get(
        "role"
    )


    if role == "it_support":

        pass

    elif role == "employee":

        employee_id = request.session.get(
            "employee_id"
        )

        employee = Employee.objects.filter(
            employee_id=employee_id
        ).first()

        if employee is None:
            return redirect("login")

        if asset.assigned_employee != employee:
            return redirect("assets")

    else:

        return redirect("login")

    return render(
        request,
        "asset_detail.html",
        {
            "asset": asset
        }
    )


# =========================================================
# READ - ASSET LIST
# IT SUPPORT ONLY
# =========================================================

def asset_list(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("assets")

    assets = Asset.objects.all()

    return render(
        request,
        "asset_list.html",
        {
            "assets": assets
        }
    )


# =========================================================
# UPDATE - EDIT ASSET
# IT SUPPORT ONLY
# =========================================================

def asset_edit(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("assets")

    asset = get_object_or_404(
        Asset,
        id=id
    )

    # Store old status before editing

    old_status = asset.status

    employees = Employee.objects.all()

    if request.method == "POST":

        assigned_employee_id = request.POST.get(
            "assigned_employee"
        )

        employee = None

        if assigned_employee_id:

            employee = get_object_or_404(
                Employee,
                id=assigned_employee_id
            )

        asset.asset_name = request.POST.get(
            "asset_name"
        )

        asset.asset_id = request.POST.get(
            "asset_id"
        )

        asset.asset_tag = request.POST.get(
            "asset_tag"
        )

        asset.asset_type = request.POST.get(
            "asset_type"
        )

        asset.brand = request.POST.get(
            "brand"
        )

        asset.model = request.POST.get(
            "model"
        )

        asset.serial_number = request.POST.get(
            "serial_number"
        )

        asset.purchase_date = request.POST.get(
            "purchase_date"
        )

        asset.price = request.POST.get(
            "price"
        )

        asset.status = request.POST.get(
            "status"
        )

        asset.assigned_employee = employee

        asset.description = request.POST.get(
            "description"
        )

        asset.save()

        # =================================================
        # SENT FOR REPAIR
        # =================================================

        if old_status != "Repair" and asset.status == "Repair":

            Activity.objects.create(
                asset=asset,
                action="Sent for Repair",
                description=(
                    f"{asset.asset_id} "
                    f"({asset.asset_name}) "
                    f"was sent for repair."
                ),
                performed_by=request.user
            )

        # =================================================
        # REPAIR COMPLETED
        # =================================================

        if old_status == "Repair" and asset.status == "Available":

            Activity.objects.create(
                asset=asset,
                action="Repair Completed",
                description=(
                    f"{asset.asset_id} "
                    f"({asset.asset_name}) "
                    f"repair was completed."
                ),
                performed_by=request.user
            )

        # =================================================
        # GENERAL ASSET UPDATE
        # =================================================

        Activity.objects.create(
            asset=asset,
            action="Asset Updated",
            description=(
                f"Asset {asset.asset_id} "
                f"({asset.asset_name}) was updated."
            ),
            performed_by=request.user
        )

        messages.success(
            request,
            "Asset updated successfully."
        )

        return redirect(
            "assets"
        )

    return render(
        request,
        "asset_form.html",
        {
            "asset": asset,
            "employees": employees
        }
    )


# =========================================================
# UPDATE - ASSIGN ASSET
# IT SUPPORT ONLY
# =========================================================

def assign_asset(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("assets")

    asset = get_object_or_404(
        Asset,
        id=id
    )

    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get(
            "employee"
        )

        if not employee_id:

            messages.error(
                request,
                "Please select an employee."
            )

            return render(
                request,
                "assign_asset.html",
                {
                    "asset": asset,
                    "employees": employees
                }
            )

        employee = get_object_or_404(
            Employee,
            id=employee_id
        )

        asset.assigned_employee = employee

        asset.status = "Assigned"

        asset.save()

        # REAL ACTIVITY

        Activity.objects.create(
            asset=asset,
            employee=employee,
            action="Asset Assigned",
            description=(
                f"{asset.asset_id} was assigned "
                f"to {employee.name} ({employee.employee_id})."
            ),
            performed_by=request.user
        )

        messages.success(
            request,
            f"{asset.asset_name} assigned successfully to {employee.name}."
        )

        return redirect(
            "assets"
        )

    return render(
        request,
        "assign_asset.html",
        {
            "asset": asset,
            "employees": employees
        }
    )


# =========================================================
# UPDATE - RETURN ASSET
# IT SUPPORT ONLY
# =========================================================

def return_asset(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("assets")

    asset = get_object_or_404(
        Asset,
        id=id
    )

    # Check whether asset is actually assigned

    if not asset.assigned_employee:

        messages.error(
            request,
            "This asset is not assigned to any employee."
        )

        return redirect(
            "asset_detail",
            id=asset.id
        )

    employee = asset.assigned_employee

    # =====================================================
    # RETURN ASSET
    # =====================================================

    asset.assigned_employee = None

    asset.status = "Available"

    asset.save()

    # REAL ACTIVITY

    Activity.objects.create(
        asset=asset,
        employee=employee,
        action="Asset Returned",
        description=(
            f"{asset.asset_id} was returned by "
            f"{employee.name} ({employee.employee_id})."
        ),
        performed_by=request.user
    )

    messages.success(
        request,
        f"{asset.asset_name} returned successfully."
    )

    return redirect(
        "asset_detail",
        id=asset.id
    )


# =========================================================
# DELETE - ASSET
# IT SUPPORT ONLY
# =========================================================

def asset_delete(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.session.get("role") != "it_support":
        return redirect("assets")

    asset = get_object_or_404(
        Asset,
        id=id
    )

    if request.method == "POST":

        # Save activity before deleting asset

        Activity.objects.create(
            asset=asset,
            action="Asset Deleted",
            description=(
                f"Asset {asset.asset_id} "
                f"({asset.asset_name}) was deleted."
            ),
            performed_by=request.user
        )

        asset.delete()

        messages.success(
            request,
            "Asset deleted successfully."
        )

        return redirect(
            "assets"
        )

    return render(
        request,
        "asset_confirm_delete.html",
        {
            "asset": asset
        }
    )