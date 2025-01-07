from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Anamnesis

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'profile_picture', 'bio', 'birth_date', 'fitness_goals', 
                 'color_palette', 'email_notifications', 'follower_notifications', 'workout_notifications', 
                 'login_notifications', 'private_profile', 'show_workout_stats', 'two_factor_auth')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'fitness_goals': forms.Textarea(attrs={'rows': 4}),
        }

class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'profile_picture', 'bio', 'birth_date', 'fitness_goals')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'fitness_goals': forms.Textarea(attrs={'rows': 4}),
        }

class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('color_palette',)
        widgets = {
            'color_palette': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

class UserPrivacyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('private_profile', 'show_workout_stats', 'two_factor_auth')
        widgets = {
            'private_profile': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'show_workout_stats': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'two_factor_auth': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
        }

class UserNotificationsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email_notifications', 'follower_notifications', 'workout_notifications', 'login_notifications')
        widgets = {
            'email_notifications': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'follower_notifications': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'workout_notifications': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'login_notifications': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
        }

class AnamnesisForm(forms.ModelForm):
    class Meta:
        model = Anamnesis
        fields = ('weight', 'height', 'activity_level', 'goals', 'medical_restrictions', 'available_days', 'injury_history')
        widgets = {
            'weight': forms.NumberInput(attrs={'step': '0.1'}),
            'height': forms.NumberInput(attrs={'step': '0.01'}),
            'activity_level': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'goals': forms.Textarea(attrs={'rows': 4}),
            'medical_restrictions': forms.Textarea(attrs={'rows': 4}),
            'available_days': forms.TextInput(attrs={'placeholder': 'Ex: Segunda, Quarta, Sexta'}),
            'injury_history': forms.Textarea(attrs={'rows': 4}),
        }
