---
title: "Speechy"
description: "The Speechy project allows recording voice and transcribing what was said as well as summarizing with key points covered."
pubDate: "Apr 22, 2024"
lang: "en"
heroImage: "/portfolio/projects/speechy/speechy.webp"
badge: "PERSONAL"
tags: ["Azure", "AI", "LLM", "Nuxt", "TypeScript"]
---

This project is still under development.

## Links
The project is available on GitHub:
* [Front-end](https://github.com/IssamSisbane/speechy-frontend)
* [Back-end](https://github.com/IssamSisbane/speechy-backend)

[View the hosted version](https://speechy.snzprojects.tech/)

## Need
This project was carried out during my free time for my own needs. During my alternating studies, I discovered a very important element in my work: **note-taking**. Indeed, as a student alternating between school and work, I had long periods without school and conversely long periods without work. Thus, when I returned to school or work, I quickly realized that it was impossible to remember everything I had done and what I was working on.

So, I started **taking notes** and **documenting** everything I did and learned, whether at school or at work. I started using Google Docs and then switched to Notion, which I still use. However, after a few years, I realized that when I finished a meeting, for example, and formatted my notes, I omitted some things because I wanted to both expand and rephrase my notes. So, I lost some information.

Then one day, I tried an online tool that allowed **transcription** of what I said, and this allowed me to not omit anything from the meeting I had just had. Moreover, I found this way of working useful when I was thinking about a project, for example. That being said, I needed a **personal platform** to do this and connect it to my notion (where I keep all my written traces).

## Objectives
The objective is therefore to create a website that allows transcription of voice recording and provides a summary as well as the key points of this recording.

Another objective was to use AI in a real project to discover the power of these tools.

## Methodology
I started by developing a POC that works, and I will improve it as I need.

## Technologies Used
I am still in full reflection. Indeed, I started a **POC** using Whisper from OpenAI and GPT to summarize and get the key points. However, I realized that in terms of cost, it would quickly become expensive.

I then turned to lighter open source models that I could run locally (for processing after transcription). This worked (a little less well than Whisper certainly because the models are lighter) and saved me from paying a lot for nothing. However, I want to be able to use this project anywhere without necessarily running an LLM on every PC I want to use.

So, I am starting to think about hosting this model on Azure. This will save me a lot of money compared to using an LLM via the OpenAI API, for example. Moreover, I could use functions to further limit costs.

* `Azure`
* `Nuxt`
* `TypeScript`
* `Azure Functions`
* `Azure Static Apps`
* `Azure Key Vault`
* `Whisper`
* `GPT-3.5-Turbo`

## **Architecture**
![speechy-architecture](/portfolio/projects/speechy/speechy-architecture.png)

## Results
The project works well, I can record my voice or directly add an audio file. This will then be sent to my backend (Azure Function) and finally to OpenAI to get the transcription. With the transcription, we send this time to GPT-3.5-Turbo to get a summary and the key points covered.

I decided to use GPT-3.5-Turbo rather than GPT-4 to limit costs even more, especially since for such a simple task, it was not really necessary to have a more powerful model.

## Remaining Tasks
The project is currently functional but it can still be improved. Indeed, it would be necessary to:

* **Code:**
    * Add a limit to the duration of a recording to maximize token usage.
    * Check the added files and their format before sending them to OpenAI.
    * Improve error outputs.
    * Add a timer to know the duration of the recording.
    * Add Tests
    
* **Architecture:**
    * Add a database to keep track of the latest transcriptions.
    * Add connection to Notion and sending data to a Notion page.
    * Allow configuration of the solution for use by other people.
    * Find a cheaper alternative to the OpenAI API.

## Conclusion
I am proud to have been able to carry out this project; it was not very difficult since I use the OpenAI API, which is very easy to use. The project works quite well and meets my needs, but I would like to improve it even more.
