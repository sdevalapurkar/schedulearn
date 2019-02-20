"""This module contains the views that render the webpages when the user wants
    to go to a route.
"""
import datetime
import base64
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.core.files.base import ContentFile
from accounts.models import Availability, Skill, Notification, BlockedUsers
from schedule_lessons.local_settings import (
    EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_PORT, VERIFY_USER_EMAIL
    )
from .models import Lesson, Relationship
from allauth.socialaccount.models import SocialAccount, SocialToken


DAYS_OF_THE_WEEK = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
    ]
UTC_ZONE = datetime.timezone(datetime.timedelta(0))

@login_required
def agenda(request):
    """A view that serves the agenda page for a logged-in user."""
    pending_lesson_list = []
    scheduled_lesson_list = []
    if request.user.profile.user_type == "student":
        lessons = Lesson.objects.filter(student=request.user)
    else:
        lessons = Lesson.objects.filter(tutor=request.user)
    for lesson in lessons:
        data = {
            "id": lesson.id,
            "name": lesson.name,
            "location": lesson.location,
            "tutor_name": lesson.tutor.get_full_name(),
            "tutor_id": lesson.tutor.profile.id,
            "student_name": lesson.student.get_full_name(),
            "student_id": lesson.student.profile.id,
            "start_time": lesson.start_time,
            "end_time": lesson.end_time,
            "display_options": lesson.created_by != request.user,
        }
        if lesson.pending:
            pending_lesson_list.append(data)
        else:
            scheduled_lesson_list.append(data)
    context = {
        "scheduled_lessons": scheduled_lesson_list,
        "pending_lessons": pending_lesson_list,
        "gcalendar_access": "/accounts/google/login/?process=&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar"
        }
    no_results_found = request.GET.get("no_search_result")
    context["gcalender_success"] = request.GET.get("gcalender_success", "")
    context["scheduled_successful"] = request.GET.get("schedule", False)
    context["rescheduled_successful"] = request.GET.get("reschedule", False)
    if no_results_found:
        context["no_results"] = "No results were found"
    if context["scheduled_successful"]:
        context["successful_schedule_msg"] = ("You've successfully scheduled "
                                             + request.GET.get("lesson"))
    if context["rescheduled_successful"]:
        context["successful_schedule_msg"] = ("You've successfully rescheduled "
                                             + request.GET.get("lesson"))
    notifications = Notification.objects.filter(
        user=request.user).order_by("-created_on") # most recent
    context["notifications"] = []
    for notification in notifications:
        notification.time_info = get_timestamp(notification.created_on)
        notification.save()
        context["notifications"].append(notification)
    context["unread_notifications"] = len(Notification.objects.filter(
        user=request.user, unread=True))
    return render(request, "dashboard/agenda.html", context)

@login_required
def save_gcalendar_lesson(request, lesson_id):
    """A view handles the POST request for saving a lesson to the requesting
       user"s google calendar.
    """
    response = redirect("agenda")
    insert_calendar_url = "https://www.googleapis.com/calendar/v3/calendars"
    list_calendar_url = ("https://www.googleapis.com/calendar/v3/users/me/"
                         "calendarList")
    if SocialAccount.objects.filter(user_id=request.user).exists():
        try:
            lesson_to_save = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            response["Location"] += "?gcalender_success=No"
            return response
        if not (request.user == lesson_to_save.tutor or
                request.user == lesson_to_save.student):
            response["Location"] += "?gcalender_success=No"
            return response
        access_token = SocialToken.objects.get(account__user=request.user)
        headers = {
            "Authorization": "Bearer " + access_token.token
            }
        user_calendars = requests.get(list_calendar_url,
                                      headers=headers).json().get("items", False)
        if not user_calendars:
            response["Location"] += "?gcalender_success=invalid_permission"
            return response
        schedulearn_calendar_exists = False
        for calendar in user_calendars:
            if calendar["summary"] == "My Lessons (Schedulearn)":
                schedulearn_calendar_exists = True
                schedulearn_calendar_id = calendar["id"]
        if not schedulearn_calendar_exists:
            requests.post(insert_calendar_url, headers=headers,
                          json={
                              "summary": "My Lessons (Schedulearn)",
                              "timeZone": "Etc/UTC"
                              })
            user_calendars = requests.get(list_calendar_url,
                                          headers=headers).json()["items"]
            for calendar in user_calendars:
                if calendar["summary"] == "My Lessons (Schedulearn)":
                    schedulearn_calendar_id = calendar["id"]
        change_calendar_color_url = "{}/{}?colorRgbFormat=True".format(
            list_calendar_url, schedulearn_calendar_id)
        requests.put(change_calendar_color_url, headers=headers, json={
            "foregroundColor": "#ffffff", "backgroundColor": "#D14F52",
            "selected": True
            })
        start_time = "{}T{}+00:00".format(lesson_to_save.start_time.date(),
                                          lesson_to_save.start_time.time())
        end_time = "{}T{}+00:00".format(lesson_to_save.end_time.date(),
                                        lesson_to_save.end_time.time())
        create_event_url = "https://www.googleapis.com/calendar/v3/calendars/"\
            + schedulearn_calendar_id + "/events?sendNotifications=True"
        event = {
            "summary": lesson_to_save.name,
            "start": {
                "dateTime": start_time
            },
            "end": {
                "dateTime": end_time
            },
            "location": lesson_to_save.location,
            "status": "tentative",
            "attendees": [
                {
                    "displayName": (lesson_to_save.student.get_full_name() if
                                    request.user == lesson_to_save.tutor else
                                    lesson_to_save.tutor.get_full_name()),
                    "email": (lesson_to_save.student.email if
                              request.user == lesson_to_save.tutor else
                              lesson_to_save.tutor.email),
                    "responseStatus": "tentative",
                }
            ]
        }
        if requests.post(create_event_url, headers=headers,
                         json=event).status_code == 200:
            response["Location"] += "?gcalender_success=Yes"
        else:
            response["Location"] += "?gcalender_success=No"
    return response


