#! /bin/bash

docker build -t jcheroske/custom-gpt .
# docker tag jcheroske/custom-gpt nas.lan:5555/jcheroske/custom-gpt
# docker push nas.lan:5555/jcheroske/custom-gpt
# docker rm -f custom-gpt
# docker run -it --name custom-gpt -v /Users/jay/repos/custom-gpt/tmp/docs:/docs -v /Users/jay/repos/custom-gpt/tmp/index:/index --network host --env-file .env jcheroske/custom-gpt
