from django.contrib.auth.models import User
from rest_framework.parsers import FileUploadParser
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.db.models import Q

from accounts.models import Department
from accounts.serializers import DepartmentSerializer
from internship.models import Enterprise, Convention

from .models import (
    Framer,
    Promotion,
    Student,
    Teacher,
    Classroom,
    Task,
    Project,
    Skill,
    TaskComment,
    Attachments,
    ConventionMessage,
    RapportComment,
    Notification,
    StudentWhiteList,
    TeacherWhiteList,
    FramerWhiteList
)
from .serializers import (
    FramerSerializer,
    LoginSerializer,
    PromotionSerializer,
    RegisterSerializer,
    StudentSerializer,
    TeacherSerializer,
    UserSerializer,
    ClassroomSerializer,
    TaskSerializer,
    SkillSerializer,
    ProjectSerializer,
    TaskCommentSerializer,
    AttachmentsSerializer,
    ConventionMessageSerializer,
    RapportCommentSerializer,
    NotificationSerializer,
    StudentWhiteListSerializer,
    TeacherWhiteListSerializer,
    FramerWhiteListSerializer,
    PromotionRegisterSerializer
)


def notify(title, from_, to, taskId=None, projectId=None, rapport_studentId=None):
    UserFrom_ = User.objects.get(id=from_)
    UsersTo = [User.objects.get(id=id) for id in to]
    notification = Notification.objects.create(title=title, userFrom=UserFrom_)
    notification.save()
    notification.to.add(*UsersTo)
    if projectId:
        project = Project.objects.get(id=projectId)
        notification.project = project
    if taskId:
        task = Task.objects.get(id=taskId)
        notification.task = task
    if rapport_studentId:
        rapport_student = Student.objects.get(id=rapport_studentId)
        notification.rapport_student = rapport_student

    notification.save()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_class = (FileUploadParser,)
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = request.data['firstname']
        last_name = request.data['lastname']
        phone = request.data["phone"]
        email = request.data["email"]

        try:
            User.objects.get(email=email)
            return Response({
                "error": "email deja utilise"
            })
        except:
            pass
        image = ''
        try:
            image = request.data["image"]
        except:
            pass
        if request.data['status'] == 'student':
            try :
                StudentWhiteList.objects.get(email=email, phone=phone)
                pass
            except:
                return Response({
                    'error' : "Vous n'avez le droit d'acces a la platforme avec cet email"
                })
            department_name = request.data['department']
            birthday = request.data['birthday']
            department = Department.objects.get(name=department_name)
            classroom = Classroom.objects.get(name=request.data['classe'])
            promo = Promotion.objects.get(
                name=request.data['promotion'])
            user = serializer.save()
            Student.objects.create(user=user, promotion=promo, first_name=first_name,
                                   last_name=last_name, department=department, classroom=classroom, phone=phone, image=image, birthday=birthday)

        elif request.data['status'] == 'teacher':
            try :
                TeacherWhiteList.objects.get(email=email, phone=phone)
                pass
            except:
                return Response({
                    'error' : "Vous n'avez le droit d'acces au platforme"
                })
            department_name = request.data['department']
            department = Department.objects.get(name=department_name)
            user = serializer.save()
            Teacher.objects.create(user=user, first_name=first_name,
                                   last_name=last_name, department=department, phone=phone, image=image)

        elif request.data['status'] == 'framer':
            try :
                FramerWhiteList.objects.get(email=email, phone=phone)
                pass
            except:
                return Response({
                    'error' : "Vous n'avez le droit d'acces au platforme"
                })
            user = serializer.save()
            enterprise = Enterprise.objects.get(id=request.data['enterprise'])
            Framer.objects.create(user=user, first_name=first_name,
                                  last_name=last_name, phone=phone, image=image, enterprise=enterprise)

        user.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *args, **kwargs):
        print((request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UsersAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = User.objects.all()


class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user


class DepartmentAPI(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]


class StudentAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = StudentSerializer
    parser_class = (FileUploadParser,)

    def get_queryset(self):
        queryset_search = Student.objects.all()
        query = self.request.GET.get('search')
        
        if query:
            queryset_search = queryset_search.filter(
                Q(first_name__icontains=query)
            ).distinct()
        return queryset_search

    def update(self, request, pk):
        student = Student.objects.get(id=pk)
        if 'skills' in request.data:
            skills_id = request.data['skills']
            skills = []
            for id in skills_id:
                skills.append(Skill.objects.get(id=id))

            student.skills.add(*skills)

        if 'skill' in request.data:

            skill_id = request.data['skill']
            skill = Skill.objects.get(id=skill_id)
            student.skills.remove(skill)

        if 'first_name' in request.data:
            student.first_name = request.data["first_name"]
        if 'last_name' in request.data:
            student.last_name = request.data["last_name"]
        if 'image' in request.data:
            if request.data['image'] != 'undefined':
                student.image = request.data['image']
        if 'phone' in request.data:
            student.phone = request.data["phone"]
        if 'gender' in request.data:
            student.gender = request.data["gender"]
        if 'socialStatus' in request.data:
            student.socialStatus = request.data["socialStatus"]
        if 'address' in request.data:
            student.address = request.data["address"]
        student.save()

        return Response(StudentSerializer(student).data)


class TeacherAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class FramerAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Framer.objects.all()
    serializer_class = FramerSerializer


class PromotionAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Promotion.objects.all().order_by('-id')
    serializer_class = PromotionSerializer
class PromotionRegisterAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Promotion.objects.all().order_by('-id')
    serializer_class = PromotionRegisterSerializer


class ClassroomAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('-id')
    serializer_class = SkillSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer

    def create(self, request):
        title = request.data['title']
        description = request.data['description']
        framer = Framer.objects.get(id=request.data['framer'])
        task = Task.objects.create(
            title=title, description=description, framer=framer)

        if 'project' in request.data:
            project = Project.objects.get(id=request.data['project'])
            task.project = project
        if 'starting_time' in request.data:
            task.starting_time = request.data['starting_time']
        if 'finish_time' in request.data:
            task.finish_time = request.data['finish_time']

        task.save()

        # sending notification
        UserToNotify = []
        for id in request.data['students']:
            student = Student.objects.get(id=id)
            UserToNotify.append(student.user.id)
            task.students.add(student)
        git = Department.objects.get(name="GIT")
        teachers = Teacher.objects.filter(department=git)
        UserToNotify += [teacher.user.id for teacher in teachers]

        title_notification = "Creation d'une nouvelle tache : " + title
        if 'project' in request.data:
            notify(title_notification, framer.user.id,
                   UserToNotify, task.id, project.id)
        else:
            notify(title_notification, framer.user.id, UserToNotify, task.id)
        return Response(TaskSerializer(task).data)

    def update(self, request, pk):
        task = Task.objects.get(id=pk)
        userId = request.data["user"]
        state = request.data['state']
        task.state = state
        task.save()

        # Sending notification
        git = Department.objects.get(name="GIT")
        teachers = Teacher.objects.filter(department=git)
        UserToNotify = [teacher.user.id for teacher in teachers]

        user = User.objects.get(id=userId)
        fromm = ''
        status = ''
        framer = Framer.objects.filter(user=user)
        if len(framer) > 0:
            fromm = user.framer.first_name + " " + user.framer.last_name
            status = 'Encadreur '
            for student in task.students.all():
                UserToNotify.append(student.user.id)
        else:
            fromm = user.student.first_name + " " + user.student.last_name
            status = "Eleve"
            UserToNotify.append(task.framer.user.id)

        title_notification = "La tache " + task.title + \
            " est deplacee en " + state + " par " + status + " : " + fromm
        if task.project:
            notify(title_notification, userId,
                   UserToNotify, task.id, task.project.id)
        else:
            notify(title_notification, userId, UserToNotify, task.id)
        return Response(TaskSerializer(task).data)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset_project = Project.objects.filter(is_deleted=False).order_by('-id')
        query = self.request.GET.get('framerId')
        if query:
            framer = Framer.objects.get(id=query)
            queryset_project = queryset_project.filter(framer=framer)
        return queryset_project

    def create(self, request):
        name = request.data['name']
        description = request.data['description']
        aim = request.data['aim']
        enterprise = Enterprise.objects.get(id=request.data['enterprise'])
        framer = Framer.objects.get(id=request.data['framer'])
        pro = Project.objects.create(
            name=name, description=description, aim=aim, framer=framer, enterprise=enterprise)

        if 'starting_time' in request.data:
            pro.starting_time = request.data['starting_time']
        if 'finish_time' in request.data:
            pro.finish_time = request.data['finish_time']

        pro.save()

        for id in request.data['students']:
            pro.students.add(Student.objects.get(id=id))

        # send notification

        title_notification = "Une nouvelle tache vous a ete assignee : " + title
        notify(title_notification, framer.user.id, userStudentId, task.id)

        return Response(ProjectSerializer(pro).data)
    
    def update(self, request, pk):
        project = Project.objects.get(id=pk)
        if 'is_deleted' in request.data:
            project.is_deleted = True
        
        project.save()
        return Response(ProjectSerializer(project).data)

class AttachmentsViewSet(viewsets.ModelViewSet):
    parser_class = (FileUploadParser,)
    queryset = Attachments.objects.all().order_by('-id')
    serializer_class = AttachmentsSerializer


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all().order_by('-id')
    serializer_class = TaskCommentSerializer

    def create(self, request):
        content = request.data['comment']
        author = User.objects.get(id=request.data['author'])
        task = Task.objects.get(id=request.data['task'])

        comment = TaskComment.objects.create(
            comment=content, author=author, task=task)
        comment.save()
        return Response(TaskCommentSerializer(comment).data)


class RapportCommentViewSet(viewsets.ModelViewSet):
    serializer_class = RapportCommentSerializer

    def get_queryset(self):
        queryset_comment = RapportComment.objects.all()
        query = self.request.GET.get('studentId')
        if query:
            student = Student.objects.get(id=query)
            queryset_comment = queryset_comment.filter(student=student)
        return queryset_comment

    def create(self, request):
        content = request.data['comment']
        author = User.objects.get(id=request.data['author'])
        student = Student.objects.get(id=request.data['student'])

        comment = RapportComment.objects.create(
            comment=content, author=author, student=student)
        comment.save()

        # notify
        git = Department.objects.get(name="GIT")
        title_notification = ''
        UserToNotify = []
        framer = Framer.objects.filter(user=author)
        teacher = Teacher.objects.filter(user=author)

        if len(framer) > 0:
            fromm = author.framer.first_name + " " + author.framer.last_name
            title_notification = "L'encadreur " + fromm + " a commenter le rapport de " + \
                student.first_name + " " + student.last_name
            teachers = Teacher.objects.filter(department=git)
            UserToNotify += [teacher.user.id for teacher in teachers]
            UserToNotify.append(student.user.id)
        elif len(teacher) > 0:
            fromm = author.teacher.first_name + " " + author.teacher.last_name
            title_notification = "Le professeur " + fromm + \
                " a commente le rapport de " + student.first_name + " " + student.last_name
            teachers = Teacher.objects.filter(
                department=git).exclude(id=author.teacher.id)
            UserToNotify += [teacher.user.id for teacher in teachers]
            UserToNotify.append(student.user.id)
            framers = Framer.objects.filter(enterprise=student.enterprise)
            UserToNotify += [framer.user.id for framer in framers]

        else:
            fromm = author.student.first_name + " " + author.student.last_name
            title_notification = "L'eleve " + fromm + " a commenter son rapport de stage "
            framers = Framer.objects.filter(enterprise=student.enterprise)
            UserToNotify += [framer.user.id for framer in framers]
            teachers = Teacher.objects.filter(department=git)
            UserToNotify += [teacher.user.id for teacher in teachers]

        notify(title_notification, author.id,
               UserToNotify, rapport_studentId=student.id)

        return Response(RapportCommentSerializer(comment).data)


class ConventionMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ConventionMessageSerializer

    def get_queryset(self):
        queryset_msg = ConventionMessage.objects.all()
        query = self.request.GET.get('convID')
        if query:
            convention = Convention.objects.get(id=query)
            queryset_msg = queryset_msg.filter(convention=convention)
        return queryset_msg

    def create(self, request):
        content = request.data['content']
        sender = User.objects.get(id=request.data['sender'])
        convention = Convention.objects.get(id=request.data['convention'])
        sender_status = request.data['sender_status']
        conv_message = ConventionMessage.objects.create(content=content, sender=sender, convention=convention, sender_status=sender_status)
        conv_message.save()

        return Response(ConventionMessageSerializer(conv_message).data)
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset_msg = Notification.objects.all().order_by('-id')
        query = self.request.GET.get('userID')
        if query:
            convention = Notification.objects.get(id=query)
            queryset_msg = queryset_msg.filter(convention=convention)
        return queryset_msg

    def update(self, request, pk):
        notification = Notification.objects.get(id=pk)

        user = User.objects.get(id=request.data['read'])
        notification.to.remove(user)
        notification.read.add(user)

        notification.save()

        return Response(NotificationSerializer(notification).data)


class StudentWhiteListViewSet(viewsets.ModelViewSet):
    queryset = StudentWhiteList.objects.all().order_by('-id')
    serializer_class = StudentWhiteListSerializer
class TeacherWhiteListViewSet(viewsets.ModelViewSet):
    queryset = TeacherWhiteList.objects.all().order_by('-id')
    serializer_class = TeacherWhiteListSerializer
class FramerWhiteListViewSet(viewsets.ModelViewSet):
    queryset = FramerWhiteList.objects.all().order_by('-id')
    serializer_class = FramerWhiteListSerializer
