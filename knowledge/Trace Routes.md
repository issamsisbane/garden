[[Networking]]

## Trace route

The output will display a list of '**hops**'. Each hop represents a **router** or **gateway** that packets pass through on their way to the **destination**. For each hop, you'll typically see:

- The **hop's number** in the sequence.
- The **IP address** of the **hop**.
- The **round-trip time (RTT)** for packets to **reach** that hop and return **to** your computer. This is usually shown in milliseconds (ms) and may be displayed three times for accuracy.

### Linux
``` shell
traceroute google.com
```
![[traceroute_screenshot.png]]
### Windows
``` bash
tracert google.com
```
![[tracert_screenshot.png]]

## What it could be used for 

- **Internet Routing Complexity:** Demonstrates the multiple intermediate steps a packet takes through different networks to reach its destination.
- **Network Performance:** The RTT times can give you an idea of the latency between your computer and each hop along the path.
- **Troubleshooting:** Identifying where packets are getting delayed or lost can help diagnose network connectivity issues.