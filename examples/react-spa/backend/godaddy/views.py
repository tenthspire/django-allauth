import json
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .utils import godaddy_api_request
from django.views.decorators.csrf import csrf_exempt
from .models import DomainPuchase

def search_domain(request):
    domain_name = request.GET.get("domain", "example.com")
    endpoint = f"/v1/domains/available"
    params = {"domain": domain_name}
    response = godaddy_api_request(endpoint, params=params)
    return JsonResponse(response)

@csrf_exempt
def purchase_domain(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            domain_name = data.get("domain")
            contact = data.get("contact")

            if not domain_name or not contact:
                return JsonResponse({"error": "Domain name or contact is missing"}, status=400)
            
            is_domain_available = check_domain_availability(domain_name)

            if not is_domain_available:
                return JsonResponse({
                    "error": "Domain is not available",
                    "domain_details": {
                        "domain_name": domain_name,
                        "availability": "Not Available"
                    }
                }, status=400)
            
            purchase = DomainPuchase.objects.create(
                domain_name=domain_name,
                contact_info=contact,
            )

            response_data = {
                "message": "Domain purchased successfully",
                "domain_details": {
                    "domain_name": domain_name,
                    "contact_info": contact
                }
            }

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
# def check_domain_availability(domain_name):
#     taken_domains = ["example.com", "test.com", "domain.com"]
#     if domain_name in taken_domains:
#         return False  # Domain is not available
#     return True

def check_domain_availability(domain_name):
    endpoint = "/v1/domains/available"
    params = {"domain": domain_name}

    response = godaddy_api_request(endpoint, params=params)

    if response.get("available"):
        return JsonResponse({
            "available": True,
            "domain_name": domain_name,
            "currency": response.get("currency"),
            "price": response.get("price"),
            "period": response.get("period"),
            "message": "Domain is available for registration."
        })
    else:
        return JsonResponse({
            "available": False,
            "domain_name": domain_name,
            "message": "Domain is not available for registration."
        })