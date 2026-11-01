from django.test import TestCase
from django.urls import reverse


class SharedNavigationTests(TestCase):
    def test_about_heading_and_copy_share_column_opposite_the_manifesto(self):
        response = self.client.get(reverse('website:home'))
        content = response.content.decode()

        about_section = content.split('<section id="sobre"', maxsplit=1)[1].split('</section>', maxsplit=1)[0]
        self.assertIn('<div class="about-copy">', about_section)
        self.assertIn('<h2 id="sobre-title">Uma empresa de tecnologia com direção</h2>', about_section)
        self.assertIn('<aside class="about-manifesto"', about_section)
        self.assertLess(
            about_section.index('<h2 id="sobre-title">'),
            about_section.index('<aside class="about-manifesto"'),
        )

    def test_home_has_accessible_floating_whatsapp_link(self):
        response = self.client.get(reverse('website:home'))

        self.assertContains(response, 'class="whatsapp-float"')
        self.assertContains(response, 'href="https://wa.me/5551984597510?')
        self.assertContains(response, 'aria-label="Fale pelo WhatsApp (abre em nova aba)"')
        self.assertContains(response, 'rel="noopener noreferrer"')

    def test_home_has_all_services_in_horizontal_cards(self):
        response = self.client.get(reverse('website:home'))

        self.assertContains(response, 'id="services-track"')
        self.assertContains(response, 'aria-label="Serviços disponíveis"')
        self.assertContains(response, 'data-services-direction="1"')
        self.assertEqual(response.content.decode().count('class="service-card"'), 7)

    def test_experience_and_competencies_share_one_section(self):
        response = self.client.get(reverse('website:home'))
        content = response.content.decode()

        self.assertIn('id="experiencia"', content)
        self.assertIn('id="competencias"', content)
        self.assertIn('<strong>8+</strong>', content)
        self.assertIn('Analista de Sistemas e Product Owner', content)
        self.assertNotIn('experience-item__period', content)
        self.assertIn('class="course-highlight__eyebrow"', content)

    def test_company_logos_and_nonvisual_cresol_attribution_are_present(self):
        response = self.client.get(reverse('website:home'))
        content = response.content.decode()

        for logo in (
            'img/companies/cresol.png',
            'img/companies/klassmatt.png',
            'img/companies/gruposc-mark.png',
            'img/companies/auxiliadora-predial.webp',
            'img/companies/sicredi.png',
        ):
            self.assertIn(logo, content)

        self.assertIn('id="cresol-logo-attribution"', content)
        self.assertIn('class="visually-hidden" id="cresol-logo-attribution"', content)
        self.assertNotIn('class="company-experience__note"', content)

    def test_privacy_policy_navigation_targets_home_sections(self):
        response = self.client.get(reverse('website:privacy_policy'))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        for section in (
            'sobre',
            'servicos',
            'diferenciais',
            'metodologia',
            'competencias',
            'experiencia',
            'faq',
            'contato',
        ):
            self.assertIn(f'href="/#{section}"', content)
            self.assertNotIn(f'href="#{section}"', content)

    def test_privacy_policy_names_hosting_and_email_providers(self):
        response = self.client.get(reverse('website:privacy_policy'))

        self.assertContains(response, 'Vercel')
        self.assertContains(response, 'Google (Gmail)')

    def test_skip_link_targets_focusable_main_content(self):
        response = self.client.get(reverse('website:privacy_policy'))

        self.assertContains(response, 'href="#conteudo"')
        self.assertContains(
            response,
            '<main id="conteudo" class="site-main" tabindex="-1">',
            html=False,
        )
