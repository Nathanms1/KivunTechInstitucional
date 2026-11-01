const mobileNav = document.querySelector('.mobile-nav');

const servicesTrack = document.querySelector('#services-track');

if (servicesTrack) {
  const serviceCards = [...servicesTrack.querySelectorAll('.service-card')];
  const servicesStatus = document.querySelector('.services-status');
  const serviceControls = [...document.querySelectorAll('[data-services-direction]')];

  const updateServicesControls = () => {
    const gap = Number.parseFloat(window.getComputedStyle(servicesTrack).columnGap) || 0;
    const cardStride = serviceCards[0].getBoundingClientRect().width + gap;
    const firstIndex = Math.min(
      serviceCards.length - 1,
      Math.max(0, Math.round(servicesTrack.scrollLeft / cardStride)),
    );
    const visibleCount = Math.max(
      1,
      Math.floor((servicesTrack.clientWidth + gap) / cardStride),
    );

    servicesStatus.textContent = `${firstIndex + 1}–${Math.min(
      serviceCards.length,
      firstIndex + visibleCount,
    )} de ${serviceCards.length} serviços`;

    serviceControls.forEach((control) => {
      const direction = Number(control.dataset.servicesDirection);
      control.disabled = direction < 0
        ? servicesTrack.scrollLeft <= 1
        : servicesTrack.scrollLeft + servicesTrack.clientWidth >= servicesTrack.scrollWidth - 1;
    });
  };

  serviceControls.forEach((control) => {
    control.addEventListener('click', () => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      servicesTrack.scrollBy({
        left: servicesTrack.clientWidth * Number(control.dataset.servicesDirection),
        behavior: reducedMotion ? 'auto' : 'smooth',
      });
    });
  });

  servicesTrack.addEventListener('scroll', updateServicesControls, { passive: true });
  window.addEventListener('resize', updateServicesControls);
  updateServicesControls();
}

const whatsappFloat = document.querySelector('.whatsapp-float');
const contactSection = document.querySelector('#contato');

if (whatsappFloat && contactSection) {
  let contactIsVisible = false;

  const contactObserver = new IntersectionObserver(([entry]) => {
    contactIsVisible = entry.isIntersecting;
    whatsappFloat.hidden = contactIsVisible && document.activeElement !== whatsappFloat;
  });

  contactObserver.observe(contactSection);
  whatsappFloat.addEventListener('blur', () => {
    if (contactIsVisible) {
      whatsappFloat.hidden = true;
    }
  });
}

if (mobileNav) {
  const summary = mobileNav.querySelector('summary');

  mobileNav.addEventListener('toggle', () => {
    summary.setAttribute('aria-expanded', String(mobileNav.open));
  });

  document.querySelectorAll('.mobile-nav__list a, .mobile-nav__cta').forEach((link) => {
    link.addEventListener('click', () => {
      mobileNav.open = false;
    });
  });
}

document.addEventListener('keydown', (event) => {
  if (!mobileNav?.open || window.getComputedStyle(mobileNav).display === 'none') {
    return;
  }

  if (event.key === 'Escape') {
    mobileNav.open = false;
    mobileNav.querySelector('summary')?.focus();
    return;
  }

  if (event.key !== 'Tab') {
    return;
  }

  const focusableElements = [
    mobileNav.querySelector('summary'),
    ...mobileNav.querySelectorAll('.mobile-nav__panel a[href]'),
  ];
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  if (event.shiftKey && document.activeElement === firstElement) {
    event.preventDefault();
    lastElement.focus();
  } else if (!event.shiftKey && document.activeElement === lastElement) {
    event.preventDefault();
    firstElement.focus();
  }
});

const navigationLinks = [...document.querySelectorAll(
  '.site-nav__list a[href*="#"], .mobile-nav__list a[href*="#"]',
)];
const observedSections = new Map();
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      observedSections.set(entry.target, entry.boundingClientRect.top);
    } else {
      observedSections.delete(entry.target);
    }
  });

  const activeSection = [...observedSections.entries()]
    .sort((left, right) => left[1] - right[1])[0]?.[0];

  navigationLinks.forEach((link) => {
    if (activeSection && link.hash === `#${activeSection.id}`) {
      link.setAttribute('aria-current', 'location');
    } else {
      link.removeAttribute('aria-current');
    }
  });
}, {
  rootMargin: '-20% 0px -70% 0px',
});

