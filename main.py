from collections import UserDict


class AddressBook(UserDict):    # Наслідується від UserDict, словник з полями name, phone....
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_record_from_book(self, name):
        for record in self.data.values():
            if record.name.value.lower() == name.lower():
                return record
        return None
        
class Record:                   # Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання обов'язкового поля Name.
  
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add(self, phone):
        self.phones.append(Phone(phone))

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
    
    
    

class Field:                    # Батьківський для всіх полів, у ньому потім реалізуємо логіку, загальну для всіх полів.
    def __init__(self, value):
        self.value = value

class Name(Field):              # Обов'язкове поле з ім'ям
    pass
    


class Phone(Field):             # Необов'язкове поле з телефоном та таких один запис (Record) може містити кілька.
    pass

class Birthday(Field):             # Необов'язкове поле з днем народження. може бути лише одне
    pass


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
    if not phone.isnumeric():
        return 'Incorect phone'
    record = address_book.get_record_from_book(name)
    if not record:
        record = Record(name)
    record.add(phone)
    address_book.add_record(record)
    return 'Number added!'


def change(data):                     # міняємо номер phone на new_phone для контакту name
    name, phone, new_phone = parse_data(data)
    if not phone.isnumeric() or not new_phone.isnumeric():
        return 'Incorect phone or new phone'
    record = address_book.get_record_from_book(name)
    if not record:
        return f'Contact with name {name} not found'
    record.change_phone(phone, new_phone)
    address_book.add_record(record)
    return f'The number {phone} has been changed to {new_phone} for contact {name}!'

def delete(data):                                # видаляємо номер phone для контакту name
    name, phone = parse_data(data)
    if not phone.isnumeric():
        return 'Incorect phone'
    record = address_book.get_record_from_book(name)
    if not record:
        return f'Contact with name {name} not found'
    record.delete_phone(phone)
    address_book.add_record(record)
    return f'The number {phone} has been delete for contact {name}!'

def info(data):                                # пошук по name
    name = parse_data(data)[0]
    record = address_book.get_record_from_book(name)
    if not record:
        return f'Contact with name {name} not found'
    return f'The contact {name} has the following phone numbers {", ".join(j.value for j in record.phones)}!'

def show_all():                                 #вивід всієї книги
    if not address_book.data: 
        return 'Maybe namber list is empty!'
    else:
        print('Contact list:')
        result = []
        for phone in address_book.data.values():
            result.append(f'name: {phone.name.value}, phone: {", ".join(j.value for j in phone.phones)}') 
        return '\n'.join(result)

def exit_func():
    return 'Good bye!'

def incorrect_input():
    return 'incorrect command input'

def sanitize_phone(phone):
    new_phone = (
        phone.removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
    )
    return new_phone

def parse_data(data):
    new_data = []
    for field in data.strip().split():
        new_data.append(field)

    return new_data


@input_error
def choise_comand(request):

    COMANDS = {
    'hello': hello,
    'show all' : show_all,
    'info': info,
    'add': add,
    'change': change,
    'delete': delete,
    'close': exit_func, 
    'exit': exit_func,
    'good bye': exit_func
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


