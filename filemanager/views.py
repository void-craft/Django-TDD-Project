from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rooms.models import Thing
from users.models import CustomUser
import csv
import logging

logger = logging.getLogger('django')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_things_csv(request):
    logger.info(f"CSV export requested by user {request.user.email}")

    try:
        custom_user = CustomUser.objects.get(email=request.user.email)
        things = Thing.objects.filter(room__owner=custom_user)
    except CustomUser.DoesNotExist:
        things = Thing.objects.none()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_things.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Room', 'Quantity'])
    
    for thing in things:
        writer.writerow([thing.name, thing.room.name, thing.quantity])
    
    logger.info(f"CSV export completed - {things.count()} items exported")
    return response