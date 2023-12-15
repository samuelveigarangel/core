import logging
import sys

from django.db.models import Q
from django.db.utils import DataError
from lxml import etree

from packtools.sps.models.article_abstract import Abstract
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.article_authors import Authors
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.article_ids import ArticleIds
from packtools.sps.models.article_license import ArticleLicense
from packtools.sps.models.article_titles import ArticleTitles
from packtools.sps.models.article_toc_sections import ArticleTocSections
from packtools.sps.models.dates import ArticleDates
from packtools.sps.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.models.funding_group import FundingGroup
from packtools.sps.models.journal_meta import Title as Journal
from packtools.sps.models.kwd_group import KwdGroup
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre

from article import models
from institution.models import Sponsor
from issue.models import TocSection
from tracker.models import UnexpectedEvent


class XMLSPSArticleSaveError(Exception):
    ...

class LicenseDoesNotExist(Exception):
    ...

def load_article(user, xml=None, file_path=None):
    if xml:
        xmltree = etree.fromstring(xml)
    elif file_path:
        for xml_with_pre in XMLWithPre.create(file_path):
            xmltree = xml_with_pre.xmltree
    else:
        raise ValueError(
            "article.sources.xmlsps.load_article requires xml or file_path"
        )
    
    xml_detail_error = etree.tostring(xmltree)
    pids = ArticleIds(xmltree=xmltree).data
    pid_v2 = pids.get("v2")
    pid_v3 = pids.get("v3")

    try:
        article = models.Article.objects.get(Q(pid_v2=pid_v2) | Q(pid_v3=pid_v3))
    except models.Article.DoesNotExist:
        article = models.Article()
    try:
        set_pids(xmltree=xmltree, article=article)
        article.journal = get_journal(xmltree=xmltree)
        set_date_pub(xmltree=xmltree, article=article)
        article.article_type = get_or_create_article_type(xmltree=xmltree, user=user)
        article.issue = get_or_create_issues(xmltree=xmltree, user=user)
        set_first_last_page(xmltree=xmltree, article=article)
        set_elocation_id(xmltree=xmltree, article=article)
        article.save()
        article.abstracts.set(create_or_update_abstract(xmltree=xmltree, user=user))
        article.doi.set(get_or_create_doi(xmltree=xmltree, user=user))
        article.license.set(get_licenses(xmltree=xmltree, user=user))
        article.researchers.set(
            create_or_update_researchers(xmltree=xmltree, user=user)
        )
        article.languages.add(get_or_create_main_language(xmltree=xmltree, user=user))
        article.keywords.set(get_or_create_keywords(xmltree=xmltree, user=user))
        article.toc_sections.set(get_or_create_toc_sections(xmltree=xmltree, user=user))
        article.fundings.set(get_or_create_fundings(xmltree=xmltree, user=user))
        article.titles.set(create_or_update_titles(xmltree=xmltree, user=user))
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        UnexpectedEvent.create(
            exception=e,
            exc_traceback=exc_traceback,
            detail=dict(
                function="article.sources.xmlsps.load_article",
                message=f"{xml_detail_error}",
            ),
        )


def get_or_create_doi(xmltree, user):
    doi_with_lang = DoiWithLang(xmltree=xmltree).data
    data = []
    for doi in doi_with_lang:
        obj = models.DOI.get_or_create(
            value=doi.get("value"),
            language=get_or_create_language(doi.get("lang"), user=user),
            creator=user,
        )
        data.append(obj)
    return data


def get_journal(xmltree):
    journal_title = Journal(xmltree=xmltree).journal_title
    try:
        return models.Journal.objects.get(title=journal_title)
    except models.Journal.DoesNotExist:
        return None


def get_or_create_fundings(xmltree, user):
    """
    Ex fundings_group:
    [{'funding-source': ['CNPQ'], 'award-id': ['12345', '67890']},
        {'funding-source': ['FAPESP'], 'award-id': ['23456', '56789']},]
    """

    fundings_group = FundingGroup(xmltree=xmltree).award_groups
    data = []
    if fundings_group:
        for funding in fundings_group:
            funding_source = funding.get("funding-source", [])
            award_ids = funding.get("award-id", [])

            for fs in funding_source:
                for id in award_ids:
                    obj = models.ArticleFunding.get_or_create(
                        award_id=id,
                        funding_source=create_or_update_sponsor(
                            funding_name=fs, user=user
                        ),
                        user=user,
                    )
                    data.append(obj)
    return data


