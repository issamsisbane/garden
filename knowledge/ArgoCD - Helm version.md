# ArgoCD - Helm Version
On peut mettre dynamiquement les versions pour les charts helm avec ArgoCD.

![[Pasted image 20251118120341.png]]

[Tracking and Deployment Strategies - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/)

Parcontre il faut faire attention car les prereleases version ne sont pas pris en compte par le `*`. 

Les préleases sont de la forme : 
- `1.2.0-RC2`
- `1.2.0-RC3`
- ...

Pour prendre en compte ces prereleases, il faut utiliser cela : `1.2.*-0`


## Sources 

Cela vient du composant de gestion de version semver utiliser par ArgoCD.

https://github.com/Masterminds/semver?tab=readme-ov-file#working-with-prerelease-versions

> Working With Prerelease Versions
Pre-releases, for those not familiar with them, are used for software releases prior to stable or generally available releases. Examples of pre-releases include development, alpha, beta, and release candidate releases. A pre-release may be a version such as 1.2.3-beta.1 while the stable release would be 1.2.3. In the order of precedence, pre-releases come before their associated releases. In this example 1.2.3-beta.1 < 1.2.3.

> According to the Semantic Version specification, pre-releases may not be API compliant with their release counterpart. It says,

> A pre-release version indicates that the version is unstable and might not satisfy the intended compatibility requirements as denoted by its associated normal version.

> SemVer's comparisons using constraints without a pre-release comparator will skip pre-release versions. For example, >=1.2.3 will skip pre-releases when looking at a list of releases while >=1.2.3-0 will evaluate and find pre-releases.

> The reason for the 0 as a pre-release version in the example comparison is because pre-releases can only contain ASCII alphanumerics and hyphens (along with . separators), per the spec. Sorting happens in ASCII sort order, again per the spec. The lowest character is a 0 in ASCII sort order (see an ASCII Table)