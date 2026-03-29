
# Principles 

- The entire system (infra & apps) is described declaratively. 
- The desired system state is versioned in Git.
- Changes approved (though MR) are automated and applied to the system
- Software agents ensure correctness and alert on divergence
- Nothing had access to the cluster to make changes, the gitops controller is the only one allowed to make changes in the cluster