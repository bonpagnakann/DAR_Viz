import os
from exemplar_size_list import *

def new_old_class_acc(dataset, scenario, params):

    # string to search in file
    words = ['Test accuracies over tasks ' + str(len(scenario)-1) + ': [', 'Random sequence of classes:']
    result_only = ''
    result_only1 = ''
    result = ''

    people = ['0','1','2']
    icarl= params[scenario]['icarl']
    lucir= params[scenario]['lucir']

    i=0

    for person in people:
        sample_num = calculate_exemp_size(dataset, scenario[1:], person)
        folder_file = [('EWC_Replay_0', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_1', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_2', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_3', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_4', person + '_ce_ewc_random_10.txt'),
                       ('iCaRL_0', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_1', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_2', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_3', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_4', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('LUCIR_0', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_1', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_2', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_3', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_4', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('Random_0', person + '_ce_random_10.txt'), ('Random_1', person + '_ce_random_10.txt'),
                       ('Random_2', person + '_ce_random_10.txt'),
                       ('Random_3', person + '_ce_random_10.txt'), ('Random_4', person + '_ce_random_10.txt'),
                       ('VAE_Adapt', person + '_ce_vae_adaptive_boundary_none_10.txt'),
                       ('VAE_BBox', person + '_ce_vae_boundary_box_none_10.txt'),
                       ('VAE_Filter', person + '_ce_vae_boundary_box_probability_10.txt'),
                       ('VAE_GMM', person + '_ce_vae_gmm_none_10.txt')
                       ]

        for (folder_name,file_name) in folder_file:
            for sample in sample_num:
                in_file_path = scenario + './Person_' + person + '/' + folder_name + '/log/log/' + file_name[:-6] + str(sample) + '.txt'
                output_new_dir = scenario + './Person_' + person + '/' + folder_name + '/stat/new_classes'
                output_old_dir = scenario + './Person_' + person + '/' + folder_name + '/stat/old_classes'
                os.makedirs(output_new_dir, exist_ok=True)
                os.makedirs(output_old_dir, exist_ok=True)

                new_classes_by_tasks_path = output_new_dir + '/new_classes_accuracy_by_task' + str(sample) + '.txt'
                old_classes_acc_path = output_old_dir + '/old_classes_accuracy_by_task' + str(sample) + '.txt'
                result_only = ''
                result = ''
                first_number_string = 0
                first_number_string1 = 0
                found_base_classes = False
                count = 0
                count1 = 0
                # Open the file in read mode
                with open(in_file_path, 'r') as file:
                    # read all lines in a list
                    lines = file.readlines()
                    for line in lines:
                        if 'Base classes' in line:
                            found_base_classes = True
                            # If this line contains "Old classes" and the flag is set, extract the value
                        elif 'Old classes' in line and found_base_classes:
                            count += 1
                            first_number_string = line.split(':')[1].split()[0]
                            print("'Old classes'")
                            print("first_number_string", first_number_string)
                            first_number = float(first_number_string)*0.01
                            print("first_number", first_number)

                            if len(scenario) == 2:
                                result += f"{first_number}\n"
                            else:
                                if count % (len(scenario)-1) == 0:
                                    result += f"{first_number}\n"
                                else:
                                    result += f"{first_number},"

                        elif 'New classes' in line and found_base_classes:
                            count1 += 1
                            first_number_string1 = line.split(':')[1].split()[0]
                            print("'New classes'")
                            print("first_number_string1", first_number_string1)
                            first_number1 = float(first_number_string1)*0.01
                            print("first_number1", first_number1)

                            if len(scenario) == 2:
                                result_only += f"{first_number1}\n"
                            else:
                                if count1 % (len(scenario)-1) == 0:
                                    result_only += f"{first_number1}\n"
                                else:
                                    result_only += f"{first_number1},"

                            found_base_classes = False

                file = open(new_classes_by_tasks_path, 'a')
                file.write(result_only)
                file.close()
                #file = open('tasks.txt', 'a')
                #file.write(result_only1)
                #file.close()
                file = open(old_classes_acc_path, 'a')
                file.write(result)
                file.close()

def all_class_acc(dataset, scenario, params):

    # string to search in file
    words = ['Test accuracies over tasks ' + str(len(scenario)-1) + ': [', 'Random sequence of classes:']
    result_only = ''
    result_only1 = ''
    result = ''

    people = ['0','1','2']
    icarl= params[scenario]['icarl']
    lucir= params[scenario]['lucir']

    i=0

    for person in people:
        sample_num = calculate_exemp_size(dataset, scenario[1:], person)

        folder_file = [('EWC_Replay_0', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_1', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_2', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_3', person + '_ce_ewc_random_10.txt'),
                       ('EWC_Replay_4', person + '_ce_ewc_random_10.txt'),
                       ('iCaRL_0', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_1', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_2', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_3', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('iCaRL_4', person + '_kd_kldiv_icarl_' + icarl + '_10.txt'),
                       ('LUCIR_0', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_1', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_2', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_3', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('LUCIR_4', person + '_cn_lfc_mr_icarl_' + lucir + '_10.txt'),
                       ('Random_0', person + '_ce_random_10.txt'), ('Random_1', person + '_ce_random_10.txt'),
                       ('Random_2', person + '_ce_random_10.txt'),
                       ('Random_3', person + '_ce_random_10.txt'), ('Random_4', person + '_ce_random_10.txt'),
                       ('VAE_Adapt', person + '_ce_vae_adaptive_boundary_none_10.txt'),
                       ('VAE_BBox', person + '_ce_vae_boundary_box_none_10.txt'),
                       ('VAE_Filter', person + '_ce_vae_boundary_box_probability_10.txt'),
                       ('VAE_GMM', person + '_ce_vae_gmm_none_10.txt')
                       ]

        for (folder_name,file_name) in folder_file:
            for sample in sample_num:
                in_file_path = scenario + '/Person_' + person + '/' + folder_name + '/log/log/' + file_name[:-6] + str(sample) + '.txt'
                output_all_dir = scenario + '/Person_' + person + '/' + folder_name + '/stat/all_classes'
                os.makedirs(output_all_dir, exist_ok=True)

                acc_by_tasks_path = output_all_dir + '/accuracy_by_task' + str(sample) + '.txt'
                all_acc_path = output_all_dir + '/all_accuracy' + str(sample) + '.txt'
                result_only = ''
                result = ''
                if i%2 == 1:
                    i+=1
                with open(in_file_path, 'r') as fp:
                    # read all lines in a list
                    lines = fp.readlines()
                    for line in lines:
                        for word in words:
                            # check if string present on a current line
                            if line.find(word) != -1:
                                if i%2==0:
                                    print(line, end=',')

                                    result_only += f"{line.strip()[31:-1]}\n"
                                    result += f"{line.strip()[31:-1]},"

                                    i+=1
                                else:
                                    print(line)
                                    result_only1 += f"{line[28:-1]}\n"
                                    result += f"{line[28:-1]}\n"
                                    i+=1

                file = open(acc_by_tasks_path, 'a')
                file.write(result_only)
                file.close()
                #file = open('tasks.txt', 'a')
                #file.write(result_only1)
                #file.close()
                file = open(all_acc_path, 'a')
                file.write(result)
                file.close()