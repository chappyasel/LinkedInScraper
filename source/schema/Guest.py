from typing import Optional
from enum import Enum
import linkedin
from linkedin_scraper import Person, Education, Experience


class Status(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"


class Guest(object):
    def __init__(self, source: dict):
        name = source["Name"].split(" ")
        self.firstName = name[0]
        self.lastName = " ".join(name[1:])
        self.status = Status(source["Status"])
        self.plusones = source["Plus ones"]
        self.rsvpdate = source["RSVP date"]
        phone = source["What is your phone number?"]
        self.phone = self.normalizePhone(phone)
        email = source["What is your email?"]
        self.email = self.normalizeEmail(email)
        linkedinUrl = source["What is your LinkedIn?"]
        self.linkedinUrl = self.normalizeLinkedIn(linkedinUrl)
        self.linkedin = None
        self.industry = None
        self.company = None
        self.notes = None

    @property
    def name(self):
        return f"{self.firstName} {self.lastName}"

    def normalizeLinkedIn(self, linkedinUrl: str) -> Optional[str]:
        if "/in/" in linkedinUrl:
            return "https://www.linkedin.com/in/" + linkedinUrl.split("/in/")[1]
        return None

    def normalizePhone(self, phone: str) -> Optional[str]:
        for char in phone:
            if not char.isdigit():
                phone = phone.replace(char, "")
        return phone if len(phone) >= 10 else None

    def normalizeEmail(self, email: str) -> Optional[str]:
        return email if "@" in email else None

    def fetchLinkedin(self):
        print(f"Fetching {self.name} from LinkedIn...")
        if not self.linkedinUrl:
            return
        person = linkedin.getPerson(self.linkedinUrl)
        if not person:
            return
        self.linkedin = person
        self.industry = person.job_title
        self.company = person.company
        about = linkedin.getAboutStr(person)
        experienceStr = linkedin.getExperienceStr(person)
        educationStr = linkedin.getEducationStr(person)
        self.notes = f"{', '.join(experienceStr)}. {', '.join(educationStr)}, {about}"

    def googleSheetsOutput(self):
        linkedin = self.linkedinUrl if self.linkedinUrl else ""
        phone = self.phone if self.phone else ""
        email = self.email if self.email else ""
        industry = self.industry if self.industry else ""
        company = self.company if self.company else ""
        notes = self.notes if self.notes else ""
        return (
            f"{self.name}, {linkedin}, {industry}, {company}, {phone}, {email}, {notes}"
        )

    def __repr__(self):
        return f"Guest({self.name}, {self.phone}, {self.email}, {self.linkedinUrl})"
