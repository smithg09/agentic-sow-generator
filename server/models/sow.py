from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SOWUserInput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_objectives = db.Column(db.Text,nullable = False)
    project_scope = db.Column(db.Text,nullable = False)
    detailed_desc = db.Column(db.Text,nullable = False)
    specific_feature = db.Column(db.Text,nullable = False)
    platform_tech = db.Column(db.Text,nullable = False)
    integrations = db.Column(db.Text,nullable = False)
    design_specification = db.Column(db.Text,nullable = False)
    out_of_scope = db.Column(db.Text,nullable = False)
    deliverables = db.Column(db.Text,nullable = False)
    project_timeline = db.Column(db.Text,nullable = False)