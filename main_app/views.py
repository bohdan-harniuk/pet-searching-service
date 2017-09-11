from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import get_template
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as sys_login, logout as sys_logout
from django.views.generic import View
from .forms import RegisterForm, LoginForm, UserForm, AddressForm, ReportForm, PetForm, Pet_breedForm, CoatForm, CreateMessageForm
from .models import Address, Chat, Message, Report, Pet, Report_type
from .forms import PET_SEX, PET_HEIGHT, PET_WEIGHT, PET_PRED_COLOR, COAT_TITLE, COAT_LENGTH
from django.db.models import Max
from django.db.models import Q

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image
from reportlab.lib.units import inch,mm
from reportlab.lib.colors import HexColor

from io import BytesIO
from xhtml2pdf import pisa


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'main_app/user-page.html'
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['reports'] = Report.objects.filter(user_id=self.kwargs['pk'])
        context['reports_count'] = context['reports'].count()
        context['counter'] = get_report_count(self.request.user.id)
        return context
    
class AllGiftReportView(View):
    template_name = 'main_app/report-type3.html'
    
    def get(self, request):
        reports = Report.objects.filter(report_type__id=3).order_by('-created')
        reports_count = reports.count()
        counter = get_report_count(request.user.id)
        
        page_request_var = 'page'
        paginator = Paginator(reports, 10)
        page = self.request.GET.get(page_request_var)
        current_page = page
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
            current_page = 1
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'reports':reports, 'page_request_var':page_request_var, 'current_page':current_page,'counter':counter,'reports_count':reports_count})
    
class AllShelterReportView(View):
    template_name = 'main_app/report-type4.html'
    
    def get(self, request):
        reports = Report.objects.filter(report_type__id=4).order_by('-created')
        reports_count = reports.count()
        counter = get_report_count(request.user.id)
        
        page_request_var = 'page'
        paginator = Paginator(reports, 10)
        page = self.request.GET.get(page_request_var)
        current_page = page
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
            current_page = 1
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'reports':reports, 'page_request_var':page_request_var, 'current_page':current_page,'counter':counter,'reports_count':reports_count})
    
class AllSearchReportView(View):
    template_name = 'main_app/report-type1.html'
    
    def get(self, request):
        reports = Report.objects.filter(report_type__id=1).order_by('-created')
        reports_count = reports.count()
        counter = get_report_count(request.user.id)
        
        page_request_var = 'page'
        paginator = Paginator(reports, 10)
        page = self.request.GET.get(page_request_var)
        current_page = page
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
            current_page = 1
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'reports':reports, 'page_request_var':page_request_var, 'current_page':current_page,'counter':counter,'reports_count':reports_count})

