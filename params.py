def get_params_from_dotenv(path='./.env'):
    env_dict = {}
    with open(path, 'r') as file:
        for line in file:
            key, value = [word.strip() for word in line.strip().split('=')]
            env_dict[key] = value
    return env_dict
aux_dict = get_params_from_dotenv()
GET_NOTES_API = aux_dict['GET_NOTES_API']
SPREADSHEET_ID = aux_dict['SPREADSHEET_ID']
EVALUATION_NAME = aux_dict['EVALUATION_NAME']
SHEET_ID = aux_dict['SHEET_ID']
