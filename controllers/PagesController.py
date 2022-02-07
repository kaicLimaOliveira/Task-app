import csv
import random
import string
import threading
import uuid
from datetime import datetime as date
from flask import redirect, render_template, url_for
from models import ContractsModel, ImportModel

class Pages:
    def __init__(self):
        self.imports = ImportModel.Imports()
        self.contract = ContractsModel.Contracts()
        self.status_type = "Ativo"
        self.file_import = f'import_{uuid.uuid4()}.csv'
        self.file_link = f'links_{uuid.uuid4()}.csv'
        
        self.key_access = None
        self.link_random = None
        self.link_user = {
            "key_access": [],
            "link_random": [],
            "error_status": []
        }
        
        self.count_error = 0  # contador de erros
        self.line_errors = {}
        self.errors = {
            "count": 0,
            "line_errors": {}
        }

    def monetary_format(self, input_value):
        if "." in input_value:
            input_value = input_value.replace('.', '')      

            if "," in input_value:
                input_value = float(input_value.replace(',', '.'))

                return input_value

        elif "," in input_value:
            input_value = float(input_value.replace(',', '.'))

            return input_value

    def process(self, file_name):
        with open('static/uploads/' + file_name.filename, 'r', encoding='utf-8') as read_file_CSV:

            next(read_file_CSV)
            table = csv.reader(read_file_CSV, delimiter=';')

            count_line = 1  # em qual linha está
            count_contract_success = 0
            for index in table:
                count_error = 0
                for x in range(1):
                    self.link_random = ''.join(random.choice(string.ascii_letters)for _ in range(10))
                    self.link_user["link_random"].append(self.link_random)
                try:
                    name = index[0]
                    self.key_access = index[1]
                    contract = index[2]
                    input_value = index[3]
                    date_entries = index[4]
                    installment_amount = index[5]
                    installment = index[6]
                    value_installment = index[7]
                    expire = index[8]

                    if not name:  # nome completo
                        count_error += 1
                        if index[0] == '':
                            self.line_errors[f'{count_line}-1'] = 'coluna nome vazia'

                    if not self.key_access:  # chave de acesso
                        count_error += 1
                        if index[1] == '':
                            self.line_errors[f'{count_line}-2'] = 'coluna chave de acesso vazia'

                    if not contract:  # contrato
                        count_error += 1
                        if index[2] == '':
                            self.line_errors[f'{count_line}-3'] = 'coluna contrato vazia'

                    if not input_value:  # valor de entrada
                        count_error += 1
                        if index[3] == '':
                            self.line_errors[f'{count_line}-4'] = 'coluna valor de entrada vazia'
                    else:
                        self.monetary_format(input_value)

                    if not date_entries:  # data de entrada
                        count_error += 1
                        if index[4] == '':
                            self.line_errors[f'{count_line}-5'] = 'coluna data de entrada vazia'
                    else:
                        date_entries = date_entries.split('/')
                        for data in range(len(date_entries)):
                            date_entries[data] = int(date_entries[data])

                        date_entries = date(date_entries[2], date_entries[1], date_entries[0]).strftime('%d/%m/%Y')

                    if not installment_amount:  # quantidade
                        count_error += 1
                        if index[5] == '':
                            self.line_errors[f'{count_line}-6'] = 'coluna quantidade de parcelas vazia'
                    else:
                        installment_amount = int(installment_amount)

                    if not installment:  # vencimento
                        count_error += 1
                        if index[6] == '':
                            self.line_errors[f'{count_line}-7'] = 'coluna vencimentos das parcelas vazia'
                    else:
                        installment = int(installment)

                    if not value_installment:  # valor das parcelas
                        count_error += 1
                        if index[7] == '':
                            self.line_errors[f'{count_line}-8'] = 'coluna valor das parcelas vazia'
                    else:
                        value_installment = int(value_installment)

                    if not expire:  # expiração das parcelas
                        count_error += 1
                        if index[8] == '':
                            self.line_errors[f'{count_line}-9'] = 'coluna expiração das parcelas vazia'
                    else:
                        expire = expire.split('/')
                        for data in range(len(expire)):
                            expire[data] = int(expire[data])

                        expire = date(expire[2], expire[1], expire[0]).strftime('%d/%m/%Y')

                    self.errors['count'] = self.errors['count'] + count_error
                    self.errors['line_errors'] = self.line_errors

                    if count_error > 0:
                        self.link_user["error_status"].append('Sim')
                    else:
                        data_user = self.contract.find({})
                        wallet = 5
                        company_id = 1
                        status = True
                        
                        db_key_access = data_user[count_contract_success]['access_key']
                        db_contract = data_user[count_contract_success]['contract']
                        db_wallet = data_user[count_contract_success]['wallet']
                        db_company_id = data_user[count_contract_success]['company_id']
                        
                        if db_key_access == self.key_access and db_contract == contract and db_wallet == wallet and db_company_id == company_id:
                            status = False
                            self.status_type = "Atualizado"
                            for i in data_user:
                                self.contract.update({'_id':i["_id"]}, {"status": status, "status_type": self.status_type})
                                 
                            data_contract = {
                                "full_name": name,
                                "access_key": self.key_access,
                                "contract": contract,
                                "entry_value": input_value,
                                "entry_date": date_entries,
                                "parcels_value": value_installment,
                                "parcels_quantity": installment_amount,
                                "parcels_day": installment,
                                "expire_date": expire,
                                "variables": {},
                                "link": self.link_random,
                                "status": True,
                                "wallet": wallet,
                                "company_id": company_id,
                                "status_type": "Ativo"  # Tipos - ativo, atualizado e expirado
                            }
                            
                            self.contract.create(data_contract)
                            
                            continue
                        else:
                            data_contract = {
                                "full_name": name,
                                "access_key": self.key_access,
                                "contract": contract,
                                "entry_value": input_value,
                                "entry_date": date_entries,
                                "parcels_value": value_installment,
                                "parcels_quantity": installment_amount,
                                "parcels_day": installment,
                                "expire_date": expire,
                                "variables": {},
                                "link": self.link_random,
                                "status": status,
                                "wallet": wallet,
                                "company_id": company_id,
                                "status_type": self.status_type  # Tipos - ativo, atualizado e expirado
                            }
                    
                            self.contract.create(data_contract)
                            
                        self.link_user["error_status"].append('Não')
                        count_contract_success += 1
                        
                except Exception as e:
                    print(e)
                
                count_line += 1
                self.link_user["key_access"].append(self.key_access)
                
            data_import = {
                "user": "Kaic de Lima Oliveira",
                "errors": self.errors,
                "company_dir": "Kaic",
                "links_file": self.file_link,
                "original_name": file_name.filename,
                "wallet": 5,
                "company_id": 1,
                "contracts_quantity": count_contract_success,
                "file": self.file_import,
                "variables": []
            }

            self.imports.create(data_import)

    def index(self, req):
        if req.method == 'GET':
            return render_template('index.html')

    def new_imports(self, req):
        if req.method == 'GET':
            data = self.imports.find({})
            return render_template('import.html', data=data)
        elif req.method == 'POST':
            try:
                file_name = req.files['fileName']

                file_name.save('static/uploads/' + self.file_import)  # Salvando um arquivo CSV

                t = threading.Thread(target=self.process, args=(file_name, ))  # Execução do Thread
                t.start()

                with open('static/downloads/' + self.file_link, 'w', newline='', encoding='utf-8') as new_file:  # Escrevendo um arquivo CSV manualmente
                    writer_csv = csv.writer(new_file, delimiter=';')

                    data_writer = [
                        [f"{self.link_user['key_access'][0]}", f"{self.link_user['link_random'][0]}", f"{self.link_user['error_status'][0]}"],
                        [f"{self.link_user['key_access'][1]}", f"{self.link_user['link_random'][1]}", f"{self.link_user['error_status'][1]}"],
                        [f"{self.link_user['key_access'][2]}", f"{self.link_user['link_random'][2]}", f"{self.link_user['error_status'][2]}"],
                        [f"{self.link_user['key_access'][3]}", f"{self.link_user['link_random'][3]}", f"{self.link_user['error_status'][3]}"],
                        [f"{self.link_user['key_access'][4]}", f"{self.link_user['link_random'][4]}", f"{self.link_user['error_status'][4]}"],
                        [f"{self.link_user['key_access'][5]}", f"{self.link_user['link_random'][5]}", f"{self.link_user['error_status'][5]}"]
                    ]

                    writer_csv.writerows(data_writer)
            except Exception as e:
                print(e)

        return redirect(url_for('pages.imports', filename=file_name))

    def errors_report(self, req):
        return render_template('errors.html', error=self.errors)
    
    def user(self, req, link):
        user = self.contract.find({'link':link})
        return render_template('user.html', users=user)