import pdfplumber as pb

def get_data(file_like_object):
    data_dict = {}

    with pb.open(file_like_object) as pdf:
        
        for page in pdf.pages:
            
            text = page.extract_text()
            
            for line in text.split('\n'):
                if ':' in line:  
                    key, value = line.split(':', 1) 
                    data_dict[key.strip().replace('\0002','')] = value.strip()
    return data_dict