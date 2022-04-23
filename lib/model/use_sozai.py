from lib.db import db

class Use_sozai(db.Model):

    __tablename__ = 'use_sozai'

    NO = db.Column(db.Integer, primary_key=True)
    s1_2_name_1 = db.Column(db.String(50))
    s1_2_num_1 = db.Column(db.Integer)
    s1_2_name_2 = db.Column(db.String(50))
    s1_2_num_2 = db.Column(db.Integer)
    s1_2_name_3 = db.Column(db.String(50))
    s1_2_num_3 = db.Column(db.Integer)

    s2_3_name_1 = db.Column(db.String(50))
    s2_3_num_1 = db.Column(db.Integer)
    s2_3_name_2 = db.Column(db.String(50))
    s2_3_num_2 = db.Column(db.Integer)
    s2_3_name_3 = db.Column(db.String(50))
    s2_3_num_3 = db.Column(db.Integer)
    s2_3_name_4 = db.Column(db.String(50))
    s2_3_num_4 = db.Column(db.Integer)

    s3_4_name_1 = db.Column(db.String(50))
    s3_4_num_1 = db.Column(db.Integer)
    s3_4_name_2 = db.Column(db.String(50))
    s3_4_num_2 = db.Column(db.Integer)
    s3_4_name_3 = db.Column(db.String(50))
    s3_4_num_3 = db.Column(db.Integer)

    s4_5_name_1 = db.Column(db.String(50))
    s4_5_num_1 = db.Column(db.Integer)
    s4_5_name_2 = db.Column(db.String(50))
    s4_5_num_2 = db.Column(db.Integer)
    s4_5_name_3 = db.Column(db.String(50))
    s4_5_num_3 = db.Column(db.Integer)
    s4_5_name_4 = db.Column(db.String(50))
    s4_5_num_4 = db.Column(db.Integer)

    s5_6_name_1 = db.Column(db.String(50))
    s5_6_num_1 = db.Column(db.Integer)
    s5_6_name_2 = db.Column(db.String(50))
    s5_6_num_2 = db.Column(db.Integer)
    s5_6_name_3 = db.Column(db.String(50))
    s5_6_num_3 = db.Column(db.Integer)

    s6_7_name_1 = db.Column(db.String(50))
    s6_7_num_1 = db.Column(db.Integer)
    s6_7_name_2 = db.Column(db.String(50))
    s6_7_num_2 = db.Column(db.Integer)
    s6_7_name_3 = db.Column(db.String(50))
    s6_7_num_3 = db.Column(db.Integer)
    s6_7_name_4 = db.Column(db.String(50))
    s6_7_num_4 = db.Column(db.Integer)

    s7_8_name_1 = db.Column(db.String(50))
    s7_8_num_1 = db.Column(db.Integer)
    s7_8_name_2 = db.Column(db.String(50))
    s7_8_num_2 = db.Column(db.Integer)

    s8_9_name_1 = db.Column(db.String(50))
    s8_9_num_1 = db.Column(db.Integer)
    s8_9_name_2 = db.Column(db.String(50))
    s8_9_num_2 = db.Column(db.Integer)


    def __init__(self, NO, s1_2_name_1, s1_2_num_1 , s1_2_name_2, s1_2_num_2 , s1_2_name_3, s1_2_num_3 , s2_3_name_1, s2_3_num_1 , s2_3_name_2, s2_3_num_2 , s2_3_name_3, s2_3_num_3 , s3_4_name_1, s3_4_num_1 , s3_4_name_2, s3_4_num_2 , s3_4_name_3, s3_4_num_3 , s4_5_name_1, s4_5_num_1 , s4_5_name_2, s4_5_num_2 , s4_5_name_3, s4_5_num_3 , s5_6_name_1, s5_6_num_1 , s5_6_name_2, s5_6_num_2 , s5_6_name_3, s5_6_num_3 , s6_7_name_1, s6_7_num_1 , s6_7_name_2, s6_7_num_2 , s6_7_name_3, s6_7_num_3 , s7_8_name_1, s7_8_num_1 , s7_8_name_2, s7_8_num_2 , s8_9_name_1, s8_9_num_1 , s8_9_name_2, s8_9_num_2, s2_3_name_4 , s2_3_num_4 ,s4_5_name_4, s4_5_num_4 , s6_7_name_4, s6_7_num_4):

        self.NO = NO
        self.s1_2_name_1 = s1_2_name_1
        self.s1_2_num_1 =  s1_2_num_1 
        self.s1_2_name_2 = s1_2_name_2
        self.s1_2_num_2 =  s1_2_num_2 
        self.s1_2_name_3 = s1_2_name_3
        self.s1_2_num_3 =  s1_2_num_3 

        self.s2_3_name_1 = s2_3_name_1
        self.s2_3_num_1 =  s2_3_num_1 
        self.s2_3_name_2 = s2_3_name_2
        self.s2_3_num_2 =  s2_3_num_2 
        self.s2_3_name_3 = s2_3_name_3
        self.s2_3_num_3 =  s2_3_num_3 
        self.s2_3_name_4 = s2_3_name_4
        self.s2_3_num_4 = s2_3_num_4

        self.s3_4_name_1 = s3_4_name_1
        self.s3_4_num_1 =  s3_4_num_1 
        self.s3_4_name_2 = s3_4_name_2
        self.s3_4_num_2 =  s3_4_num_2 
        self.s3_4_name_3 = s3_4_name_3
        self.s3_4_num_3 =  s3_4_num_3 
        self.s4_5_name_4 = s4_5_name_4
        self.s4_5_num_4 = s4_5_num_4

        self.s4_5_name_1 = s4_5_name_1
        self.s4_5_num_1 =  s4_5_num_1 
        self.s4_5_name_2 = s4_5_name_2
        self.s4_5_num_2 =  s4_5_num_2 
        self.s4_5_name_3 = s4_5_name_3
        self.s4_5_num_3 =  s4_5_num_3 

        self.s5_6_name_1 = s5_6_name_1
        self.s5_6_num_1 =  s5_6_num_1 
        self.s5_6_name_2 = s5_6_name_2
        self.s5_6_num_2 =  s5_6_num_2 
        self.s5_6_name_3 = s5_6_name_3
        self.s5_6_num_3 =  s5_6_num_3 

        self.s6_7_name_1 = s6_7_name_1
        self.s6_7_num_1 =  s6_7_num_1 
        self.s6_7_name_2 = s6_7_name_2
        self.s6_7_num_2 =  s6_7_num_2 
        self.s6_7_name_3 = s6_7_name_3
        self.s6_7_num_3 =  s6_7_num_3 
        self.s6_7_name_4 = s6_7_name_4
        self.s6_7_num_4 = s6_7_num_4

        self.s7_8_name_1 = s7_8_name_1
        self.s7_8_num_1 =  s7_8_num_1 
        self.s7_8_name_2 = s7_8_name_2
        self.s7_8_num_2 =  s7_8_num_2 

        self.s8_9_name_1 = s8_9_name_1
        self.s8_9_num_1 =  s8_9_num_1 
        self.s8_9_name_2 = s8_9_name_2
        self.s8_9_num_2 =  s8_9_num_2 
