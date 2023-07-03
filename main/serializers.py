from rest_framework import serializers
from main.models import Paciente, Diagnostico, Prontuario, Recepcionista, Medico
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class PacienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Paciente
        fields = ('user',)
    def create(self, validated_data):
        user = UserSerializer(data = validated_data['user'])
        if user.is_valid():
            user = user.save()
            user.set_password(validated_data['user']['password'])
            user.save()
        else:
            raise serializers.ValidationError(user.errors)
        paciente = Paciente.objects.create(user = user)
        return paciente   

class RecepcionistaSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Recepcionista
        fields = ('user',)
    def create(self, validated_data):
        user = UserSerializer(data = validated_data['user'])
        if user.is_valid():
            user = user.save()
            user.set_password(validated_data['user']['password'])
            user.save()
        else:
            raise serializers.ValidationError(user.errors)
        recepcionista = Recepcionista.objects.create(user = user)
        return recepcionista

class MedicoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Medico
        fields = ('user','especialidade')
    def create(self, validated_data):
        user = UserSerializer(data = validated_data['user'])
        if user.is_valid():
            user = user.save()
            user.set_password(validated_data['user']['password'])
            user.save()
        else:
            raise serializers.ValidationError(user.errors)
        medico = Medico.objects.create(user = user)
        return medico

class ProntuarioSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer()	
    class Meta:
        model = Prontuario
        fields = ('id','paciente','birthday','sex', 'address', 'city', 'state', 'zip_code', 'description', 'allergies','medico')
        read_only_fields = ('medico',)
    def create(self, validated_data):
        medico = self.context['medico']
        validated_data['medico'] = medico
        return super().create(validated_data)

class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ('prontuario','description','date','medico')
        read_only_fields = ('date','medico')
    def create(self, validated_data):
        medico = self.context['medico']
        validated_data['medico'] = medico
        return super().create(validated_data)

