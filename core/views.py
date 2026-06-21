from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import RegisterForm, RequestTicketForm
from .models import RequestTicket, Asset


def register_view(request):
    """New employee signup. After signup, auto-login and send to dashboard."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Welcome to DeskFlow.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


class DeskFlowLoginView(LoginView):
    """Custom login view, just to use our own template."""
    template_name = 'core/login.html'


def is_admin(user):
    """Helper: Admin/IT team = staff users."""
    return user.is_staff


@login_required
def dashboard_view(request):
    """
    Single entry point after login.
    Sends staff users to admin dashboard, everyone else to employee dashboard.
    """
    if is_admin(request.user):
        return admin_dashboard(request)
    return employee_dashboard(request)


@login_required
def employee_dashboard(request):
    """
    Employee view:
    - See assets currently assigned to them
    - See their own past requests
    - Raise a new request
    """
    if request.method == 'POST':
        form = RequestTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Your request has been submitted!")
            return redirect('dashboard')
    else:
        form = RequestTicketForm()

    my_assets = Asset.objects.filter(assigned_to=request.user)
    my_tickets = RequestTicket.objects.filter(user=request.user)

    context = {
        'my_assets': my_assets,
        'my_tickets': my_tickets,
        'form': form,
    }
    return render(request, 'core/employee_dashboard.html', context)


@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Admin/IT view:
    - See ALL requests
    - Search by employee username
    - Filter by status (Pending/Approved/Rejected)
    - Paginated list
    """
    tickets = RequestTicket.objects.select_related('user').all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        tickets = tickets.filter(user__username__icontains=search_query)

    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    paginator = Paginator(tickets, 10)  # 10 tickets per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'core/admin_dashboard.html', context)


@user_passes_test(is_admin)
def approve_ticket(request, ticket_id):
    """Admin approves a ticket -> also assigns/creates an asset record."""
    ticket = get_object_or_404(RequestTicket, id=ticket_id)
    ticket.status = 'Approved'
    ticket.save()

    # Simple bonus logic: create an Asset record marked as assigned to this user
    Asset.objects.create(
        name=f"{ticket.asset_type} for {ticket.user.username}",
        asset_type=ticket.asset_type,
        status='Assigned',
        assigned_to=ticket.user,
    )

    messages.success(request, f"Ticket #{ticket.id} approved.")
    return redirect('admin_dashboard')


@user_passes_test(is_admin)
def reject_ticket(request, ticket_id):
    """Admin rejects a ticket."""
    ticket = get_object_or_404(RequestTicket, id=ticket_id)
    ticket.status = 'Rejected'
    ticket.save()
    messages.success(request, f"Ticket #{ticket.id} rejected.")
    return redirect('admin_dashboard')
