from django.shortcuts  import render, get_object_or_404, redirect
from orders.models     import Order
from orderitems.models import Orderitem
from products.models   import Product
from clients.models    import Client
from employees.models  import Employee
from invoices.views    import create_invoice_for_order

# Create your views here.

def list_orders(request: HttpRequest) -> HttpReponse:
    template_name = "orders/list_orders.html"
    orders        = Order.objects.select_related("client", "employee").all()
    context = {
        "orders": orders,
    }
    return render(request, template_name, context)

def list_items_products(request: HttpRequest) -> HttpResponse:
    template_name = "orders/list_items_products.html"
    products = Product.objects.filter(isactive = True)
    context = {
        "products": products,
    }
    return render(request, template_name, context)

def cart(request: HttpRequest) -> HttResponse:
    template_name = "orders/cart.html"
    cart          = request.session.get("cart", {})
    total         = 0.0
    for key, item in cart.items():
        total += float(item["subtotal"])
    context = {
        "cart": cart,
        "total": total,
    }
    return render(request, template_name, context)

def add_cart(request: HttpRequest, id: int) -> HttpResponse:
    product = get_object_or_404(Product, id = id)
    cart    = request.session.get("cart", {})
    pid     = str(product.id)
    if pid in cart:
        cart[pid]["quantity"] += 1
    else:
        cart[pid] = {
            "name"     : product.name,
            "price"    : float(product.price),
            "quantity" : 1,
            "subtotal" : float(product.price),
        }
    quantity                 = cart[pid]["quantity"]
    price                    = float(cart[pid]["price"])
    cart[pid]["subtotal"]    = price * quantity
    request.session["cart"]  = cart
    request.session.modified = True
    return redirect("orders:cart")

def edit_cart(request: HttpRequest, id: int) -> HttpResponse:
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart     = request.session.get("cart", {})
        pid      = str(id)
        if pid in cart:
            if quantity < 1:
                del cart[pid]
            else:
                price = float(cart[pid]["price"])
                cart[pid]["quantity"] = quantity
                cart[pid]["subtotal"] = price * quantity
        request.session["cart"]  = cart
        request.session.modified = True
    return redirect("orders:cart")

def delete_cart(request: HttpRequest, id: int) -> HttpResponse:
    cart = request.session.get("cart", {})
    pid  = str(id)
    if pid in cart:
        del cart[pid]
    request.session["cart"] = cart
    request.session.modified = True
    return redirect("orders:cart")

def checkout(request: HttpRequest) -> HttpResponse:
    template_name = "orders/checkout.html"
    cart          = request.session.get("cart", {})
    total         = 0.0
    for key, item in cart.items():
        total += float(item["subtotal"])
    clients   = Client.objects.all()
    employees = Employee.objects.all()
    if request.method == "POST":
        client_id      = request.POST.get("client")
        employee_id    = request.POST.get("employee")
        payment_method = request.POST.get("payment_method")
        client         = get_object_or_404(Client, id = client_id)
        employee       = get_object_or_404(Employee, id = employee_id)
        order = Order.objects.create(
            client         = client,
            employee       = employee,
            payment_method = payment_method,
            status         = "Finalizado",
            total          = 0
        )
        total_order = 0.0
        for product_id, item in cart.items():
            product    = get_object_or_404(Product, id = product_id)
            quantity   = int(item["quantity"])
            unit_price = float(item["price"])
            subtotal   = unit_price * quantity
            Orderitem.objects.create(
                order      = order,
                product    = product,
                quantity   = quantity,
                unit_price = unit_price,
                subtotal   = subtotal
            )
            total_order += subtotal
        order.total = total_order
        order.save()
        create_invoice_for_order(order)
        request.session["cart"] = {}
        request.session.modified = True
        return redirect("orders:view_order", id = order.id)
    context = {
        "cart"            : cart,
        "total"           : total,
        "clients"         : clients,
        "employees"       : employees,
        "payment_methods" : Order._meta.get_field("payment_method").choices,
    }
    return render(request, template_name, context)

def cancel_order(request: HttpRequest, id: int) -> HttpResponse:
    order = get_object_or_404(Order, id = id)
    if order.status != "Cancelado":
        order.status = "Cancelado"
        order.save()
    return redirect("orders:list_orders")

def view_order(request: HttpRequest, id: int) -> HttpResponse:
    template_name = "orders/view_order.html"
    order         = get_object_or_404(Order, id = id)
    items         = order.items.all()
    context = {
        "order" : order,
        "items" : items,
    }
    return render(request, template_name, context)
