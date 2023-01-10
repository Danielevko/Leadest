# Leadest

Most organizations from the automotive and leasing industry (private companies to large organizations) make the sale of car rentals done in an outdated method.
An outdated method means that when a person or company are interested in a car rental service - they fill their details on the leasing company website, Company’s Social Networks, or contact the leasing company by phone. Then, the various salespeople contact those potential customers in the FIFO method (First In- First Out) to convert the lead to a sale. 
As a result of recognizing this uncomfortable and inefficient method leasing companies use, a recommendation system has been developed in this project. 
With the recommendation system, the aim is to rank the leads and define those with the highest probability of converting into actual sales while simplifying the salesperson's job and increasing the company's profit. 
In addition, the system displays a dynamic dashboard that contains graphs that help analyze the leads and sales so that branch managers can have more meaningful insights into the leads' distribution and characterize the most significant parameters of the ones that are turning into actual sales.
Our project has the advantage of utilizing two different types of machine learning methods: supervised and unsupervised learning.
After registering on the site, the user uploads a leads file. The data file received from the user undergoes several processes: data preparation, filtering, and data processing. At the end of the process, the algorithm from the unsupervised learning is activated and divides the data into four groups: hot, high, medium, and low.
The second time the user uses the system, and the leasing company has used a group's division file to make a sale, algorithms from the supervised learning family are activated which learn which leads have converted to a sale. Finally, the algorithm with the highest accuracy will be maintained in the user's cloud. 
In the third and final stage, the system classifies a file according to supervised learning. It predicts which leads have the most appropriate characteristics to be converted to an actual sale. For the system to be interactive, at each stage, the user receives an email to the email address documented during the registration, and the files are stored in the user's dedicated cloud while using Google's API.
This document summarizes the final project and contains a weighting of the SOW document and the midterm report written during the construction of the system which contained the characterization, planning, and definition of the system.
As a result of reviewing the existing worldwide situation, focusing on Israel, and defining stakeholders, we were able to determine the project's goals, objectives, and metrics. By defining all those metrics, we were able to decide on the best option for establishing the system - an independent development using free programming packages in Python code, while also adjusting the functional requirements, time, and budget for the project. The literature has made it possible to dive deeper into the diverse alternatives in the world of programming to build the system and site. We discovered different methods and noticed that Python is also 

considered a leading actor in the Data Science world that obtains many machine learning capabilities.
Finally, we concluded that the combined tools of Python as a programming language for both developing the website and writing the algorithms while using the integration of object-oriented programming are the best solutions for a dynamic system that can provide all the user inquiries. 
The database used is SQLite, and client-side development languages were combined with Python, HTML, CSS, and JavaScript along with the Bootstrap and Flask libraries. The system used a built-in lead file for its creation, we used the Data Generator by employing conditions that simulate the real world of leasing.
The future developments that we anticipate for the system are the improvement of the supervised learning algorithm which reached an accuracy of 83% during our tests.
This document details the system's design with documentation of verbal explanations, diagrams, tables, and the system's different processes.
