from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import Client,Project,User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .serializers import ClientSerializer,ClientDetailSerializer,ClienEdittSerializer,ProjectPostSerializer,ProjectVIewSerializer

#  you need to login first using the loginapi to fetch other apis

# View to login for the user
class SessionLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Use Django's built-in AuthenticationForm to handle validation
        form = AuthenticationForm(data=request.data)
        
        if form.is_valid():
            # Authenticate the user
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            if user is not None:
                # Log the user in using Django's session system
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)


#view for logout the user
class SessionLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

#view to see all clients
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

#view for creating client
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
#view for  fetching the details of particular client
class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

#view to  updata the client
class ClientUpdateView(generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = ClienEdittSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


    def put(self, request, *args, **kwargs):
        client = self.get_object() 
        serializer = self.get_serializer(client, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#view to delete the client 
class ClientDeleteView(generics.DestroyAPIView):
    queryset = Client.objects.all()
    lookup_field = 'id'


# view to create project
class ProjectCreateView(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectPostSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        client_id = kwargs.get('id')
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({"detail": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


        project_name = request.data.get('project_name')
        users_data = request.data.get('users', [])

    
        user_ids = [user['id'] for user in users_data]
        

        users = User.objects.filter(id__in=user_ids)

        
        if len(users) != len(user_ids):
            return Response({"detail": "Some users not found"}, status=status.HTTP_400_BAD_REQUEST)

    
        project = Project.objects.create(project_name=project_name, client=client, created_by=request.user)
        
    
        project.users.set(users)
        project.save()

        
        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# view to see all the projects assigned to user
class UserAssignedProjectsView(generics.ListAPIView):
    serializer_class = ProjectVIewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the projects that the logged-in user is assigned to
        return Project.objects.filter(users=self.request.user)

