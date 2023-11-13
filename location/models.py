import csv
import logging
import os

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtailautocomplete.edit_handlers import AutocompletePanel

from core.forms import CoreAdminModelForm
from core.models import CommonControlField, Language, TextWithLang


class City(CommonControlField):
    """
    Represent a list of cities

    Fields:
        name
    """

    name = models.TextField(_("Name of the city"), unique=True)

    base_form_class = CoreAdminModelForm
    panels = [FieldPanel("name")]
    autocomplete_search_field = "name"

    def autocomplete_label(self):
        return str(self)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def load(cls, user, city_data=None):
        if not cls.objects.exists():
            if not city_data:
                with open("./location/fixtures/cities.csv", "r") as fp:
                    city_data = fp.readlines()
            for name in city_data:
                try:
                    cls.get_or_create(name=name, user=user)
                except Exception as e:
                    logging.exception(e)

    @classmethod
    def get_or_create(cls, user=None, name=None):
        name = name.strip()
        if not name:
            raise ValueError("City.get_or_create requires name")
        try:
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            city = City()
            city.name = name
            city.creator = user
            city.save()
            return city


class State(CommonControlField):
    """
    Represent the list of states

    Fields:
        name
        acronym
    """

    name = models.TextField(_("State name"), null=True, blank=True)
    acronym = models.CharField(_("State Acronym"), max_length=2, null=True, blank=True)

    base_form_class = CoreAdminModelForm
    panels = [FieldPanel("name"), FieldPanel("acronym")]

    @staticmethod
    def autocomplete_custom_queryset_filter(search_term):
        return State.objects.filter(
            Q(name__icontains=search_term) | Q(acronym__icontains=search_term)
        )

    def autocomplete_label(self):
        return f"{self.acronym or self.name}"

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "acronym",
                ]
            ),
        ]

    def __unicode__(self):
        return f"{self.acronym or self.name}"

    def __str__(self):
        return f"{self.acronym or self.name}"

    @classmethod
    def load(cls, user, state_data=None):
        if not cls.objects.exists():
            if not state_data:
                with open("./location/fixtures/states.csv", "r") as csvfile:
                    state_data = csv.DictReader(
                        csvfile, fieldnames=["name", "acronym", "region"], delimiter=";"
                    )
                    for row in state_data:
                        logging.info(row)
                        cls.get_or_create(
                            name=row["name"],
                            acronym=row["acronym"],
                            user=user,
                        )

    @classmethod
    def get_or_create(cls, user=None, name=None, acronym=None):
        return cls.create_or_update(user, name=name, acronym=acronym)

    @classmethod
    def get(cls, name=None, acronym=None):
        name = name and name.strip()
        acronym = acronym and acronym.strip()
        if not name and not acronym:
            raise ValueError("State.get requires name or acronym")
        if name and acronym:
            # os valores fornecidos são name e acronym
            # mas não necessariamente ambos estão registrados
            try:
                # estão no mesmo registro
                return cls.objects.get(
                    Q(name__iexact=name) | Q(acronym__iexact=acronym)
                )
            except cls.MultipleObjectsReturned:
                try:
                    # name e acron estão no mesmo registro
                    return cls.objects.get(name__iexact=name, acronym__iexact=acronym)
                except cls.DoesNotExist:
                    # não encontrados juntos no mesmo registro
                    pass
        if acronym:
            # prioridade para acronym
            return cls.objects.get(acronym__iexact=acronym)
        if name:
            return cls.objects.get(name__iexact=name)

    @classmethod
    def create_or_update(cls, user, name=None, acronym=None):
        name = name and name.strip()
        acronym = acronym and acronym.strip()
        try:
            obj = cls.get(name=name, acronym=acronym)
            obj.updated_by = user
        except cls.DoesNotExist:
            obj = cls()
            obj.creator = user

        obj.name = name or obj.name
        obj.acronym = acronym or obj.acronym
        obj.save()

        return obj


