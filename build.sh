#!/bin/bash

export http_proxy=http://192.168.1.104:8118
export https_proxy=http://192.168.1.104:8118

hugo  --theme=Hugo-Octopress