@login_required
def relationships(request):
    """A view handles the GET request for serving the relationships page for
       users.
    """
    context = {
        "notifications": [],
        "unread_notifications": len(Notification.objects.filter(
            user=request.user, unread=True)),
        "no_results": "No results were found" if request.GET.get(
            "no_search_result") else False
    }
    notifications = Notification.objects.filter(
        user=request.user).order_by("-created_on") # most recent
    for notification in notifications:
        notification.time_info = get_timestamp(notification.created_on)
        notification.save()
        context["notifications"].append(notification)
    if request.user.profile.user_type == "tutor":
        context["requests_from_students"] = []
        context["requested_students"] = []
        context["accepted_students"] = []
        users_relationships = Relationship.objects.filter(tutor=request.user)
        for relationship in users_relationships:
            if relationship.pending:
                if relationship.created_by == request.user:
                    context["requested_students"].append(relationship.student)
                else:
                    context["requests_from_students"].append(
                        relationship.student)
            else:
                context["accepted_students"].append(relationship.student)
    if request.user.profile.user_type == "student":
        context["requests_from_tutors"] = []
        context["requested_tutors"] = []
        context["accepted_tutors"] = []
        users_relationships = Relationship.objects.filter(student=request.user)
        for relationship in users_relationships:
            if relationship.pending:
                if relationship.created_by == request.user:
                    context["requested_tutors"].append(relationship.tutor)
                else:
                    context["requests_from_tutors"].append(relationship.tutor)
            else:
                context["accepted_tutors"].append(relationship.tutor)
    return render(request, "dashboard/relationships.html", context)

@login_required
def search(request):
    """A view handles the POST request for finding users given an email."""
    email = request.GET.get("searchResult")
    if not email:
        response = HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        response["Location"] += "?no_search_result=True"
        return response
    try:
        user_result = User.objects.get(email__iexact=email)
        user_id = str(user_result.profile.id)
        return redirect("public_profile", user_id)
    except User.DoesNotExist:
        response = HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        response["Location"] += "?no_search_result=True"
        return response

def public_profile(request, user_id):
    """A view that handles the GET request for displaying the public profile of
       a user.
    """
    try:
        context = {
            "profile_user": User.objects.get(profile__id=user_id),
            "availabilities": return_availabilities(user_id),
            "days_of_the_week": DAYS_OF_THE_WEEK
        }
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if not request.user.is_anonymous:
        context["rel_exists"] = relationship_exists(context["profile_user"],
                                                    request.user)
        try:
            BlockedUsers.objects.get(user=request.user,
                                     blocked_user=context["profile_user"])
            context["block_user_url"] = "{}dashboard/unblock/{}".format(
                                    request.build_absolute_uri("/"), user_id)
            context["blocked"] = True
        except BlockedUsers.DoesNotExist:
            context["block_user_url"] = "{}dashboard/block/{}".format(
                                    request.build_absolute_uri("/"), user_id)
            context["blocked"] = False
        try:
            BlockedUsers.objects.get(user=context["profile_user"])
            context["blocked_by_user"] = True
        except BlockedUsers.DoesNotExist:
            context["blocked_by_user"] = False

        if context["rel_exists"]:
            try:
                relationship = Relationship.objects.get(
                    tutor=request.user, student=context["profile_user"])
            except Relationship.DoesNotExist:
                relationship = Relationship.objects.get(
                    tutor=context["profile_user"], student=request.user)

            context["rel_pending"] = relationship.pending
            if request.user == relationship.created_by and relationship.pending:
                context["rel_created_by_request_user"] = True
            if request.user != relationship.created_by and relationship.pending:
                if request.user.profile.user_type == "tutor":
                    context["add_student_url"] = "{}dashboard/add_student/{}"\
                        .format(request.build_absolute_uri("/"), user_id)
                    context["remove_student_url"] = (
                        "{}dashboard/remove_student/{}".format(
                            request.build_absolute_uri("/"), user_id))
                else:
                    context["add_tutor_url"] = "{}dashboard/add_tutor/{}"\
                        .format(request.build_absolute_uri("/"), user_id)
                    context["remove_tutor_url"] = "{}dashboard/remove_tutor/{}"\
                        .format(request.build_absolute_uri("/"), user_id)
            elif not relationship.pending:
                if request.user.profile.user_type == "tutor":
                    context["remove_student_url"] = (
                        "{}dashboard/remove_student/{}".format(
                            request.build_absolute_uri("/"), user_id))
                else:
                    context["remove_tutor_url"] = "{}dashboard/remove_tutor/{}"\
                        .format(request.build_absolute_uri("/"), user_id)
        else:
            if request.user.profile.user_type == "tutor":
                context["add_student_url"] = "{}dashboard/add_student/{}"\
                        .format(request.build_absolute_uri("/"), user_id)
            else:
                context["add_tutor_url"] = "{}dashboard/add_tutor/{}".format(
                    request.build_absolute_uri("/"), user_id)
        notifications = Notification.objects.filter(
            user=request.user).order_by("-created_on") # most recent
        context["notifications"] = []
        for notification in notifications:
            notification.time_info = get_timestamp(notification.created_on)
            notification.save()
            context["notifications"].append(notification)
        context["unread_notifications"] = len(Notification.objects.filter(
            user=request.user, unread=True))
    return render(request, "dashboard/public_profile.html", context)

