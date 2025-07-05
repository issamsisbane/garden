---
title: "Mawaqit Discord Notify"
description: "A Discord bot for sending notifications at specific times of the day obtained by scraping a website."
lang: "en"
pubDate: "Apr 8 2024"
heroImage: "/portfolio/projects/mawaqit_discord/mawaqit.webp"
badge: "PERSONAL"
tags: ["Cloud", "Azure", "Cron", "Docker", "Javascript", "Scraping"]
---

## **Links**

- [The project](https://github.com/IssamSisbane/mawaqit-discord-notify)
- [MAWAQIT](https://mawaqit.net/fr/)

## **Need**

There is an application called MAWAQIT that provides prayer times for a given mosque, among other features. I really appreciate this application and use it daily.

However, I have a small issue with its functionality. It is possible to set up notifications to be alerted at the time of a prayer, but these notifications are only audible and can only be emitted on my Android phone. Sometimes, I work on my computer and do not touch my phone for a while.

I had found a solution by opening a MAWAQIT web page that emitted a small beep at each prayer, but this posed a problem when I already had sound on my computer or when I did not have my headphones plugged in. So, I needed a system that would allow me to receive notifications both on my computer and on my phone.

## **Objectives**

The objective of this project is to set up a system that sends notifications at the time of each prayer, every day.

## **Methodology**

The goal is to send notifications five times a day at changing times daily. For this, several problems need to be solved:

1. Retrieve prayer times for a given day.
2. Send notifications at the time of one of the retrieved prayers.
3. Ensure that this runs every day.

I started with the first problem. I could have used any API for this, but I really wanted the data from MAWAQIT to have accurate prayer times for nearby mosques. So, I analyzed the MAWAQIT website and realized that everything was already loaded via the page (calling a php page). Thus, the solution to retrieve the times was to directly scrape the site. I set this up using Node.js and Puppeteer, which allowed me to get a script to retrieve the prayer times for the whole day.

The next step was to send notifications at each prayer time. For this, I had the idea of using Discord. I have been using Discord for many years and have always wanted to test bot development, but I hadn't had a reason to do so until now. So, my solution was to create a bot that would send a message in my private server channel. This would allow me to receive notifications both on my computer and on my phone. It was ideal. I started researching how to create a Discord bot and finally used the DiscordJs library. Very simply, I was able to send a message via a bot in a specific channel.

Finally, the missing step was to make this happen every day. My first idea was to put this code in an Azure function, but the code wasn't suitable. Currently, the code retrieves the prayer times and then waits for each prayer to send notifications, which would require the code to run all day to work. So, I opted for containers. I thought of using job containers that could be executed every day, but I realized that they apparently have a maximum time limit and running them all day is apparently not possible or too expensive.

So, I chose to use simple containers using Azure Container Instance. I thought I would use a logic app to launch the container every day, but that's not possible. With a logic app, you can only manage a group of containers and not a single container. I didn't want to create a group of containers just for this small project. So, I found a solution, which was to create a cron directly in Node that would run every day by itself. That way, I would just need to start the container and let it run.

## **Used Technologies**

- `Azure`
- `Azure Key Vault`
- `Azure Container Instances`
- `CosmosDB`
- `Node.js`
- `Javascript`

## **Architecture**

![mawaqit_discord_architecture.drawio.png](/portfolio/projects/mawaqit_discord/mawaqit_discord_architecture.png)

## **Results**

So, everything works very well and meets my needs. I am very happy to have been able to realize this little project that took me very little time and that has been on my mind for a long time.

## **Possible Improvements**

The project is functional and customizable using environment variables, especially to choose the mosque and the Discord channel for message destination. However, I would like to develop a dedicated application without going through Discord, which would be a general notification application for all devices and would allow receiving reminders, especially about what I have to do during my day...

## **Conclusion**

I really enjoyed working on this little project. I had very few problems, but I find it very interesting to work on issues that concern me because I can clearly identify the needs and therefore adapt the solutions as best as possible.
