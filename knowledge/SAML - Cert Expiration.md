---
foam_template:
  filepath: "0 - INBOX/SAML - Cert Expiration.md"
  description: "New note"
created: "2025-12-02"
---

# SAML - Cert Expiration

[source-stack-overflow](https://stackoverflow.com/questions/79258910/how-am-i-supposed-to-handle-an-expiring-saml-certificate-as-an-sp#:~:text=According%20to%20the%20OASIS%20SAML%20V2.0%20Metadata%20Interoperability,validation%20that%20would%20warrant%20certificate%20expiry%20or%20renewal.)

**The SAML certificate can remain expired.**

According to the OASIS SAML V2.0 Metadata Interoperability Profile v1.0, SAML uses the IdP or SP certificate purely as a container for the public key – it does not use any of the certificate's metadata (e.g. Subject or SAN), thus there is no validation that would warrant certificate expiry or renewal. That is handled solely at the level of the SAML metadata document.

(For the same reason, it's common for SAML certificates to be self-signed – their "trust" comes from being included in the SAML metadata, so the issuer has no bearing on it.)

So if you wish (or if your IdP insists), the safest option is to issue a new certificate using the same private key, and as far as SAML is concerned it will still be the same certificate.

(If you must generate a new keypair, that is also fine but you must also give your IdP your updated metadata document or upload the updated certificate separately.)

In fact, SAML doesn't really use the SP certificate for much – the IdP only issues assertions for a specific entityID as 'audience', whereas your certificate does not become part of the SP's identity at all. To the best of my knowledge, SP certificates are only used a) for assertion encryption if that option is enabled on the IdP, and b) signing the logout requests when SLO (SingleLogOut) is in use.