from django.shortcuts import render,redirect
from django.http import JsonResponse
import random
# ToDiu_dec19
def setvalues(request):
    if request.method == 'POST':
        minv = int(request.POST.get('min',1))
        maxv = int(request.POST.get('max',100))
        if minv > maxv:
            minv, maxv = maxv, minv
        request.session['min'] = minv
        request.session['max'] = maxv  

        request.session['numbers'] = list(range(minv, maxv+1))
        request.session['used'] = []
        request.session.pop('result', None)
    return redirect('generator:index')

def index(request):
    if 'numbers' not in request.session:
        request.session['used'] = []
        request.session['min'] = 1
        request.session['max'] = 100
        request.session['numbers'] = list(range(1,101))
    remain = len(request.session['numbers'])
    used = request.session.get('used', [])
    total = remain + len(used)
    return render(request, 'spin.html', {
        'result': request.session.get('result'),   
        'remain': remain,
        'min': request.session.get('min',1),
        'max': request.session.get('max',100),  
        'used': used,
        'numbers': request.session.get('numbers',[]),
        'total': total
    })

def spin_number(request):
    if request.method == 'POST':
        numbers = request.session.get('numbers', [])
        used = request.session.get('used', [])
        if numbers:
            numbers_copy = list(numbers)
            used_copy = list(used)

            number = random.choice(numbers_copy)
            numbers_copy.remove(number)
            used_copy.append(number)
            
            request.session['numbers'] = numbers_copy
            request.session['used'] = used_copy
            request.session['result'] = number
            
            remain = len(numbers_copy)
            total = remain + len(used_copy)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'result': number,
                    'remain': remain,
                    'used_count': len(used_copy),
                    'total': total,
                    'used': used_copy,
                    'min': request.session.get('min', 1),
                    'max': request.session.get('max', 100)
                })
    return redirect('generator:index')