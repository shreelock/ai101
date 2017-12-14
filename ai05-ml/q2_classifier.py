import csv
import sys
from math import log, exp


# In[223]:


def update_dict(worddict, word, count):
    if word in worddict:
        worddict[word] += count
    else:
        worddict[word] = count

def train_words(label, wordfreq):
    global tot_non_spam_words_freq, tot_spam_words_freq, words_in_non_spam_dict, words_in_spam_dict
    for word in wordfreq:
        count = float(wordfreq[word])
        if label=='ham':
            update_dict(words_in_non_spam_dict, word, count)
            tot_non_spam_words_freq += count
        else:
            update_dict(words_in_spam_dict, word, count)
            tot_spam_words_freq += count


# In[232]:


def get_conditional_prob_of_word_0(word, spam_bool):
    if spam_bool:
        return words_in_spam_dict.get(word,0.0) / tot_spam_words_freq
    else:
        return words_in_non_spam_dict.get(word,0.0) / tot_non_spam_words_freq


# In[233]:


def get_conditional_prob_of_word_1(word, spam_bool):
    global alpha
    if spam_bool:
        return (words_in_spam_dict.get(word,0.0) + alpha) / (tot_spam_words_freq + alpha*tot_distinct_words)
    else:
        return (words_in_non_spam_dict.get(word,0.0) + alpha) / (tot_non_spam_words_freq + alpha*tot_distinct_words)


# In[247]:


def get_conditional_prob_of_word_2(word, spam_bool):
    global const_addendum
    if spam_bool:
        if word in words_in_spam_dict:
            return words_in_spam_dict.get(word) / tot_spam_words_freq
        else:
            return avg_spam_word_freq / tot_spam_words_freq
    else:
        if word in words_in_non_spam_dict:
            return words_in_non_spam_dict.get(word) / tot_non_spam_words_freq
        else:
            return avg_non_spam_word_freq / tot_non_spam_words_freq


# In[257]:


def get_conditional_prob_of_email_0(email_wordsfreq, check_for_spam):
    result = 1.0
    for word in email_wordsfreq:
        #freq = int(email_wordsfreq[word])
        result *= get_conditional_prob_of_word_2(word, check_for_spam)
    return result


# In[258]:


def overall_result(email_wordsfreq):
    spam = p_spam*get_conditional_prob_of_email_0(email_wordsfreq, True)
    not_spam = p_not_spam*get_conditional_prob_of_email_0(email_wordsfreq, False)
    return spam > not_spam


# In[224]:
if __name__ == '__main__':
    # input format = python q2_classifier.py -f1 <train_dataset> -f2 <test_dataset> -o <output_file>
    trainfilename = sys.argv[2]
    testfilename = sys.argv[4]
    outputfilename = sys.argv[6]

    print trainfilename, testfilename, outputfilename

    # trainfile = open("./train", "rb")
    trainfile = open(trainfilename, "rb")
    filereader = csv.reader(trainfile, delimiter=' ')
    num_spam = 0.0
    num_not_spam = 0.0
    tot_spam_words_freq = 0.0
    tot_non_spam_words_freq = 0.0
    words_in_spam_dict = {}
    words_in_non_spam_dict = {}

    for row in filereader:
        wordfreq = {}
        label = row[1]
        wrds = row[2:]
        for j in range(len(wrds[2:])/2):
            wordfreq[wrds[2*j]] = wrds[2*j +1]
        train_words(label, wordfreq)

        if label =='spam':
            num_spam += 1
        else:
            num_not_spam += 1

    trainfile.close()


    # In[225]:


    num_files = num_spam + num_not_spam
    tot_words_freq = tot_spam_words_freq + tot_non_spam_words_freq

    p_spam = num_spam / num_files
    p_not_spam = num_not_spam / num_files

    # print p_spam, p_not_spam
    # print words_in_spam_dict
    # print words_in_non_spam_dict
    # print tot_words_freq, tot_spam_words_freq, tot_non_spam_words_freq

    avg_spam_word_freq = sum(words_in_spam_dict.values())/len(words_in_spam_dict.values())
    avg_non_spam_word_freq = sum(words_in_non_spam_dict.values())/len(words_in_non_spam_dict.values())

    tot_distinct_spam_words = len(words_in_spam_dict.keys())
    tot_distinct_non_spam_words = len(words_in_non_spam_dict.keys())
    tot_distinct_words = tot_distinct_spam_words + tot_distinct_non_spam_words




    # In[259]:


    # testfile = open("./test", "rb")
    testfile = open(testfilename, "rb")
    filereader = csv.reader(testfile, delimiter=' ')
    pred_labels = []
    labels = []
    alpha = 1
    const_addendum = 1000
    opwritefile = open(outputfilename, 'wb')
    csvwriter = csv.writer(opwritefile, delimiter=' ')

    for row in filereader:
        testwordfreq = {}
        fileindex = row[0]
        testlabel = row[1]
        labels.append(testlabel)
        testwrds = row[2:]
        for j in range(len(testwrds[2:])/2):
            testwordfreq[testwrds[2*j]] = testwrds[2*j +1]

        #print overall_result(testwordfreq), testlabel
        pred = overall_result(testwordfreq)
        if pred:
            pred_labels.append('spam')
            csvwriter.writerow([fileindex, 'spam'])
        else:
            pred_labels.append('ham')
            csvwriter.writerow([fileindex, 'ham'])

    from sklearn.metrics import accuracy_score
    print accuracy_score(labels, pred_labels)