class AllFoundReportView(View):
    template_name = 'main_app/report-type2.html'
    
    def get(self, request):
        reports = Report.objects.filter(report_type__id=2).order_by('-created')
        reports_count = reports.count()
        counter = get_report_count(request.user.id)
        
        page_request_var = 'page'
        paginator = Paginator(reports, 10)
        page = self.request.GET.get(page_request_var)
        current_page = page
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
            current_page = 1
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'reports':reports, 'page_request_var':page_request_var, 'current_page':current_page,'counter':counter,'reports_count':reports_count})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    '''file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()   
    return HttpResponse(pdf, content_type="application/pdf")'''
    pdf = pisa.pisaDocument(html.encode('utf-8'), result, encoding='utf-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None

def generate_pdf(request, pk):
    template = get_template("main_app/user-report-form.html")
    context = {}
    report = Report.objects.get(pk=pk)
    context = {'report':report}
    context['sex_dict'] = dict((x,y) for x,y in PET_SEX)
    context['height_dict'] = dict((x,y) for x,y in PET_HEIGHT)
    context['weight_dict'] = dict((x,y) for x,y in PET_WEIGHT)
    context['color_dict'] = dict((x,y) for x,y in PET_PRED_COLOR)
    context['coat_title_dict'] = dict((x,y) for x,y in COAT_TITLE)
    context['coat_length_dict'] = dict((x,y) for x,y in COAT_LENGTH)
    
    html = template.render(context)
    pdf = render_to_pdf('main_app/user-report-form.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def index(request):
    reports = Report.objects.all()
    index_counter = {}
    index_counter['k1'] = reports.filter(report_type__id=1).count()
    index_counter['k2'] = reports.filter(report_type__id=2).count()
    index_counter['k3'] = reports.filter(report_type__id=3).count()
    return render(request, 'main_app/index.html', {'index_counter':index_counter})


def about(request):
    reports = Report.objects.all()
    index_counter = {}
    index_counter['k1'] = reports.filter(report_type__id=1).count()
    index_counter['k2'] = reports.filter(report_type__id=2).count()
    index_counter['k3'] = reports.filter(report_type__id=3).count()
    return render(request, 'main_app/about_us.html', {'index_counter':index_counter})

def volunteer(request):
    return render(request, 'main_app/volunteer.html')


def get_pet_type(pet_type):
    if pet_type == 'Собака':
        return pet_type
    elif pet_type == 'Кішка':
        return pet_type
    elif pet_type == 'Птах':
        return 'Пташка'
    elif pet_type == 'Малий ссавець':
        return 'Тварина'
    elif pet_type == 'Рептилія':
        return pet_type
    else:
        return 'Тварина'
    
def report_pdf(request, pk):
    saved = False
    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pdfmetrics.registerFont(TTFont('Open Sans', 'opensans.ttf'))
    pdfmetrics.registerFont(TTFont('Open Sans Bold', 'opensansbold.ttf'))
    pdfmetrics.registerFont(TTFont('Open Sans Italic', 'opensanslightitalic.ttf'))
    
    report = Report.objects.get(pk=pk)
    img = report.pet.pet_img.path
    im = Image(img)
    header = 'Загубилася '+report.pet.pet_type.title+'!!!'
    
    if report.report_type.id == 1:
        header = 'Загубилася '+report.pet.pet_type.title+'!!!'
        color = '#ff0000'
    elif report.report_type.id == 2:
        header = 'Знайшлася '+get_pet_type(report.pet.pet_type.title)+'!!!'
        color = '#008000'
    
    pdf = canvas.Canvas(response)
    pdf.setFont("Open Sans", 36)
    pdf.setFillColor(HexColor(color))
    pdf.drawString(100,750, header.upper())
    pdf.drawImage(img,80,450, width=150*mm, height= 100*mm)
    
    if report.pet.name and report.pet.age:
        pdf.drawString(180,415, report.pet.name+', '+report.pet.age)
    if report.pet.pet_breed.breed_title:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,390, 'Порода домашнього улюбленця:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(330,390, report.pet.pet_breed.breed_title)
    if report.pet.sex:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,365, 'Стать:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pet_sex = dict((x,y) for x,y in PET_SEX)
        pdf.drawString(130,365, pet_sex[report.pet.sex])
    if report.pet.coat.coat_title:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,340, 'Тип шерсті:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pet_coat = dict((x,y) for x,y in COAT_TITLE)
        pdf.drawString(170,340, pet_coat[report.pet.coat.coat_title])
    if report.pet.coat.length:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,315, 'Довжина шерсті:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pet_length = dict((x,y) for x,y in COAT_LENGTH)
        pdf.drawString(210,315, pet_length[report.pet.coat.length])
    if report.pet.predominant_color:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,290, 'Домінуючий колір:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pet_pred_col = dict((x,y) for x,y in PET_PRED_COLOR)
        pdf.drawString(228,290, pet_pred_col[report.pet.predominant_color])
    if report.pet.height:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,265, 'Висота до плеча:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pet_height = dict((x,y) for x,y in PET_HEIGHT)
        pdf.drawString(220,265, pet_height[report.pet.height])
    if report.pet.weight:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,240, 'Довжина тулуба:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pet_weight = dict((x,y) for x,y in PET_WEIGHT)
        pdf.drawString(213,240, pet_weight[report.pet.weight])
    if report.pet.ident_mark_feat:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,215, 'Деталі для ідентифікації:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(270,215, report.pet.ident_mark_feat)
    if report.pet.collar:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        rantime_pos_x = 80
        pdf.drawString(rantime_pos_x,190, 'Ошейник:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len('Ошейник:') * 10
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,190, report.pet.collar)
    if report.ident_det:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,165, 'Примітка (дата та опис місця втрати/знаходження):')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,140, report.ident_det)
    rantime_pos_x = 80
    if report.address.region.name:
        pdf.setFont("Open Sans", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,115, 'Район:')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len('Район:') * 8.2
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,115, report.address.region.name)
        text_len = len(report.address.region.name) * 8.2
        rantime_pos_x += text_len
    if report.address.street:
        pdf.setFont("Open Sans", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(rantime_pos_x,115, ', вул.')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len(', вул.') * 8.2
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,115, report.address.street)
        
    pdf.setFont("Open Sans Bold", 18)
    pdf.setFillColor(HexColor('#333'))
    pdf.drawString(80,80, 'Контактні дані: ')

    rantime_pos_x = 80
    if report.user.profile.name:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,55, "Ім'я: ")
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len("Ім'я: ") * 8.2
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,55, report.user.profile.name)
    if report.user.email:
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len(report.user.profile.name) * 8.2
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,55, '('+report.user.email+')')
    rantime_pos_x = 80
    if report.user.profile.main_phone:
        pdf.setFont("Open Sans Bold", 14)
        pdf.setFillColor(HexColor('#333'))
        pdf.drawString(80,30, 'Номер телефону: ')
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len("Номер телефону: ") * 8.2
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,30, report.user.profile.main_phone)
    if report.user.profile.alternate_phone:
        pdf.setFont("Open Sans Italic", 14)
        pdf.setFillColor(HexColor('#333'))
        text_len = len(report.user.profile.main_phone) * 8.2
        rantime_pos_x += text_len
        pdf.drawString(rantime_pos_x,30, '('+report.user.profile.alternate_phone+')')
        
        
    pdf.setFont("Open Sans", 10)
    pdf.setFillColor(HexColor('#333'))
    pdf.drawString(250,10, report.created.strftime("%Y-%m-%d %H:%M:%S"))
        
    
    pdf.showPage()
    pdf.save()
    saved = True
    if saved:
        return response
    return redirect('main_app:user_report_detail', pk)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def get_report_count(user_id):
    my_reports = Report.objects.filter(user_id=user_id)
    counter = {'my_report_count':'', 'my_report_1_count':'', 'my_report_2_count':'', 'my_report_3_count':''}
    counter['my_report_count'] = Report.objects.filter(user_id=user_id).count()
    counter['my_report_1_count'] = my_reports.filter(report_type__id=1).count()
    counter['my_report_2_count'] = my_reports.filter(report_type__id=2).count()
    counter['my_report_3_count'] = my_reports.filter(report_type__id=3).count()
    return counter
    

