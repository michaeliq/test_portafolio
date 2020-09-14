from app import AppFlask

db = AppFlask.get_instance_db()

class Skill(db.Model):
    __tablename__= 'Skills'
    id = db.Column(db.Integer,primary_key=True)  
    target = db.Column(db.String,nullable=False) 
    knowlegd = db.Column(db.Float)            
    description = db.Column(db.String)
    
                                         
    def __init__(self,target,knowlegd,description = None):                      
        self.target= target          
        self.knowlegd= knowlegd       
        self.description = description


    def __repr__(self):
        return f'Target: {self.target}'

    def __str__(self):
        return self.target

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id_target):
        id_tag = db.session.query(Skill).get(id_target)
        return id_tag

    def delete_tag(self):         
        db.session.delete(self)

    def update_tag(self, knowlegd, description):
        self.knowlegd = knowlegd or self.knowlegd                             
        self.description = description or self.description                      
        db.session.commit()   

    @staticmethod         
    def get_all():
        return Skill.query.all()


class Client(db.Model):
    __tablename__= "Clients"                                                          
    id = db.Column(db.Integer,primary_key=True) 
    name = db.Column(db.String,nullable=False)  
    telephone = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    def __init__(self,name,telephone,email):
        self.name = name              
        self.telephone = telephone       
        self.email = email

    def __repr__(self):
        return f'Client: {self.name}'

    def __str__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Client.query.all()
