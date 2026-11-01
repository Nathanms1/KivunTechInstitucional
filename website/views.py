import logging
import smtplib

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from .forms import ContactForm


logger = logging.getLogger(__name__)


class HomeView(FormView):
    template_name = 'website/home.html'
    form_class = ContactForm

    def get_initial(self):
        initial = super().get_initial()
        service = self.request.GET.get('servico')
        if service in dict(ContactForm.SERVICE_CHOICES):
            initial['service'] = service
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_sent'] = self.request.GET.get('enviado') == '1'
        return context

    def get_success_url(self):
        return f'{reverse("website:home")}?enviado=1#contato'

    def get_spam_url(self):
        return f'{reverse("website:home")}#contato'

    def form_valid(self, form):
        if form.is_spam:
            return HttpResponseRedirect(self.get_spam_url())

        recipient = settings.CONTACT_EMAIL.strip()
        if not recipient:
            logger.error('Contact email delivery is not configured.')
            form.add_error(
                None,
                'Não foi possível enviar sua mensagem agora. '
                'Tente novamente mais tarde ou use um canal direto de contato.',
            )
            return self.form_invalid(form)

        service_label = dict(ContactForm.SERVICE_CHOICES)[form.cleaned_data['service']]
        message = EmailMessage(
            subject='Nova mensagem pelo site da Kivun Tech',
            body='\n'.join(
                (
                    f"Nome: {form.cleaned_data['name']}",
                    f"E-mail: {form.cleaned_data['email']}",
                    f"Empresa: {form.cleaned_data['company'] or 'Não informada'}",
                    f"Telefone: {form.cleaned_data['phone'] or 'Não informado'}",
                    f'Serviço: {service_label}',
                    '',
                    'Mensagem:',
                    form.cleaned_data['message'],
                )
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[form.cleaned_data['email']],
        )

        try:
            sent_count = message.send(fail_silently=False)
        except (OSError, smtplib.SMTPException) as error:
            logger.error(
                'Contact email delivery failed (%s).',
                type(error).__name__,
            )
            sent_count = 0

        if sent_count != 1:
            if sent_count == 0:
                logger.error('Contact email backend did not accept the message.')
            form.add_error(
                None,
                'Não foi possível enviar sua mensagem agora. '
                'Tente novamente mais tarde ou use um canal direto de contato.',
            )
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        if form.is_spam:
            return HttpResponseRedirect(self.get_spam_url())
        return super().form_invalid(form)


class PrivacyPolicyView(TemplateView):
    template_name = 'website/privacy_policy.html'


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sitemap_url'] = self.request.build_absolute_uri(reverse('sitemap'))
        return context


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
