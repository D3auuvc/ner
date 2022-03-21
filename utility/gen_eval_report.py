from distutils.log import error
import json
from unittest import result

_DATASET_PATH = r'./data/EstNER_joint'
_OUTPUT_PATH = r'./output'
_EVAL_OUTPUT_PATH = r'./eval_output'

_DATASET_FILE = r'EstNER_joint_dev.json'
_VALIDATION_FILE = r'validations.txt'
_EVAL_FILE = r'val_result.txt'

# Get validations result from model output


def _get_validations():
    validations = []
    with open(f'{_OUTPUT_PATH}/{_VALIDATION_FILE}') as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    validations = [line.split(' ') for line in data]
    return validations

# Get dev joint dataset


def _get_dev_dataset():
    dev_dataset = {}
    with open(f'{_DATASET_PATH}/{_DATASET_FILE}') as f:
        dev_dataset = json.loads(f.read())
    return dev_dataset


def generate_eval_rsult(dev_dataset, validations):
    _B_PREFIX = 'B-'
    _I_PREFIX = 'I-'
    eval_result_lst = []
    line_cnt = 0
    for doc in dev_dataset['documents']:
        for sent in doc['sentences']:
            b_flag = False
            i_flag = False
            b_err_flag=False
            error_cnt = 0
            b_tmp = ''
            i_tmp = ''
            error_ner_lst = []
            b_tmp_dic = {}
            for word, result in zip(sent['words'], validations[line_cnt]):
                # 'O'
                if result == 'O':
                    b_flag = False
                    i_flag = False
                    b_err_flag=False
                    b_tmp = ''
                    i_tmp = ''
                    b_tmp_dic = {}
                    error_ner_lst.append(result)

                # 'B-'
                elif result[:2] == _B_PREFIX:
                    b_flag = True
                    b_err_flag=False
                    i_flag = False
                    b_tmp = result
                    b_tmp_dic = word
                    error_ner_lst.append(result)
                # 'B-' + 'I-'*n
                elif (result[:2] == _I_PREFIX) and (b_flag):
                    
                    if (result[2:] != b_tmp[2:]) and (i_flag == False):
                        error_cnt += 1
                        error_ner_lst.pop()
                        error_ner_lst.append(f"({b_tmp}/{b_tmp_dic['ner_1']})")
                        error_ner_lst.append(f"({result}/{word['ner_1']})")
                        b_err_flag=True

                    if (b_err_flag==False):
                        error_ner_lst.append(result)
                    elif(i_flag):
                        error_cnt += 1
                        error_ner_lst.append(f"({result}/{word['ner_1']})")
                    i_flag = True
                # 'O' + 'I-'
                elif (result[:2] == _I_PREFIX) and (b_flag == False):
                    error_cnt += 1
                    error_ner_lst.append(f"({result}/{word['ner_1']})")
            if error_cnt != 0:
                eval_result_lst.append(dict(word=" ".join([word['word'] for word in sent['words']]),
                                            ner_1=" ".join(
                                                [word['ner_1'] for word in sent['words']]),
                                            eval=" ".join(error_ner_lst)))
            line_cnt += 1

    return eval_result_lst


def main():
    validations = _get_validations()
    dev_dataset = _get_dev_dataset()

    eval_result_lst = generate_eval_rsult(dev_dataset, validations)
    with open(f'{_EVAL_OUTPUT_PATH}/{_EVAL_FILE}', 'w') as f:
        for eval in eval_result_lst:
            f.write(eval['word']+'\n')
            f.write(eval['ner_1']+'\n')
            f.write(eval['eval']+'\n\n')


if __name__ == "__main__":
    main()
