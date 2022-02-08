from flask import redirect, render_template, url_for
from models import ContractsModel

class User:
    def __init__(self):
        self.contract  = ContractsModel.Contracts()
        
    def index(self, req, link):
        user = self.contract.find({'link':link})
        return render_template('user.html', users=user)