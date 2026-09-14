---
creation date: 2026-08-04-22:39:44
modification date: 2026-08-04-22:39:44
imageNameKey: Install_a_binary_from_github
---
# Install a binary from github

An Exemple for Kubebench

1. Download the `tar.gz`:

```bash
curl -L https://github.com/aquasecurity/kube-bench/releases/download/v0.12.0/kube-bench_0.12.0_linux_amd64.tar.gz -o kube-bench_0.12.0_linux_amd64.tar.gz
```

2. Extract the archive

```bash
mkdir kube-bench && cd kube-bench tar -xvf ../kube-bench_0.12.0_linux_amd64.tar.gz
```

3. Move to a directory in `$PATH`

```bash
sudo mv kube-bench /usr/local/bin/
```