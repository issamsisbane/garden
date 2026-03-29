---
title: "Clippy"
description: "A web platform allowing for the ephemeral sharing of information, following the model of Pastebin."
lang: "en"
pubDate: "Feb 15 2024"
heroImage: "/portfolio/projects/clippy/clippy.jpg"
badge: "PERSONAL"
tags: ["Cloud", "Azure", "Nuxt", "CosmosDB", "Typescript"]
---

## **Links**
The project is available via GitHub:
* [Front-end](https://github.com/IssamSisbane/clippy-frontend)
* [Back-end](https://github.com/IssamSisbane/clippy-backend)

[The hosted version](https://clippy.snzprojects.tech/)

## **Need**
This project was conducted during my free time for my personal needs. I often found myself in need of a platform to quickly and easily copy and paste information between two devices. When using two devices that belong to me, such as my phone and PC, I would use a private Discord server as a clipboard. However, sometimes one of the devices did not belong to me, so I could not use this method. There are alternatives on the market in the form of websites, but the generated URLs are quite cumbersome and impractical to manually copy and paste into a browser.

## **Objectives**
Thus, the objective of this project is to create a website that allows for the ephemeral sharing of information via simple URLs for copying and pasting.

## **Methodology**
I started by defining what I wanted in my application, then I created a schema of the architecture I would implement. Finally, I began coding and iterating on this code as I went along.

## **Technologies Used**
Backend:
* `Azure`
* `Azure Function`
* `Azure Blob Storage`
* `CosmosDB`
* `Azure Key Vault`
* `Typescript`

Frontend:
* `Nuxt`
* `Nuxt-ui`
* `Typescript`

## **Architecture**
![clippy-architecture](/portfolio/clippy/clippy-architecture.webp)

## **Results**
Having some experience with Azure technologies and JavaScript, this project was relatively straightforward to set up and use. Ultimately, it is possible to create a 'clip' that can be either text or a file. It is also possible to decide the validity period of the clip. After creation, a path for the clip is generated, which corresponds to an animal name. Thus, you just need to type the site's URL followed by the clip's path to access it. Deletion occurs automatically every day, and access to the clip is denied if the validity period has expired but it has not yet been deleted.

## **Possible Improvements**
The project is functional, but there is still room for improvement. Indeed, it would be necessary to implement a more robust security for files, add a verification to ensure they are of acceptable size, and above all, without risks.

Furthermore, the interface can still be greatly improved, especially in terms of responsiveness.

Finally, We could add some tests.

## **Conclusion**
I enjoyed this project because I was able to work with technologies that I particularly enjoy. Additionally, I was able to utilize many skills that I have acquired within the same project.

