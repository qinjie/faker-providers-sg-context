from faker.providers import BaseProvider
from faker import Faker
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SgNricProvider(BaseProvider):
    """
    A Faker provider for Singapore NRIC (National Registration Identity Card) Number
    """

    def __init__(self, generator):
        super().__init__(generator)
        self.fake = Faker()
    
    
    @staticmethod
    def first_characters():
        """
        Return list of possible first character.        
        """
        return {
            "S": "Singapore citizens and permanent residents born before 1 January 2000.",
            "T": "Singapore citizens and permanent residents born on or after 1 January 2000",
            "F": "Foreigners issued with long-term passes before 1 January 2000", 
            "G": "Foreigners issued with long-term passes from 1 January 2000 to 31 December 2021",
            "M": "Foreigners issued with long-term passes on or after 1 January 2022"
        }
            
    @classmethod
    def checksum(cls, nric: str)->str:
        """
        Generate checksum from 7 digits
        """
        LETTERS = {
         1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E',
         6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'Z', 11: 'J'
        }
        if len(nric) != 7 or (not nric.isdigit()):
            raise Exception('NRIC must be 7 digits')

        s = list(nric)
        weights = [2, 7, 6, 5, 4, 3, 2]
        sum = 0
        for i in range(len(weights)):
            sum = sum + int(s[i]) * weights[i]
            r = sum % 11
            c = 11 - r
        return LETTERS[c]

    
    def sg_nric_type_s(self, min_age=None, max_age=115):
        """
        "S": "Singapore citizens and permanent residents born before 1 January 2000.",
        Singapore citizens and permanent residents born on or after 1 January 1968 are issued NRIC numbers starting with their year of birth.
        For Singapore citizens and permanent residents born on or before 31 December 1967, the NRIC numbers commonly begin with 0 or 1.
        Non-native residents born before 1968 are assigned the heading numbers 2 or 3 upon attaining permanent residency or citizenship.
        """
        # Get birthday between 
        end_date = datetime(1999, 12, 31)
        current = datetime.today()
        difference = relativedelta(current, end_date)
        
        if not min_age:
            min_age = difference.years        
        elif min_age and (min_age < difference.years):
            print(f'Minimum age for S type NRIC is {difference.years}.')
            min_age = difference.years
        
        if min_age > max_age:
            return None

        birthday = self.fake.date_of_birth(tzinfo=None, minimum_age=min_age, maximum_age=max_age)

        nric = f'{datetime.strftime(birthday,"%y")}#####'
        nric = self.fake.numerify(nric)
        
        if birthday < datetime(1967, 12, 31).date():
            nric = self.fake.random_element(elements=('0', '1', '2', '3')) + nric[1:]
        checksum = self.checksum(nric)
        nric_full = 'S'+nric+checksum
        return {'birthday': datetime.strftime(birthday, '%Y-%m-%d'), "nric": nric_full}
        
    
    def sg_nric_type_t(self, min_age=None, max_age=None):
        """
        "T": "Singapore citizens and permanent residents born on or after 1 January 2000",
        """
        start_date = datetime(2000,1,1)
        current = datetime.today()
        difference = relativedelta(current, start_date)
        
        if not min_age or (min_age < 0):
            min_age = 0
        
        if not max_age:
            max_age = difference.years
        elif max_age and (max_age > difference.years):
            print(f'Maximum age for T type NRIC is {difference.years}.')
            max_age = difference.years

        if min_age > max_age:
            return None
        
        birthday = self.fake.date_of_birth(tzinfo=None, minimum_age=min_age, maximum_age=max_age)

        nric = f'{datetime.strftime(birthday,"%y")}#####'
        nric = self.fake.numerify(nric)        
        checksum = self.checksum(nric)
        nric_full = 'T'+nric+checksum
        return {'birthday': datetime.strftime(birthday, '%Y-%m-%d'), "nric": nric_full}

    
    def sg_nric_type_f(self, min_age=None, max_age=115):
        """
        "F": "Foreigners issued with long-term passes before 1 January 2000", 
        """
        # Get birthday between 
        end_date = datetime(1999, 12, 31)
        current = datetime.today()
        difference = relativedelta(current, end_date)
        
        if not min_age:
            min_age = difference.years        
        elif min_age and (min_age < difference.years):
            print(f'Minimum age for F type NRIC is {difference.years}.')
            min_age = difference.years

        if min_age > max_age:
            return None

        birthday = self.fake.date_of_birth(tzinfo=None, minimum_age=min_age, maximum_age=max_age)

        nric = self.fake.numerify('#######')
        checksum = self.checksum(nric)
        nric_full = 'F'+nric+checksum
        return {'birthday': datetime.strftime(birthday, '%Y-%m-%d'), "nric": nric_full}
        
    
    def sg_nric_type_g(self, min_age=None, max_age=None):
        """
        "G": "Foreigners issued with long-term passes from 1 January 2000 to 31 December 2021",
        """
        start_date = datetime(2000,1,1)
        end_date = datetime(2021,12,31)
        current = datetime.today()
        diff_max = relativedelta(current, start_date)
        diff_min = relativedelta(current, end_date)
        
        if not min_age or (min_age < 0):
            min_age = diff_min.years
        elif min_age and (min_age < diff_min.years):
            print(f'Minimum age for G type NRIC is {diff_min.years}.')
            min_age = diff_min.years

        if min_age > max_age:
            return None

        if not max_age:
            max_age = diff_max.years
        elif max_age and (max_age > diff_max.years):
            print(f'Maximum age for G type NRIC is {diff_max.years}.')
            max_age = diff_max.years

        birthday = self.fake.date_of_birth(tzinfo=None, minimum_age=min_age, maximum_age=max_age)

        nric = self.fake.numerify('#######')
        checksum = self.checksum(nric)
        nric_full = 'G'+nric+checksum
        return {'birthday': datetime.strftime(birthday, '%Y-%m-%d'), "nric": nric_full}

    
    def sg_nric_type_m(self, min_age=None, max_age=115):
        """
        "M": "Foreigners issued with long-term passes on or after 1 January 2022"
        """
        start_date = datetime(2022,1,1)
        current = datetime.today()
        difference = relativedelta(current, start_date)
        
        if not min_age or (min_age < 0):
            min_age = 0
        
        if not max_age:
            max_age = difference.years
        elif max_age and (max_age > difference.years):
            print(f'Maximum age for T type NRIC is {difference.years}.')
            max_age = difference.years

        if min_age > max_age:
            return None

        birthday = self.fake.date_of_birth(tzinfo=None, minimum_age=min_age, maximum_age=max_age)

        nric = f'#######'
        nric = self.fake.numerify(nric)        
        checksum = self.checksum(nric)
        nric_full = 'M'+nric+checksum
        return {'birthday': datetime.strftime(birthday, '%Y-%m-%d'), "nric": nric_full}

    
    def sg_nric(self, categories=['S', 'T', 'F', 'G', 'M'], count=5, min_age=0, max_age=115):
        """
        Return fake SG NRIC number.
        """
        result = []
        while len(result) < count:
            category = self.fake.random_element(elements=categories)
            method_name = f'sg_nric_type_{category.lower()}'
            # Make sure object has the function 
            if not hasattr(self, method_name):
                print(f'Invalid attribute name {method_name} for object {self}')
                continue

            method_to_call = getattr(self, method_name)
            # Make sure the attribute is callable
            if not callable(method_to_call):
                print(f'Invalid function {method_to_call} for object {self}')
                continue

            nric = method_to_call(min_age=min_age, max_age=max_age)
            if nric:
                result.append(nric)
        
        return result