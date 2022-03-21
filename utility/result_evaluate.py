import json

_VAL_NER_OUTPUT_FILE = r'validations.txt'
_ANA_OUTPUT_PATH = r'./val_output'


def get_validation_result():
    val_result = []
    with open(_VAL_NER_OUTPUT_FILE, 'r') as f:
        val_result = [line.rstrip('\n') for line in f.readlines()]

    val_result = [word.split() for word in val_result]
    return val_result


def get_val_dataset():
    _PATH = r'./data/EstNER_joint'
    _FILE = r'EstNER_joint_dev.json'
    val_dataset = dict()
    with open(f'{_PATH}/{_FILE}', 'r') as f:
        val_dataset = json.loads(f.read())

    return val_dataset


def validate_result(result, dataset):
    data_dic = {}
    doc_lst = []
    error_cnt = 0
    ner_cnt = 0

    _VAL_RESULT_FILE = r'val_result.txt'
    _B_PREFIX = 'B-'
    _I_PREFIX = 'I-'
    line_cnt = 0

    for doc in dataset['documents']:
        sent_lst = []
        sent_dic = {}

        for sent in doc['sentences']:
            words_lst = []
            words_dic = {}
            b_flag = False
            b_tmp = ''
            i_tmp = ''
            b_tmp_dic = {}
            i_tmp_dic = {}

            err_ent_lst = []
            for val_word, word in zip(result[line_cnt], sent['words']):
                # if word is labeled as entity
                if val_word != 'O':
                    ner_cnt += 1

                # if is 'O'
                if val_word == 'O':
                    b_flag = False
                    b_tmp = ''
                    i_tmp = ''
                    b_tmp_dic = {}
                # 'B-'
                elif val_word[:2] == _B_PREFIX:
                    b_flag = True
                    b_tmp = val_word
                    i_tmp = ''
                    b_tmp_dic = word
                # 'B-' + 'I-'*n
                elif (val_word[:2] == _I_PREFIX) and (b_flag):
                    if val_word[2:] != b_tmp[2:]:
                        error_cnt += 1
                        err_ent_lst.append(
                            f"{b_tmp_dic['word']} ({b_tmp}/{b_tmp_dic['ner_1']})")
                        err_ent_lst.append(
                            f"{word['word']} ({val_word}/{word['ner_1']})")
                    if i_tmp == '':
                        i_tmp = val_word
                    else:
                        if val_word[2:] != i_tmp[2:]:
                            err_ent_lst.append(
                                f"{word['word']} ({val_word}/{word['ner_1']})")
                            error_cnt += 1
                            i_tmp = val_word
                # 'O' + 'I-'
                elif (val_word[:2] == _I_PREFIX) and (b_flag == False):
                    error_cnt += 1
                    err_ent_lst.append(
                        f"{word['word']} ({val_word}/{word['ner_1']})")

                word_dict = {}
                word_dict['word'] = word['word']
                word_dict['ner_1'] = word['ner_1']
                word_dict['val_ner'] = val_word
                words_lst.append(
                    f"{word['word']} ({val_word}/{word['ner_1']})")

            line_cnt += 1
            with open(_VAL_RESULT_FILE, 'a') as f:
                if len(err_ent_lst) != 0:
                    f.write(f'{err_ent_lst}\n')

            words_dic['words'] = words_lst
            sent_lst.append(words_dic)
        sent_dic['sentences'] = sent_lst
        doc_lst.append(sent_dic)
        data_dic['documents'] = doc_lst

    print(line_cnt)
    with open(_VAL_RESULT_FILE, 'a') as f:
        f.write('*****'*10+'\n')
        f.write(f'num of error: {error_cnt}\n')
        f.write(f'num of enties:{ner_cnt}\n')
        f.write(f'error rate: {error_cnt/ner_cnt}\n')
    return data_dic


def analyze_result(data_dic):
    _ERR_RESULT_FILE = r'error_result.txt'
    error_lst = []
    for doc in data_dic['documents']:
        for sent in doc['sentences']:
            err_lst = []
            for word in sent['words']:
                if word['ner_1'] != word['val_ner']:
                    error_lst.append(word)
                    err_str = f"{word['word']} ({word['val_ner']}/{word['ner_1']})"
                    err_lst.append(err_str)
            with open(_ERR_RESULT_FILE, 'a') as f:
                if len(err_lst) != 0:
                    f.write(f'{err_lst}\n')
    return error_lst


def main():
    _RESULT_FILE = r'result.json'
    _ERROR_FILE = r'error.json'
    print(type(get_validation_result()))
    print(type(get_val_dataset()))
    result = get_validation_result()
    dataset = get_val_dataset()
    data_dic = validate_result(result, dataset)
    with open(_RESULT_FILE, 'w') as f:
        json.dump(data_dic, f)

    # with open(_ERROR_FILE, 'w') as f:
    #     err_dict = {}
    #     err_dict['error'] = analyze_result(data_dic)
    #     json.dump(err_dict, f)


if __name__ == "__main__":
    main()
