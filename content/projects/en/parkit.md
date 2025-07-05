---
title: "Park IT !"
description: "The Park It! project is an innovative IoT solution aimed at simplifying parking. With smart sensors and a user-friendly application, it provides an optimized parking experience."
lang: "en"
pubDate: "Jan 24 2024"
heroImage: "/portfolio/projects/parkit/parkit_img.webp"
badge: "ACADEMIC"
tags: ["Arduino", "FreeRtos", "Express", "TypeScript", "React Native"]
selected: true
---
## **Liens**
* [The project API](https://github.com/IssamSisbane/parkit-api)

## **Description**

The Parking Connect project, also known as "Park It!", is an innovative solution aimed at addressing the challenges of urban parking in bustling metropolises. It leverages the Internet of Things (IoT) to create a smart parking system that enhances the parking experience for both drivers and parking lot operators.

## **Objectives**

The primary goal of the project is to design and develop a connected parking solution that optimizes parking space utilization and provides real-time parking availability information to users. Additionally, the project aims to streamline the reservation process, enhance user experience through a mobile application, and integrate various IoT technologies for seamless operation.

## **Methodology**

This project was realised in group with two other students. I was in charged of the backend and communications. The project follows a comprehensive approach, beginning with conceptualization and design, followed by development and implementation. The team adopted an iterative methodology, allowing for continuous refinement and adaptation to challenges encountered during the project lifecycle. Collaboration and communication among team members were essential for effective project management and problem-solving.

## **Technology Used**:

The Parking Connect project utilizes a range of technologies to achieve its objectives:

* `React Native`: for developing the mobile application interface.
* `Node.js & Express.js`: for building the API backend.
* `MongoDB`: for storing and managing parking-related data.
* `FreeRTOS & ESP32`: for the microcontroller-based IoT infrastructure.
* `MQTT Protocol`: for communication between API and ESP32 devices.
* `Expo`: for streamlined development and deployment of the mobile application.
* `Swagger/OpenAPI`: for documenting and defining API endpoints.
* Various dependencies for frontend, backend, and IoT components.

## **Architecture**

The architecture of the Parking Connect system comprises three main components:

**Mobile Application:** Developed using React Native and Expo, the mobile app provides users with features such as parking reservation, real-time availability, and account management.

**API Backend:** Built with Node.js and Express.js, the API serves as the intermediary between the mobile app and the database. It handles requests, communicates with the MongoDB database, and interacts with the ESP32 devices via MQTT.

**IoT Infrastructure:** Implemented using FreeRTOS and ESP32 microcontrollers, the IoT infrastructure includes sensors, actuators, and communication modules deployed in physical parking spaces. These devices interact with the API to provide real-time data and control parking operations.

## **Results**

The project successfully delivered a proof of concept demonstrating the core functionalities of the smart parking system. Users can access real-time parking availability information, make reservations through the mobile application, and interact with the physical parking infrastructure. Despite hardware and budget constraints, the project achieved its primary objectives and laid the foundation for future enhancements and scalability.

## **Improvements**

As students, we had hardware and budget constraints for this project. Despite this, we achieved a satisfactory proof of concept. However, some aspects could be improved.

Firstly, the design could have been more realistic, but we were limited by the available hardware.

Secondly, an administrator's intervention is required to set up the parking, which could be simplified with a dedicated web interface.

We also added a statistics system, but a specific interface for parking owners would have been preferable, offering customizable graphs for entries, reservations, and parking space occupancy.

Finally, We could add some tests.


## **Conclusion**

The Parking Connect project represents a successful integration of IoT, mobile application development, and backend infrastructure to address urban parking challenges. Despite constraints, the project delivered a functional solution that enhances parking convenience and efficiency. Moving forward, there is potential for further enhancements, including administrative tools, user experience improvements, and scalability for larger deployments.