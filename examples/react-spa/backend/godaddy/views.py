import json
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from .utils import godaddy_api_request
from django.views.decorators.csrf import csrf_exempt
from .models import DomainPuchase,UpdatedDomainDetail
from .serializers import DomainPurchaseSerializer
from rest_framework import status
from rest_framework.decorators import api_view

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
    
@api_view(['GET'])
def list_domain_purchases(request):
    """
    List all domain purchases.
    """
    domains = DomainPuchase.objects.all()
    serializer = DomainPurchaseSerializer(domains, many=True)
    return Response(serializer.data)

@csrf_exempt
def update_domain_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            domain_name = data.get("domain_name")
            contact_info = data.get("contact_info")

            if not domain_name or not contact_info:
                return JsonResponse({"error": "Domain name or contact info is missing"}, status=400)
            
            domain = DomainPuchase.objects.filter(domain_name=domain_name).first()

            if not domain:
                return JsonResponse({"error": "Domain not found"}, status=404)
            
            domain.contact_info = contact_info
            domain.save()

            updated_domain = UpdatedDomainDetail.objects.create(
                domain_name=domain_name,
                contact_info=contact_info
            )

            return JsonResponse({"message": "Domain contact info updated successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