class UserReportView(View):
    template_name = 'main_app/user-reports.html'
    
    def get(self, request):
        my_reports = Report.objects.filter(user_id=request.user.id).order_by('-created')
        counter = get_report_count(request.user.id)
        
        report_type = {'k1':{'count':'','reports':''},'k2':{'count':'','reports':''},'k3':{'count':'','reports':''}}
        report_type['k1']['reports'] = my_reports.filter(report_type__id=1)
        report_type['k1']['count'] = my_reports.filter(report_type__id=1).count()
        report_type['k2']['reports'] = my_reports.filter(report_type__id=2)
        report_type['k2']['count'] = my_reports.filter(report_type__id=2).count()
        report_type['k3']['reports'] = my_reports.filter(report_type__id=3)
        report_type['k3']['count'] = my_reports.filter(report_type__id=3).count()
        
        page_request_var0 = 'report_type'
        report_type0 = self.request.GET.get(page_request_var0)
        
        if report_type0 == '2':
            my_reports =  report_type['k2']['reports']
        elif report_type0 == '3':
            my_reports =  report_type['k3']['reports']
        elif report_type0 == '1':
            my_reports =  report_type['k1']['reports']
        elif report_type0 == None:
            my_reports =  report_type['k1']['reports']
        
        
        page_request_var = 'page'
        paginator = Paginator(my_reports, 10)
        page = self.request.GET.get(page_request_var)
        current_page = page
        try:
            my_reports = paginator.page(page)
        except PageNotAnInteger:
            my_reports = paginator.page(1)
            current_page = 1
        except EmptyPage:
            my_reports = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'my_reports':my_reports, 'page_request_var':page_request_var, 'current_page':current_page, 'report_type':report_type,'page_request_var0':page_request_var0,'counter':counter})

    
class UserReportDetailView(generic.DetailView):
    model = Report
    template_name = 'main_app/report-detail.html'

            
    def get_context_data(self, **kwargs):
        context = super(UserReportDetailView, self).get_context_data(**kwargs)
        context['sex_dict'] = dict((x,y) for x,y in PET_SEX)
        context['height_dict'] = dict((x,y) for x,y in PET_HEIGHT)
        context['weight_dict'] = dict((x,y) for x,y in PET_WEIGHT)
        context['color_dict'] = dict((x,y) for x,y in PET_PRED_COLOR)
        context['coat_title_dict'] = dict((x,y) for x,y in COAT_TITLE)
        context['coat_length_dict'] = dict((x,y) for x,y in COAT_LENGTH)
        context['counter'] = get_report_count(self.request.user.id)
        report_id = self.kwargs['pk']
        if Report.objects.get(pk=report_id).user_id == self.request.user.id:
            self.template_name = 'main_app/user-report.html'
        return context
    
