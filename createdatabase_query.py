import mysql.connector

#database connection
mydb = mysql.connector.connect(
  host="localhost",
  port=3306,
  user="root",
  password="",
  database='disease_pharmacist_management'
)
print(mydb)
mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE IF NOT EXISTS Admin_Master (admin_id int(11) NOT NULL AUTO_INCREMENT,  username VARCHAR(50), password VARCHAR(100), PRIMARY KEY (admin_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS User_Master (u_id int(11) NOT NULL AUTO_INCREMENT, username VARCHAR(50), fullname VARCHAR(255), mobileno VARCHAR(50), emailid VARCHAR(255), password VARCHAR(100), PRIMARY KEY (u_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Disease_Master (d_id int(11) NOT NULL AUTO_INCREMENT,  disease_name VARCHAR(255), PRIMARY KEY (d_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Symptom_Master (s_id int(11) NOT NULL AUTO_INCREMENT,  symptom_name VARCHAR(255), PRIMARY KEY (s_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Medicine_Master (m_id int(11) NOT NULL AUTO_INCREMENT, d_id int(11), medicine_name VARCHAR(255), medicine_description LONGTEXT, img_path VARCHAR(255), medicine_price varchar(255), expiry_date varchar(255), PRIMARY KEY (m_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Order_Transaction  (o_id int(11) NOT NULL AUTO_INCREMENT, u_id int(11), medicines VARCHAR(225), trans_date VARCHAR(25), m_quantity VARCHAR(25), total_amount VARCHAR(25), order_status VARCHAR(10), d_address LONGTEXT, PRIMARY KEY (o_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS ContactUs_Transaction (cu_id int(11) NOT NULL AUTO_INCREMENT,  u_id int(11), medicine_name VARCHAR(255), message LONGTEXT, cu_date VARCHAR(25), PRIMARY KEY (cu_id))")


# symptomlist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']


# for i in symptomlist:
#   sql="INSERT INTO Symptom_Master VALUES (NULL, %s)"
#   mycursor.execute(sql, (i, ))
#   mydb.commit()


# diseaselist = ['Fungalinfection', 'Allergy', 'GERD', 'Chroniccholestasis', 'DrugReaction', 'Pepticulcerdiseae', 'AIDS', 'Diabetes', 'Gastroenteritis', 'BronchialAsthma', 'Hypertension', 'Migraine', 'Cervicalspondylosis', 'Paralysis(brainhemorrhage)', 'Jaundice', 'Malaria', 'Chickenpox', 'Dengue', 'Typhoid', 'hepatitisA', 'HepatitisB', 'HepatitisC', 'HepatitisD', 'HepatitisE', 'Alcoholichepatitis', 'Tuberculosis', 'CommonCold', 'Pneumonia', 'Dimorphichemmorhoids(piles)', 'Heartattack', 'Varicoseveins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis', 'Arthritis', '(vertigo)ParoymsalPositionalVertigo', 'Acne', 'Urinarytractinfection', 'Psoriasis', 'Impetigo']

# for i in diseaselist:
#   sql="INSERT INTO Disease_Master VALUES (NULL, %s)"
#   mycursor.execute(sql, (i, ))
#   mydb.commit()



