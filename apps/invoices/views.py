from django.shortcuts import render, get_object_or_404
from invoices.models  import Invoice

# Create your views here.

def create_invoice_for_order(order: Order) -> Invoice:
    if hasattr(order, "invoice"):
        return order.invoice
    number = f"NJ-{order.id:06d}"
    return Invoice.objects.create(
        order  = order,
        number = number
    )

def view_invoice(request: HttpRequest, id: int) -> HttpResponse:
    template_name = "invoices/view_invoice.html"
    invoice       = get_object_or_404(Invoice, id = id)
    context = {
        "invoice" : invoice,
        "order"   : invoice.order,
        "items"   : invoice.order.items.all()
    }
    return render(request, template_name, context)
