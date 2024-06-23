from datetime import date
from dataclasses import dataclass

from core.errors import InvalidError
from domain.company.entities import Company


@dataclass
class Contact:
    id: int
    company_id: int

    first_name: str
    surname: str | None = None
    patronymic: str | None = None
    phone: str | None = None
    address: str | None = None
    birthday: date | None = None
    gender: str | None = None
    workplace: str | None = None
    job_title: str | None = None
    passport: str | None = None
    passport_issued_date: date | None = None
    passport_issued_place: str | None = None

    company: Company | None = None

    FIRST_NAME_MIN_LENGTH = 3
    FIRST_NAME_MAX_LENGTH = 20

    SURNAME_MIN_LENGTH = 3
    SURNAME_MAX_LENGTH = 24

    PATRONYMIC_MIN_LENGTH = 3
    PATRONYMIC_MAX_LENGTH = 24

    ADDRESS_MIN_LENGTH = 8
    ADDRESS_MAX_LENGTH = 255

    AVAIABLE_GENDERS = ["M", "F"]

    WORKPLACE_MIN_LENGTH = 8
    WORKPLACE_MAX_LENGTH = 255

    JOB_TITLE_MIN_LENGTH = 3
    JOB_TITLE_MAX_LENGTH = 64

    PASSPORT_MIN_LENGTH = 10
    PASSPORT_MAX_LENGTH = 11

    PASSPORT_ISSUED_PLACE_MIN_LENGTH = 5
    PASSPORT_ISSUED_PLACE_MAX_LENGTH = 64

    def validate(self):
        if not isinstance(self.id, int):
            raise TypeError
        self._validate_first_name()
        if self.surname:
            self._validate_surname()
        if self.patronymic:
            self._validate_patronymic()
        if self.address:
            self._validate_address()
        if self.gender:
            self._validate_gender()
        if self.workplace:
            self._validate_workplace()
        if self.job_title:
            self._validate_job_title()
        if self.passport:
            self._validate_passport()
        if self.passport_issued_place:
            self._validate_passport_issued_place()
        
    def _validate_first_name(self):
        if not isinstance(self.first_name, str):
            raise TypeError
        
        first_name_len = len(self.first_name)
        if (
            first_name_len < self.FIRST_NAME_MIN_LENGTH
            or first_name_len > self.FIRST_NAME_MAX_LENGTH
        ):
            raise InvalidError(
                f'contact first_name\'s length must be between '
                f'{self.FIRST_NAME_MIN_LENGTH} and {self.FIRST_NAME_MAX_LENGTH}',
                loc=['contact', 'first_name'],
            )

    def _validate_surname(self):
        if not isinstance(self.surname, str):
            raise TypeError
        
        surname_len = len(self.surname)
        if (
            surname_len < self.SURNAME_MIN_LENGTH
            or surname_len > self.SURNAME_MAX_LENGTH
        ):
            raise InvalidError(
                f'contact surname\'s length must be between '
                f'{self.SURNAME_MIN_LENGTH} and {self.SURNAME_MAX_LENGTH}',
                loc=['contact', 'surname'],
            )

    def _validate_patronymic(self):
        if not isinstance(self.patronymic, str):
            raise TypeError
        
        patronymic_len = len(self.patronymic)
        if (
            patronymic_len < self.PATRONYMIC_MIN_LENGTH
            or patronymic_len > self.PATRONYMIC_MAX_LENGTH
        ):
            raise InvalidError(f'contact patronymic\'s length must be between {self.PATRONYMIC_MIN_LENGTH} and {self.PATRONYMIC_MAX_LENGTH}')

    def _validate_address(self):
        if not isinstance(self.address, str):
            raise TypeError
        
        address_len = len(self.address)
        if (
            address_len < self.ADDRESS_MIN_LENGTH
            or address_len > self.ADDRESS_MAX_LENGTH
        ):
            raise InvalidError(f'contact address\'s length must be between {self.ADDRESS_MIN_LENGTH} and {self.ADDRESS_MAX_LENGTH}')

    def _validate_gender(self):
        if not isinstance(self.gender, str):
            raise TypeError
        
        if self.gender not in self.AVAIABLE_GENDERS: 
            raise InvalidError(f'contact gender must be from this options: {", ".join(self.AVAIABLE_GENDERS)}')

    def _validate_workplace(self):
        if not isinstance(self.workplace, str):
            raise TypeError
        
        workplace_len = len(self.workplace)
        if (
            workplace_len < self.WORKPLACE_MIN_LENGTH
            or workplace_len > self.WORKPLACE_MAX_LENGTH
        ):
            raise InvalidError(f'contact workplace\'s length must be between {self.WORKPLACE_MIN_LENGTH} and {self.WORKPLACE_MAX_LENGTH}')
        
    def _validate_job_title(self):
        if not isinstance(self.job_title, str):
            raise TypeError
        
        job_title_len = len(self.job_title)
        if (
            job_title_len < self.JOB_TITLE_MIN_LENGTH
            or job_title_len > self.JOB_TITLE_MAX_LENGTH
        ):
            raise InvalidError(f'contact job_title\'s length must be between {self.JOB_TITLE_MIN_LENGTH} and {self.JOB_TITLE_MAX_LENGTH}')
        
    def _validate_passport(self):
        if not isinstance(self.passport, str):
            raise TypeError
        
        passport_len = len(self.passport)
        if (
            passport_len < self.PASSPORT_MIN_LENGTH
            or passport_len > self.PASSPORT_MAX_LENGTH
        ):
            raise InvalidError(f'contact passport\'s length must be between {self.PASSPORT_MIN_LENGTH} and {self.PASSPORT_MAX_LENGTH}')
        
    def _validate_passport_issued_place(self):
        if not isinstance(self.passport_issued_place, str):
            raise TypeError
        
        passport_issued_place_len = len(self.passport_issued_place)
        if (
            passport_issued_place_len < self.PASSPORT_ISSUED_PLACE_MIN_LENGTH
            or passport_issued_place_len > self.PASSPORT_ISSUED_PLACE_MAX_LENGTH
        ):
            raise InvalidError(f'contact passport_issued_place\'s length must be between {self.PASSPORT_ISSUED_PLACE_MIN_LENGTH} and {self.PASSPORT_ISSUED_PLACE_MAX_LENGTH}')


@dataclass
class ContactsConnection:
    contacts: list[Contact]
    total: int
