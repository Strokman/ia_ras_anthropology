from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Alias common SQLAlchemy names
session = db.session

Model = db.Model
Column = db.Column
Table = db.Table

ForeignKey = db.ForeignKey
relationship = db.relationship

Boolean = db.Boolean
DateTime = db.DateTime
Integer = db.Integer
Numeric = db.Numeric
String = db.String
