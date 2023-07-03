from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from main.models import Paciente, Diagnostico, Prontuario, Medico
from main.serializers import PacienteSerializer,RecepcionistaSerializer,MedicoSerializer, DiagnosticoSerializer, ProntuarioSerializer
from django.contrib.auth.models import User
# Create your views here.

class RegisterRecepcionista(generics.CreateAPIView):
    serializer_class = RecepcionistaSerializer

class RegisterMedico(generics.CreateAPIView):
    serializer_class = MedicoSerializer

class PacienteView(generics.ListCreateAPIView):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class ProntuarioList(generics.ListCreateAPIView):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            context['medico'] = Medico.objects.get(user = self.request.user)
        return context

class ProntuarioObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer


class DiagnosticoCreateView(generics.CreateAPIView):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['medico'] = Medico.objects.get(user = self.request.user)
        return context

class DiagnosticoList(generics.ListAPIView):
    serializer_class = DiagnosticoSerializer
    def get_queryset(self):
        prontuario_id = self.kwargs['pk']
        diagnosticos = Diagnostico.objects.filter(prontuario__id = prontuario_id) 
        return diagnosticos       

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username = username).first()
        if user is None:
            return Response({'status': 'error', 'message': 'Usuário não encontrado'}, status=404)
        if user.check_password(password):
            return Response({'status': 'success', 'token': Token.objects.create(user = user).key})
        else:
            return Response({'status': 'error', 'message': 'Senha incorreta'}, status=403)

class LogoutView(APIView):
    def get(self, request):
        token = Token.objects.filter(user = request.user)
        token.delete()
        return Response({'status': 'success', 'message': 'Logout realizado com sucesso'})

class CheckEmailView(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email = email).first()
        if user is None:
            return Response({'status': 'error', 'message': 'Email não cadastrado'})
        else:
            return Response({'status': 'sucess', 'message': f'localhost:8000/main/forgetpassword/{user.id}'}, status=400)

class ForgetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id = kwargs['pk'])
        password = request.data['password']
        user.set_password(password)
        user.save()
        return Response({'status': 'success', 'message': 'Senha alterada com sucesso'})
