import datetime
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .forms import CustomLoginForm, GroupForm, CustomerForm, AttendanceForm
from .models import Group, Customer, Attendance
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
import calendar as cld

DAYS_OF_WEEK = {
    'пн': 'monday',
    'вт': 'tuesday',
    'ср': 'wednesday',
    'чт': 'thursday',
    'пт': 'friday',
    'сб': 'saturday',
    'вс': 'sunday'
}

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('group_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Вход'
        return context
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    login_url = reverse_lazy('login')
    template_name = 'group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.all()
    
class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    login_url = reverse_lazy('login')
    form_class = GroupForm
    template_name = 'form.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Создание группы'
        return context

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    login_url = reverse_lazy('login')
    form_class = GroupForm
    template_name = 'form.html'
    success_url = reverse_lazy('group_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактирование группы'
        return context

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    login_url = reverse_lazy('login')
    template_name = 'delete.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Вы уверены что хотите удалить группу'
        context['item'] = self.get_object()
        return context

class CreateCustomerView(LoginRequiredMixin, CreateView):
    model = Customer
    login_url = reverse_lazy('login')
    form_class = CustomerForm
    template_name = 'form.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Добавить ученика'
        return context
    
class ListCustomerView(LoginRequiredMixin, ListView):
    model = Customer
    login_url = reverse_lazy('login')
    template_name = 'customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.all()
    

class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    model = Customer
    login_url = reverse_lazy('login')
    form_class = CustomerForm
    template_name = 'form.html'
    success_url = reverse_lazy('group_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Редактирование ученика'
        return context
    
class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    model = Customer
    login_url = reverse_lazy('login')
    template_name = 'delete.html'
    success_url = reverse_lazy('list_customer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Вы уверены что хотите удалить ученика'
        context['item'] = self.get_object()
        return context   

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    login_url = reverse_lazy('login')
    template_name = 'customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Данные ученика'
        return context

class AttendanceView(LoginRequiredMixin, CreateView):
    model = Attendance
    login_url = reverse_lazy('login')
    form_class = AttendanceForm
    template_name = 'attendance_form.html'
    success_url = reverse_lazy('group_list')

    def get_group(self, group_id):
        """Helper method to retrieve the group object."""
        return get_object_or_404(Group, id=group_id)

    def get(self, request, *args, **kwargs):
        self.group = self.get_group(kwargs['group_id'])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Customer.objects.filter(group=self.group)

        today = datetime.date.today()
        year, month = today.year, today.month
        last_day = cld.monthrange(year, month)[1]

        attendance_records = Attendance.objects.filter(
            group=self.group,
            date__month=month,
            date__year=year
        ).select_related('customer')


        attendance_dict = {}
        for record in attendance_records:
            customer_id = record.customer.id
            if customer_id not in attendance_dict:
                attendance_dict[customer_id] = {}
            attendance_dict[customer_id][record.date.strftime('%d.%m.%Y')] = record.is_present

        print(attendance_dict)

        days_of_week = {DAYS_OF_WEEK[day.strip().lower()] for day in self.group.weekdays.split(',')}
        today = datetime.date.today()
        year, month = today.year, today.month
        last_day = cld.monthrange(year, month)[1]

        calendar = [
            datetime.date(year, month, day)
            for day in range(1, last_day + 1)
            if datetime.date(year, month, day).strftime('%A').lower() in days_of_week
        ]

        context.update({
            'calendar': calendar,
            'header': 'Добавить посещение',
            'customers': customers,
            'attendance_records': attendance_dict  
        })
        return context

    def post(self, request, *args, **kwargs):
        self.group = self.get_group(kwargs['group_id'])
        data = request.POST.copy()
        data.pop('csrfmiddlewaretoken', None)

        attendance_entries = []
        for row, value in data.items():
            customer_id, date_str = row.split('-')
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
            is_present = value == 'on'
            customer = get_object_or_404(Customer, id=customer_id)

            attendance, created = Attendance.objects.get_or_create(
                customer=customer,
                group=self.group,
                date=date,
                defaults={'is_present': is_present}
            )

            if not created:
                attendance.is_present = is_present
                attendance_entries.append(attendance)

        Attendance.objects.bulk_update(attendance_entries, ['is_present']) if attendance_entries else None

        return super().post(request, *args, **kwargs)


