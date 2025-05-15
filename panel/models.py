from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


