from django.db import models
from django.contrib.auth import get_user_model
from accounts.utils import random_digit
from django.conf import settings
from django.contrib.auth import get_user_model
from social.utils import customize_datetime_format , day_to_string_persian
import datetime


class CallCounseling(models.Model) :

    lawyer_choices = (
        ("Mohammad_Nobari" , "محمدجواد خسرو نوبری"),
        ("Alireza_Atashzaran" , "علیرضا آتش زران"),
        ("Arghavan_Mansuri" , "ارغوان منصوری"),
        ("Atmish_Jahanshahi" , "آتمیش جهانشاهی"),
        ("Niloofar_Shahab" , "نیلوفر شهاب"),
    )

    time_choices = (
        ("20" , "20 دقیقه"),
        ("30" , "30 دقیقه"),
        ("45" , "45 دقیقه"),
    )

    payment_status_choices = (
        ("failed" , "ناموفق"),
        ("ok" , "موفق"),
        ("undone" , "انجام نشده")
    )


    status_choices = (
        ('done' , 'انجام شده'),
        ('undone' , 'انجام نشده'),
    )

    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True )
    client = models.ForeignKey(get_user_model() ,verbose_name="موکل", blank=True , null=True , on_delete=models.SET_NULL)
    lawyer = models.CharField(verbose_name="وکیل" , max_length=64 , choices=lawyer_choices , blank=True)
    subject = models.CharField(verbose_name="موضوع" , max_length=32 , blank=True , default='سایر')
    call_time = models.CharField(verbose_name="مدت زمان تماس" , max_length=3 , choices=time_choices , blank=True , default='30')
    description = models.TextField(verbose_name="توضیحات" , blank=True)
    Reservation_time = models.TimeField(verbose_name="زمان رزرو شده" , blank=True , null=True)
    Reservation_day = models.DateField(verbose_name="روز رزرو شده" , blank=True , null=True)
    payment_status = models.CharField(verbose_name="وضعیت پرداخت" , max_length=16 , choices=payment_status_choices , default="undone" , blank=True)
    payment_id = models.CharField(verbose_name="شناسه پرداخت" , max_length=64 , blank=True)
    ref_id = models.CharField(verbose_name="شماره تراکنش", max_length=32 , blank=True , null=True)
    amount_paid = models.CharField(verbose_name="مبلغ پرداخت شده" , max_length=32 , blank=True , null=True)
    status = models.CharField(verbose_name="وضعیت" , choices=status_choices , default="undone" , max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_client(self):
        if self.client != '' and self.client :
            return self.client.get_full_name()
        return 'کاربر ناشناس' 

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while CallCounseling.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity

        super().save(*args, **kwargs)

    def get_price(self) :
        if self.call_time :
            price = int(settings.PRICING.get(self.call_time))
            return price
        return None

    
    def persian_reserve_day(self) :
        if self.Reservation_day :
            date = day_to_string_persian(self.Reservation_day)
            return date
        else :
            return 'انتخاب نشده'

    def persian_reserve_time(self) :
        if self.Reservation_time :
            time = self.Reservation_time.strftime('%H:%M:%S')
            return time
        else :
            return 'انتخاب نشده'



    def __str__(self):
        return self.get_client()


class CallCounselingFiles (models.Model):
    call_counseling = models.ForeignKey(CallCounseling , on_delete=models.CASCADE , verbose_name="مشاوره تلفنی برای :" , related_name="files")
    file = models.FileField(upload_to='assets/uploaded/call-counseling/' , verbose_name="فایل")

    def __str__(self) :
        return str(self.call_counseling.identity)


class OnlineCounseling(models.Model):

    lawyer_choices = (
        ("Mohammad_Nobari" , "محمدجواد خسرو نوبری"),
        ("Alireza_Atashzaran" , "علیرضا آتش زران"),
        ("Arghavan_Mansuri" , "ارغوان منصوری"),
        ("Atmish_Jahanshahi" , "آتمیش جهانشاهی"),
        ("Niloofar_Shahab" , "نیلوفر شهاب"),
    )

    payment_status_choices = (
        ("failed" , "ناموفق"),
        ("ok" , "موفق"),
        ("undone" , "انجام نشده")
    )

    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True)
    client = models.ForeignKey(get_user_model() ,verbose_name="موکل", blank=True , null=True , on_delete=models.SET_NULL)
    lawyer = models.CharField(verbose_name="وکیل" , max_length=64 , choices=lawyer_choices , blank=True)
    payment_status = models.CharField(verbose_name="وضعیت پرداخت" , max_length=16 , choices=payment_status_choices , default="undone" , blank=True)
    payment_id = models.CharField(verbose_name="شناسه پرداخت" , max_length=64 , blank=True)
    ref_id = models.CharField(verbose_name="شماره تراکنش", max_length=32 , blank=True , null=True)
    amount_paid = models.CharField(verbose_name="مبلغ پرداخت شده" , max_length=32 , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_client(self):
        if self.client != '' and self.client :
            return self.client.get_full_name()
        return 'کاربر ناشناس' 

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while OnlineCounseling.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity

        super().save(*args, **kwargs)

    def get_price(self) :
        price = int(settings.PRICING.get('online'))
        return price

    def __str__(self):
        return self.get_client()


class OnlineCounselingRoom(models.Model):

    status_choices = (
        ('open' , "باز"),
        ('closed' , "بسته"),
    )

    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True)
    online_counseling = models.OneToOneField(verbose_name="مشاوره آنلاین" , to=OnlineCounseling , on_delete=models.CASCADE , related_name="room")
    status = models.CharField(verbose_name="وضعیت", max_length=16 , choices=status_choices , default='open')
    marked = models.BooleanField(verbose_name="نشان شده" , default=False)
    created_at = models.DateTimeField(verbose_name="ایجاد شده در" , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="بروزرسانی شده در" , auto_now=True)

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while OnlineCounselingRoom.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity
        super().save(*args, **kwargs)

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.online_counseling.client :
            return self.online_counseling.client.get_full_name()
        return 'کاربر ناشناس'


