"""File: core/wagtail_hooks.py."""

from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.navigation import get_site_for_user
from wagtail.admin.site_summary import SummaryItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from article.models import Article
from collection.models import Collection
from core.models import Gender
from journal import models

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin."""
    """Add /static/admin/css/custom.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">', static("admin/css/custom.css")
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    """Add /static/admin/css/custom.js to the admin."""
    return format_html('<script src="{}"></script>', static("admin/js/custom.js"))


@hooks.register("construct_homepage_summary_items", order=1)
def remove_all_summary_items(request, items):
    items.clear()


class CollectionSummaryItem(SummaryItem):
    order = 100
    template_name = "wagtailadmin/summary_items/collection_summary_item.html"

    def get_context_data(self, parent_context):
        site_details = get_site_for_user(self.request.user)
        total_collection = Collection.objects.filter(is_active=True).count()
        return {
            "total_collection": total_collection,
            "site_name": site_details["site_name"],
        }

    def is_shown(self):
        return True


class JournalSummaryItem(SummaryItem):
    order = 200
    template_name = "wagtailadmin/summary_items/journal_summary_item.html"

    def get_context_data(self, parent_context):
        site_details = get_site_for_user(self.request.user)
        total_journal = models.Journal.objects.all().count()
        return {
            "total_journal": total_journal,
            "site_name": site_details["site_name"],
        }

    def is_shown(self):
        return True


class ArticleSummaryItem(SummaryItem):
    order = 300
    template_name = "wagtailadmin/summary_items/article_summary_item.html"

    def get_context_data(self, parent_context):
        site_details = get_site_for_user(self.request.user)
        total_article = Article.objects.all().count()
        return {
            "total_article": total_article,
            "site_name": site_details["site_name"],
        }


@hooks.register("construct_homepage_summary_items", order=2)
def add_items_summary_items(request, items):
    items.append(CollectionSummaryItem(request))
    items.append(JournalSummaryItem(request))
    items.append(ArticleSummaryItem(request))


class WebOfKnowledgeAdmin(ModelAdmin):
    model = models.WebOfKnowledge
    menu_icon = "folder"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "code",
        "value",
    )

    search_fields = (
        "code",
        "value",
    )


class SubjectAdmin(ModelAdmin):
    model = models.Subject
    menu_icon = "folder"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "code",
        "value",
    )

    search_fields = (
        "code",
        "value",
    )


class WosAreaAdmin(ModelAdmin):
    model = models.WebOfKnowledgeSubjectCategory
    menu_icon = "folder"
    menu_order = 400
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "value",
    )
    search_fields = (
        "value",
    )


class StandardAdmin(ModelAdmin):
    model = models.Standard
    menu_icon = "folder"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "code",
        "value",
    )

    search_fields = (
        "code",
        "value",
    )


class ListCodesAdminGroup(ModelAdminGroup):
    menu_label = "List of codes"
    menu_icon = "folder-open-inverse"
    menu_order = 1100
    items = (
        SubjectAdmin,
        WebOfKnowledgeAdmin,
        WosAreaAdmin,
        StandardAdmin,
    )

modeladmin_register(ListCodesAdminGroup)