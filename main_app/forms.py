from django import forms
from .models import UserProfile, Region, Address, Report, Report_type, Pet, Pet_breed, Pet_type, Coat, Message
from django.contrib.auth.models import User

PET_SEX = [('male','Чоловіча'), ('female','Жіноча'), ('uncertain','Не визначена')]
PET_HEIGHT = [('short','Маленька: до 40 см'), ('medium','Середня: від 40 до 60 см'), ('large','Велика: більше 60 см')]
PET_WEIGHT = [('xs','До 20 см'), ('s_m','22 - 29 см'), ('ml_l','29 - 34 см'), ('xl_xxl','36 - 41 см'), ('xxl_','Більше 41 см')]
PET_PRED_COLOR = [('black','Чорний'), ('white','Білий'), ('brown','Коричневий'), ('silver or gray','Срібний або сірий'), ('tan or cream','Жовто-коричневий або кремовий'), ('yellow or blond or golden','Жовтий або блонд або золотистий'), ('reddish or orange','Червонуватий або оранжевий'), ('other','Інший')]
COAT_TITLE = [('smooth','Гладка'), ('wiry','Жорстка'), ('wavy','Хвиляста'), ('other','Інше')]
COAT_LENGTH = [('short','Коротка'), ('medium','Середня'), ('long','Довга'), ('other','Інше')]


class CreateMessageForm(forms.ModelForm):
    receiver = forms.CharField(required=False, label='Отримувач')
    message = forms.CharField(required=False, label='Повідомлення')
    class Meta:
        model = Message
        fields = ['receiver','message']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receiver'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['message'].widget = forms.Textarea(attrs={'class':'form-control','rows':'3'})



def get_report_type():
    report_type = Report_type.objects.all()
    report_dict = {}
    for obj in report_type:
        report_dict[obj.pk] = obj.label_title
    return report_dict.items()

class ReportForm(forms.ModelForm):
    report_type = forms.ModelChoiceField(queryset=Report_type.objects.all(), required=True, widget=forms.RadioSelect, label="Виберіть тип об'яви", empty_label=None)
    
    class Meta:
        model = Report
        fields = ['report_type','ident_det']
        labels = {
            'ident_det':'Примітки (Дата коли втрачено/знайдено тварину та уточнення)'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ident_det'].widget = forms.Textarea(attrs={'class':'form-control','rows':'3'})

class PetForm(forms.ModelForm):
    pet_img = forms.FileField(label='Фото домашнього улюбленця')
    sex = forms.ChoiceField(choices=PET_SEX, label='Стать', widget=forms.Select(attrs={'class':'form-control'}))
    height = forms.ChoiceField(choices=PET_HEIGHT, label='Приблизна висота до плеча', widget=forms.Select(attrs={'class':'form-control'}))
    weight = forms.ChoiceField(choices=PET_WEIGHT, label='Приблизна довжина спини', widget=forms.Select(attrs={'class':'form-control'}))
    predominant_color = forms.ChoiceField(choices=PET_PRED_COLOR, label='Домінуючий колір (якщо варіант відсутній, то виберіть "Інший" та вкажіть у примітках)', widget=forms.Select(attrs={'class':'form-control'}))
    pet_type = forms.ModelChoiceField(queryset=Pet_type.objects.all(), label='Виберіть вид домашнього улюбленця', widget=forms.Select(attrs={'class':'form-control'}))
    
        
    class Meta:
        model = Pet
        fields = ['name','sex','predominant_color','height','weight','age','ident_mark_feat','collar','pet_img','pet_type']
        labels = {
            'name':"Ім'я, на яке відзивається (для об'яв про втрачену тварину)",
            'age':"Вік (для об'яв про втрачену тварину)",
            'collar':"Опис ошейника (якщо є)",
            'ident_mark_feat':"Опишіть деталі, які допоможуть ідентифікувати тварину",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['age'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['collar'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['ident_mark_feat'].widget = forms.Textarea(attrs={'class':'form-control','rows':'3'})
        
class CoatForm(forms.ModelForm):
    coat_title = forms.ChoiceField(choices=COAT_TITLE, label='Виберіть тип шерсті', widget=forms.Select(attrs={'class':'form-control'}))
    length = forms.ChoiceField(choices=COAT_LENGTH, label='Виберіть довжину шерсті', widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Coat
        fields = ['coat_title','length']

class Pet_breedForm(forms.ModelForm):
    breed_title = forms.CharField( label='Порода (якщо відомо, інакше використайте "змішана" чи "невідомо")', widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Pet_breed
        fields = ['breed_title','pet_type']

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Логін'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Пароль'})
        

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput,label='Пароль')
    
    class Meta:
        model = User
        fields = ['username','password','email']
        labels = {
            'username':'Логін',
            'password':'Пароль',
            'email':'Мейл'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Логін'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Пароль'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'sample@mail.com'})

class UserForm(forms.ModelForm):
    avatar = forms.FileField(label='Ваш аватар', required=False)
    class Meta:
        model = UserProfile
        fields = ['name', 'surname', 'main_phone', 'alternate_phone', 'avatar']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':"Ім'я"})
        self.fields['surname'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Прізвище'})
        self.fields['main_phone'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Номер телефона'})
        self.fields['alternate_phone'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Додатковий номер'})

class AddressForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), label='Виберіть район', widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Address
        fields = ['region', 'street', 'house_num']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['street'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Вулиця'})
        self.fields['house_num'].widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Номер будинку'})