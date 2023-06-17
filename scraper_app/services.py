from typing import Optional, List

from rich.console import Console

from .gateways import (
    ArgenpropGateway,
    BaseGateway,
    LaVozGateway,
    MercadolibreGateway,
    ProperatiGateway,
    GnulaGateway,
)
from .parsers import (
    ArgenpropParser,
    BaseParser,
    LaVozParser,
    MercadolibreParser,
    ProperatiParser,
    GnulaParser,
)
from posting_app.database import Posting

console = Console()


class ScraperService:
    def __init__(
        self,
        pages: int,
        url: str,
        gateway: BaseGateway,
        parser: BaseParser,
    ):
        self._pages = pages
        self._url = url
        self._gateway = gateway
        self._parser = parser

    def get_postings_from_scraper(self) -> List[Posting]:
        postings = set()
        pages = self._pages if self._gateway.paginated else 1

        for page in range(1, pages + 1):
            console.log(f'Page {page} of {pages}')
            html = self._gateway.make_request(
                url=self._url.format(page)
            )

            self._parser.get_soup_object(html=html)
            new_postings = self._parser.extract_data()
            console.log(f'Got {len(new_postings)} new postings')

            postings = postings.union(new_postings)

        return postings


class ScraperServiceFactory:
    @classmethod
    def build_for_gnula(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=GnulaGateway(),
            parser=GnulaParser(),
        )

    @classmethod
    def build_for_argenprop(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ArgenpropGateway(),
            parser=ArgenpropParser(),
        )

    @classmethod
    def build_for_mercadolibre(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=MercadolibreGateway(),
            parser=MercadolibreParser(),
        )

    @classmethod
    def build_for_la_voz(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=LaVozGateway(),
            parser=LaVozParser(),
        )

    @classmethod
    def build_for_properati(
        cls,
        pages: int,
        full_url: str
    ) -> ScraperService:
        return ScraperService(
            pages=pages,
            url=full_url,
            gateway=ProperatiGateway(),
            parser=ProperatiParser(),
        )
