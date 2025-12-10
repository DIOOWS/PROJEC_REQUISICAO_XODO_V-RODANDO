import io
import base64
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Sum
from django.conf import settings

import qrcode
import traceback


from core.models import Order, Requisition, OrderItem

try:
    from weasyprint import HTML
except Exception:
    HTML = None


# --------------------------------------------------------------------
# Utilitário
# --------------------------------------------------------------------
def get_pending_orders():
    return Order.objects.filter(is_read=False).count()


# --------------------------------------------------------------------
# LOGIN / LOGOUT PÚBLICO
# --------------------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            redirect_url = request.GET.get("next", "requisition_list")
            return redirect(redirect_url)

        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# --------------------------------------------------------------------
# LOGIN ADMIN
# --------------------------------------------------------------------
def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect("admin_home")

        messages.error(request, "Acesso não permitido.")

    return render(request, "admin_login.html")


@user_passes_test(lambda u: u.is_staff)
def admin_home(request):
    return render(request, "admin/home.html", {
        "pending_orders": get_pending_orders()
    })


# --------------------------------------------------------------------
# ÁREA DO USUÁRIO
# --------------------------------------------------------------------
@login_required
def requisition_list(request):
    try:
        requisitions = Requisition.objects.all()
        print("REQUISITIONS FOUND:", requisitions.count())
        return render(request, "user/requisition_list.html", {
            "requisitions": requisitions
        })
    except Exception as e:
        print("ERROR IN requisition_list:", str(e))
        traceback.print_exc()
        return HttpResponse("Internal Error", status=500)



@login_required
def requisition_detail(request, id):
    requisition = get_object_or_404(Requisition, id=id)
    products = requisition.products.all()

    return render(request, "user/requisition_detail.html", {
        "requisition": requisition,
        "products": products
    })


@login_required
def send_order(request, id):
    requisition = get_object_or_404(Requisition, id=id)

    order = Order.objects.create(
        user=request.user,
        requisition=requisition
    )

    for product_id, quantity in request.POST.items():
        if quantity.isdigit() and int(quantity) > 0:
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity=int(quantity)
            )

    return redirect("order_sent")


@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "user/user_orders.html", {
        "orders": orders
    })


def order_sent(request):
    return render(request, "user/order_sent.html")


# --------------------------------------------------------------------
# SETOR / ESTOQUE
# --------------------------------------------------------------------
@staff_member_required
def order_list(request):
    orders = Order.objects.all().order_by("-created_at")

    Order.objects.filter(is_read=False).update(is_read=True)

    return render(request, "admin/orders.html", {
        "orders": orders,
        "pending_orders": get_pending_orders(),
    })


# --------------------------------------------------------------------
# PDF – WEASYPRINT
# --------------------------------------------------------------------
@staff_member_required
def generate_pdf(request, id):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    import qrcode
    import io
    import os

    order = get_object_or_404(Order, id=id)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # -----------------------------
    # LOGO
    # -----------------------------
    logo_path = os.path.join(settings.BASE_DIR, "core", "static", "logo_xodo.png")
    if os.path.exists(logo_path):
        pdf.drawImage(logo_path, 20 * mm, height - 40 * mm, width=40 * mm, preserveAspectRatio=True)

    # -----------------------------
    # TÍTULO
    # -----------------------------
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(20 * mm, height - 50 * mm, f"Pedido #{order.id}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(20 * mm, height - 60 * mm, f"Requisição: {order.requisition.name}")
    pdf.drawString(20 * mm, height - 70 * mm, f"Usuário: {order.user.username}")
    pdf.drawString(20 * mm, height - 80 * mm, f"Data: {order.created_at.strftime('%d/%m/%Y %H:%M')}")

    # -----------------------------
    # QR CODE
    # -----------------------------
    qr_url = f"https://{request.get_host()}/xodo-admin/pedidos/{order.id}/"
    qr_img = qrcode.make(qr_url)

    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    pdf.drawImage(ImageReader(qr_buffer), 150 * mm, height - 60 * mm, width=40 * mm, height=40 * mm)

    # -----------------------------
    # ITENS DO PEDIDO
    # -----------------------------
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(20 * mm, height - 100 * mm, "Itens do Pedido:")

    y = height - 110 * mm
    pdf.setFont("Helvetica", 12)

    for item in order.items.all():
        pdf.drawString(25 * mm, y, f"- {item.product.name} (Qtd: {item.quantity})")
        y -= 8 * mm

        if y < 20 * mm:  # quebra de página
            pdf.showPage()
            y = height - 20 * mm

    # Finaliza o PDF
    pdf.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="pedido_{order.id}.pdf"'
    return response


# --------------------------------------------------------------------
# DASHBOARD
# --------------------------------------------------------------------
@staff_member_required
def dashboard(request):
    pedidos_por_dia = (
        Order.objects.values("created_at__date")
        .annotate(total=Count("id"))
        .order_by("created_at__date")
    )

    produtos_mais = (
        OrderItem.objects.values("product__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]
    )

    return render(request, "admin/dashboard.html", {
        "pedidos_por_dia": pedidos_por_dia,
        "produtos_mais_pedidos": produtos_mais,
        "pending_orders": get_pending_orders(),
    })
