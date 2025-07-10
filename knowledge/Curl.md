[[Tools]] [[CEA - Week 1 - Cloud Fondamentals]]

Curl is a tool to make HTTP request.

## Install curl 

We are going to use curl inside the wsl 2 of windows.

``` bash
sudo apt install curl 
```

## Make a request

``` bash
curl url
```

## Get request status code

``` bash
curl -I url
```

## Download content to file

``` shell
curl url -o nameOfTheFile
```