class ReportCreate(View):
    form_class1 = ReportForm
    form_class2 = PetForm
    form_class4 = Pet_breedForm
    form_class5 = AddressForm
    form_class6 = CoatForm
    template_name = 'main_app/user-report-add.html'
    
    def get(self, request):
        all_reports = Report.objects.all()
        form1 = self.form_class1(None)
        form2 = self.form_class2(None)
        form4 = self.form_class4(None)
        form5 = self.form_class5(None)
        form6 = self.form_class6(None)
        
        return render(request, self.template_name, {'all_reports': all_reports, 'form1':form1, 'form2':form2, 'form4':form4, 'form5':form5, 'form6':form6})
    
    def post(self,request):
        all_reports = Report.objects.all()
        form1 = self.form_class1(request.POST)
        form2 = self.form_class2(request.POST, request.FILES)
        form4 = self.form_class4(request.POST)
        form5 = self.form_class5(request.POST)
        form6 = self.form_class6(request.POST)
        report = None
        pet = None
        coat = None
        breed = None
        address = None
        
        if form1.is_valid():
            report = form1.save(commit=False)
            report.user = request.user
            if form2.is_valid():
                pet = form2.save(commit=False)
                if form6.is_valid():
                    coat = form6.save(commit=False)
                    coat.save()
                    pet.coat_id = coat.id
                if form4.is_valid():
                    breed = form4.save(commit=False)
                    breed.pet_type = pet.pet_type
                    breed.save()
                    pet.pet_breed_id = breed.id
            else:
                return render(request, self.template_name, {'form1':form1, 'form2':form2, 'form4':form4, 'form5':form5, 'form6':form6})
            if form5.is_valid():
                address = form5.save(commit=False)
                address.save()
                report.address_id = address.id
            else:
                return render(request, self.template_name, {'form1':form1, 'form2':form2, 'form4':form4, 'form5':form5, 'form6':form6})
            pet.save()
            report.pet_id = pet.id
            report.save()
            return redirect('main_app:user_reports')
        else:
            return render(request, self.template_name, {'all_reports': all_reports, 'form1':form1, 'form2':form2, 'form4':form4, 'form5':form5, 'form6':form6})

class MessageCreateView(View):
    template_name = 'main_app/message-create.html'
    form_class1 = CreateMessageForm
    
    def get(self, request):
        form1 = self.form_class1(None)
        return render(request, self.template_name, {'form1':form1})
    
    def post(self, request):
        form1 = self.form_class1(request.POST)

        if form1.is_valid():
            msg = form1.save(commit=False)
            username = form1.cleaned_data['receiver']
            messg = form1.cleaned_data['message']
            receiver = User.objects.get(username=username)
            receiver = receiver.id 
            sender = User.objects.get(pk=request.user.id)
            chat_count = Chat.objects.filter(user=request.user.id).filter(receiver=receiver).count()
            if chat_count == 0:
                chat = Chat(user=request.user,receiver=receiver)
                chat.save()
            else:
                chat = Chat.objects.get(user=request.user,receiver=receiver)
            msg.chat = chat
            msg.sender = request.user.id
            msg.receiver = receiver
            msg.save()
            
            chat_count0 = Chat.objects.filter(receiver=request.user.id).filter(user=receiver).count()
            if chat_count0 == 0:
                an_receiver = User.objects.get(pk=int(receiver))
                chat0 = Chat(user=an_receiver,receiver=request.user.id)
                chat0.save()
            else:
                an_receiver = User.objects.get(pk=int(receiver))
                chat0 = Chat.objects.get(user=an_receiver,receiver=request.user)
            msg_succ = Message(chat=chat0, sender=receiver, receiver=request.user.id, message=messg)
            msg_succ.save()
        return redirect('main_app:user_message')
            
from itertools import chain

def user_message(request):
    counter = get_report_count(request.user.id)
    all_chat = None
    chats = {}
    last_message = None
    if Chat.objects.filter(user=request.user).count() > 0:
        all_chat = Chat.objects.filter(user=request.user)
    if all_chat == None:
        if Chat.objects.filter(receiver=str(request.user.id)).count() > 0:
            all_chat = Chat.objects.filter(receiver=str(request.user.id))
    if all_chat:
        for obj in all_chat:
            all_message = Message.objects.filter(chat__id=obj.id)
            last_message = all_message.order_by('-created').first()
            receiver = User.objects.get(id=obj.user.id)
            chats[receiver] = last_message
  
    return render(request, 'main_app/user-message.html', {'chats':chats, 'counter':counter})
            
            
