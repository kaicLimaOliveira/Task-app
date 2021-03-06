import csv
from operator import contains
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
        
        self.file_import = f'import_{uuid.uuid4()}.csv'
        self.file_link = f'links_{uuid.uuid4()}.csv'
        
        self.key = []

        self.link_random = None
        self.link_user = {
            "key_access": [],
            "link_random": [],
            "error_status": []
        }
        
        self.variables = {}        
        self.count_error = 0  # contador de erros
        self.line_errors = {}
        self.errors = {
            "count": 0,
            "line_errors": {}
        }

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
                
            except Exception as e:
                print(e)

        return redirect(url_for('pages.imports', filename=file_name)) 

    def errors_report(self, req):
        errors = self.imports.find({})
        return render_template('errors.html', errors=errors)

    def process(self, file_name):
        with open('static/uploads/' + file_name.filename, 'r', encoding='utf-8') as read_file_CSV:

            # next(read_file_CSV)
            table = csv.reader(read_file_CSV, delimiter=';')

            count_line = 1  # em qual linha está
            count_contract_success = 0
            index_count = 0
            
            for row in table:
                self.new_variables(row, count_line)
                count_error = 0
                self.generate_link_random()
                try:
                    name = row[0]
                    key_access = row[1]
                    contract = row[2]
                    input_value = row[3]
                    date_entries = row[4]
                    installment_amount = row[5]
                    installment = row[6]
                    value_installment = row[7]
                    expire = row[8]
                    
                    if not name:  
                        count_error += 1
                        self.line_errors[f'{count_line}-1'] = 'coluna nome vazia'

                    if not key_access:  
                        count_error += 1
                        self.line_errors[f'{count_line}-2'] = 'coluna chave de acesso vazia'

                    if not contract:  
                        count_error += 1
                        self.line_errors[f'{count_line}-3'] = 'coluna contrato vazia'

                    if not input_value:  
                        count_error += 1
                        self.line_errors[f'{count_line}-4'] = 'coluna valor de entrada vazia'
                    else:
                        self.monetary_format(input_value)

                    if not date_entries:  
                        count_error += 1
                        self.line_errors[f'{count_line}-5'] = 'coluna data de entrada vazia'
                    else:
                        date_entries = date_entries.split('/')
                        for data in range(len(date_entries)):
                            print(data, 'data')
                            print(len(date_entries), 'len date')
                            date_entries[data] = int(date_entries[data])

                        date_entries = date(date_entries[2], date_entries[1], date_entries[0]).strftime('%d/%m/%Y')

                    if not installment_amount:  
                        count_error += 1
                        self.line_errors[f'{count_line}-6'] = 'coluna quantidade de parcelas vazia'
                    else:
                        installment_amount = int(installment_amount)

                    if not installment:  
                        count_error += 1
                        self.line_errors[f'{count_line}-7'] = 'coluna vencimentos das parcelas vazia'
                    else:
                        installment = int(installment)

                    if not value_installment:  
                        count_error += 1
                        self.line_errors[f'{count_line}-8'] = 'coluna valor das parcelas vazia'
                    else:
                        value_installment = int(value_installment)

                    if not expire:  
                        count_error += 1
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
                        wallet = 5
                        company_id = 1
                        user_access_control = self.contract.find({'company_id':company_id, 'access_key': key_access})   
                                        
                        if len(user_access_control) > 0:
                            self.contract.update(
                                {
                                    'access_key': key_access, 
                                    'contract': contract, 
                                    'wallet': wallet, 
                                    'company_id': company_id
                                }, 
                                {"status": False, "status_type": "Atualizado"}
                            )
                            
                            link_user_old = user_access_control[-1]['link']
                            self.create_contracts_bd(
                                name, key_access, contract, input_value, 
                                date_entries, value_installment,installment_amount, 
                                installment, expire, wallet, company_id
                            )
                            
                            self.contract.update(
                                {'link':self.link_random},
                                {'link': link_user_old}
                            )
                            
                        else:         
                            self.create_contracts_bd(
                                name, key_access, contract, input_value, 
                                date_entries, value_installment,installment_amount, 
                                installment, expire, wallet, company_id
                            )

                        self.link_user["error_status"].append('Não')
                        count_contract_success += 1

                    self.link_user["key_access"].append(key_access)
                    self.writer_csv_file(index_count, count_line)
                    
                except Exception as e:
                    print(e)
                
                count_line += 1

            self.create_imports_bd(file_name, count_contract_success)
            
    def new_variables(self, row, count_line):
        index_value = 9
        index_key = 9 
        
        if count_line == 1: 
            if len(row) < 8:
                pass
            else:
                try:
                    while row[index_key]:
                        self.key.append(row[index_key])
                        self.variables[row[index_key]] = ''
                        index_key += 1

                        #fazer replace no padrão das Variaveis
        
                except Exception as e:
                    print(e)

        elif count_line >= 2:           
            if len(row) < 8:
                pass
            else:
                try:
                    for i in self.key:
                        self.variables[i] = row[index_value]
                        index_value += 1
                
                except Exception as e:
                    print(e)
                         
    def monetary_format(self, input_value):
        if "." in input_value:
            input_value = input_value.replace('.', '')      

        if "," in input_value:
            input_value = float(input_value.replace(',', '.'))
            return input_value

        elif "," in input_value:
            input_value = float(input_value.replace(',', '.'))
            return input_value
                
    def create_contracts_bd(self, name, key_access, contract, input_value, date_entries, value_installment,installment_amount, installment,expire, wallet, company_id):
        data_contract = {
            "full_name": name,
            "access_key": key_access,
            "contract": contract,
            "entry_value": input_value,
            "entry_date": date_entries,
            "parcels_value": value_installment,
            "parcels_quantity": installment_amount,
            "parcels_day": installment,
            "expire_date": expire,
            "variables": self.variables,
            "link": self.link_random,
            "status": True,
            "wallet": wallet,
            "company_id": company_id,
            "status_type": "Ativo"  # Tipos - ativo, atualizado e expirado
        }
        
        self.contract.create(data_contract)
                  
    def create_imports_bd(self,file_name, count_contract_success):
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
               
    def generate_link_random(self):
        for x in range(1):
            self.link_random = ''.join(random.choice(string.ascii_letters)for _ in range(10))
            self.link_user["link_random"].append(self.link_random)
    
    def writer_csv_file(self, index_count, count):
        with open('static/downloads/' + self.file_link, 'w', newline='', encoding='utf-8') as new_file:  # Escrevendo um arquivo CSV manualmente
            writer_csv = csv.writer(new_file, delimiter=';')
            
            for i in range(count):
                data_writer = [
                    ['chave_de_acesso', 'link_do_usuario', 'erro'],
                    [
                        f"{self.link_user['key_access'][index_count]}", 
                        f"{self.link_user['link_random'][index_count]}", 
                        f"{self.link_user['error_status'][index_count]}"    
                    ] 
                ]
                
                index_count += 1
                writer_csv.writerows(data_writer)