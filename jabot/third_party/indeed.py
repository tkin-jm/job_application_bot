from .browser import Browser
from playwright._impl._api_types import TimeoutError as PlaywrightTimeoutError

class Indeed(Browser):

    card_list_selector = 'ul.jobsearch-ResultsList.css-0'
    job_description_selector = '#jobDescriptionText'
    company_name_selector = '*[class*="companyName"]'
    job_title_selector = 'span[id*="jobTitle"]'
    job_location_selector = '*[class*="companyLocation"]'

    def __init__(self):
        super().__init__(page_address=None)


    def fetch_jobs(self, role: str, location: str) -> list:
        self.page_address = f"https://se.indeed.com/jobs?q={role}&l={location}"
        self.start()

        try:
            card_list = self.page.wait_for_selector(self.card_list_selector, timeout=5000)
            cards = card_list.query_selector_all("> *")
        except PlaywrightTimeoutError:
            self.stop()
            raise TimeoutError("No jobs found!")

        jobs_data = []

        for card in cards:
            
            job_data = {}

            if card.query_selector("div[id*='mosaic']"):
                continue

            try:
                card.click(timeout=2000)
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["job_title"] = card.wait_for_selector(self.job_title_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["company_name"] = card.wait_for_selector(self.company_name_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["job_description"] = self.page.wait_for_selector(self.job_description_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue

            try:
                job_data["job_location"] = card.wait_for_selector(self.job_location_selector, timeout=4000).text_content()
            except PlaywrightTimeoutError:
                continue
                
            jobs_data.append(job_data)

        self.stop()
        return jobs_data
