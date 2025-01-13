import random
import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import json
import os


class Prediction:

    def __init__(self):
        self.current_path = os.getcwd()
    layer_1 = "./models/layer-1.pkl"
    layer_2_major = "./models/layer-2-major.pkl"
    layer_2_minor = "./models/layer-2-minor.pkl"
    layer_3_acc = "./models/layer-3-major-acc-fin.pkl"
    layer_3_admin = "./models/layer-3-major-admin.pkl"
    layer_3_it = "./models/layer-3-major-comp-it.pkl"
    layer_3_sales = "./models/layer-3-major-sales.pkl"
    layer_3_edu = "./models/layer-3-minor-edu.pkl"
    layer_3_media = "./models/layer-3-minor-media.pkl"
    layer_3_engg = "./models/layer-3-minor-engineering.pkl"

    def _dict_for_label(self, layer, key):
        f = open(self.current_path +
                 '/jss_prediction_components/prediction_label_map.json')
        data = json.load(f)
        return data[layer][key]

    def _fac_map(self, fac_name):
        f = open(self.current_path +
                 '/jss_prediction_components/faculty_map.json', "r")
        data = json.load(f)
        return data[fac_name]

    def _demo_data(self):
        f = open(self.current_path+'/jss_prediction_components/sample_data.json')
        data = json.load(f)
        return data

    def _label_encode(self, data_frame, features: list, column_alias=""):

        data_copy = data_frame.copy()
        label_encoders = {}
        for column in features:
            le = LabelEncoder()
            data_copy[column] = le.fit_transform(data_copy[column])
            if column_alias == "":
                label_encoders[column] = le
            else:
                label_encoders[column+'_'+column_alias] = le
        return (data_copy, label_encoders)

    def _apply_encodings(self, new_data, label_encoders):
        new_data_copy = new_data.copy()
        for column, encoder in label_encoders.items():
            if column in new_data_copy.columns:
                new_data_copy[column] = encoder.transform(
                    new_data_copy[column])
        return new_data_copy

    def _predict_layer_1(self, data_frame):
        with open(self.layer_1, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 1)
        return predict

    def _predict_layer_2_major(self, data_frame):
        with open(self.layer_2_major, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 4)
        return predict

    def _predict_layer_2_minor(self, data_frame):
        with open(self.layer_2_minor, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 5)
        return predict

    def _predict_layer_3_major_it(self, data_frame):
        with open(self.layer_3_it, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 2)
        return predict

    def _predict_layer_3_major_acc(self, data_frame):
        with open(self.layer_3_acc, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 3)
        return predict

    def _predict_layer_3_major_admin(self, data_frame):
        with open(self.layer_3_admin, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 3)
        return predict

    def _predict_layer_3_major_sales(self, data_frame):
        with open(self.layer_3_sales, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 2)
        return predict

    def _predict_layer_3_minor_Engg(self, data_frame):
        with open(self.layer_3_engg, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(self, data_frame)[0]
        # predict = random.randint(0, 2)
        return predict

    def _predict_layer_3_minor_mediaself(self, data_frame):
        with open(self.layer_3_media, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 2)
        return predict

    def _predict_layer_3_minor_edu(self, data_frame):
        with open(self.layer_3_edu, 'rb') as file:
            model = pickle.load(file)
        predict = model.predict(data_frame)[0]
        # predict = random.randint(0, 1)
        return predict

    def _predict_layer_3_minor_hotel(data_frame):
        # with open(layer_3_edu, 'rb') as file:
        #     model = pickle.load(file)
        # predict = model.predict(data_frame)[0]
        predict = 1
        return predict

    def _predict_layer_3_minor_service(data_frame):
        # with open(layer_3_edu, 'rb') as file:
        #     model = pickle.load(file)
        # predict = model.predict(data_frame)[0]
        predict = 1
        return predict

    def _convert_gpa(self, value):
        value = float(value)
        if value < 0 or value > 4:
            return "Invalid input"
        elif value < 2:
            return "0-1.99"
        elif value < 2.5:
            return "2.00-2.49"
        elif value < 3:
            return "2.50-2.99"
        elif value < 3.5:
            return "3.00-3.49"
        elif value <= 4:
            return "3.50-4.00"
        else:
            return "No_data"

    def _sort_dict(self, main_dict, reference_dict):
        key_order = list(reference_dict.keys())
        sorted_dict = {key: main_dict[key] for key in sorted(
            main_dict.keys(), key=lambda x: key_order.index(x))}
        return sorted_dict

    def _convert_original_data(self, data):
        df1 = pd.read_csv("./data/for-reco-2021.csv")
        df2 = pd.read_csv("./data/for-reco-2022.csv")
        df = pd.concat([df1, df2], axis=0)
        academic_fts = [
            'Campus', 'Study_Program', 'Faculty_domain', 'Credit_transfer', 'T1_GPA', 'T2_GPA', 'T3_GPA', 'T4_GPA',
            'T5_GPA', 'T6_GPA', 'T7_GPA', 'T8_GPA', 'T9_GPA', 'T10_GPA', 'T11_GPA', 'Sponsor_category',
            'Entry_eligibility', 'BM_Score', 'BI_Score', 'Muet_Score', 'Matematik', 'Sejarah', 'Matematik_Tambahan', 'Fizik',
            'Kimia', 'Biologi', 'PENDIDIKAN_MORAL', 'Bahasa_Ci', 'Prinsip_Akaun', 'Sains'
        ]

        subject_demography_fts = [
            'Permanent_address_state', 'Nationality', 'Race', 'Gender', 'Disability', 'Status'
        ]
        dropable_fts = [
            'Index', 'Employed', 'major_minor'
        ]
        selected_ft = academic_fts+subject_demography_fts
        # df.loc[len(df)]=data
        data_frame, all_attributes = self._label_encode(df, selected_ft)
        return self._apply_encodings(data, all_attributes)

    def _get_percentages(self, js, jss):
        df1 = pd.read_csv("./data/for-reco-2021.csv")
        df2 = pd.read_csv("./data/for-reco-2022.csv")
        df = pd.concat([df1, df2], axis=0)

        data_group_js = df.groupby(['JS_Job_sector'])['Campus'].count()
        data_group_dict_js = data_group_js.to_dict()
        data_group_js_keys = data_group_dict_js.keys()
        data_group_js_keys = list(data_group_dict_js.keys())
        data_group_js_values = list(data_group_dict_js.values())
        highlight_label_js = js  # The label of the slice to highlight
        labels = np.array(data_group_js_keys)
        data = np.array(data_group_js_values)
        highlight_index = np.where(labels == highlight_label_js)[0][0]
        highlight_data_count_js = data[highlight_index]

        data_group = df.groupby(['JS_Job_sub_sector'])['Campus'].count()
        data_group_dict = data_group.to_dict()
        data_group_keys = data_group_dict.keys()
        data_group_keys = list(data_group_keys)
        data_group_values = list(data_group_dict.values())
        highlight_label = jss  # The label of the slice to highlight
        labels = np.array(data_group_keys)
        data = np.array(data_group_values)
        highlight_index = np.where(labels == highlight_label)[0][0]
        highlight_data_count = data[highlight_index]

        percentages = (100*highlight_data_count)//highlight_data_count_js
        return percentages

    def _data_transform(self, data):
        ft_list = ['Gender', 'Permanent address state', 'Race', 'Campus', 'Program description',
                   'Faculty domain', 'Status', 'Disability', 'Entry Eligibility',
                   'Additional Mathematics', 'Biology', 'Chemistry', 'English Language', 'History',
                   'Mathematics', 'Moral Education', 'Physics', 'MUET', 't1_gpa', 't2_gpa', 't3_gpa', 't4_gpa', 't5_gpa', 't6_gpa']
        transformed_data = {
            'T1_GPA': 'no_data',
            'T2_GPA': 'no_data',
            'T3_GPA': 'no_data',
            'T4_GPA': 'no_data',
            'T5_GPA': 'no_data',
            'T6_GPA': 'no_data',
            'T7_GPA': 'no_data',
            'T8_GPA': 'no_data',
            'T9_GPA': 'no_data',
            'T10_GPA': 'no_data',
            'T11_GPA': 'no_data',
            'BM_Score': 'Irrelavant',
            'BI_Score': 'Irrelavant',
            'Nationality': 'Malaysian',
            'Credit_transfer': 'No',
            'Prinsip_Akaun': 'no_data',
            'Sains': 'no_data',
            'Sponsor_category': 'Loan'

        }
        for key, val in data.items():
            if key not in ft_list:
                continue
            if key == 'Program description':
                transformed_data['Study_Program'] = self._fac_map(val.upper())
            elif key == 'Permanent address state':
                transformed_data['Permanent_address_state'] = val.upper()
            elif key == 'Faculty domain':
                transformed_data['Faculty_domain'] = val
            elif key == 't1_gpa':
                transformed_data['T1_GPA'] = self._convert_gpa(val)
            elif key == 't2_gpa':
                transformed_data['T2_GPA'] = self._convert_gpa(val)
            elif key == 't3_gpa':
                transformed_data['T3_GPA'] = self._convert_gpa(val)
            elif key == 't4_gpa':
                transformed_data['T4_GPA'] = self._convert_gpa(val)
            elif key == 't5_gpa':
                transformed_data['T5_GPA'] = self._convert_gpa(val)
            elif key == 't6_gpa':
                transformed_data['T6_GPA'] = self._convert_gpa(val)
            elif key == 'Entry Eligibility':
                transformed_data['Entry_eligibility'] = val
            elif key == 'Additional Mathematics':
                transformed_data['Matematik_Tambahan'] = val
            elif key == 'Biology':
                transformed_data['Biologi'] = val
            elif key == 'Chemistry':
                transformed_data['Kimia'] = val
            elif key == 'English Language':
                transformed_data['Bahasa_Ci'] = val
            elif key == 'History':
                transformed_data['Sejarah'] = val
            elif key == 'Mathematics':
                transformed_data['Matematik'] = val
            elif key == 'Moral Education':
                transformed_data['PENDIDIKAN_MORAL'] = val
            elif key == 'Physics':
                transformed_data['Fizik'] = val
            elif key == 'MUET':
                transformed_data['Muet_Score'] = val
            else:
                transformed_data[key] = val
        return transformed_data

    def predict(self, data):
        t_data = self._data_transform(data)
        t_data = self._sort_dict(t_data, self._demo_data()[0])
        dataframe = pd.DataFrame([t_data])

        dataframe = self._convert_original_data(dataframe)

        t_data = dataframe
        layer_1_res = self._predict_layer_1(t_data)
        
        layer_2_js = ""
        layer_3_js = ""
        
        if layer_1_res == 0:
            # Major
            layer_2_res = self._predict_layer_2_major(t_data)
            layer_2_js = self._dict_for_label(
                'layer_2_major', str(layer_2_res))

            if layer_2_res == 0:
                layer_3_res = self._predict_layer_3_major_acc(t_data)
                layer_3_js = self._dict_for_label('layer_3_acc', str(
                    layer_3_res))

            elif layer_2_res == 1:
                layer_3_res = self._predict_layer_3_major_admin(t_data)
                layer_3_js = self._dict_for_label('layer_3_admin', str(
                    layer_3_res))

            elif layer_2_res == 2:
                layer_3_res = self._predict_layer_3_major_it(t_data)
                layer_3_js = self._dict_for_label('layer_3_it', str(
                    layer_3_res))

            elif layer_2_res == 3:
                layer_3_res = self._predict_layer_3_major_sales(t_data)
                layer_3_js = self._dict_for_label('layer_3_sales', str(
                    layer_3_res))

            else:
                if data['Faculty domain']== 'LAW':
                    layer_3_js = 'Lawyer/Legal Asst'
                else:
                    layer_3_js = 'Customer Service'
        else:

            layer_2_res = self._predict_layer_2_minor(t_data)
            layer_2_js = self._dict_for_label('layer_2_minor', str(
                layer_2_res))

            if layer_2_res == 0:
                layer_3_res = self._predict_layer_3_minor_media(t_data)
                layer_3_js = self._dict_for_label('layer_3_media', str(
                    layer_3_res))
            elif layer_2_res == 1:
                layer_3_res = self._predict_layer_3_minor_edu(t_data)
                layer_3_js = self._dict_for_label('layer_3_edu', str(
                    layer_3_res))
            elif layer_2_res == 2:
                layer_3_res = self._predict_layer_3_minor_Engg(t_data)
                layer_3_js = self._dict_for_label('layer_3_engg', str(
                    layer_3_res))
            elif layer_2_res == 3:
                layer_3_js = "Food/Beverage/Restaurant"
            elif layer_2_res == 4:
                layer_3_js = "Manufacturing"
            else:
                layer_3_js = "Others"
            print(layer_2_js,layer_3_js)
        percentage = self._get_percentages(layer_2_js, layer_3_js)
        return (layer_2_js, layer_3_js, percentage)