def get_or_create_toc_sections(xmltree, user):
    toc_sections = ArticleTocSections(xmltree=xmltree).all_section_dict
    data = []
    for key, value in toc_sections.items():
        if value:
            obj = TocSection.get_or_create(
                value=value,
                language=get_or_create_language(key, user=user),
                user=user,
            )
            data.append(obj)
    return data


def get_licenses(xmltree, user):
    licenses = ArticleLicense(xmltree=xmltree).licenses
    data = []
    for license in licenses:
        try:
            obj = models.License.get(
                url=license.get("link"),
                license_type=None,
                # user=user,
            )
        except models.License.DoesNotExist:
            raise LicenseDoesNotExist()
        data.append(obj)
    return data


def get_or_create_keywords(xmltree, user):
    kwd_group = KwdGroup(xmltree=xmltree).extract_kwd_data_with_lang_text(subtag=False)

    data = []
    for kwd in kwd_group:
        obj = models.Keyword.get_or_create(
            text=kwd.get("text"),
            language=get_or_create_language(kwd.get("lang"), user=user),
            ## TODO
            ## Verificar relacao keyword com vocabulary
            # vocabulary=None,
            user=user,
        )
        data.append(obj)
    return data


def create_or_update_abstract(xmltree, user):
    data = []
    if xmltree.find(".//abstract") is not None:
        abstract = Abstract(xmltree=xmltree).get_abstracts(style="inline")
        for ab in abstract:
            obj = models.DocumentAbstract.create_or_update(
                text=ab.get("abstract"),
                language=get_or_create_language(ab.get("lang"), user=user),
                user=user,
            )
            data.append(obj)
    return data


def create_or_update_researchers(xmltree, user):
    authors = Authors(xmltree=xmltree).contribs
    # Falta gender e gender_identification_status
    data = []
    for author in authors:
        obj = models.Researcher.create_or_update(
            given_names=author.get("given_names"),
            last_name=author.get("surname"),
            declared_name=None,
            email=None,
            orcid=author.get("orcid"),
            suffix=author.get("suffix"),
            lattes=author.get("lattes"),
            affiliation=None,
            user=user,
        )
        data.append(obj)
    return data


def set_pids(xmltree, article):
    pids = ArticleIds(xmltree=xmltree).data
    if pids.get("v2") or pids.get("v3"):
        article.set_pids(pids)


def set_date_pub(xmltree, article):
    dates = ArticleDates(xmltree=xmltree).article_date
    article.set_date_pub(dates)


def set_first_last_page(xmltree, article):
    article.first_page = ArticleMetaIssue(xmltree=xmltree).fpage
    article.last_page = ArticleMetaIssue(xmltree=xmltree).lpage


def set_elocation_id(xmltree, article):
    article.elocation_id = ArticleMetaIssue(xmltree=xmltree).elocation_id


def create_or_update_titles(xmltree, user):
    titles = ArticleTitles(xmltree=xmltree).article_title_list
    data = []
    for title in titles:
        format_title = " ".join(title.get("text", "").split())
        if format_title:
            obj = models.DocumentTitle.create_or_update(
                title=format_title,
                title_rich=title.get("text"),
                language=get_or_create_language(title.get("lang"), user=user),
                user=user,
            )
            data.append(obj)
    return data


def get_or_create_article_type(xmltree, user):
    article_type = ArticleAndSubArticles(xmltree=xmltree).main_article_type
    obj, created = models.ArticleType.objects.get_or_create(text=article_type)
    return obj


def get_or_create_issues(xmltree, user):
    issue_data = ArticleMetaIssue(xmltree=xmltree).data
    collection_date = ArticleDates(xmltree=xmltree).collection_date
    obj = models.Issue.get_or_create(
        journal=get_journal(xmltree=xmltree),
        number=issue_data.get("number"),
        volume=issue_data.get("volume"),
        season=collection_date.get("season"),
        year=collection_date.get("year"),
        month=collection_date.get("month"),
        supplement=collection_date.get("suppl"),
        user=user,
    )
    return obj


def get_or_create_language(lang, user):
    obj = models.Language.get_or_create(code2=lang, creator=user)
    return obj


def get_or_create_main_language(xmltree, user):
    lang = ArticleAndSubArticles(xmltree=xmltree).main_lang
    obj = get_or_create_language(lang, user)
    return obj


def create_or_update_sponsor(funding_name, user):
    return Sponsor.get_or_create(
        user=user,
        name=funding_name,
        acronym=None,
        level_1=None,
        level_2=None,
        level_3=None,
        location=None,
        official=None,
        is_official=None,
        url=None,
        institution_type=None,
    )
