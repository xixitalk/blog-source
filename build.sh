#!/bin/bash

export http_proxy=http://192.168.1.104:8118
export https_proxy=http://192.168.1.104:8118

cd public
rm -fr blog post css page tags twitter  categories
cd ..

hugo  --theme=Hugo-Octopress

