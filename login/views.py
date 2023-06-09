from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from database.models import user
from login.forms import UserRegistrationForm, SubjectForm, ExamForm

from database.models import subject, exams, score, question_set, question, response, answer, user

from django.contrib import messages
from . import jaro2, leven, jac, pre  # hamming
import nltk
import string
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import hamming

from nltk.corpus import stopwords

# jaccard
from sklearn.feature_extraction.text import TfidfVectorizer

import string

# cosine
from sklearn.metrics.pairwise import cosine_similarity

# ----


import math

uname = ""
q_id = 0
session_teacher = ['false']
session_student = ['false']

homepage_teacher = ['false']
homepage_student = ['false']

# create another row to check wheather a student has already taken an exam


# Create your views here.

def homepage(request):
    if homepage_teacher[0] == "false" and homepage_student[0] == "false":
        return render(request, 'login/homepage.html')

    elif homepage_teacher[0] == "true":
        session_teacher.insert(0, "true")
        messages.info(
            request, 'You are already logged in so you can not go to the homepage,inorder to access the homepage please logout!')
        return redirect('/teacher/dashboard/')

    elif homepage_student[0] == "true":
        session_student.insert(0, "true")
        messages.info(
            request, 'You are already logged in so you can not go to the homepage,inorder to access the homepage please logout!')
        return redirect('/student/dashboard/')

    else:
        print("value of homepage_student", homepage_student)
        return render(request, 'login/homepage.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('registration_success')
    else:
        form = UserRegistrationForm()

    return render(request, 'login/registration.html', {'form': form})


def register_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    else:
        form = SubjectForm()

    return render(request, 'courses/subject.html', {'form': form})


def login_teacher(request):
    usrs = user.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        global uname
        uname = username

        print("the user name is", username)
        print("the password is", password)

        i = 0
        k = len(usrs)
        while i < k:
            if usrs[i].role == "teacher" or usrs[i].role == "Teacher":
                if usrs[i].username == username and usrs[i].password == password:
                    print(usrs[i].username, usrs[i].password)
                    session_teacher.insert(0, "true")
                    return redirect('/teacher/dashboard/')
                    break
            i = i+1
        else:
            messages.info(
                request, 'Make sure you choose the right login! Invalid username or password!')
            return redirect('/teacher/login/')

    if homepage_teacher[0] == "false" and homepage_student[0] == "false":
        return render(request, 'login/login_teacher1.html')
    elif homepage_teacher[0] == "true":
        messages.info(
            request, 'You are already logged in so you can not go to the teacher login page,inorder to access the login page please logout!')
        return redirect('/teacher/dashboard/')
    else:
        messages.info(
            request, 'You are already logged in so you can not go to the teacher login page,inorder to access the login page please logout!')
        return redirect('/student/dashboard/')


# teacher dashboard --------------->


def teacher_dashboard(request):
    subs = subject.objects.all()
    global uname
    uname = uname.title()
    if session_teacher[0] == "true":
        homepage_teacher.insert(0, "true")
        return render(request, 'courses/course_list.html', {'subs': subs, 'uname': uname})
    else:
        return redirect('/')


def course_detail(request, subject_id):
   #  subs = subject.objects.all()
    sub = get_list_or_404(subject, subject_id=subject_id)
    xms = get_list_or_404(exams, subject_id_id=subject_id)
    # print(subject_id)
    context = {
        'sub': sub,
        'subject_id': subject_id,
        'xms': xms,
    }
    if session_teacher[0] == "true":
        homepage_teacher.insert(0, "true")
        return render(request, 'courses/course_details.html', context)
    else:
        return redirect('/')

    # if homepage_teacher[0] == "false" and homepage_student[0] == "false":
    #     return render(request, 'login/login_teacher.html')
    # elif homepage_teacher[0] == "true":
    #     messages.info(
    #         request, 'You are already logged in so you can not go to the teacher login page,inorder to access the login page please logout!')
    #     return redirect('/teacher/dashboard/')
    # else:
    #     messages.info(
    #         request, 'You are already logged in so you can not go to the teacher login page,inorder to access the login page please logout!')
    #     return redirect('/teacher/dashboard/')


# def teacher_dashboard(request):
#     subs = subject.objects.all()
#     global uname
#     uname = uname.title()
#     if session_teacher[0] == "true":
#         homepage_teacher.insert(0, "true")
#         return render(request, 'courses/course_list.html', {'subs': subs, 'uname': uname})
#     else:
#         return redirect('/')


def login_student(request):
    usrs = user.objects.all()
    if request.method == "POST":
        username1 = request.POST['username1']
        password1 = request.POST['password1']
        global uname
        uname = username1

        i = 0
        k = len(usrs)
        while i < k:
            if usrs[i].role == "student" or usrs[i].role == "Student":
                if usrs[i].username == username1 and usrs[i].password == password1:
                    print(usrs[i].username, usrs[i].password)
                    session_student.insert(0, "true")
                    return redirect('/student/dashboard/')
                    break
            i = i+1

        else:
            messages.info(
                request, 'Make sure you choose the right login! Invalid username or password!')
            return redirect('/student/login/')

    if homepage_student[0] == "false" and homepage_teacher[0] == "false":
        return render(request, 'login/login_student1.html')
    elif homepage_student[0] == "true":
        messages.info(
            request, 'You are logged in! Logut to access the Homepage!')
        return redirect('/student/dashboard/')
    else:
        messages.info(
            request, 'You are logged in! Logut to access the Homepage!')
        return redirect('/teacher/dashboard/')


def student_dashboard(request):
    subs = subject.objects.all()
    global uname
    uname = uname.title()
    # usr = get_object_or_404(user, username=uname)
    # print("usr:", usr, "usr id", usr.user_id)
    if session_student[0] == "true":
        homepage_student.insert(0, "true")
        return render(request, 'courses/st_course_list.html', {'subs': subs, 'uname': uname})
    else:
        return redirect('/')


# def course_detail(request, subject_id):
#    #  subs = subject.objects.all()
#     sub = get_list_or_404(subject, subject_id=subject_id)
#     if session_teacher[0] == "true":
#         homepage_teacher.insert(0, "true")
#         return render(request, 'courses/course_details.html', {'sub': sub})
#     else:
#         return redirect('/')


def st_course_detail(request, subject_id):
   #  subs = subject.objects.all()
    sub = get_list_or_404(subject, subject_id=subject_id)
    xms = get_list_or_404(exams, subject_id_id=subject_id)
    # print(subject_id)
    global uname
    uname = uname.title()
    context = {
        'sub': sub,
        'subject_id': subject_id,
        'xms': xms,
        'uname': uname,
    }
    if session_student[0] == "true":
        homepage_student.insert(0, "true")
        return render(request, 'courses/st_course_details.html', context)
    else:
        return redirect('/')


def create_exam(request, subject_id):
    sub = get_list_or_404(subject, subject_id=subject_id)
    sub = sub[0]
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.subject_id_id = sub.subject_id
            exam.save()
            exam_id = exam.exam_id
            return redirect('login:create_set', subject_id=subject_id, exam_id=exam_id)
    else:
        form = ExamForm()
    context = {
        'form': form,
        'sub': sub,
    }
    if session_teacher[0] == "true":
        homepage_teacher.insert(0, "true")
        return render(request, 'courses/new_exam2.html', context)
    else:
        return redirect('/')
    # return render(request, 'login/registration.html', {'form': form})


# def legacy_create_exam(request, subject_id):

#     subs = subject.objects.all()
#     sub = get_list_or_404(subject, subject_id=subject_id)
#     sub = sub[0]

#     context = {
#         'subject_id': subject_id,
#         'sub': sub,
#     }
#     if request.method == 'POST':
#         exam_id = request.POST['exam_id']
#         exam_name = request.POST['exam_name']

#         # create exam obj
#         exam = exams.objects.create(subject_id_id=subject_id,
#                                     exam_name=exam_name)
#         exam.save()
#         # save_exam_id(exam_id)
#         # redirect to a success page
#         return redirect('login:create_set', subject_id=subject_id, exam_id=exam_id)

#     if session_teacher[0] == "true":
#         homepage_teacher.insert(0, "true")
#         return render(request, 'courses/new_exam.html', context)
#     else:
#         return redirect('/')


def exam_detail(request, subject_id, exam_id):
    # xm_id = save_exam_id
    sub = get_list_or_404(subject, subject_id=subject_id)
    xm = get_list_or_404(exams, exam_id=exam_id)
    context = {
        'sub': sub,
        'xm': xm,
        'subject_id': subject_id,
        'exam_id': exam_id,
    }
    render(request, 'courses/exam_detail.html', context)
    if session_teacher[0] == "true":
        homepage_teacher.insert(0, "true")
        return render(request, 'courses/exam_detail.html', context)
    else:
        return redirect('/')


def delete_exam(request, subject_id, exam_id):
    exam = get_object_or_404(exams, exam_id=exam_id)
    print(exam)
    exam.delete()
    return redirect('login:course_detail', subject_id=subject_id)


def st_exam_detail(request, subject_id, exam_id):
    # xm_id = save_exam_id
    sub = get_list_or_404(subject, subject_id=subject_id)
    xm = get_list_or_404(exams, exam_id=exam_id)
    # print("user name:", uname)

    context = {
        'sub': sub,
        'xm': xm,
        'subject_id': subject_id,
        'exam_id': exam_id,
    }
    # render(request, 'courses/st_exam_detail.html', context)
    if session_student[0] == "true":
        homepage_student.insert(0, "true")
        return render(request, 'courses/st_exam_detail.html', context)
    else:
        return redirect('/')


def choose_most_frequent_score(score_answer1, score_answer_jw2, jac_scr2, ham_scr2, cos_score2):
    # Get the frequencies of each score.
    score_answer1 = math.ceil(score_answer1)
    score_answer_jw2 = math.ceil(score_answer_jw2)
    jac_scr2 = math.ceil(jac_scr2)
    ham_scr2 = math.ceil(ham_scr2)
    cos_score2 = math.ceil(cos_score2)

    frequencies = {}
    for score in [score_answer1, score_answer_jw2, jac_scr2, ham_scr2, cos_score2]:
        if score not in frequencies:
            frequencies[score] = 1
        else:
            frequencies[score] += 1
    # Find the most frequent score.
    most_frequent_score = max(frequencies.keys(), key=frequencies.get)
    # If there are two scores with the same frequency, choose the highest score.
    if frequencies[most_frequent_score] == 1:
        return max(frequencies.keys())
    else:
        return most_frequent_score


def take_exam(request, subject_id, exam_id):

    # xm_id = save_exam_id
    sub = get_list_or_404(subject, subject_id=subject_id)
    xm = get_list_or_404(exams, exam_id=exam_id)
    ques_set = get_list_or_404(question_set, exam_id=exam_id)
    global uname
    uname = uname.lower()
    print("uname in take exam:", uname)
    usr = get_list_or_404(user, username=uname)
    print("take exam usr:", usr[0], "usr id", usr[0].user_id)
    # get questions
    ques = get_list_or_404(question, set_id_id=ques_set[0].set_id)
    # q_set_id = ques_set[0].set_id
    # get standard answers
    ans1 = get_list_or_404(answer, question_id_id=ques[0].question_id)
    ans2 = get_list_or_404(answer, question_id_id=ques[1].question_id)
    standard_answer1 = ans1[0].answer_text
    standard_answer2 = ans2[0].answer_text

    # global uname
    user_name = uname
    usr = get_list_or_404(user, username=user_name)
    uid = usr[0].user_id
    print("uid:", uid)
    # ger response texts
    if request.method == 'POST':
        res_text1 = request.POST['res_text1']
        res_text2 = request.POST['res_text2']
        # create response obj

        resp = response.objects.create(
            question_id_id=ques[0].question_id, user_id_id=uid, response_text=res_text1)

        resp.save()
        resp2 = response.objects.create(
            question_id_id=ques[1].question_id, user_id_id=uid, response_text=res_text2)

        resp2.save()

        # s1, s2 = leven.preprocess(standard_answer1, res_text1)
        s1, s2 = standard_answer1, res_text1
        similarity_score = leven.levenshtein_similarity(s1, s2)

        # print("The similarity of question" ":", similarity_score)
        score_answer = 10*similarity_score
        score_answer = round(score_answer, 2)
        jw_similarity = jaro2.jaro_winkler(s1, s2)
        score_answer_jw = 10*jw_similarity
        score_answer_jw = round(score_answer_jw, 2)
        # ------ jaccard------

        inp = standard_answer1
        inp1 = res_text1

        # tokenizing and remove stopword from Standard Answer
        tokens = word_tokenize(inp.lower())
        tokens = [
            token for token in tokens if token not in string.punctuation]
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        processed_text = ' '.join(tokens)

        tokens1 = word_tokenize(inp1.lower())
        tokens1 = [
            token for token in tokens1 if token not in string.punctuation]
        stop_words1 = set(stopwords.words('english'))
        tokens1 = [
            token for token in tokens1 if token not in stop_words]
        processed_text1 = ' '.join(tokens1)

        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(
            [processed_text, processed_text1])

        # Calculate the Jaccard similarity
        # jaccard_distance1 = jaccard.jaccard_similarity(
        #     tfidf_matrix[0].toarray().flatten(), tfidf_matrix[1].toarray().flatten())

        s1, s2 = pre.preprocess(s1, s2)
        sc = jac.jaccard_similarity(s1, s2)
        jac_scr1 = sc
        jac_scr1 = jac_scr1 * 10
        jac_scr1 = round(jac_scr1, 2)

        # --------- hamming---

        hamming_distance = hamming(tfidf_matrix[0].toarray(
        ).flatten(), tfidf_matrix[1].toarray().flatten())
        hamming_score1 = 1 - hamming_distance
        ham_scr1 = hamming_score1*10
        ham_scr1 = round(ham_scr1, 2)
        # -------- end hamming
        # cosine ---
        cos_distance = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        cos_distance = float(cos_distance[0])
        # Calculate the similarity score
        cos_score1 = cos_distance*10
        cos_score1 = round(cos_score1, 2)

        cm_scr1 = choose_most_frequent_score(
            score_answer, score_answer_jw, jac_scr1, ham_scr1, cos_score1)

        # save score
        save_scr1 = score.objects.create(
            question_id_id=ques[0].question_id, user_id_id=uid, score=score_answer)
        # save_scr1.save()

        # send the score to template
        # answer = {
        #     'score': score_answer
        # }
        # get similarity for question

        # ----------------2 ----------------
        s1, s2 = standard_answer2, res_text2
        similarity_score = leven.levenshtein_similarity(s1, s2)
        score_answer1 = 10*similarity_score
        score_answer1 = round(score_answer1, 2)
        # ------ jw2---
        jw_similarity = jaro2.jaro_winkler(s1, s2)
        score_answer_jw2 = 10*jw_similarity
        score_answer_jw2 = round(score_answer_jw2, 2)

        # jaccard2
        inp = standard_answer2
        inp1 = res_text2

        # tokenizing and remove stopword from Standard Answer
        tokens = word_tokenize(inp.lower())
        tokens = [
            token for token in tokens if token not in string.punctuation]
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        processed_text = ' '.join(tokens)
        tokens1 = word_tokenize(inp1.lower())
        tokens1 = [
            token for token in tokens1 if token not in string.punctuation]
        # stop_words1 = set(stopwords.words('english'))
        tokens1 = [
            token for token in tokens1 if token not in stop_words]
        processed_text1 = ' '.join(tokens1)

        vectorizer = TfidfVectorizer()

        tfidf_matrix = vectorizer.fit_transform(
            [processed_text, processed_text1])

        # Calculate the Jaccard similarity
        s1, s2 = pre.preprocess(s1, s2)
        sc = jac.jaccard_similarity(s1, s2)
        jac_scr2 = sc
        jac_scr2 = jac_scr2 * 10
        jac_scr2 = round(jac_scr2, 2)
        # end jaccard
        # hamming2
        hamming_distance = hamming(tfidf_matrix[0].toarray(
        ).flatten(), tfidf_matrix[1].toarray().flatten())
        hamming_score2 = 1 - hamming_distance
        ham_scr2 = hamming_score2*10
        ham_scr2 = round(ham_scr2, 2)

        # cosine2 ---
        cos_distance = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        cos_distance = float(cos_distance[0])

        # Calculate the similarity score
        cos_score2 = cos_distance*10
        cos_score2 = round(cos_score2, 2)

        # choose the most frequent score among score_answer1, score_answer_jw2, jac_scr2, ham_scr2, cos_score2
        # if among these five scores any two scores are same then choose that score
        # else choose the highest score
        # provide the code

        # choosen score 2 of all algos
        cm_scr2 = choose_most_frequent_score(
            score_answer1, score_answer_jw2, jac_scr2, ham_scr2, cos_score2)
        save_scr2 = score.objects.create(
            question_id_id=ques[0].question_id, user_id_id=uid, score=score_answer1)
        # save_scr2.save()
        print("score:", score_answer)
        total = cm_scr1+cm_scr2
        total = math.ceil(total)
        answer1 = {
            'score': score_answer,
            'score2': score_answer1,
            'jw1': score_answer_jw,
            'jw2': score_answer_jw2,
            'jac1': jac_scr1,
            'jac2': jac_scr2,
            'ham1': ham_scr1,
            'ham2': ham_scr2,
            'cos1': cos_score1,
            'cos2': cos_score2,
            'total_value': total,
        }
        return render(request, 'login/result.html', answer1)
    context = {
        'sub': sub,
        'xm': xm,
        'subject_id': subject_id,
        'exam_id': exam_id,
        'ques_set': ques_set,
        'ques': ques,
        'user_name': user_name
        # 'q_set_id': q_set_id,
    }
    # render(request, 'courses/take_exam.html', context)
    if session_student[0] == "true":
        homepage_student.insert(0, "true")
        return render(request, 'courses/take_exam.html', context)
    else:
        return redirect('/')


def create_set(request, subject_id, exam_id):
    sub = get_list_or_404(subject, subject_id=subject_id)
    xm = get_list_or_404(exams, exam_id=exam_id)
    context = {
        'sub': sub,
        'xm': xm,
        'subject_id': subject_id,
        'exam_id': exam_id,
    }
    if request.method == 'POST':
        set_id = request.POST['set_id']
        set_number = request.POST['set_number']
        ques_set = question_set.objects.create(subject_id_id=subject_id,
                                               exam_id_id=exam_id, set_id=set_id, set_number=set_number)
        ques_set.save()

        # redirect to a success page
        return redirect('login:create_ques', subject_id=subject_id, exam_id=exam_id, set_id=set_id)

    if session_teacher[0] == "true":
        homepage_teacher.insert(0, "true")
        return render(request, 'courses/create_set.html', context)
    else:
        return redirect('/')


def create_ques(request, subject_id, exam_id, set_id):
    sub = get_list_or_404(subject, subject_id=subject_id)
    xm = get_list_or_404(exams, exam_id=exam_id)
    sets = get_list_or_404(
        question_set, subject_id_id=subject_id, exam_id_id=exam_id)
    sets = sets[0]

    context = {
        'sub': sub,
        'xm': xm,
        'subject_id': subject_id,
        'exam_id': exam_id,
        'set_id': set_id,
        'set': sets,
    }
    if request.method == 'POST':
        ques1 = request.POST['ques1']
        ans1 = request.POST['ans1']
        ques2 = request.POST['ques2']
        ans2 = request.POST['ans2']
        # create response obj

        ques = question.objects.create(
            set_id_id=set_id, question_text=ques1, question_number=1)

        ques.save()
        ques = question.objects.create(
            set_id_id=set_id, question_text=ques2, question_number=1)

        ques.save()
        # save ans
        q = get_list_or_404(question, set_id_id=set_id)
        q1 = q[0].question_id
        q2 = q[1].question_id

        ans = answer.objects.create(
            question_id_id=q1, answer_text=ans1)

        ans.save()
        anss = answer.objects.create(
            question_id_id=q2, answer_text=ans2)

        anss.save()

        return HttpResponse('success')

    if session_teacher[0] == "true":
        homepage_teacher.insert(0, "true")
        return render(request, 'courses/ques_create.html', context)
    else:
        return redirect('/')


# text similarity views
# def similarity(request):


def teacher_result(request, subject_id, exam_id):
    global uname

    usr = get_list_or_404(user)

    xm = get_list_or_404(exams, exam_id=exam_id)
    xm_id = xm[0].exam_id
    scr = get_list_or_404(score)

    context = {
        'usr': usr,
        'xm_id': xm_id,
        'scr': scr
    }
    return render(request, 'courses/t_result.html', context)


def st_result(request, subject_id, exam_id):
    scores = score.objects.all()
    context = {
        'scores': scores
    }
    return render(request, 'login/result.html', context)


def logout_user(request):
    session_teacher.insert(0, "false")
    session_student.insert(0, "false")
    homepage_teacher.insert(0, "false")
    homepage_student.insert(0, "false")
    return redirect('/')
