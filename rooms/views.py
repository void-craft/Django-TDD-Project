from rest_framework import viewsets, permissions
from .models import Room, Thing
from .serializers import RoomSerializer, ThingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class RoomViewSet(viewsets.ModelViewSet):
    queryset         = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # users only see their own rooms
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ThingViewSet(viewsets.ModelViewSet):
    queryset         = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # limit to things in rooms the user owns
        return self.queryset.filter(room__owner=self.request.user)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def shopping_list(request):
    """
    GET: list all things across user’s rooms.
    POST: add a new thing to a specified room.
    """
    if request.method == 'GET':
        things = Thing.objects.filter(room__owner=request.user)
        return Response(ThingSerializer(things, many=True).data)

    # POST
    serializer = ThingSerializer(data=request.data)
    if serializer.is_valid():
        # ensure the room belongs to the user
        room_id = request.data.get('room')
        room = Room.objects.filter(id=room_id, owner=request.user).first()
        if not room:
            return Response({'detail': 'Invalid room.'}, status=400)
        serializer.save(room=room)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
