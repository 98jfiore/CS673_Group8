# CS673_Group8

## Team 8: Patient Communication Mobile App

Roster
* Joseph Fiore - Microserverices Developer
* Calin Blauth - Data Architect
* David Amajor - Quality & Dev Ops
* Kadiri Venkata Thorannath - UI/UX Developer

### Far Vision

We will design an application for healthcare patients who want a way to access their healthcare information on the go.
The Patient Communication Mobile App is a mobile based application that allows the patient to track their appointments, message their doctor, check their account information, and alert them of upcoming appointments.
Unlike other mobile healthcare applications like MyChart our product displays all the necessary information in a single place that is clean and easy to navigate, all at the touch of a finger.

### Near Vision as of 9/22/2021

We will work together with the other teams to get an application to display basic patient and appointment information with UI that doesn't clash with the web version, which could confuse customers.

### Stakeholders

#### Stakeholder Types
Patients who need access to their healthcare information and appointments when they are on the go.
Doctors/Nurses who need a way to ensure their patients are getting proper care and access.
Our Company who will benefit from expanding our customer base to those who prefer to have healthcare information on hand at all times.

#### Real Stakeholder

Jane Doe <br>
A 35 year old single-mother of two living in Cranford, New Jersey.  She is very busy balancing her life, career, and kids, and strugles remembering all of her healthcare information and appointment times/dates. <br>
She has tried other applications, but they haven't been as useful as she wants.  She's not particularly tech savy, so the more complicated portals have been a nightmare to navigate.  Others have not included all of the features she wanted so she had to use multiple at once.  Additionally, she gets nervous about her children's health and finds getting in contact with their doctors difficult.

### Backlog

Tracker: https://www.pivotaltracker.com/projects/2532883

#### Backlog Items (From the Pivotal Tracker)

Display of Healthcare Account Information <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a patient I want to be able to view my information through the mobile application so that I can view information relevant to my account such as my username, account number, and account details at any time.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Basic information about the user (username, account number, etc.) is displayed on an application.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 1<br>
<br>
Coordinate With Other Teams to Develop A Consistent UI <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user I want to easily navigate my account, schedule, and messages on both my computer and application so that my experience is more consistent and less confusing.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Discussions are held with other teams to ensure that our UI is consistent with theirs.  Additionally, we will make sure all the UI works on our application.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 3<br>
<br>
Display Insurance Information <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to quickly view my insurance information, so that I can reference when either paying bills, or when discussing my healthcare with my doctor or provider.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: To ensure the UI is working, we will start displaying more complex information, namely the user's insurance information. Additionally, this will help us build up functionality.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 1<br>
<br>
Send Messages to Doctor <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to get in touch with a doctor or nurse quickly, so that I can ask them questions about perscriptions, upcoming appointments, or anything else related to my health needs. <br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Messages can be sent from the patient using the application to their doctor.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 3<br>
<br>
Store Messages From User and Doctor <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to view messages with my doctor, both old and new, so that I can come to a better understanding of my healthcare over time.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Messages sent to or from the user, via the application, are retained between sessions.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 1<br>
<br>
View Messages From Doctor <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to view the messages that my physician has sent to me, so that I can understand the state of my care.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Users can view messages from their doctors in order to receive information from their doctors (instead of just giving it).<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 2<br>
<br>
Notifications for New Messages <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to get updates when I get new messages, so that I do not miss them, and so that I am able to respond in time.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Notifications are given to the user alerting them of messages to make this messaging work similar to other services.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 1<br>
<br>
Display Appointment Information <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to view all of my future appointments (with information such as the doctor I'll be seeing, when, and where) so that I can make sure not to miss them and so that I don't make conflicting appointments.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: The UI is expanded to include information about appointments as our functionality expands.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 2<br>
<br>
Notifications for Appointments <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to receive notifications based on upcoming appointment times, so that I'm reminded of appointments and don't miss them.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: Just as with message notifications, we will make the appointments more useful by ensuring patients are alerted about upcoming ones.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 1<br>
<br>
Display Visual Representation of Appointments <br>
&nbsp;&nbsp;&nbsp;&nbsp;User Story: As a user, I want to be able to view my appointment schedule in a calendar format, so that I can easily understand my upcoming appointments and when they will occur. <br>
&nbsp;&nbsp;&nbsp;&nbsp;Details: We will display information about appointments in a more visually clear way (likely in the form of a calendar) to make it easier to use.<br>
&nbsp;&nbsp;&nbsp;&nbsp;Story Points: 2<br>
<br>

#### Backlog Order Reasoning

1.  We first want to test our access to our backend and ability to display it in the front end.
2.  Once the former has been established, we want to develop the UI for the rest of the mobile application.
3.  Once the UI is developed, we will add the ability to access insurance information to test that UI and begin expanding it.
4.  We would like to be able to send messages to doctors, a core feature we want to complete as soon as possible.
5.  We want to make sure we can access, store, and retrieve messages, so that they can be archived for future reference.  This is key to why messages are so important for our app.
6.  This is another core feature for our userbase that we want to implement as soon as we are sure we are properly connected to the message backend.
7.  We want to add message notifications now to put a final finishing touch on the messages part of the application.
8.  Once we have developed messages, we want to move onto our other central feature: meeting information.
9.  This will help us round off the appointments feature and utilize information we learned while developing the messages component.
10.  This will be our way of finishing the appointment feature for the userbase by making it more usable.

### Estimating Activity

Relative Estimation:  Did a call, estimating how long each backlog item would take by comparing them to past work we've done on various other projects.
