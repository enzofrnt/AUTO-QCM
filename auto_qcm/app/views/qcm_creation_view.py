from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import QCM
from app.forms import QcmForm, ReponseFormSet
from app.decorators import teacher_required

@login_required(login_url='login')
@teacher_required
def create_qcm(request):
    if request.method == 'POST':
        form = QcmForm(request.POST)
        formset = ReponseFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            qcm = form.save(commit=False)
            qcm.save()

            formset.instance = qcm
            formset.save()

            return redirect('qcm-list')
        else:
            print(form.errors, formset.errors)
    else:
        form = QcmForm()
        formset = ReponseFormSet()

    return render(request, 'qcm/qcm_form.html', {'form': form, 'formset': formset})