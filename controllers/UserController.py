from flask import jsonify, redirect, render_template, url_for
from models import ContractsModel

class User:
    def __init__(self):
        self.contract  = ContractsModel.Contracts()
        
    def index(self, req, link):
        return render_template('user.html', link_user=link)
    
    def code(self, req, code):
        user = self.contract.find({'link':code, 'status': True})
        user_json = jsonify(user)
        return user_json
        