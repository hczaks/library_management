from django import forms
from app1 import models


class BootStrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapForm(BootStrap, forms.Form):
    pass


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True,
    )


class BookForm(BootStrapModelForm):
    ctime = forms.DateField(
        label="入库时间",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'placeholder': '入库时间',
            'data-provide': 'datepicker',
            'id': 'dt',
        }),
        required=True
    )

    class Meta:
        model = models.Book
        exclude = ['published_date']


class BorrowerForm(BootStrapModelForm):
    class Meta:
        model = models.Borrower
        fields = "__all__"


class BorrowingForm(BootStrapModelForm):
    class Meta:
        model = models.Borrowing
        fields = ['borrower', 'borrowed_date']
        widgets = {
            'borrowed_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AdminForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = "__all__"