class OnlineCounselingRoomMessage (models.Model) :
    room = models.ForeignKey(to=OnlineCounselingRoom , verbose_name="گفت گو"  , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(to=get_user_model() , verbose_name="فرستنده" , null=True , on_delete=models.SET_NULL)
    message = models.TextField(verbose_name="پیام")
    file = models.FileField(verbose_name="فایل" , upload_to='assets/uploaded/online-counseling/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def created_persian_time(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime["time"]

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime


    def __str__(self) :
        if self.room.online_counseling.client :
            return self.room.online_counseling.client.get_full_name()
        return 'کاربر ناشناس'


class FreeCounselingRoom(models.Model):

    status_choices = (
        ('open' , "باز"),
        ('closed' , "بسته"),
    )

    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True)
    client = models.ForeignKey(to=get_user_model() , verbose_name="موکل" , null=True , on_delete=models.SET_NULL)
    status = models.CharField(verbose_name="وضعیت", max_length=16 , choices=status_choices , default='open')
    marked = models.BooleanField(verbose_name="نشان شده" , default=False)
    created_at = models.DateTimeField(verbose_name="ایجاد شده در" , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="بروزرسانی شده در" , auto_now=True)

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while FreeCounselingRoom.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity
        super().save(*args, **kwargs)

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.client :
            return self.client.get_full_name()
        else :
            return 'کاربر ناشناس'


class FreeCounselingRoomMessage (models.Model) :
    room = models.ForeignKey(to=FreeCounselingRoom , verbose_name="گفت گو"  , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(to=get_user_model() , verbose_name="فرستنده" , null=True , on_delete=models.SET_NULL)
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def created_persian_time(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime["time"]

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.room.client :
            return self.room.client.get_full_name()
        return 'کاربر ناشناس'


class ComplaintRoom(models.Model):
    status_choices = (
        ('open' , "باز"),
        ('closed' , "بسته"),
    )

    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True)
    client = models.ForeignKey(to=get_user_model() , verbose_name="موکل" , null=True , on_delete=models.SET_NULL)
    status = models.CharField(verbose_name="وضعیت", max_length=16 , choices=status_choices , default='open')
    marked = models.BooleanField(verbose_name="نشان شده" , default=False)
    created_at = models.DateTimeField(verbose_name="ایجاد شده در" , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="بروزرسانی شده در" , auto_now=True)

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while FreeCounselingRoom.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity
        super().save(*args, **kwargs)

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.client :
            return self.client.get_full_name()
        return 'کاربر ناشناس'


class ComplaintRoomMessage (models.Model) :
    room = models.ForeignKey(to=ComplaintRoom , verbose_name="گفت گو"  , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(to=get_user_model() , verbose_name="فرستنده" , null=True , on_delete=models.SET_NULL)
    message = models.TextField(verbose_name="پیام")
    file = models.FileField(verbose_name="فایل" , upload_to='assets/uploaded/complaint/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def created_persian_time(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime["time"]

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.room.client :
            return self.room.client.get_full_name()
        return 'کاربر ناشناس'


class ContractRoom(models.Model):
    status_choices = (
        ('open' , "باز"),
        ('closed' , "بسته"),
    )

    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True)
    client = models.ForeignKey(to=get_user_model() , verbose_name="موکل" , null=True , on_delete=models.SET_NULL)
    status = models.CharField(verbose_name="وضعیت", max_length=16 , choices=status_choices , default='open')
    marked = models.BooleanField(verbose_name="نشان شده" , default=False)
    created_at = models.DateTimeField(verbose_name="ایجاد شده در" , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="بروزرسانی شده در" , auto_now=True)

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while FreeCounselingRoom.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity
        super().save(*args, **kwargs)

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.client :
            return self.client.get_full_name()
        return 'کاربر ناشناس'


class ContractRoomMessage (models.Model) :
    room = models.ForeignKey(to=ContractRoom , verbose_name="گفت گو"  , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(to=get_user_model() , verbose_name="فرستنده" , null=True , on_delete=models.SET_NULL)
    message = models.TextField(verbose_name="پیام")
    file = models.FileField(verbose_name="فایل" , upload_to='assets/uploaded/contract/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def created_persian_time(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime["time"]

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.room.client :
            return self.room.client.get_full_name()
        return 'کاربر ناشناس'


class LegalPanel(models.Model) :

    status_choices = (
        ('open' , "باز"),
        ('closed' , "بسته"),
    )

    
    lawyer_choices = (
        ("Mohammad_Nobari" , "محمد نوبری"),
        ("Alireza_Atashzaran" , "علیرضا آتش زران"),
        ("Arghavan_Mansuri" , "ارغوان منصوری"),
        ("Atmish_Jahanshahi" , "آتمیش جهانشیری"),
        ("Niloofar_Shahab" , "نیلوفر شهاب"),
        ("None" , "هنوز انتخاب نشده")
    )


    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True)
    client = models.ForeignKey(to=get_user_model() , verbose_name="موکل" , null=True , on_delete=models.SET_NULL)
    lawyer = models.CharField(verbose_name="وکیل" , max_length=64 , choices=lawyer_choices , blank=True , default='None')
    status = models.CharField(verbose_name="وضعیت", max_length=16 , choices=status_choices , default='open')
    marked = models.BooleanField(verbose_name="نشان شده" , default=False)
    created_at = models.DateTimeField(verbose_name="ایجاد شده در" , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="بروزرسانی شده در" , auto_now=True)

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while LegalPanel.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity

        super().save(*args, **kwargs)

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.client :
            return self.client.get_full_name()
        return 'کاربر ناشناس'


class LegalPanelMessage (models.Model) :
    room = models.ForeignKey(to=LegalPanel , verbose_name="گفت گو"  , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(to=get_user_model() , verbose_name="فرستنده" , null=True , on_delete=models.SET_NULL)
    message = models.TextField(verbose_name="پیام")
    file = models.FileField(verbose_name="فایل" , upload_to='assets/uploaded/legal-panel/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def created_persian_time(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime["time"]

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.room.client :
            return self.room.client.get_full_name()
        return 'کاربر ناشناس'

class SupportRoom(models.Model) :
    identity = models.IntegerField(verbose_name="شناسه" , unique=True , blank=True , null=True)
    user = models.ForeignKey(to=get_user_model(),verbose_name="کاربر" , null=True , on_delete=models.SET_NULL)
    subject = models.CharField(verbose_name="موضوع"  , max_length=64)
    created_at = models.DateTimeField(verbose_name="ایجاد شده در" , auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="بروزرسانی شده در" , auto_now=True)

    def created_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        return self.subject

    def save(self, *args, **kwargs):
        if self.identity is None :
            identity = random_digit(6)
            while LegalPanel.objects.filter(identity=identity).exists() :
                identity = random_digit(6)

            self.identity = identity

        super().save(*args, **kwargs)


class SupportRoomMessage(models.Model):
    room = models.ForeignKey(to=SupportRoom , verbose_name="گفت گو"  , on_delete=models.CASCADE , related_name="messages")
    sender = models.ForeignKey(to=get_user_model() , verbose_name="فرستنده" , null=True , on_delete=models.SET_NULL)
    message = models.TextField(verbose_name="پیام")
    file = models.FileField(verbose_name="فایل" , upload_to='assets/uploaded/support-room/' , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def created_persian_time(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime["time"]

    def created_at_persian(self):
        customize_datetime = customize_datetime_format(self.created_at)
        return customize_datetime

    def __str__(self) :
        if self.room.user:
            return self.room.user.get_full_name()
        return 'کاربر ناشناس'



