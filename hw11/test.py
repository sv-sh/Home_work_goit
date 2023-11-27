from _collections_abc import Iterator
from datetime import datetime
import main
from main import AddressBook, Record

address_book = AddressBook()
record1 = Record("John Doe", "1985-12-15")
record1.add_phone("0934567677")
address_book.add_record(record1)
print(record1.days_to_birthday())
print(record1)

record2 = Record("John Smith", "1985-09-03")
record2.add_phone("0934569823")
address_book.add_record(record2)
print(record2.days_to_birthday())
print(record2)

record3 = Record("Jin Bork", "2000-03-19")
record3.add_phone("0934568877")
print(record3.days_to_birthday())
address_book.add_record(record3)
print(record3)

for page in address_book:
    for record in page:
        print(record)
        print(record.days_to_birthday())
    print('*' * 20)