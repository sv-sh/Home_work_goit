from _collections_abc import Iterator
from collections import UserDict
from datetime import datetime
import re

class Field:                                        #parrent 
    def __init__(self, value=None):
        self.__value = None
        self.value = value
    
    @property                                       #getter
    def value(self):
        return self.__value
    
    @value.setter                                   #setter
    def value(self, value):
        self.__value = value
    
    def __repr__(self):                             #get readable form
        return f"{self.__class__.__name__}({self.value})"

class Name(Field):                                  # Name 
    @Field.value.setter
    def value(self, value:str):
        if not(re.findall(r'[^a-zA-Z\s]', value)):  # check if name is valid: [value.isalpha\s]
            self._Field__value = value
        else:
            raise ValueError('Name should include only letter character')
    
class Birthday(Field):                               # Birthday
    @Field.value.setter
    def value(self, value=None):
        if value:
            try:                                       
                self._Field__value = datetime.strptime(value, '%Y-%m-%d').date() 
            except Exception:
                print("Date should be in the format YYYY-MM-DD") # add info about format of the date

class Phone(Field):                                  #Phone
    @Field.value.setter
    def value(self, value):
        phone_pattern_ua = re.compile(r"^0[3456789]\d{8}$") # format UA mobile_operators,10 numbers and only digits,first 0
        if phone_pattern_ua.match(value):
            self._Field__value = value
        else:
            raise ValueError('Phone is not valid')
    
class Record:                                       
    def __init__(self, name, birthday=None) -> None:
        self.name = Name(name)
        self.birthday = Birthday(birthday)  
        self.phones = []  
   
    def add_phone(self, phone_number:str): 
        phone = Phone(phone_number)  
        if phone not in self.phones: 
            self.phones.append(phone) 

    def remove_phone(self, phone_number:str): 
        phone = Phone(phone_number)
        for i in self.phones:
         if phone.value == i.value:
            self.phones.remove(i)  

    def edit_phone(self, old_phone, new_phone):  
        if not self.find_phone(old_phone): 
            raise ValueError
        for i, phone in enumerate(self.phones): # get position for replasement, phone
            if phone.value == old_phone:
                new_phone_obj = Phone(new_phone) 
                self.phones[i] = new_phone_obj   


    def find_phone(self, phone_number:str): 
        phone = Phone(phone_number)
        for i in self.phones:
            if i.value == phone.value: 
                return i
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            date_now = datetime.now().date()
            user_next_birthday = datetime(date_now.year, self.birthday.value.month, self.birthday.value.day).date() # birthday will be in this year
            user_next_year = user_next_birthday.replace(year=date_now.year +1)                                      # birthday will be in next year
            delta = user_next_birthday - date_now if user_next_birthday >= date_now else user_next_year - date_now
            return f'days to birthday: {delta.days}'
   
    def __str__(self) -> str: 
        return f"contact name:{self.name.value}, phones:{'; '.join(i.value for i in self.phones)}, birthday:{self.birthday.value if self.birthday else 'N/A'}"



class AddressBook(UserDict): 
    def add_record(self, record: Record): 
        key = record.name.value
        self.data[key] = record

    def find(self, name):   
        return self.data.get(name)

    def delete(self, name):  
        if name in self.data:
            del self.data[name]
    
    def __iter__(self) -> Iterator:  
        return AddressBookIterator(self.data.values(), page_size=1)  # Iterable class
    
    def __repr__(self):
        return f"AddressBook({self.data})"

class AddressBookIterator:
    def __init__(self, records_list, page_size):
        self.records = list(records_list)
        self.page_size = page_size
        self.counter = 0                                # quantity on page
        self.page = len(self.records) // self.page_size # use for showing part of the reccords that size < page_size
    
    def __next__(self):
        if self.counter >= len(self.records):
            raise StopIteration
        else:
            if self.page > 0:
                result = list(self.records[self.counter:self.counter + self.page_size]) # slice reccords on the page
                self.page -= 1
                self.counter += self.page_size
            else:
                result = list(self.records[self.counter:])  #the rest of the records on the page
                self.counter = len(self.records)
        return result        
