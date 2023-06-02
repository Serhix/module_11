from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):    # Наслідується від UserDict, словник з полями name, phone....
  
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_record_from_book(self, name):
        for record in self.data.values():
            if record.name.value.lower() == name.lower():
                return record
        return None

    def iterator(self, N = 3):
        data_output = []
        iter_index = 0
        for record in self.data.values():
            data_output.append(record)
            iter_index += 1
            if iter_index >= N:
                yield data_output 
                data_output = []
                iter_index = 0
        if data_output:
            yield data_output

        
        
class Record:                   # Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name.
  
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ''
        self.has_birthday = False

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def delete_phone(self, phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                self.phones.remove(phone_number)
                break

    def change_phone(self, phone, new_phone):
        for phone_number in self.phones:
            if phone_number.value == phone:
                phone_number.value = new_phone
                break
    
    def days_to_birthday(self):
        if self.has_birthday == True:
            birthday_in_this_year = datetime(
                year=datetime.now().year, 
                month=str_to_date(self.birthday.value).month, 
                day=str_to_date(self.birthday.value).day
            )
            if birthday_in_this_year.date() == datetime.now().date():
                return 'Birthday today'
            elif birthday_in_this_year.date() < datetime.now().date():
                how_many_days = datetime(year=datetime.now().year + 1, month=birthday_in_this_year.month, day=birthday_in_this_year.day) - datetime.now()
            else:
                how_many_days = datetime(year=datetime.now().year, month=birthday_in_this_year.month, day=birthday_in_this_year.day) - datetime.now()
            return f'Birthday in {how_many_days.days} days!'
        return f'No birthday added for contact {self.name}'
    
    def __str__(self) -> str:
        if self.has_birthday:
            return f'Name: {self.name.value}, phone: {", ".join(j.value for j in self.phones)}, birthday: {self.birthday.value}!'
        return f'Name: {self.name.value}, phone: {", ".join(j.value for j in self.phones)}'

    
    

class Field:                    # Батьківський для всіх полів, у ньому потім реалізуємо логіку, загальну для всіх полів.

    def __init__(self, value):
        self.__value = None
        self.value = value


class Name(Field):              # Обов'язкове поле з ім'ям

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if new_value and not new_value.isnumeric():
            self.__value = new_value
        else:
            print('Incorect name! setter')
    

class Phone(Field):             # Необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if new_value.isnumeric():
            self.__value = new_value
        else:
            print('Incorect phone! setter')


class Birthday(Field):             # Необов'язкове поле з днем народження. може бути лише одне

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        # дату вводити в форматі дд.мм.рррр.
        birthday_date = str_to_date(new_value)
        if birthday_date.year > 1900 and birthday_date <= datetime.now():
            self.__value = new_value
        else:
            print('Incorect birthday!')



# блок функцій з модуля 9(змінено)

def input_error(func):
    
    def wrapper(*args):        
        try:
            return func(*args)
        except KeyError:
            return "KeyError, maybe contact list is empty"
        except (IndexError, AttributeError, TypeError):
            return "Enter the correct command!!!"
        except ValueError as error:
            return str(error)

    return wrapper

def hello():
    return 'How can I help you?'

def add(data):                                    # додаємо новий номер до адресної книги(до існуючого або нового контакту)
    name, phone = parse_data(data)
    name = Name(name)
    phone = Phone(phone)
    record = address_book.get_record_from_book(name.value)
    if not record:
        record = Record(name.value)
    record.add_phone(phone.value)
    address_book.add_record(record)
    return 'Number added!'

def add_birthday(data):                                    # додаємо birthday(до існуючого або нового контакту)
    name, birthday = parse_data(data)
    name = Name(name)
    birthday = Birthday(birthday)
    record = address_book.get_record_from_book(name.value)
    if not record:
        record = Record(name.value)
    record.add_birthday(birthday.value)
    record.has_birthday = True
    address_book.add_record(record)
    return 'Birthday added!'


def change(data):                     # міняємо номер phone на new_phone для контакту name
    name, phone, new_phone = parse_data(data)
    name = Name(name)
    phone = Phone(phone)
    new_phone = Phone(new_phone) 
    record = address_book.get_record_from_book(name.value)
    if not record:
        return f'Contact with name {name.value} not found'
    record.change_phone(phone.value, new_phone.value)
    address_book.add_record(record)
    return f'The number {phone.value} has been changed to {new_phone.value} for contact {name.value}!'

def delete(data):                                # видаляємо номер phone для контакту name
    name, phone = parse_data(data)
    name = Name(name)
    phone = Phone(phone)
    record = address_book.get_record_from_book(name.value)
    if not record:
        return f'Contact with name {name.value} not found'
    record.delete_phone(phone.value)
    address_book.add_record(record)
    return f'The number {phone.value} has been delete for contact {name.value}!'

def info(data):                                # пошук по name
    name = parse_data(data)[0]
    name = Name(name)
    record = address_book.get_record_from_book(name.value)
    if not record:
        return f'Contact with name {name.value} not found'
    return str(record)

def when_birthday(data):                                # пошук по name
    name = parse_data(data)[0]
    name = Name(name)
    record = address_book.get_record_from_book(name.value)
    if not record:
        return f'Contact with name {name.value} not found'
    return record.days_to_birthday()

def show_all(data):
    N = int(parse_data(data)[0])
    all_book = ''
    page_number = 1
    for page in address_book.iterator(N):
        all_book += f'Page -- {page_number} -- \n'
        for record in page:
            all_book += f'{str(record)} \n'
        page_number += 1
    return all_book

def exit_func():
    return 'Good bye!'

def incorrect_input():
    return 'incorrect command input'

def parse_data(data):
    new_data = []
    for field in data.strip().split():
        new_data.append(field)
    return new_data

def str_to_date(value: str): # dd.mm.yyyy
    return datetime(day = int(value.split('.')[0]), month = int(value.split('.')[1]), year = int(value.split('.')[2]))

@input_error
def choise_comand(request):

    COMANDS = {
    'hello': hello,
    'show all' : show_all,
    'info': info,
    'add': add,
    'birthday': add_birthday,
    'change': change,
    'delete': delete,
    'close': exit_func, 
    'exit': exit_func,
    'good bye': exit_func,
    'when birthday': when_birthday,

}
    comand = request
    data = ''
    for key in COMANDS:
        if request.strip().lower().startswith(key):
            comand = key
            data = request[len(comand):]
            break
    if data:
        return COMANDS.get(comand, incorrect_input)(data)
    return COMANDS.get(comand, incorrect_input)()

def main():
    while True:
        request = input('- ').lower()
        result = choise_comand(request)
        print(result)
        if result == 'Good bye!':
            break


if __name__ == '__main__':
    address_book = AddressBook()
    main()


