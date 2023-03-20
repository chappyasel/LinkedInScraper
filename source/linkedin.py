from linkedin_scraper import actions, Person, Education, Experience
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import keys

# https://github.com/joeyism/linkedin_scraper
# https://github.com/SergeyPirogov/webdriver_manager

# If you're having issues with etree on Apple Silicon, see:
# https://apple.stackexchange.com/a/443379

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
actions.login(driver, keys.linkedinUsername, keys.linkedinPassword)


def getPerson(url) -> Person:
    person = Person(url, driver=driver, close_on_complete=False)
    return person


def getAboutStr(person: Person) -> str:
    about = person.about.partition(".")[0]
    return about


def getEducationStr(person: Person) -> str:
    educations = person.educations[:3]
    return [f"{e.degree} @ {e.institution_name}" for e in educations]


def getExperienceStr(person: Person) -> str:
    experiences = person.experiences[:3]
    return [f"{e.position_title} @ {e.institution_name}" for e in experiences]