@login_required
def add_student(request, student_id):
    """A view that handles the POST request for adding a student."""
    try:
        student = User.objects.get(profile__id=student_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    blocking_relationship = []
    blocking_relationship.append(
        BlockedUsers.objects.filter(user=request.user, blocked_user=student))
    blocking_relationship.append(
        BlockedUsers.objects.filter(user=student, blocked_user=request.user))
    if (student.profile.user_type != "student"
            or request.user.profile.user_type != "tutor") or blocking_relationship:
        return HttpResponse(status=400)
    rel_exists = relationship_exists(student, request.user)
    if rel_exists:
        relationship = Relationship.objects.get(tutor=request.user,
                                                student=student)
        if relationship.pending and relationship.created_by != request.user:
            relationship.pending = False
            relationship.save()
            message = "{} has accepted your friend request.".format(
                request.user.get_full_name())
            url = "/dashboard/profile/{}".format(request.user.profile.id)
            Notification(user=student, message=message,
                         created_on=datetime.datetime.now(tz=UTC_ZONE),
                         picture=request.user.profile.profile_pic,
                         link=url).save()
        else:
            return HttpResponse(status=400)
    else:
        new_rel = Relationship(student=student, tutor=request.user,
                               created_by=request.user, pending=True)
        new_rel.save()
        url = "/dashboard/profile/{}".format(request.user.profile.id)
        message = "{} has sent out a friend request.".format(
            request.user.get_full_name())
        Notification(user=student, message=message,
                     created_on=datetime.datetime.now(tz=UTC_ZONE),
                     picture=request.user.profile.profile_pic,
                     link=url).save()

    return redirect("relationships")

@login_required
def remove_student(request, student_id):
    """A view that handles the POST request for removing a student."""
    try:
        student = User.objects.get(profile__id=student_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if student.profile.user_type != "student":
        return HttpResponse(status=400)
    try:
        old_rel = Relationship.objects.get(student=student, tutor=request.user)
    except Relationship.DoesNotExist:
        return HttpResponse(status=400)
    old_rel.delete()
    Lesson.objects.filter(student=student, tutor=request.user).delete()
    return redirect("relationships")


@login_required
def add_tutor(request, tutor_id):
    """A view that handles the POST request for adding a tutor."""
    try:
        tutor = User.objects.get(profile__id=tutor_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    blocking_relationship = []
    blocking_relationship.append(
        BlockedUsers.objects.filter(user=request.user, blocked_user=tutor))
    blocking_relationship.append(
        BlockedUsers.objects.filter(user=tutor, blocked_user=request.user))
    if (tutor.profile.user_type != "tutor"
            or request.user.profile.user_type != "student") or blocking_relationship:
        return HttpResponse(status=400)
    rel_exists = relationship_exists(tutor, request.user)
    if rel_exists:
        relationship = Relationship.objects.get(tutor=tutor,
                                                student=request.user)
        if relationship.pending and relationship.created_by != request.user:
            relationship.pending = False
            relationship.save()
            message = "{} has accepted your friend request.".format(
                request.user.get_full_name())
            url = "/dashboard/profile/{}".format(request.user.profile.id)
            Notification(user=tutor, message=message,
                         created_on=datetime.datetime.now(tz=UTC_ZONE),
                         picture=request.user.profile.profile_pic,
                         link=url).save()
        else:
            return HttpResponse(status=400)
    else:
        new_rel = Relationship(student=request.user, tutor=tutor,
                               created_by=request.user, pending=True)
        new_rel.save()
        url = "/dashboard/profile/{}".format(request.user.profile.id)
        message = "{} has sent out a friend request.".format(
            request.user.get_full_name())
        Notification(user=tutor, message=message,
                     created_on=datetime.datetime.now(tz=UTC_ZONE),
                     picture=request.user.profile.profile_pic,
                     link=url).save()
    return redirect("relationships")

@login_required
def remove_tutor(request, tutor_id):
    """A view that handles the POST request for removing a tutor."""
    try:
        tutor = User.objects.get(profile__id=tutor_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if tutor.profile.user_type != "tutor":
        return HttpResponse(status=400)
    try:
        old_rel = Relationship.objects.get(student=request.user,
                                           tutor=tutor)
    except Relationship.DoesNotExist:
        return HttpResponse(status=400)
    old_rel.delete()
    Lesson.objects.filter(tutor=tutor, student=request.user).delete()
    return redirect("relationships")


@login_required
def choose_person(request):
    """A view that handles the GET request for presenting the choose_person
       page.
    """
    context = {
        "notifications": [],
        "unread_notifications": len(Notification.objects.filter(
            user=request.user, unread=True))
    }
    notifications = Notification.objects.filter(
        user=request.user).order_by("-created_on") # most recent
    for notification in notifications:
        notification.time_info = get_timestamp(notification.created_on)
        notification.save()
        context["notifications"].append(notification)
    if request.GET.get("no_search_result"):
        context["no_results"] = "No results were found"
    if request.user.profile.user_type == "tutor":
        students = []
        user_relationships = Relationship.objects.filter(tutor=request.user,
                                                         pending=False)
        for relationship in user_relationships:
            student_data = {
                "first_name": relationship.student.first_name,
                "last_name": relationship.student.last_name,
                "email": relationship.student.email,
                "profile_pic": relationship.student.profile.profile_pic,
                "id": relationship.student.profile.id
                }
            students.append(student_data)
        context["students"] = students
    else:
        tutors = []
        user_relationships = Relationship.objects.filter(student=request.user,
                                                         pending=False)
        for relationship in user_relationships:
            tutor_data = {
                "first_name": relationship.tutor.first_name,
                "last_name": relationship.tutor.last_name,
                "email": relationship.tutor.email,
                "profile_pic": relationship.tutor.profile.profile_pic,
                "id": relationship.tutor.profile.id,
            }
            tutors.append(tutor_data)
        context["tutors"] = tutors

    return render(request, "dashboard/choose_person.html", context)

@login_required
def schedule_lesson(request, user_id):
    """A view that handles the GET and POST request for scheduling lessons."""
    context = {
        "user_id": user_id,
        "days_of_the_week": DAYS_OF_THE_WEEK,
        "status": 500,
        "unread_notifications": len(Notification.objects.filter(
            user=request.user, unread=True)),
    }
    if request.method == "POST":
        new_lesson = Lesson()
        context = error_check_and_save_lesson(request, new_lesson, context)
        return JsonResponse(context)
    if request.method == "GET":
        context["person_to_schedule_with"] = User.objects.get(
            profile__id=context["user_id"])
        context["availabilities"] = return_availabilities(user_id)
        notifications = Notification.objects.filter(
            user=request.user).order_by("-created_on") # most recent
        context["notifications"] = []
        for notification in notifications:
            notification.time_info = get_timestamp(notification.created_on)
            notification.save()
            context["notifications"].append(notification)
    return render(request, "dashboard/schedule_lesson.html", context)

@login_required
def confirm_lesson(request, lesson_id):
    """A view that handles the POST request for confirming lessons."""
    try:
        lesson_to_confirm = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return HttpResponse(status=404)
    if (lesson_to_confirm and (lesson_to_confirm.tutor == request.user or
                               lesson_to_confirm.student == request.user)
            and request.user != lesson_to_confirm.created_by):
        person_to_schedule_with = (lesson_to_confirm.tutor if
                                   lesson_to_confirm.tutor != request.user else
                                   lesson_to_confirm.student)
        lesson_to_confirm.pending = False
        lesson_to_confirm.save()
        url = "/dashboard/agenda/"
        message = ("{} has accepted your request to schedule lesson: '{}'"
                .format(request.user.get_full_name(), lesson_to_confirm.name))
        Notification(user=person_to_schedule_with, message=message,
                     created_on=datetime.datetime.now(tz=UTC_ZONE),
                     picture=request.user.profile.profile_pic,
                     link=url).save()
    return redirect("agenda")


@login_required
def decline_lesson(request, lesson_id):
    """A view that handles the POST request for declining lessons."""
    try:
        lesson_to_delete = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return HttpResponse(status=404)
    if (lesson_to_delete and (lesson_to_delete.tutor == request.user or
                              lesson_to_delete.student == request.user)):
        person_to_schedule_with = (lesson_to_delete.tutor if
                                   lesson_to_delete.tutor != request.user else
                                   lesson_to_delete.student)
        url = "/dashboard/agenda/"
        message = ("{} has declined your request to schedule lesson: '{}'"
                    .format(request.user.get_full_name(), lesson_to_delete.name)
                   if lesson_to_delete.pending else "{} has cancelled your lesson: "
                   "'{}'".format(request.user.get_full_name(),
                                 lesson_to_delete.name))
        Notification(user=person_to_schedule_with, message=message,
                     created_on=datetime.datetime.now(tz=UTC_ZONE),
                     picture=request.user.profile.profile_pic,
                     link=url).save()
        lesson_to_delete.delete()
    return redirect("agenda")


@login_required
def reschedule_lesson(request, lesson_id):
    """A view that handles the GET and POST request for rescheduling lessons."""
    try:
        lesson_to_reschedule = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return HttpResponse(status=404)
    context = {
        "user_id": lesson_to_reschedule.student.profile.id\
        if request.user.profile.user_type == "tutor"\
        else lesson_to_reschedule.tutor.profile.id,
        "days_of_the_week": DAYS_OF_THE_WEEK,
        "status": 500
    }
    if request.method == "POST":
        context["rescheduled_lesson"] = True
        context = error_check_and_save_lesson(request, lesson_to_reschedule,
                                              context)
        return JsonResponse(context)
    if request.method == "GET":
        notifications = Notification.objects.filter(
            user=request.user).order_by("-created_on") # most recent
        context["notifications"] = []
        for notification in notifications:
            notification.time_info = get_timestamp(notification.created_on)
            notification.save()
            context["notifications"].append(notification)
        context["unread_notifications"] = len(Notification.objects.filter(
            user=request.user, unread=True))
        context["person_to_schedule_with"] = User.objects.get(
            profile__id=context["user_id"])
        if lesson_to_reschedule and (lesson_to_reschedule.tutor == request.user\
                            or lesson_to_reschedule.student == request.user):
            context["availabilities"] = return_availabilities(
                context["person_to_schedule_with"].profile.id)
            context["lesson_to_reschedule"] = {
                "name": lesson_to_reschedule.name,
                "location": lesson_to_reschedule.location,
                "start_time": lesson_to_reschedule.start_time,
                "end_time": lesson_to_reschedule.end_time,
            }
        else:
            return HttpResponse(status=404)
    return render(request, "dashboard/schedule_lesson.html", context)

# viewing MY profile will be different than viewing somebody else"s profile, hence
# a new view template and url will be set up for the feature of viewing someone else"s profile.
@login_required
def my_profile(request):
    """A view that handles the GET request for the my profile page."""
    context = {
        "user": request.user,
        "availabilities": return_availabilities(request.user.profile.id),
        "skills": return_skills(request.user.profile.id),
        "reset_email": request.GET.get("reset_email", False),
        "days_of_the_week": DAYS_OF_THE_WEEK,
        "password_change": request.GET.get("password_change", False),
        "notifications":  [],
        "unread_notifications": len(Notification.objects.filter(
            user=request.user, unread=True)),
        "blocked_people": []
    }
    blocked_people = BlockedUsers.objects.filter(user=request.user)
    for blocked_person in blocked_people:
        context["blocked_people"].append({
            "full_name": blocked_person.blocked_user.get_full_name(),
            "unblock_url": "{}dashboard/unblock/{}".format(
            request.build_absolute_uri("/"),
            str(blocked_person.blocked_user.profile.id))
        })
    notifications = Notification.objects.filter(
        user=request.user).order_by("-created_on") # most recent
    for notification in notifications:
        notification.time_info = get_timestamp(notification.created_on)
        notification.save()
        context["notifications"].append(notification)
    return render(request, "dashboard/my_profile.html", context)

@login_required
def delete_account(request):
    """A view that handles the DELETE request for deleting an account."""
    if request.method == "DELETE":
        user_to_delete = request.user
        user_to_delete.delete()
    return HttpResponse(status=200)

@login_required
def change_password(request):
    """A view that handles the POST request for changing a user"s password."""
    if request.method == "POST":
        data = {
            "status_code": 400
        }
        current_user = request.user
        if SocialAccount.objects.filter(user_id=current_user).exists():
            data["social_error"] = ("You are using a social account so "
                                    "you can't change your password.")
            return JsonResponse(data)
        old_password = request.POST.get("old_password", "")
        new_password1 = request.POST.get("new_password1", "")
        new_password2 = request.POST.get("new_password2", "")
        if not old_password or not new_password1 or not new_password2:
            data["missing_field"] = "Please fill in a missing field."
            return JsonResponse(data)
        if not current_user.check_password(old_password):
            data["invalid_old_password"] = ("Your old password is wrong, please "
                                            "try again.")
            return JsonResponse(data)
        if new_password1 != new_password2:
            data["inequal_password"] = "Your new passwords do not match."
            return JsonResponse(data)

        current_user.set_password(new_password1)
        current_user.save()
        data["status_code"] = 200
        return JsonResponse(data)
    return HttpResponse(status=403)

@login_required
def edit_profile(request):
    """A view that handles the GET and POST request for the edit profile page.
    """
    context = {
        "notifications": [],
        "unread_notifications": len(Notification.objects.filter(
            user=request.user, unread=True)),
        "skills": []
        }
    notifications = Notification.objects.filter(
        user=request.user).order_by("-created_on") # most recent
    for notification in notifications:
        notification.time_info = get_timestamp(notification.created_on)
        notification.save()
        context["notifications"].append(notification)
    if request.method == "POST":
        if "profile_pic" in request.POST:
            cropped_img = request.POST["profile_pic"]
            format_img, imgstr = cropped_img.split(";base64,")
            ext = format_img.split("/")[-1]
            cropped_img = ContentFile(base64.b64decode(imgstr),
                                      name="temp." + ext)
            request.user.profile.profile_pic = cropped_img
            request.user.save()
            return HttpResponse(status=200)
        request.user.first_name = request.POST["firstName"]
        if not request.POST["lastName"]:
            request.user.last_name = " "
        else:
            request.user.last_name = request.POST["lastName"]
        request.user.profile.bio = request.POST["bio"]
        # then handle email
        email = request.POST["email"]
        skills = request.POST.getlist("tags")
        Skill.objects.filter(profile=request.user.profile).delete()
        for skill in skills:
            Skill(profile=request.user.profile, skill=skill).save()
        if not email == request.user.email:
            # send a mail
            request.user.email = email
            request.user.profile.email_verified = False
            user_id = request.user.profile.id
            url = "{}accounts/verify_email/{}".format(
                request.build_absolute_uri("/"), user_id)
            with get_connection(host=EMAIL_HOST, port=EMAIL_PORT,
                                username=VERIFY_USER_EMAIL,
                                password=EMAIL_HOST_PASSWORD,
                                use_tls=True,
                                ) as connection:
                EmailMessage("Schedulearn - Verify Your Email Address",
                             "Click on the following link to verify your"
                             " email address\n\n" + url,
                             VERIFY_USER_EMAIL,
                             [email],
                             connection=connection).send()
            request.user.save()
            response = redirect("my_profile")
            response["Location"] += "?reset_email=True"
            return response
        request.user.save()
        return redirect("my_profile")
    if request.method == "GET":
        skills_db = Skill.objects.filter(profile=request.user.profile)
        for skill in skills_db:
            context["skills"].append(skill.skill)
    return render(request, "dashboard/edit_profile.html", context)

@login_required
def edit_availability(request):
    """A view that handles the GET and POST request for the edit availability
       page.
    """
    context = {"days_of_the_week": DAYS_OF_THE_WEEK,
               "day": request.POST.get("day", ""),
               "start_time": request.POST.get("startingTime", ""),
               "end_time": request.POST.get("endingTime", ""),
               "status": 500}
    if request.method == "POST":
        date = get_date_from_day(context["day"]).date()
        time_difference = datetime.timezone(datetime.timedelta(
            minutes=int(request.POST.get("timezoneInfo", ""))))
        context["starting_time_error"] = False if context["start_time"]\
                                                else True
        context["ending_time_error"] = False if context["end_time"] else True
        if (context.get("ending_time_error")
                or context.get("starting_time_error")):
            return JsonResponse(context)
        start_time_naive = datetime.datetime.strptime(
            request.POST["startingTime"], "%I:%M %p").time()
        end_time_naive = datetime.datetime.strptime(
            request.POST["endingTime"], "%I:%M %p").time()
        start_time = datetime.datetime.combine(date, start_time_naive,
                                               time_difference)
        end_time = datetime.datetime.combine(date, end_time_naive,
                                             time_difference)
        if start_time > end_time:
            context["time_error"] = ("The starting time provided is greater "
                                     "than the end time. Please fix this.")
            return JsonResponse(context)
        existing_availabilities = Availability.objects.filter(
            profile__id=request.user.profile.id, day=context["day"])
        for availability in existing_availabilities:
            existing_start_time = availability.start_time
            existing_end_time = availability.end_time
            if (existing_start_time < end_time)\
                    and (existing_end_time > start_time):
                context["time_error"] = ("The timings you provided overlap "
                                         "with other timings that you have set")
                return JsonResponse(context)
        # If timings aren"t overlapping, add availability to database.
        new_availability = Availability()
        new_availability.profile = request.user.profile
        new_availability.start_time = start_time.astimezone(UTC_ZONE)
        new_availability.end_time = end_time.astimezone(UTC_ZONE)
        new_availability.day = context["day"]
        new_availability.save()
        context["status"] = 200
        return JsonResponse(context)
    if request.method == "GET":
        context["availabilities"] = return_availabilities(
            request.user.profile.id)
        notifications = Notification.objects.filter(
            user=request.user).order_by("-created_on") # most recent
        context["notifications"] = []
        for notification in notifications:
            notification.time_info = get_timestamp(notification.created_on)
            notification.save()
            context["notifications"].append(notification)
        context["unread_notifications"] = len(Notification.objects.filter(
            user=request.user, unread=True))
    return render(request, "dashboard/edit_availability.html", context)

@login_required
def delete_availability(request, availability_id):
    """A view that handles the POST request to delete an availability."""
    try:
        delete_day = Availability.objects.get(
            profile__id=request.user.profile.id, id=availability_id)
    except Availability.DoesNotExist:
        return HttpResponse(status=404)
    delete_day.delete()
    return redirect("edit_availability")

@login_required
def clear_notifications(request):
    """A view that handles the POST request to clear notifications."""
    notifications = Notification.objects.filter(user=request.user, unread=True)
    for notification in notifications:
        notification.unread = False
        notification.save()
    return HttpResponse(status=200)

@login_required
def block_user(request, user_id):
    """This view will grab all connection between the request user and
    the user with the parameter and delete them. (e.g. lessons, relationship)"""
    try:
        user_to_be_blocked = User.objects.get(profile__id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    if user_to_be_blocked == request.user:
        return HttpResponse(status=400)
    try:
        BlockedUsers.objects.get(user=request.user,
                                 blocked_user=user_to_be_blocked)
    except BlockedUsers.DoesNotExist:
        BlockedUsers(user=request.user, blocked_user=user_to_be_blocked).save()
        Lesson.objects.filter(tutor=request.user,
                              student=user_to_be_blocked).delete()
        Lesson.objects.filter(student=request.user,
                              tutor=user_to_be_blocked).delete()
        Relationship.objects.filter(tutor=request.user,
                              student=user_to_be_blocked).delete()
        Relationship.objects.filter(student=request.user,
                              tutor=user_to_be_blocked).delete()
    return redirect(public_profile, user_id=user_id)

@login_required
def unblock_user(request, user_id):
    try:
        user = User.objects.get(profile__id=user_id)
    except:
        return HttpResponse(status=404)
    try:
        BlockedUsers.objects.get(user=request.user, blocked_user=user).delete()
    except BlockedUsers.DoesNotExist:
        return HttpResponse(status=404)
    return redirect(public_profile, user_id=user_id)

# Helper Functions

def error_check_and_save_lesson(request, lesson, context):
    """A helper function that helps the scheduling and rescheduling views in
       error checking the POST data.
    """
    person_to_schedule_with = User.objects.get(profile__id=context["user_id"])
    rel_exists = relationship_exists(person_to_schedule_with, request.user)
    blocking_relationship = []
    blocking_relationship.append(
        BlockedUsers.objects.filter(user=request.user,
                                    blocked_user=person_to_schedule_with))
    blocking_relationship.append(
        BlockedUsers.objects.filter(user=person_to_schedule_with,
                                    blocked_user=request.user))
    if blocking_relationship:
        context['no_blocking_error'] = False
    if rel_exists:
        try:
            relationship = Relationship.objects.get(
                tutor=person_to_schedule_with, student=request.user)
        except Relationship.DoesNotExist:
            relationship = Relationship.objects.get(
                tutor=request.user, student=person_to_schedule_with)
        if relationship.pending:
            context["pending_relationship_error"] = True
    else:
        context["no_relationship_error"] = True
    # Get lesson timezone when (re)scheduling lessons
    time_difference = datetime.timezone(datetime.timedelta(minutes=int(
        request.POST.get("timezoneInfo", ""))))
    # Get lesson name when (re)scheduling lessons
    if not request.POST["name"]:
        context["no_name_error"] = True
    else:
        lesson.name = request.POST["name"]
        context["lesson_name"] = request.POST["name"]
    # Get lesson location when (re)scheduling lessons
    if not request.POST["location"]:
        context["no_location_error"] = True
    else:
        lesson.location = request.POST["location"]
    # Get lesson date when (re)scheduling lessons
    if not request.POST["date"]:
        context["no_date_error"] = True
    else:
        date = datetime.datetime.strptime(request.POST["date"],
                                          "%m/%d/%Y").date() # a date object.
    # Get lesson starting time when (re)scheduling lessons
    if not request.POST["startingTime"]:
        context["no_starting_time_error"] = True
    else:
        start_time = datetime.datetime.strptime(request.POST["startingTime"],
                                                "%I:%M %p").time()
    # Get lesson ending time when (re)scheduling lessons
    if not request.POST["endingTime"]:
        context["no_ending_time_error"] = True
    else:
        end_time = datetime.datetime.strptime(request.POST["endingTime"],
                                              "%I:%M %p").time()
    if start_time > end_time:
        context["bigger_start_time_error"] = (
            "The starting time provided is greater than the end time."
            " Please fix this.")
    lesson.tutor = request.user\
                            if request.user.profile.user_type == "tutor"\
                            else person_to_schedule_with
    lesson.student = request.user\
                                if request.user.profile.user_type == "student"\
                                else person_to_schedule_with

    if (not context.get("no_name_error") and not
            context.get("no_location_error") and not
            context.get("no_date_error") and not
            context.get("no_starting_time_error") and not
            context.get("no_ending_time_error") and not
            context.get("bigger_start_time_error") and not
            context.get("pending_relationship_error") and not
            context.get("no_relationship_error") and not
            context.get("")):
        start_time_in_local_time = datetime.datetime.combine(date, start_time,
                                                             time_difference)
        if start_time_in_local_time < datetime.datetime.now(tz=time_difference):
            context["past_lesson_error"] = (
                "Fix starting time or date of lesson to make sure it's after "
                "current time.")
            return context
        context["status"] = 200
        end_time_in_local_time = datetime.datetime.combine(date, end_time,
                                                           time_difference)
        lesson.start_time = start_time_in_local_time.astimezone(UTC_ZONE)
        lesson.end_time = end_time_in_local_time.astimezone(UTC_ZONE)
        lesson.created_by = request.user
        lesson.save()
        url = "/dashboard/agenda/"
        message = "{} has rescheduled the lesson: {}".format(request.user.\
            get_full_name(), lesson.name) if context.get(
                "rescheduled_lesson", False) else "{} has requested to schedule\
                lesson '{}' with you.".format(request.user.get_full_name(),
                                              lesson.name)
        Notification(user=person_to_schedule_with, message=message,
                     created_on=datetime.datetime.now(tz=UTC_ZONE),
                     picture=request.user.profile.profile_pic,
                     link=url).save()
        context["schedule_success"] = (
            "Your Lesson '" + lesson.name + "' Was Scheduled Successfully.")
    return context

def get_date_from_day(day):
    """Takes in a string paramater corresponding to a day of the weekself.
       Returns a datetime object corresponding to that day.
    """
    if day.lower() == "monday":
        return datetime.datetime(2018, 7, 30)
    if day.lower() == "tuesday":
        return datetime.datetime(2018, 7, 31)
    if day.lower() == "wednesday":
        return datetime.datetime(2018, 8, 1)
    if day.lower() == "thursday":
        return datetime.datetime(2018, 8, 2)
    if day.lower() == "friday":
        return datetime.datetime(2018, 8, 3)
    if day.lower() == "saturday":
        return datetime.datetime(2018, 8, 4)
    return datetime.datetime(2018, 8, 5)

def relationship_exists(person_one, person_two):
    """Takes in 2 users and returns a boolearn corresponding to whether they are
       in a relationship or not.
    """
    try:
        Relationship.objects.get(student=person_one, tutor=person_two)
        return True
    except Relationship.DoesNotExist:
        try:
            Relationship.objects.get(student=person_two, tutor=person_one)
            return True
        except Relationship.DoesNotExist:
            return False

# Will return a list of availabilities (dictionary) of the profile id,
# sorted by order Monday To Sunday.
def return_availabilities(user_id):
    """A helper function that returns a list of the availabilities of a user
    given the user"s id.
    """
    availabilities = []
    for day in DAYS_OF_THE_WEEK:
        availabilities_in_day = Availability.objects.filter(profile__id=user_id,
                                                            day=day)
        if availabilities_in_day:
            for availability_in_day in availabilities_in_day:
                availabilities.append(availability_in_day)

    return availabilities

def return_skills(user_id):
    """A helper function that returns a list of the skills of a user given the
    user"s id.
    """
    skills = []
    skills_db = Skill.objects.filter(profile__id=user_id)
    for skill in skills_db:
        skills.append(skill.skill)
    return skills

def get_timestamp(time_of_notification):
    """A helper function that returns a list of the skills of a user given the
    user"s id.
    """
    time_difference = datetime.datetime.now(datetime.timezone.utc) - time_of_notification
    time_in_seconds = int(time_difference.total_seconds())
    time_in_minutes = int(time_in_seconds / 60)
    time_in_hours = int(time_in_minutes / 60)
    time_in_days = int(time_in_hours / 24)
    time_in_months = int(time_in_days / 30)
    time_in_years = int(time_in_months / 12)
    if time_in_seconds < 60: # less than a minute ago.
        return "Less than a minute ago"
    elif time_in_minutes < 60: # less than an hour
        if time_in_minutes == 1:
            return (str(time_in_minutes) + " minute ago")
        return (str(time_in_minutes) + " minutes ago")
    elif time_in_hours < 24: # less than 24 hour
        if time_in_hours == 1:
            return (str(time_in_hours) + " hour ago")
        return (str(time_in_hours) + " hours ago")
    elif time_in_days < 30: # less than 30 days
        if time_in_days == 1:
            return (str(time_in_days) + " day ago")
        return (str(time_in_days) + " days ago")
    elif time_in_months < 12: # less than 12 months
        if time_in_months == 1:
            return (str(time_in_months) + " month ago")
        return (str(time_in_months) + " months ago")
    else:
        if time_in_years == 1:
            return (str(time_in_years) + " year ago")
        return (str(time_in_years) + " years ago")
