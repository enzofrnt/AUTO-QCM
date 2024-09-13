from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import QCM
from app.forms import QcmForm, ReponseFormSet

@login_required(login_url='login')
def create_or_edit_qcm(request,pk = None):
    if pk :
        qcm = get_object_or_404(QCM,pk=pk)
    else:
        qcm = QCM()
    if request.method == 'POST':
        form = QcmForm(request.POST,instance=qcm)
        
        if form.is_valid():
            qcm = form.save(commit=False)
            print(request.user)
            qcm.creator = request.user
            qcm.save()

            return redirect('qcm-list')
        print(form.errors)
    else:
        form = QcmForm(instance=qcm)

    return render(request, 'qcm/qcm_form.html', {'form': form})