import json

_OUTPUT_DIR = r'ner_check_output'
_DATASET_DIR = r'data/EstNER_joint'
_B_PREFIX = 'B-'
_I_PREFIX = 'I-'


file_list = {'EstNER_joint_test.json',
             'EstNER_joint_dev.json', 'EstNER_joint_train.json'}

for jf in file_list:
    data_dic = {}
    doc_lst = []
    error_cnt = 0
    ner_cnt = 0
    with open(f'{_DATASET_DIR}/{jf}', 'r+') as f:
        data = json.load(f)
        for doc in data['documents']:
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
                for word in sent['words']:
                    # if is 'O'
                    if word['ner_1'] == 'O':
                        b_flag = False
                        b_tmp = ''
                        i_tmp = ''
                        b_tmp_dic = {}
                    # 'B-'
                    elif word['ner_1'][:2] == _B_PREFIX:
                        b_flag = True
                        b_tmp = word['ner_1']
                        i_tmp = ''
                        b_tmp_dic = word
                    # 'B-' + 'I-'*n
                    elif (word['ner_1'][:2] == _I_PREFIX) and (b_flag):
                        if word['ner_1'][2:] != b_tmp[2:]:
                            error_cnt += 1
                            err_ent_lst.append(
                                f"{b_tmp_dic['word']} ({b_tmp_dic['ner_1']})")
                            err_ent_lst.append(
                                f"{word['word']} ({word['ner_1']})")
                        if i_tmp == '':
                            i_tmp = word['ner_1']
                        else:
                            if word['ner_1'][2:] != i_tmp[2:]:
                                err_ent_lst.append(
                                    f"{word['word']} ({word['ner_1']})")
                                error_cnt += 1
                                i_tmp = word['ner_1']
                    # 'O' + 'I-'
                    elif (word['ner_1'][:2] == _I_PREFIX) and (b_flag == False):
                        error_cnt += 1
                        err_ent_lst.append(
                            f"{word['word']} ({word['ner_1']})")
                        
                with open(f'{_OUTPUT_DIR}/{jf[:-5]}.txt', 'a') as f:
                    if len(err_ent_lst) != 0:
                        f.write(f'{err_ent_lst}\n')