navigationLinks.forEach((link) => {
  const section = document.querySelector(link.hash);
  if (section) {
    sectionObserver.observe(section);
  }
});

document.querySelectorAll('.service-card a[data-service]').forEach((link) => {
  link.addEventListener('click', () => {
    const serviceField = document.querySelector('#id_service');
    if (serviceField) {
      serviceField.value = link.dataset.service;
    }
  });
});

const contactForm = document.querySelector('.contact-form');

if (contactForm) {
  const submitKey = 'kivun-contact-form-submitted';
  let feedback = contactForm.querySelector('.form-feedback');
  const fieldset = contactForm.querySelector('fieldset');
  const submitButton = contactForm.querySelector('[type="submit"]');
  const formLoadedAt = performance.now();
  let submittedInThisPage = false;
  let submitting = false;
  let sessionStorageAvailable = true;

  const readSubmissionState = () => {
    try {
      return window.sessionStorage.getItem(submitKey) === '1';
    } catch (error) {
      if (error.name !== 'SecurityError') {
        throw error;
      }

      sessionStorageAvailable = false;
      return submittedInThisPage;
    }
  };

  const saveSubmissionState = () => {
    submittedInThisPage = true;
    if (!sessionStorageAvailable) {
      return;
    }

    try {
      window.sessionStorage.setItem(submitKey, '1');
    } catch (error) {
      if (error.name !== 'SecurityError') {
        throw error;
      }

      sessionStorageAvailable = false;
    }
  };

  const clearSubmissionState = () => {
    submittedInThisPage = false;
    if (!sessionStorageAvailable) {
      return;
    }

    try {
      window.sessionStorage.removeItem(submitKey);
    } catch (error) {
      if (error.name !== 'SecurityError') {
        throw error;
      }

      sessionStorageAvailable = false;
    }
  };

  const showError = (message) => {
    const errorFeedback = feedback || document.createElement('div');
    errorFeedback.className = 'form-feedback form-feedback--error';
    errorFeedback.setAttribute('role', 'alert');
    errorFeedback.setAttribute('tabindex', '-1');

    if (!feedback) {
      const paragraph = document.createElement('p');
      errorFeedback.append(paragraph);
      contactForm.insertBefore(errorFeedback, fieldset);
      feedback = errorFeedback;
    }

    errorFeedback.querySelector('p').textContent = message;
    errorFeedback.focus();
  };

  if (contactForm.dataset.errors === 'true') {
    clearSubmissionState();
    const firstInvalidField = contactForm.querySelector('[aria-invalid="true"]');
    (firstInvalidField || feedback)?.focus();
  } else if (contactForm.dataset.success === 'true') {
    saveSubmissionState();
    submitButton.disabled = true;
    fieldset.disabled = true;
  } else if (readSubmissionState()) {
    submitButton.disabled = true;
    fieldset.disabled = true;
    showError('Uma mensagem já foi enviada nesta aba. Se precisar complementar, use um dos canais diretos de contato.');
  }

  contactForm.addEventListener('submit', (event) => {
    if (readSubmissionState()) {
      event.preventDefault();
      showError('Uma mensagem já foi enviada nesta aba. Se precisar complementar, use um dos canais diretos de contato.');
      return;
    }

    if (submitting) {
      event.preventDefault();
      return;
    }

    const minimumTime = Number(contactForm.dataset.minSubmitTime) * 1000;
    if (performance.now() - formLoadedAt < minimumTime) {
      event.preventDefault();
      showError('Aguarde alguns segundos antes de enviar sua mensagem.');
      return;
    }

    submitting = true;
    submitButton.disabled = true;
    submitButton.textContent = 'Enviando…';
    contactForm.setAttribute('aria-busy', 'true');
  });
}
