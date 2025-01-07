from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Anamnesis

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'})
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'placeholder': 'Seu sobrenome'})
    )
    
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Como você quer ser chamado'})
    )
    
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Crie uma senha forte'})
    )
    
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite a senha novamente'})
    )
    
    profile_picture = forms.ImageField(
        required=False,
        label='Foto de perfil',
        widget=forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'})
    )
    
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        label='Tipo de usuário'
    )
    
    bio = forms.CharField(
        required=False,
        label='Biografia',
        widget=forms.Textarea(attrs={'placeholder': 'Conte um pouco sobre você', 'rows': 3})
    )
    
    birth_date = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    fitness_goals = forms.CharField(
        required=False,
        label='Objetivos de condicionamento físico',
        widget=forms.Textarea(attrs={'placeholder': 'Quais são seus objetivos de condicionamento físico?', 'rows': 3})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture', 'user_type', 'bio', 'birth_date', 'fitness_goals')

class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove o campo de senha do formulário
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'})
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'placeholder': 'Seu sobrenome'})
    )
    
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Como você quer ser chamado'})
    )
    
    profile_picture = forms.ImageField(
        required=False,
        label='Foto de perfil',
        widget=forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'})
    )
    
    bio = forms.CharField(
        required=False,
        label='Biografia',
        widget=forms.Textarea(attrs={'placeholder': 'Conte um pouco sobre você', 'rows': 3})
    )
    
    birth_date = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    fitness_goals = forms.CharField(
        required=False,
        label='Objetivos de condicionamento físico',
        widget=forms.Textarea(attrs={'placeholder': 'Quais são seus objetivos de condicionamento físico?', 'rows': 3})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'bio', 'birth_date', 'fitness_goals')

class AnamnesisForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    ]
    
    GOAL_CHOICES = [
        ('weight_loss', 'Perda de peso'),
        ('muscle_gain', 'Ganho de massa muscular'),
        ('maintenance', 'Manutenção'),
        ('health', 'Saúde geral'),
        ('performance', 'Melhoria de performance')
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentário'),
        ('light', 'Levemente ativo'),
        ('moderate', 'Moderadamente ativo'),
        ('very', 'Muito ativo'),
        ('extra', 'Extremamente ativo')
    ]

    birth_date = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Gênero'
    )
    
    height = forms.IntegerField(
        label='Altura (cm)',
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={'placeholder': '170'})
    )
    
    weight = forms.FloatField(
        label='Peso (kg)',
        min_value=30,
        max_value=300,
        widget=forms.NumberInput(attrs={'placeholder': '70.5'})
    )
    
    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        label='Objetivo principal'
    )
    
    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        label='Nível de atividade física'
    )
    
    medical_conditions = forms.CharField(
        required=False,
        label='Condições médicas',
        widget=forms.Textarea(attrs={'placeholder': 'Liste quaisquer condições médicas relevantes', 'rows': 3})
    )
    
    medications = forms.CharField(
        required=False,
        label='Medicamentos',
        widget=forms.Textarea(attrs={'placeholder': 'Liste os medicamentos que você toma regularmente', 'rows': 3})
    )
    
    allergies = forms.CharField(
        required=False,
        label='Alergias',
        widget=forms.Textarea(attrs={'placeholder': 'Liste suas alergias', 'rows': 3})
    )
    
    injuries = forms.CharField(
        required=False,
        label='Lesões',
        widget=forms.Textarea(attrs={'placeholder': 'Liste lesões passadas ou atuais', 'rows': 3})
    )

    class Meta:
        model = Anamnesis
        exclude = ['user', 'created_at', 'updated_at']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'})
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'placeholder': 'Seu sobrenome'})
    )
    
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Nome de usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Como você quer ser chamado'})
    )
    
    profile_picture = forms.ImageField(
        required=False,
        label='Foto de perfil',
        widget=forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'})
    )
    
    bio = forms.CharField(
        required=False,
        label='Biografia',
        widget=forms.Textarea(attrs={'placeholder': 'Conte um pouco sobre você', 'rows': 3})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'bio')
