# Docker Notes

These will be run as docker containers

    cd <project>
    vi fig.yml  ### todo link 
    mkdir -p ./volumes/es/data

Create Elasticsearch config file at `./volumes/es/data/elasticsearch.yml`.

    path:
      logs: /data/log
      data: /data/data

Set up boot2docker

    $ brew install docker
    $ brew install boot2docker
    $ boot2docker init
    $ boot2docker up
    Writing /Users/mperry/.boot2docker/certs/boot2docker-vm/ca.pem
    Writing /Users/mperry/.boot2docker/certs/boot2docker-vm/cert.pem
    Writing /Users/mperry/.boot2docker/certs/boot2docker-vm/key.pem

    To connect the Docker client to the Docker daemon, please set:
        export DOCKER_HOST=tcp://192.168.59.103:2376
        export DOCKER_CERT_PATH=/Users/mperry/.boot2docker/certs/boot2docker-vm
        export DOCKER_TLS_VERIFY=1

**Docker is not workin for me... too many implicit, undocumented and just plain bad decisions made by the people that implement containers**

Fig is awesome and actually way easier than using docker at the command line.
Fig is the interface docker *should* have. But ultimately Linux containers lose their 
value on OS X as the added complexity of having to run boot2docker makes it less
efficient (in terms of developer time) than virtual machines and vagrant. Unless 
you're using docker as part of a production deployment system, why fight with it
during development? 