class CountryName(TextWithLang, Orderable):
    country = ParentalKey(
        "Country",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="country_name",
    )

    base_form_class = CoreAdminModelForm
    panels = [FieldPanel("text"), AutocompletePanel("language")]
    autocomplete_search_filter = "text"

    def autocomplete_label(self):
        return f"{self.text} ({self.language})"

    class Meta:
        verbose_name = _("Country name")
        verbose_name_plural = _("Country names")
        indexes = [
            models.Index(
                fields=[
                    "language",
                ]
            ),
            models.Index(
                fields=[
                    "text",
                ]
            ),
        ]

    @property
    def data(self):
        d = {
            "country_name__text": self.text,
            "country_name__language": self.language,
        }

        return d

    def __unicode__(self):
        return f"{self.text} ({self.language})"

    def __str__(self):
        return f"{self.text} ({self.language})"

    @classmethod
    def get_or_create(cls, country, language, text, user=None):
        return cls.create_or_update(user, country, language, text)

    @classmethod
    def get(cls, country, language):
        if not country and not language:
            raise ValueError("CountryName.get requires country or language")
        return cls.objects.get(country=country, language=language)

    @classmethod
    def create_or_update(cls, user, country, language, text):
        text = text and text.strip()
        try:
            obj = cls.get(country, language)
            obj.updated_by = user
        except cls.DoesNotExist:
            obj = cls()
            obj.creator = user

        obj.country = country or obj.country
        obj.language = language or obj.language
        obj.text = text or obj.text
        obj.save()

        return obj

    @classmethod
    def get_country(cls, name):
        name = name and name.strip()
        for item in CountryName.objects.filter(text=name).iterator():
            if item.country:
                return item.country
        raise cls.DoesNotExist(f"CountryName {name} does not exist")


class Country(CommonControlField, ClusterableModel):
    """
    Represent the list of Countries

    Fields:
        name
        acronym
    """

    name = models.CharField(_("Country Name"), blank=True, null=True, max_length=255)
    acronym = models.CharField(
        _("Country Acronym (2 char)"), blank=True, null=True, max_length=2
    )
    acron3 = models.CharField(
        _("Country Acronym (3 char)"), blank=True, null=True, max_length=3
    )

    base_form_class = CoreAdminModelForm
    panels = [
        FieldPanel("name"),
        FieldPanel("acronym"),
        FieldPanel("acron3"),
        InlinePanel("country_name", label=_("Country names")),
    ]

    @staticmethod
    def autocomplete_custom_queryset_filter(search_term):
        return Country.objects.filter(
            Q(name__icontains=search_term)
            | Q(acronym__icontains=search_term)
            | Q(acron3__icontains=search_term)
        )

    def autocomplete_label(self):
        return self.name or self.acronym

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        indexes = [
            models.Index(
                fields=[
                    "name",
                ]
            ),
            models.Index(
                fields=[
                    "acronym",
                ]
            ),
        ]

    def __unicode__(self):
        return self.name or self.acronym

    def __str__(self):
        return self.name or self.acronym

    @classmethod
    def load(cls, user):
        # País (pt);País (en);Capital;Código ISO (3 letras);Código ISO (2 letras)
        if cls.objects.count() == 0:
            fieldnames = ["name_pt", "name_en", "Capital", "acron3", "acron2"]
            with open("./location/fixtures/country.csv", newline="") as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=";")
                for row in reader:
                    cls.create_or_update(
                        user,
                        name=row["name_en"],
                        acronym=row["acron2"],
                        acron3=row["acron3"],
                        country_names={"pt": row["name_pt"], "en": row["name_en"]},
                    )

    @classmethod
    def get(
        cls,
        name,
        acronym=None,
        acron3=None,
    ):
        name = name and name.strip()
        acronym = acronym and acronym.strip()
        acron3 = acron3 and acron3.strip()

        if acronym:
            return cls.objects.get(acronym=acronym)
        if acron3:
            return cls.objects.get(acron3=acron3)
        if name:
            try:
                return cls.objects.get(name=name)
            except cls.DoesNotExist:
                try:
                    return CountryName.get_country(name)
                except CountryName.DoesNotExist as e:
                    raise cls.DoesNotExist(e)
        raise ValueError("Country.get requires parameters")

    @classmethod
    def create_or_update(
        cls,
        user,
        name=None,
        acronym=None,
        acron3=None,
        country_names=None,
        lang_code2=None,
    ):
        name = name and name.strip()
        acronym = acronym and acronym.strip()
        acron3 = acron3 and acron3.strip()
        lang_code2 = lang_code2 and lang_code2.strip()

        try:
            obj = cls.get(name, acronym, acron3)
            obj.updated_by = user
        except cls.DoesNotExist:
            obj = cls()
            obj.creator = user

        obj.name = name or obj.name
        obj.acronym = acronym or obj.acronym
        obj.acron3 = acron3 or obj.acron3
        obj.save()

        country_names = country_names or {}

        if lang_code2 and name:
            country_names[lang_code2] = name

        for lang_code2, text in country_names.items():
            logging.info(f"{lang_code2} {text}")
            language = Language.get_or_create(code2=lang_code2)
            CountryName.create_or_update(
                country=obj, language=language, text=text, user=user
            )
        return obj


