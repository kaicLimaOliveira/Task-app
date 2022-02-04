from time import mktime
from validate_docbr import CPF, CNPJ
import datetime
import re
import uuid
import unidecode
from hashlib import sha256

class Utils(object):

    def only_numbers(self, string):
        return re.sub('[^0-9]', '', string)

    # Valida se é CPF ou CNPJ
    def validate_doc(self, doc):
        if doc is None:
            return False
        doc = self.only_numbers(doc)
        validate = False
        if CPF().validate(doc):
            validate = {"type": "cpf", "person_type": "F", "doc": doc}
        elif CNPJ().validate(doc):
            validate = {"type": "cnpj", "person_type": "J", "doc": doc}
        return validate

    def validate_phone(self, phone):
        phone = self.only_numbers(phone)
        if len(phone) != 11:
            return False
        try:
            int(phone)
        except:
            return False
        if phone[2] != '9':
            return False
        return phone

    def validate_email(self, email):
        check_at = [m.start() for m in re.finditer('@', email)]
        check_dot = [m.start() for m in re.finditer('.', email)]
        validate = False
        if len(check_at) == 1 and len(check_dot) > 0:
            email_explode = email.split('@')[0]
            username = email_explode[0]
            domain = email_explode[1]
            validate = {"email": email, "username": username, "domain": domain}
        return validate

    def validate_dob(self, dob):
        try:
            dob = datetime.datetime.strptime(dob, "%d/%m/%Y")
            print(((datetime.datetime.now() - dob).days / 365))
            if (((datetime.datetime.now() - dob).days / 365) < 18 or (
                    (datetime.datetime.now() - dob).days / 365) > 130):
                return False
            return True
        except:
            return False

    def format_currency(self, value):
        try:
            value = '{:,.2f}'.format(value)
            value = str(value)
            value = value.replace(',', '-')
            value = value.replace('.', ',')
            value = value.replace('-', '.')
        except:
            value = value
        return value

    def truncate_date(self, some_date):
        return some_date.replace(day=1, hour=0, minute=0, microsecond=0)

    def truncate_hour(self, some_date):
        return some_date.replace(hour=0, minute=0, microsecond=0)

    def transform_datetime(self, date):
        if date == '':
            return ''
        return date.strftime('%d/%m/%Y - %H:%M:%S')

    def transform_date(self, date):
        if date == '':
            return ''
        return date.strftime('%d/%m/%Y')

    def unformat_currency(self, value):
        value = str(value)
        value = value.replace(',', '-')
        value = value.replace('.', '')
        value = value.replace('-', '.')
        return value

    def len_to_bool(self, data):
        try:
            number = len(data)
        except:
            return False
        try:
            if int(number) == 0:
                return False
            else:
                return True
        except:
            return False

    def generate_random(self):
        return str(uuid.uuid4())

    def generate_date_string(self, fmt):
        return datetime.datetime.now().strftime(fmt)

    def generate_date_datetime(self):
        return datetime.datetime.now()

    def cypher_password(self, password):
        return sha256(str(password).encode('UTF-8')).hexdigest()

    def get_date(self, date, days, operation):
        date_now = datetime.timedelta(days=days)

        if not isinstance(operation, str):
            raise ValueError('O operador deve ser uma string!')
        elif not operation.isalpha():
            raise ValueError('Operador não reconhecido, é permitido apenas add ou remove')
        elif operation == 'add' or operation == 'remove':
            pass
        else:
            raise ValueError('Operador não reconhecido, é permitido apenas add ou remove')

        if not isinstance(date, datetime.datetime):
            raise ValueError('A data deve ser do tipo datetime')

        if operation == 'remove':
            date_now = date - date_now
        elif operation == 'add':
            date_now = date + date_now
        else:
            return date_now
        return  date_now

    def filename(self, extension):
        extension = f'.{str(extension)}'
        return str(datetime.datetime.timestamp(datetime.datetime.now())).replace('.', '') + extension

    def transform_time(self, date):
        if date == '':
            return ''
        else:
            dt = datetime.fromtimestamp(mktime(date))
            return dt.strftime('%d/%m/%Y')

    def transform_date_iso(self, date):
        if date == '':
            return ''
        return date.strftime('%Y-%m-%d')

    def brdate_to_datetime(self, text):
        if text == '':
            return False
        try:
            if len(text.split("/")[2]) == 2:
                text = text.split('/')
                text[2] = "20" + text[2]
                text = "/".join(text)
            dt = datetime.strptime(text, '%d/%m/%Y')
            return dt
        except:
            return False

    def brdate_to_datetime_expires(self, text):
        if text == '':
            return False
        try:
            if len(text.split("/")[2]) == 2:
                text = text.split('/')
                text[2] = "20" + text[2]
                text = "/".join(text)
            text = text + " 23:59"
            dt = datetime.strptime(text, '%d/%m/%Y %H:%M')
            return dt
        except:
            return False

    def brdate_hour_to_datetime(self, date):
        try:
            dt = datetime.strptime(date, '%d/%m/%Y %H:%M')
            return dt
        except:
            return False

    def generate_password(self):
        pass

    def boolean(self, data):
        dct = {True: "Sim", False: "Não"}
        return dct[data]

    def format_docs(self, doc):
        pass

    # Faz o tratamento, retirando pontuações, e devolve um float
    def normalize_number(self, text):
        try:
            text = str(text)
            text = text.replace(".", "")
            text = text.split(",")

            first_part = text[0]

            try:
                second_part = text[1]
            except:
                return first_part

            return f"{first_part}.{second_part[0: 2]}"
        except:
            return text

    # Formata um float em forma monetária
    def format_money(self, text):
        try:
            text = str(text)
            text = text.split(".")

            first_part = text[0]

            try:
                second_part = text[1]
                if len(second_part) == 1:
                    second_part += "0"
                elif len(second_part) == 0:
                    second_part = "00"
            except:
                second_part = "00"

            new_str = ''
            first_part = list(first_part)
            first_part.reverse()

            for i in range(len(first_part)):
                if i % 3 == 0:
                    new_str += "." + first_part[i]
                else:
                    new_str += first_part[i]

            new_str = list(new_str)
            new_str[0] = ""
            new_str.reverse()
            new_str = "".join(new_str)
            new_str = new_str + "," + second_part

            return new_str

        except:

            return text

    # Faz formatação de um int para casa de milhar
    def format_number(self, text):
        try:
            text = str(text)
            new_str = ''
            text = list(text)
            text.reverse()

            for i in range(len(text)):
                if i % 3 == 0:
                    new_str += "." + text[i]
                else:
                    new_str += text[i]

            new_str = list(new_str)
            new_str[0] = ""
            new_str.reverse()
            new_str = "".join(new_str)

            return new_str
        except:
            return text

    def remove_ponctuation(self, doc):
        if not isinstance(doc, str):
            raise ValueError('Type doc must be string.')
        doc = unidecode.unidecode(doc)
        return doc

    def valid_date(self, date):
        try:
            date = date.split("/")
            if len(date[2]) == 2:
                date[2] = "20" + date[2]
            int(date[2])
            int(date[1])
            int(date[0])
            return True
        except:
            return False

    def valid_date_less_than_now(self, date):
        try:
            date = date.split("/")
            if len(date[2]) == 2:
                date[2] = "20" + date[2]
            int(date[2])
            int(date[1])
            int(date[0])
            if date < datetime.now():
                return False
            else:
                return True
        except:
            return False
