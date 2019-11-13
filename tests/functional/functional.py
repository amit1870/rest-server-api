#!/usr/bin/env python3
# pylint: disable=invalid-name,too-few-public-methods,E1101
''' This modules is for functional testing of api '''

import json
import random
from faker import Faker

from locust import HttpLocust, TaskSet, task
import payloads

faker = Faker()



class Student(TaskSet):
    '''
    This Taskset class with add a new student with its IN and OUT record.
    After inserting IN and OUT record for the student, fetch timesheet.
    '''

    @task
    def add_new_student(self):
        ''' add new student '''
        payload = payloads.STUDENT_PAYLOAD
        payload['firstName'] = faker.first_name()
        payload['middleName'] = faker.first_name()
        payload['lastName'] = faker.first_name()
        payload['lastName'] = faker.first_name()
        payload['dob'] = faker.date(pattern="%Y-%m-%d", end_datetime=None)
        payload['class'] = str(random.choice([9, 10, 11, 12]))
        payload['section'] = str(random.choice(['A', 'B', 'C', 'D', 'E']))
        payload['dateOfJoining'] = faker.date(pattern="%Y-%m-%d")
        payload['gender'] = random.choice(['Male', 'Female', 'Other'])
        payload['category'] = random.choice(['General', 'OBC', 'SC', 'ST', 'OBC-NCL'])
        payload['nationality'] = random.choice(['Bharat', 'Pak', 'Bangla', 'Bhutan'])

        response = self.client.post("http://172.30.76.214/student", json=payload)
        if response.status_code == 201:
            response = json.loads(response.text)
            student_id = response['username']
            response = self.get_student_details(student_id)
            if response.status_code == 200:
                print("Student details %s " % json.loads(response.text))
            response = self.add_in_out_record(student_id)
            response = self.add_in_out_record(student_id)
            response = self.add_in_out_record(student_id)
            response = self.add_in_out_record(student_id)
            if response.status_code == 200:
                response = self.get_timesheet_for_student(student_id)
                if response.status_code == 200:
                    print("Student timesheet %s " % json.loads(response.text))
                else:
                    print(response, response.text)
            else:
                print(response, response.text)
        else:
            print(response, response.text)

    def get_timesheet_for_student(self, student_id):
        ''' get timesheet for student '''
        response = self.client.get(
            "http://172.30.76.214/student/{}/timesheet?startDate=2019-08-01&endDate=2019-09-04"
            .format(student_id))
        return response

    def get_student_details(self, student_id):
        ''' get details of student '''
        response = self.client.get("http://172.30.76.214/student/{}".format(student_id))
        return response

    def add_in_out_record(self, handle):
        ''' This function will insert IN and OUT record. '''
        in_month = random.choice([8, 9])
        in_day = random.choice(range(1, 30))
        hour = random.choice(['06', '07', '08', '09'])
        payload = {
            "id": handle,
            "inout": "IN",
            "source": "CAM",
            "source_id": 100010000001,
            "timestamp": "2019-{}-{}T{}:00:56.044Z".format(in_month, in_day, hour)
        }
        response = self.client.post(
            "http://172.30.76.214/edgeDevice/recordAttendance",
            json=payload
        )
        if response.status_code == 200:
            hour = random.choice(['15', '16', '18', '19'])
            payload = {
                "id": handle,
                "inout": "OUT",
                "source": "CAM",
                "source_id": 100010000001,
                "timestamp": "2019-{}-{}T{}:00:56.044Z".format(in_month, in_day, hour)
            }
            response = self.client.post(
                "http://172.30.76.214/edgeDevice/recordAttendance",
                json=payload
            )
            return response
        return response


class Employee(TaskSet):
    '''
    This Taskset class with add a new employee with its IN and OUT record.
    After inserting IN and OUT record for the employee, fetch timesheet.
    '''

    @task
    def add_new_employee(self):
        ''' add new employee '''
        payload = payloads.EMPLOYEE_PAYLOAD
        payload['firstName'] = faker.first_name()
        payload['middleName'] = faker.first_name()
        payload['lastName'] = faker.first_name()
        payload['lastName'] = faker.first_name()
        payload['dob'] = faker.date(pattern="%Y-%m-%d", end_datetime=None)
        payload['dateOfJoining'] = faker.date(pattern="%Y-%m-%d")
        payload['gender'] = random.choice(['Male', 'Female', 'Other'])
        payload['category'] = random.choice(['General', 'OBC', 'SC', 'ST', 'OBC-NCL'])
        payload['nationality'] = random.choice(['Bharat', 'Pak', 'Bangla', 'Bhutan'])
        payload['role'] = random.choice(['Teacher', 'Admin', 'Principal', 'Security'])

        response = self.client.post("http://172.30.76.214/employee", json=payload)
        if response.status_code == 201:
            response = json.loads(response.text)
            employee_id = response['username']
            response = self.get_employee_details(employee_id)
            if response.status_code == 200:
                print("Employee details %s " % json.loads(response.text))
            response = self.add_in_out_record(employee_id)
            response = self.add_in_out_record(employee_id)
            response = self.add_in_out_record(employee_id)
            response = self.add_in_out_record(employee_id)
            if response.status_code == 200:
                response = self.get_timesheet_for_employee(employee_id)
                if response.status_code == 200:
                    print("Employee timesheet %s " % json.loads(response.text))
                else:
                    print(response, response.text)
            else:
                print(response, response.text)
        else:
            print(response, response.text)

    def get_timesheet_for_employee(self, employee_id):
        ''' get timesheet for employee '''
        response = self.client.get(
            "http://172.30.76.214/employee/{}/timesheet?startDate=2019-08-01&endDate=2019-09-04"
            .format(employee_id))
        return response

    def get_employee_details(self, employee_id):
        ''' get details of employee '''
        response = self.client.get("http://172.30.76.214/employee/{}".format(employee_id))
        return response

    def add_in_out_record(self, handle):
        ''' This function will insert IN and OUT record. '''
        in_month = random.choice([8, 9])
        in_day = random.choice(range(1, 30))
        hour = random.choice(['06', '07', '08', '09'])
        payload = {
            "id": handle,
            "inout": "IN",
            "source": "CAM",
            "source_id": 100010000001,
            "timestamp": "2019-{}-{}T{}:00:56.044Z".format(in_month, in_day, hour)
        }
        response = self.client.post(
            "http://172.30.76.214/edgeDevice/recordAttendance",
            json=payload
        )
        if response.status_code == 200:
            hour = random.choice(['15', '16', '18', '19'])
            payload = {
                "id": handle,
                "inout": "OUT",
                "source": "CAM",
                "source_id": 100010000001,
                "timestamp": "2019-{}-{}T{}:00:56.044Z".format(in_month, in_day, hour)
            }
            response = self.client.post(
                "http://172.30.76.214/edgeDevice/recordAttendance",
                json=payload
            )
            return response
        return response



class UserBehaviour(TaskSet):
    ''' Swarm User Behaviour '''
    tasks = {Student:1, Employee:2}

class WebsiteUser(HttpLocust):
    ''' WebsiteUser '''
    task_set = UserBehaviour
    weight = 1
    min_wait = 1000
    max_wait = 1000
