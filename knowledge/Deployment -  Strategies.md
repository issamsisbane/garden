
Deployment strategies determine how new code changes are released to a live production environment. Choosing the right strategy depends on several factors, including:

- The **nature of the application**: How critical is uptime, and how sensitive is the application to updates?
- The **client’s risk tolerance**: How much disruption can be tolerated by the user base during deployment?
- The **infrastructure’s architecture**: Does the infrastructure support multiple environments, and can it handle rolling updates?

Each strategy has its strengths and trade-offs, making it important to choose the right one for your specific use case.

## Blue-Green Deployment

![[Blue_green_deployment.png]]
https://dzone.com/articles/blue-green-deployment-for-cloud-native-application
### Definition

	Switch between two identical envrionements. One serves traffic while the other is updated.

**Blue-Green Deployment** involves switching between two identical environments, **blue** and **green**, for production traffic. At any given time, one environment serves live traffic while the other is updated. Once the new environment is tested and confirmed to be stable, the **router switches traffic** to it.

- The **Blue** environment serves production traffic.
- The **Green** environment is where updates are applied and tested.

Once the green environment is fully prepared and tested, the router switches all traffic to the green environment, making it the new live environment. If issues are detected post-switch, the router can be reverted back to the blue environment for **immediate rollback**.

### Advantages

- **Zero downtime** during deployment: Since both environments are live, switching traffic happens instantly with no service disruption.
- **Easy rollback**: If any issues are found in the new environment, you can switch back to the original environment almost immediately, minimizing downtime and risk.

### Drawbacks

* **Resource-heavy**: Requires **double the infrastructure** since you need to maintain two production-like environments, which increases costs and resource utilization.

## Canary Deployment
![[Canary_deployment.png]]
https://semaphoreci.com/blog/what-is-canary-deployment
### Definition

	Release to a small subset of servers or users, then gradually increase

**Canary Deployment** releases new changes to a **small subset** of users or servers first. The idea is to **gradually** introduce the update. If everything works as expected, the new version is gradually rolled out to more users or servers until the entire user base is using the new version.

- Initially, only **10%** of the users or servers might receive the new version.
- If no issues are found, more servers or users are updated until 100% deployment is reached.

If any issues are detected during this gradual rollout, the deployment can be stopped, and the previous version can be rolled back, preventing the issue from affecting the entire user base.

### Advantages
- **Risk mitigation**: Since only a small portion of the user base or servers receive the update initially, it allows for **early detection** of issues before they impact everyone.
- **Controlled feedback**: This gradual release provides useful feedback from real users without exposing the entire application to potential bugs or failures.

### Drawbacks
- **Slower deployment**: The incremental nature of Canary Deployments can make the overall deployment process slower compared to Blue-Green or Direct Deployments.
- **Complex traffic management**: It can be challenging to manage traffic and allocate different percentages of users or servers dynamically during rollout and rollback scenarios.
## Direct Production Deployment
![[spaceship.png]]

### Definition

	 Deploy changed directly to production after passing all tests.

In **Direct Production Deployment**, code changes are **deployed directly** to the live production environment once they pass all tests. This is a straightforward approach where changes are instantly applied to the production system without deploying to a staging environment first.

This strategy is often used in simpler applications or when resources are limited, making it the **fastest** and most resource-efficient method.

### Advantages 
- **Fastest deployment**: No need for additional environments or complex traffic management, making this the **quickest way** to get new code into production.
- **Lower infrastructure costs**: Since there are no parallel environments to maintain, this method requires **fewer resources**.

### Drawbacks
- **High risk**: Since changes go live immediately, any issues in the new code can cause significant **disruptions** in production. There’s also no easy rollback without downtime.
- **No safety net**: In the event of failure, there’s no backup environment to switch to, making recovery more challenging.
## Conclusion
Different strategies suit different types of applications, infrastructures, and business needs. In practice, **many companies use a combination** of these strategies based on the scale and impact of the release.

- **Blue-Green Deployment** is ideal for **major releases** that require zero downtime and minimal risk of rollback. It’s often used for **mission-critical systems** where uptime is paramount.
- **Canary Deployment** is preferable when you want to **validate the new code** with real users and closely monitor how it interacts with the application. This is typically used in systems where user experience is crucial, and any impact should be minimal.
- **Direct Production Deployment** is best for **small teams** or **startups** with limited resources or for applications that are **low-risk** and easy to roll back if issues arise. It’s fast, simple, and cost-effective.

| **Strategy**          | **Use Case**                              | **Advantages**                         | **Drawbacks**                                            |
| --------------------- | ----------------------------------------- | -------------------------------------- | -------------------------------------------------------- |
| **Blue-Green**        | Major releases, mission-critical systems  | Zero downtime, easy rollback           | Requires double the infrastructure, higher resource cost |
| **Canary**            | Gradual release, user feedback validation | Risk mitigation, early issue detection | Slower process, complex traffic management               |
| **Direct Production** | Small projects, low-risk changes          | Fast, cost-effective                   | High risk, no easy rollback                              |

By tailoring the deployment strategy to the specific needs of your system and application, teams can minimize risks while ensuring fast, reliable software releases.