class UserChat(View):
    template_name = 'main_app/user-chat.html'
    
    def get(self, request, chat_id):
        message = {}
        chat = Chat.objects.get(pk=chat_id)
        receiver = User.objects.get(pk=int(chat.receiver))
        an_chat = Chat.objects.get(user=receiver,receiver=str(request.user.id))
        my_messages = Message.objects.filter(chat__id=chat_id)
        an_messages = Message.objects.filter(chat__id=an_chat.id)
        key1 = []
        key2 = []
        for msg in my_messages:
            key1.append(msg.pk)
        for msg in an_messages:
            key2.append(msg.pk)
        
        fin_messages = Message.objects.filter(chat__id=chat_id)

        return render(request, self.template_name, {'messages':fin_messages, 'chat':chat})
       
def post(request):
        '''chat = Chat.objects.get(pk=chat_id).message_set.all()'''
        msg = request.POST.get('msgbox')
        chat = Chat.objects.get(pk=3)
        receiver = User.objects.get(pk=int(chat.receiver))
        if receiver.profile.avatar:
            avatar = receiver.profile.avatar
        else:
            avatar = 'avatar.jpg'
        msg_save = Message(chat=chat, sender=request.user.id, receiver=chat.receiver, message=msg)
        if msg != '':
            msg_save.save()
        return JsonResponse({'msg':msg, 'user':receiver.username, 'avatar':avatar})
    
def post_messages(request):
    msg = Message.objects.filter(chat__id=3)
    chat = Chat.objects.get(pk=3)
    sender = User.objects.get(pk=int(chat.user.id))
    return render(request, 'main_app/messages.html', {'messages':msg, 'sender':sender, 'chat':chat})


class UserSettingView(View):
    form_class = UserForm
    form_class2 = AddressForm
    template_name = 'main_app/user-settings.html'
    
    def get(self, request, user_id):
        counter = get_report_count(user_id)
        address_edit = False
        cur_add = None
        user = User.objects.get(pk=user_id)
        profile = user.profile
        
        if profile.address_id != None:
            address_edit = True
            cur_add = Address.objects.get(pk=profile.address_id)
        
        form = self.form_class(instance=profile)
        if address_edit:
            form2 = self.form_class2(instance=cur_add)
        else:
            form2 = self.form_class2(None)
        return render(request, self.template_name, {'form':form, 'form2':form2,'counter':counter})
    
    def post(self, request, user_id):
        address_edit = False
        form = self.form_class(request.POST, request.FILES)
        form2 = self.form_class2(request.POST)
        cur_add = None
        user = User.objects.get(pk=user_id)
        profile = user.profile
        res1,res2,res3 = (0,0,0)
        
        if form.has_changed():
            form = self.form_class(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                res1 = 1
            else:
                return render(request, self.template_name, {'form':form, 'form2':form2})
        else:
            form = self.form_class(instance=profile)
            
        if profile.address_id != None:
            address_edit = True
            cur_add = Address.objects.get(pk=profile.address_id)
        
        if address_edit:
            if form2.has_changed():
                form2 = self.form_class2(request.POST, instance = cur_add)
                if form2.is_valid():
                    form2.save()
                    res2 = 1
                else:
                    return render(request, self.template_name, {'form':form, 'form2':form2})
            else:
                form2 = self.form_class2(instance=cur_add)
        else:
            form2 = self.form_class2(request.POST)
            if form2.is_valid():
                address = form2.save(commit=False)
                address.save()
                profile.address_id = address.id
                profile.save()
                res3 = 1
            else:
                return render(request, self.template_name, {'form':form, 'form2':form2})
        return render(request, self.template_name, {'form':form, 'form2':form2, 'res1':res1, 'res2':res2, 'res3':res3})


def login(request):
    form_class = LoginForm
    template_name = 'main_app/registration_form.html'
    errors = []
    
    if request.method == 'GET':
        form = form_class(None)
        return render(request, template_name, {'form':form, 'errors':errors})
        
    if request.method == 'POST':
        form = form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                sys_login(request, user)
                user_id = user.id
                return redirect('main_app:user_settings', user_id=user_id)
        errors.append('Невірно введено логін або пароль')
        return render(request, template_name, {'form':form, 'errors':errors})

    return render(request, template_name, {'form':form, 'errors':errors})

    
def logout(request):
    sys_logout(request)
    return redirect('main_app:index')  
            
class RegFormView(View):
    form_class = RegisterForm
    template_name = 'main_app/registration_form.html'
    
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            user = authenticate(username=username,password=password)
            
            if user is not None:
                if user.is_active:
                    sys_login(request, user)
                    return redirect('main_app:user_settings', user.id)
                
        return render(request, self.template_name, {'form':form})

#class IndexView(generic.ListView):
 #   template_name = 'main_app/index.html'    
    
