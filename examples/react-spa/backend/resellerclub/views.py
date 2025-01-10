import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def check_domain_availability(request):
    if request.method == 'POST':
        domain_name = request.POST.get('domain_name')

        
        url = 'https://test.httpapi.com/api/domain/check.json'

        api_key = 'gx3jGShhLevitnD4E6FMeTiLsc6JZMU1'
        customer_id = '1269717'

        params = {
            'api_key': api_key,
            'customer_id': customer_id,
            'domain_name': domain_name
        }

        
        response = requests.post(url, data=params)
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Failed to get domain availability'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def get_domain_info(request):
    if request.method == 'GET':
        domain_name = request.GET.get('domain_name')

        
        url = f'https://test.httpapi.com/api/domain/info.json'

       
        api_key = 'gx3jGShhLevitnD4E6FMeTiLsc6JZMU1'
        customer_id = '1269717'

        params = {
            'api_key': api_key,
            'customer_id': customer_id,
            'domain_name': domain_name
        }


        response = requests.get(url, params=params)
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Failed to get domain info'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)