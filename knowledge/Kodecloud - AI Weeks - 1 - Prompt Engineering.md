
## Qwen

Qwen is a CLI AI tool like claude code. We can give it access to our infra/cluster and it can see directly. This allow it to be a lot better than external AI where we describe the problem how we can. 

Using it was very easy and it found the problems very fast. This ask a question : Can we give this level of access to an AI in a production envrionment ?

I think it's hard to do this with models depoyed externally but if the company can host models inside that could have a very huge impact on velocity for DevOps Engineers.
## Key Learnings

- **Direct Access Matters:** Qwen's kubectl access provides real insights, not guesses
- **Precision Over Theory:** Actual secret decoding beats "check your credentials"
- **Context is King:** Understanding the full system state leads to faster fixes
- **AI + Tools = Power:** Combining AI reasoning with direct tool access is transformative

## QWEN Resolution message

It is very interesting to see the structure when a problem is resolved, I think I will keep it :
- Root Cause
- Solution
- Verification

Issue Diagnosis and Resolution

   1. Root Cause:
      - There was a NetworkPolicy named "default-deny-all" in the beta
        namespace
      - This policy was blocking all ingress traffic to pods in the
        namespace
      - As a result, the frontend pods (webapp-mysql) couldn't communicate
        with the backend service (mysql)

   2. Solution:
      - Deleted the "default-deny-all" NetworkPolicy which was
        unnecessarily blocking traffic
      - This allows normal communication between services in the same
        namespace

   3. Verification:
      - After removing the NetworkPolicy, I verified that the application
        is working correctly
      - The frontend can now successfully communicate with the backend
        MySQL database
      - Accessing the web application via NodePort
        (http://192.168.214.152:30082) shows a successful database
        connection

  The application is now functioning properly with frontend-to-backend
  communication restored. The NetworkPolicy was the only blocking
  factor, and removing it resolved the issue completely.