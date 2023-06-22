from rich.console import Console

from .database import PostingRepository
from scraper_app.services import ScraperService, ScraperServiceFactory

console = Console()


class PostingService:
    def __init__(self, scraper_service: ScraperService):
        self._scraper_service = scraper_service
    
    def scrap_and_create_postings(self):
        postings = self._scraper_service.get_postings_from_scraper()
        posting_repository = PostingRepository()

        console.log(f'About to save {len(postings)} postings')
        for posting in postings:
            posting_repository.create_posting(posting)
        console.log('Postings saved successfully!', style='green')


class PostingServiceFactory:
    @classmethod
    def build_for_gnula(
        cls,
        pages: int,
        full_url: str
    ) -> PostingService:
        scrapper_service = ScraperServiceFactory.build_for_gnula(
            pages=pages,
            full_url=full_url,
        )
        return PostingService(scraper_service=scrapper_service)
