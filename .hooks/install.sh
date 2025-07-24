#!/bin/bash

cp ../.hooks/pre-commit ../.git/hooks/pre-commit
cp ../.hooks/post-merge ../.git/hooks/post-merge

chmod +x ../.git/hooks/pre-commit
chmod +x ../.git/hooks/post-merge
