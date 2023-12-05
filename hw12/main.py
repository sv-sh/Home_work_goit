from _collections_abc import Iterator
from collections import UserDict
from datetime import datetime
from faker import Faker   
import random
import re
import pickle
import os

filename = 'test.txt'
"""
For the console bot, please use the following syntax:

- `add FirstName SecondName, Number_of_the_phone_10_numbers_ua, Date_of_Birthday(YYYY-MM-DD)`: Add records to the address_book.
- `find FirstName SecondName`: Find records (case-sensitive).
- `search any_letters_of_the_name_or_numbers_of_the_phone`: Show all records that satisfy the search pattern.
- `delete FirstName SecondName`: Delete records.
- `generate`: Create 10 random records.
- `show`: Show records and days to Birthday.
"""

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

class Name(Field):
    @Field.value.setter
    def value(self, value:str):
        if not(re.findall(r'[^a-zA-Z\s]', value)): # check if name is valid: [value.isalpha\s]
            self._Field__value = value
        else:
            raise ValueError('Name should include only letter character')
    
class Birthday(Field):
    @Field.value.setter
    def value(self, value=None):
        if value:
            try:                                       
                self._Field__value = datetime.strptime(value, '%Y-%m-%d').date() 
            except Exception:
                print("Date should be in the format YYYY-MM-DD") # add info about format of the date

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        phone_pattern_ua = re.compile(r"^0[3456789]\d{8}$") # format UA mobile_operators,10 numbers and only digits,first 0
        if phone_pattern_ua.match(value):
            self._Field__value = value
        else:
            raise ValueError('Phone is not valid')
    
class Record: 
    def __init__(self, name, phone=None, birthday=None) -> None:  # create record
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phone = Phone(phone) if phone else None
        self.phones = [self.phone] if phone else [] 
   
    def add_phone(self, phone_number:str): # adding phone
        if self.phone not in self.phones: 
            self.phones.append(self.phone) 

    def remove_phone(self, phone_number:str):  #delete phone
        for i in self.phones:
         if self.phone.value == i.value:
            self.phones.remove(i)  

    def edit_phone(self, old_phone, new_phone):  # edit  reccords 
        if not self.find_phone(old_phone): 
            raise ValueError
        for i, phone in enumerate(self.phones): # get position for replasement with phone object
            if phone.value == old_phone:
                new_phone_obj = Phone(new_phone) 
                self.phones[i] = new_phone_obj   


    def find_phone(self, phone_number:str): # find phone if it exist 
        for i in self.phones:
            if i.value == self.phone.value: 
                return i
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            date_now = datetime.now().date()
            user_next_birthday = datetime(date_now.year, self.birthday.value.month, self.birthday.value.day).date() # birthday will be in this year
            user_next_year = user_next_birthday.replace(year=date_now.year +1)                                      # birthday will be in next year
            delta = user_next_birthday - date_now if user_next_birthday >= date_now else user_next_year - date_now
            return f'days to birthday: {delta.days}'
   
    def __str__(self) -> str: # readable view
        return f"contact name:{self.name.value}, phones:{'; '.join(i.value for i in self.phones)}, birthday:{self.birthday.value if self.birthday else 'N/A'}"

class AddressBook(UserDict): 
    def add_record(self, record: Record): # add record in dictionary
        key = record.name.value
        self.data[key] = record

    def find(self, name):   # get record in dictionary
        return self.data.get(name)

    def delete(self, name):  # delete record in dictionary
        if name in self.data:
            del self.data[name]
            return print(f'record {name} deleted')


    def save_to_file(self, filename):     # serialization data to file
        with open(filename, 'wb') as file_write:
            pickle.dump(self.data, file_write)
            return f'exit'
    
    def restore_from_file(self, filename): # deserialization data from file
        with open(filename, 'rb') as file_read:
            self.data = pickle.load(file_read)

    def search (self, row):  # searching records via partial name or phone
        row = row.lower()
        result = [f'{record.name.value}, {", ".join(phone.value for phone in record.phones)}, {record.birthday.value}' 
                for record in self.data.values() if row in record.name.value.lower() 
                or any(row in phone.value for phone in record.phones)]
        return "\n".join(result) if result else None
    
    def generate_random_contacts(self, n=10): # generate records for address_book
        fake = Faker()
        for i in range(n+1):
            name = fake.name()
            phone =f'{0}{random.choice("3456789")}{random.randint(10**7,10**8-1)}' # random phone numbers according pattern (r"^0[3456789]\d{8}$")
            birthday =  fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d')
            record = Record(name, phone, birthday)
            self.add_record(record)
        self.save_to_file(filename)
        print('AddressBook records are generated and saved')

   
    def __iter__(self) -> Iterator:
        return AddressBookIterator(self.data.values(), page_size=2) # Iterable class
   
    def __repr__(self):
        return f"AddressBook({self.data})"

class AddressBookIterator:
    def __init__(self, records_list, page_size):
        self.records = list(records_list)
        self.page_size = page_size
        self.counter = 0  # quantity on page
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
  
if __name__ == '__main__':   
    address_book = AddressBook()  #  create object
    if os.path.getsize(filename)>0: # check if file of data not empty
        address_book.restore_from_file(filename)

    com_dict = {'add': address_book.add_record, # part of command for CLI bot 
                'find': address_book.find,
                'delete': address_book.delete,
                'search': address_book.search}

    while True:  
        cli_in = input("input your command\n")
        cli_in = cli_in.strip()  # eliminate first, end spaces
        cli_in = re.sub(r"\s+", ' ', cli_in)  # eliminate additional spaces between words
        if cli_in.startswith('exit'):
            address_book.save_to_file(filename) 
            print(f'address_book saved')
            break
        
        elif cli_in.startswith('generate'):
            address_book.generate_random_contacts()
        
        elif cli_in.startswith('show'):
            for page in address_book:
                for record in page:
                    print(record)
                    print(record.days_to_birthday())
                print('*' * 20)
            
        else:
            try:
                com_key, data_record = cli_in.split(' ', 1)  # get command and parameters part
                data_record = re.split(r'\s*,\s*', data_record.strip()) # split parameters via ' ,' delimiter

                if com_key in com_dict:
                    if com_key == 'add' and len(data_record) == 3:
                        com_dict[com_key](Record(data_record[0], data_record[1], data_record[2]))
                        print(f'record added')
                    elif len(data_record) != 0:      # another command adress_book
                        result = com_dict[com_key](*data_record)
                        print(result)
            except ValueError:
                print(f'Invalid command')

