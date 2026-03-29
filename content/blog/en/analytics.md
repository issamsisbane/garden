---
title: "Exploring Web Traffic Analysis Tools"
description: "How to analyze website traffic to get an idea of the number of users?"
lang: "en"
pubDate: "Apr 24 2024"
heroImage: "/portfolio/blog/analytics/analytics.png"
badge: "AZURE"
tags: ["Cloud", "Azure", "Analysis"]
---

## Initial Problem

After developing and deploying several websites, including my portfolio, I was curious to gather insights about the visitors. Specifically, I shared multiple links to my portfolio, whether on LinkedIn, GitHub, or my CV.

I wanted to understand the traffic on my site, particularly the **number of unique visitors**.

## Homemade Backend

Initially, I considered creating my own solution. I envisioned a simple backend where each visit would trigger a request. However, I quickly encountered challenges. With this approach, it would be impossible to accurately count the number of unique users. For instance, page refreshes would be counted as multiple visits rather than one.

To address this issue, I explored using cookies to track unique users, as well as the information contained in request headers. However, the data available in headers was limited, providing only the browser and its version, which did not reliably identify a unique user. Since my portfolio is a static site, I'm constrained in header management and can't retrieve, for example, the IP address.

Even with IP retrieval, ensuring user uniqueness would be challenging as it can change. Cookies are also unreliable as users can delete them. Therefore, I decided to search for another solution without changing the rendering type of my site or making major modifications.

## Transition to Google Analytics

Faced with these challenges, I turned to Google Analytics, a well-established tool in the web analytics field. Integrating Google scripts into my site was straightforward. It only required adding a script to all the pages I wanted to monitor. Since I use Astro, which allows layout usage on all pages, I only needed to add the script to my layout page.

![google analytics tag](/portfolio/blog/analytics/analytics_0.png)

However, despite its integration with my Astro project, I encountered difficulties accessing the collected data, thus limiting my site traffic analysis. Initially, no data was available on the dashboard. After a few minutes, the data was still unavailable. Consequently, I decided to explore other options.

![Tableau de bord vide](/portfolio/blog/analytics/analytics_1.png)

## Adoption of Azure Application Insight

After evaluating different options, I remembered Azure [Application Insight](https://learn.microsoft.com/fr-fr/azure/azure-monitor/app/app-insights-overview), a tool that allows real-time monitoring and management of an application or API's performance.

I also realized it was possible to link Application Insight to an application even if it's not hosted on Azure (my portfolio is hosted on GitHub Pages).

The process of connecting the application to Azure was similar to Google Analytics, simply by integrating the Application Insight JavaScript tag. However, after integration and redeployment of my application, no data was visible in Application Insight.

Upon online research, I discovered that the browser extension `uBlock Origin` was blocking Azure scripts identified as trackers. By deactivating this extension or using another browser, I was finally able to see the data in the Azure portal.

Thus, I was able to create a [dashboard](https://learn.microsoft.com/en-us/azure/azure-portal/azure-portal-dashboards) to obtain information about my site visitors and a [workbook](https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview) for more precise information and detailed visualizations.

![Azure Users Dashboard](/portfolio/blog/analytics/analytics_2.png)

## Results and Conclusion

Thanks to the use of Application Insight, I obtained detailed information about my site users, such as the number of unique users, their geographical origin, and the pages they visited. Although the data was not perfectly precise, the tool proved to be a functional and relevant solution for the project's needs.

NB.

24 hours later, the data appeared on the Google Analytics dashboard. It was indeed mentioned that there could be a maximum propagation delay of 48 hours and that extensions could block Google scripts.

![Google Analytics Dashboard](/portfolio/blog/analytics/analytics_3.png)

## Key points:

- Initial need to analyze the traffic of a portfolio site.
- Challenges encountered with the implementation of custom tools and Google Analytics.
- Successful adoption of Application Insight to obtain more precise data on site users.
- Importance of testing tool compatibility with existing configurations to ensure efficient data collection.
