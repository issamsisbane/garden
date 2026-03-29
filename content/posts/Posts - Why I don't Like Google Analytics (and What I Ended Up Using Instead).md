𝐖𝐡𝐲 𝐈 𝐝𝐨𝐧'𝐭 𝐋𝐢𝐤𝐞 𝐆𝐨𝐨𝐠𝐥𝐞 𝐀𝐧𝐚𝐥𝐲𝐭𝐢𝐜𝐬 (𝐚𝐧𝐝 𝐖𝐡𝐚𝐭 𝐈 𝐄𝐧𝐝𝐞𝐝 𝐔𝐩 𝐔𝐬𝐢𝐧𝐠 𝐈𝐧𝐬𝐭𝐞𝐚𝐝)

I needed an easy solution to see who visits my portfolio and, most importantly, get a unique‑visitor count.  
  
𝟭𝘀𝘁 𝗜𝗱𝗲𝗮 : 𝗗𝗜𝗬 𝗕𝗮𝗰𝗸𝗲𝗻𝗱 - 𝗧𝗼𝗼 𝗠𝗲𝘀𝘀𝘆  
  
My first idea was to roll my own tracker: a tiny endpoint that fires on every page load. Quickly I hit the classic pitfalls:  
  
- Page refreshes = multiple hits → inflates the count.  
- Headers only give browser & version → no solid way to fingerprint a user.  
- Static site = no server‑side logic → can’t grab IPs or set sophisticated cookies.  
  
I quicky abandoned the idea.  
  
𝟮𝗻𝗱 𝗜𝗱𝗲𝗮 : 𝗚𝗼𝗼𝗴𝗹𝗲 𝗔𝗻𝗮𝗹𝘆𝘁𝗶𝗰𝘀 - 𝗧𝗼𝗼 𝗖𝗼𝗺𝗽𝗹𝗲𝘅 𝗮𝗻𝗱 𝗛𝗲𝗮𝘃𝘆  
  
Adding the one‑line script was painless, yet:  
  
- Dashboard stayed empty for minutes, then hours; real‑time data took up to 48 h.  
- Ad‑blockers silently stripped the script, so many visits never recorded.  
- The UI is complex, tied to a Google account, and feels like overkill for a simple portfolio.  
  
Not the fit I wanted.  
  
𝟯𝗿𝗱 𝗜𝗱𝗲𝗮 : 𝗔𝘇𝘂𝗿𝗲 𝗔𝗽𝗽𝗹𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗜𝗻𝘀𝗶𝗴𝗵𝘁𝘀 - 𝗘𝗮𝘀𝗶𝗹𝘆 𝗯𝗹𝗼𝗰𝗸𝗲𝗱  
  
My tests showed uBlock Origin (and similar extensions) blocked the script. Disabling the blocker (or using a clean profile) restored the data flow, allowing me to build a custom dashboard and workbook.  
  
Not really the result I expected.  
  
𝗧𝗵𝗲 𝗦𝗼𝗹𝘂𝘁𝗶𝗼𝗻 : 𝗨𝗺𝗮𝗺𝗶  
  
It's a simple Analytics Solution, GDPR compliant and privacy-focused. Easy to setup and self-hostable.  
  
A one-liner script to add to the website and the data is showing instantly on the dashboard.  
  
I ended up using it for it simplicity, speed and because it's not blocked by ad-blockers.  
  
𝗧𝗮𝗸𝗲𝘄𝗮𝘆𝘀  
  
• 𝘊𝘶𝘴𝘵𝘰𝘮 𝘵𝘳𝘢𝘤𝘬𝘦𝘳𝘴 on static sites are hard to get right without compromising privacy.  
• 𝘎𝘰𝘰𝘨𝘭𝘦 𝘈𝘯𝘢𝘭𝘺𝘵𝘪𝘤𝘴 is painless to add but can be delayed, blocked, and opaque.  
• 𝘗𝘳𝘪𝘷𝘢𝘤𝘺-𝘍𝘰𝘤𝘶𝘴𝘦𝘥 Tools works well once you verify that no browser extensions are intercepting the script.  
  
---  
  
Read the full walkthroughs :  
• Setting up Umami : [https://lnkd.in/eDqB9-jh](https://lnkd.in/eDqB9-jh)  
• Comparing analytics tools : [https://lnkd.in/e2tNTMiu](https://lnkd.in/e2tNTMiu)
![[1757874675149.jpg]]
