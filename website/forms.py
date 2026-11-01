import time

from django import forms
from django.core import signing


MIN_FORM_COMPLETION_SECONDS = 3
FORM_TIMESTAMP_MAX_AGE_SECONDS = 60 * 60 * 24
FORM_TIMESTAMP_SALT = 'website.contact_form'


class ContactForm(forms.Form):
    SERVICE_CHOICES = (
        ('direcao-ti', 'Direção e Coordenação de TI'),
        ('consultoria-sistemas', 'Consultoria e Análise de Sistemas'),
        ('integracao-sistemas', 'Arquitetura e Integração de Sistemas'),
        ('automacao-processos', 'Automação de Processos'),
        ('dados-banco', 'Dados e Banco de Dados'),
        ('observabilidade', 'Observabilidade e Sustentação de Sistemas'),
        ('projetos-transformacao', 'Projetos e Transformação Digital'),
        ('nao-sei', 'Não sei ainda'),
    )

    name = forms.CharField(
        label='Nome',
        min_length=2,
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'name',
                'aria-describedby': 'name-error',
                'minlength': '2',
            }
        ),
    )
    email = forms.EmailField(
        label='E-mail',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'aria-describedby': 'email-error',
            }
        ),
    )
    company = forms.CharField(
        label='Empresa',
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'organization',
                'aria-describedby': 'company-error',
            }
        ),
    )
    phone = forms.CharField(
        label='Telefone',
        max_length=30,
        required=False,
        widget=forms.TelInput(
            attrs={
                'autocomplete': 'tel',
                'aria-describedby': 'phone-error',
            }
        ),
    )
    service = forms.ChoiceField(
        label='Como posso ajudar?',
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={'aria-describedby': 'service-error'}),
    )
    message = forms.CharField(
        label='Mensagem',
        min_length=20,
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'aria-describedby': 'message-error',
                'minlength': '20',
            }
        ),
    )
    consent = forms.BooleanField(
        label='Concordo com o uso dos dados para retorno deste contato.',
        widget=forms.CheckboxInput(attrs={'aria-describedby': 'consent-error'}),
    )
    website = forms.CharField(
        label='',
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'off',
                'tabindex': '-1',
            }
        ),
    )
    form_started_at = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.setdefault('initial', {})
        if not args and not kwargs.get('data'):
            initial.setdefault(
                'form_started_at',
                signing.dumps(time.time(), salt=FORM_TIMESTAMP_SALT),
            )

        super().__init__(*args, **kwargs)
        self.is_spam = False

        if self.is_bound:
            for name in self.fields:
                if self[name].errors:
                    self.fields[name].widget.attrs['aria-invalid'] = 'true'

    def clean(self):
        cleaned_data = super().clean()

        if self.data.get('website', '').strip():
            self.is_spam = True
            return cleaned_data

        started_at_token = cleaned_data.get('form_started_at')
        if not started_at_token:
            self.is_spam = True
            return cleaned_data

        try:
            started_at = signing.loads(
                started_at_token,
                salt=FORM_TIMESTAMP_SALT,
                max_age=FORM_TIMESTAMP_MAX_AGE_SECONDS,
            )
        except signing.BadSignature:
            self.is_spam = True
            return cleaned_data

        if not isinstance(started_at, (int, float)):
            self.is_spam = True
            return cleaned_data

        if time.time() - started_at < MIN_FORM_COMPLETION_SECONDS:
            self.is_spam = True

        return cleaned_data