class Location(CommonControlField):
    city = models.ForeignKey(
        City,
        verbose_name=_("City"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    state = models.ForeignKey(
        State,
        verbose_name=_("State"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    base_form_class = CoreAdminModelForm

    panels = [
        AutocompletePanel("city"),
        AutocompletePanel("state"),
        AutocompletePanel("country"),
    ]

    # autocomplete_search_field = "country__name"
    @staticmethod
    def autocomplete_custom_queryset_filter(search_term):
        return Location.objects.filter(
            Q(city__name__icontains=search_term)
            | Q(state__name__icontains=search_term)
            | Q(country__name__icontain=search_term)
        )

    def autocomplete_label(self):
        return str(self)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __unicode__(self):
        return f"{self.country} | {self.state} | {self.city}"

    def __str__(self):
        return f"{self.country} | {self.state} | {self.city}"

    @classmethod
    def get(
        cls,
        location_country,
        location_state,
        location_city,
    ):
        if location_country or location_state or location_city:
            return cls.objects.get(
                country=location_country,
                state=location_state,
                city=location_city,
            )
        raise ValueError("Location.get requires country or state or city parameters")

    @classmethod
    def create_or_update(
        cls,
        user,
        location_country,
        location_state,
        location_city,
    ):
        # check if exists the location
        try:
            location = cls.get(location_country, location_state, location_city)
            location.updated_by = user
        except cls.DoesNotExist:
            location = cls()
            location.creator = user

        location.country = location_country or location.country
        location.state = location_state or location.state
        location.city = location_city or location.city
        location.save()
        return location

    @classmethod
    def create_or_update_location(
        user, country_name, country_code, state_name, city_name
    ):
        params = dict(
            country_name=country_name,
            country_code=country_code,
            state_name=state_name,
            city_name=city_name,
        )
        try:
            location_country = Country.create_or_update(
                user,
                name=country_name,
                acronym=country_code,
                acron3=None,
                country_names=None,
                lang_code2=article_lang,
            )
        except Exception as e:
            location_country = None
            logging.exception(f"params: {params} {type(e)} {e}")

        try:
            location_state = State.create_or_update(
                user,
                name=state_name,
                acronym=None,
            )
        except Exception as e:
            location_state = None
            logging.exception(f"params: {params} {type(e)} {e}")

        try:
            location_city = City.get_or_create(user=user, name=city_name)
        except Exception as e:
            location_city = None
            logging.exception(f"params: {params} {type(e)} {e}")

        return Location.create_or_update(
            user,
            location_country=location_country,
            location_state=location_state,
            location_city=location_city,
        )


class CountryFile(models.Model):
    attachment = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    is_valid = models.BooleanField(_("Is valid?"), default=False, blank=True, null=True)
    line_count = models.IntegerField(
        _("Number of lines"), default=0, blank=True, null=True
    )

    def filename(self):
        return os.path.basename(self.attachment.name)

    panels = [FieldPanel("attachment")]
