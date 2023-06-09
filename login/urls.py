from django.urls import path, include
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_user, name='register'),
    path('create_subject/', views.register_subject, name='subj'),
    path('teacher/login/', views.login_teacher, name='login_teacher'),
    path('student/login/', views.login_student, name='login_student'),
    path('teacher/dashboard/', views.teacher_dashboard),

    path('teacher/dashboard/<int:subject_id>/',
         views.course_detail, name='course_detail'),

    path('teacher/dashboard/<int:subject_id>/create_exam/',
         views.create_exam, name='create_exam'),

    path('teacher/dashboard/<int:subject_id>/create_exam/<int:exam_id>/create_set/',
         views.create_set, name='create_set'),
    #     teacher result
    path('teacher/dashboard/<int:subject_id>/<int:exam_id>/teacher_result',
         views.teacher_result, name='teacher_result'),
    #     delete exam
    path('teacher/dashboard/<int:subject_id>/<int:exam_id>/delete_exam',
         views.delete_exam, name='delete_exam'),


    #     create question & ans ------
    path('teacher/dashboard/<int:subject_id>/create_exam/<int:exam_id>/create_set/<int:set_id>',
         views.create_ques, name='create_ques'),

    path('teacher/dashboard/<int:subject_id>/<int:exam_id>',
         views.exam_detail, name='exam_detail'),

    #     student dashboard
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    path('student/dashboard/<int:subject_id>/',
         views.st_course_detail, name='st_course_detail'),

    # st exam detail
    path('student/dashboard/<int:subject_id>/<int:exam_id>',
         views.st_exam_detail, name='st_exam_detail'),

    # st take exam
    path('student/dashboard/<int:subject_id>/<int:exam_id>/take_exam/',
         views.take_exam, name='take_exam'),
    #   st  result
    path('student/dashboard/<int:subject_id>/<int:exam_id>/result',
         views.st_result, name='st_result'),



    #     path('teacher/dashboard/<int:subject_id>/create_exam/exam_created',
    #          views.exam_created, name='exam_created'),




    path('logout_user/', views.logout_user, name="logout_user"),
    path('results/', include('results.urls')),


]
