from django.shortcuts import render, redirect
from .forms import SettlementForm
from datetime import datetime

def input_page(request):
    if request.method == 'POST':
        form = SettlementForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = request.POST
            return redirect('output_page')
    else:
        form = SettlementForm()
    return render(request, 'input_page.html', {'form': form})


def output_page(request):
    data = request.session.get('form_data')
    if not data:
        return redirect('input_page')

    emp_name = data['employee_name']
    jd = datetime.strptime(data['joining_date'], '%Y-%m-%d')
    ed = datetime.strptime(data['ending_date'], '%Y-%m-%d')
    basic_salary = float(data['basic_salary'])
    allowances = float(data['allowances'])
    deductions = float(data['deductions'])
    al_used = int(data['al_used'])
    absence_days = int(data['absence_days'])

    employment_days = (ed - jd).days
    eligible_days = employment_days - absence_days

    total_salary = basic_salary + allowances

    if employment_days < 180:
        matured_al_days = 0
    else:
        matured_al_days = (30 * employment_days) / 365

    pending_al = max(matured_al_days - al_used, 0)
    pending_al_salary = (total_salary / 30) * pending_al

    if employment_days < 365:
        gratuity = 0
    else:
        years = eligible_days / 365 
        if years <= 5:
            gratuity = (basic_salary / 30) * 21 * years
        else:
            gratuity_first_5_years = (basic_salary / 30) * 21 * 5
            gratuity_after_5_years = (basic_salary / 30) * 30 * (years - 5)
            gratuity = gratuity_first_5_years + gratuity_after_5_years

    final_payable = gratuity + pending_al_salary - deductions
    total_payable = max(final_payable, 0)

    note = ""
    if final_payable < 0:
        note += f"Amount recoverable from employee: {abs(final_payable):.2f} AED<br>"
    if employment_days < 365:
        note += "Below 1 year — no gratuity is payable.<br>"


    context = {
        'emp_name': emp_name,
        'jd': jd.date(),
        'ed': ed.date(),
        'employment_days': employment_days,
        'absence_days': absence_days,
        'eligible_days': eligible_days,
        'pending_al': round(pending_al, 2),
        'pending_al_salary': round(pending_al_salary, 2),
        'gratuity': round(gratuity, 2),
        'total_payable': round(total_payable, 2),
        'note': note,

    }

    return render(request, 'output_page.html', context)
