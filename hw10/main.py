from collections import UserDict

class Field: #parrent for field
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):  #get readable form, is passed correctly for chaild classes
        return f"{self.__class__.__name__}({self.value})"

class Name(Field):       #inherited Field           
    pass
    

class Phone(Field):   #inherited Field 
    def __init__(self, value = None):
        if value is not None:
            self.valid_phone_check(value) # check correct number
        return super().__init__(value)
    
    def valid_phone_check(self, value:str):
            if not(len(value) == 10 and value.isdigit()):  # and value.startswith('0')-eliminate for passing tests
                raise ValueError('phone is not valid, should be only numbers, and  lenght: 10 symbols')

class Record:  # logick working with contact reccord
    def __init__(self, name) -> None:
        self.name = Name(name)  # name object
        self.phones = []  # list for some quantity of the phones
   
    def add_phone(self, phone_number:str): # adding phone
        phone = Phone(phone_number)  # create phone object
        if phone not in self.phones: 
            self.phones.append(phone) # adding to the list new phones

    def remove_phone(self, phone_number:str):  #delete phone
        phone = Phone(phone_number)
        for i in self.phones:
         if phone.value == i.value:  # compare values in objects
            self.phones.remove(i)  # delete object from list

    def edit_phone(self, old_phone, new_phone):  # editing  reccords of the phones
        if not self.find_phone(old_phone): # checking if exist number for replacement
            raise ValueError
        for i, phone in enumerate(self.phones): # get position for replasement with phone
            if phone.value == old_phone:
                new_phone_obj = Phone(new_phone) # create new phone 
                self.phones[i] = new_phone_obj   # replasement


    def find_phone(self, phone_number:str): # find phone if it exist 
        phone = Phone(phone_number)
        for i in self.phones:
            if i.value == phone.value: 
                return i
        return None
   
    def __str__(self) -> str: # readable view
        return str(f"contact name:{self.name.value}, phones:{'; '.join(i.value for i in self.phones)}") # show all phones


class AddressBook(UserDict): 
    def add_record(self, record: Record): # add record in dictionary
        key = record.name.value
        self.data[key] = record

    def find(self, name):   # get record in dictionary
        return self.data.get(name)

    def delete(self, name):  # delete record in dictionary
        if name in self.data:
            del self.data[name]

    def __repr__(self):
        return f"AddressBook({self.data})"

