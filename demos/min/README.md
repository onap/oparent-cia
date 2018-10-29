# Guidelines for minimizing the size of a container image

This tutorial introduces a set of guidelines for the minimization of container images.

You may choose to simply read through the tutorial or run the experiments, which is highly recommended.

Each section will guide you through an experiment that demonstrates, in a tangible manner, the benefits of following each guideline.

The expectation is that, with each experiment, you will gain insight into the value of the guideline.

## Clone the repo

This tutorial is self-contained, you should have access to all the artifacts you need to run the experiments.

To get started, get the code by cloning the repo with:

```bash
git clone https://gerrit.onap.org/r/oparent/cia
```
## Why are my numbers different?

Please note that image sizes may vary slightly from platform to platform. This tutorial was produced on a Linux server. If you use a different platform, images sizes are bound to be different. And that's OK.

## The canonical test app

We will use a web service to demonstrate the effect of the minimization guidelines on the size of a container image.

At any step of the process, you can run the container to verify the service functionality by executing:

```bash
$ docker run -p 5000:5000 <image-id or tag>
```

Point a browser to http://0.0.0.0:5000/. If everything is working fine, you should see a quote by Erwin Schrodinger.

# 1. Choose a small base image

Let's explore the effect the base image has on the size of a container image.

To demonstrate the effect of choosing the right base image, we will select three different base images to build container images that are functionally equivalent.

```bash
cd <project-root>/base-image/
```
## Using a python:2.7 base image

First, we will use a python:2.7 base image. 

In this case, Dockerfile.python, contains:

```bash
FROM python:2.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Build the image with

```bash
$docker build --force-rm -t ado/app -f Dockerfile.python .
```
And check the size of the image with

```bash
$ docker images | grep ado/app
ado/app      latest               2383bad1d517        14 seconds ago      908MB
```

Depending on your platform, the size of the container image should about 908MB.

Remove the image.

```bash
$docker rmi ado/app
```

Let's continue the exploration by selecting a different base image.

## Using an Ubuntu base image

The Dockerfile for this scenario (Dockerfile.ubuntu) contains
```bash
FROM ubuntu:latest
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python-pip \
    python-dev \
    build-essential
COPY . /app
WORKDIR /app
RUN pip install --upgrade setuptools && pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Build the image with

```bash
docker build --force-rm -t ado/app -f Dockerfile.ubuntu .
```
And check the image size with
```bash
$ docker images | grep ado/app
ado/app     latest               dc99d28dec9d        40 seconds ago      399MB
```

The ubuntu base image has reduced the image size from 908MB to 399MB while retaining the exact same service function. Remember that your numbers may vary.

Remove the image.

```bash
$docker rmi ado/app
```
Can we do better? Let's try yet another base image.

## Using an alpine base image

In this case Dockerfile.alpine, contains

```bash
FROM python:2.7-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
```
Build the image with

```bash
docker build --force-rm -t ado/app -f Dockerfile.alpine .
```
And check the image size with

```bash
$ docker images | grep ado/app 
ado/app      latest               d11ab7ba27d2        39 seconds ago      85.7MB
```

By choosing the alpine base image we were able to produce a container image that's only 85.7MB. 

That's a reduction of 91% in size compared to using the python base image. In other word we have an image that's only a tenth of the size of the python image.


Don't forget to remove the image.

```bash
$docker rmi ado/app
```
### Upshot

Before selecting a base image, determine if your application requires specific libraries or tools from a specific operating system and always use the smallest possible base images.

### Caveat emptor

We have used an alpine base image to demonstrate the dramatic effect the right base image can have on the size of the resulting container image. If your application can meet all of its requirements using a small base image, you will realize great space saving. 

Having said that, we are not suggesting that ALL container images must use this same base image.


# 2. Be mindful of where your Dockerfile is located (i.e. understand the build context)

To illustrate this concept, we will use the last image we built as a reference, modify the context and see the effect on the image size.

Files for this section are under the "context" directory.

## Build with no extra files in build context

When we built the alpine version of the image in the previous section, we executed
```bash
$ docker build --force-rm -t ado/app -f Dockerfile.alpine .
```
The backend returned the following message at the beginning of the build.

```
Sending build context to Docker daemon   85.5kB
```
Notice the size of the build context, it is only 85.5kB. Recall that the image size was 85.7MB. Again your numbers may vary slightly.

## Adding extra files to context

To modify the context, we created a new directory called "downstream" and copied a PDF file. We have done that for you. You are welcome to copy other files for your own tests.

## Build with extra files in the build context

Now that we have added an extra, and unnecessary, file to the build context, let's look at the effect on the image size.

Make sure you are in the right directory

```bash
cd <project-root>/context/
```
And build the image with

```bash
docker build --force-rm -t ado/app -f Dockerfile.alpine .
```

The build backend should respond with

```bash
Sending build context to Docker daemon  1.517MB
```

Notice that the previous message indicated that the build context was only 85.5kB.

Let's check the size of the new image with (replace the image ID accordingly).

```bash
$ docker images | grep ado/app
ado/app         latest               4fd041a960b7        21 seconds ago      87.2MB
```

Notice how the image went from 87.5MB to 87.2MB without any modifications to the code or the Dockerfile. 

Don't forget to remove the image.

```bash
$docker rmi ado/app
```

## Upshot

Inadvertently including files that are not necessary for building an image results in a larger build context and larger image size.

# 3. Chain commands together to reduce the number of layers 

In this section we explore the effect the chaining commands together on the size of a container image. Files for this section can be found under the "cmd-chain" directory.

To demonstrate the effect of chaining commands, we will work with the ubuntu Dockerfile we used before.

```bash
FROM ubuntu:latest
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python-pip \
    python-dev \
    build-essential
COPY . /app
WORKDIR /app
RUN pip install --upgrade setuptools && pip install -r requirements.txt  
ENTRYPOINT ["python"]
CMD ["app.py"]
```
Recall the size of the image was 399MB.

Now let's modify the commands and remove chaining with &&.

We now have the following Dockerfile (Dockerfile.ubuntu-no-chain)

```bash
FROM ubuntu:latest
RUN apt-get update -y                             # No command chaining
RUN apt-get install -y --no-install-recommends \  # No command chaining
    python-pip \
    python-dev \
    build-essential
COPY . /app
WORKDIR /app
RUN pip install --upgrade setuptools # No command chaining
RUN pip install -r requirements.txt  # No command chaining
ENTRYPOINT ["python"]
CMD ["app.py"]
```

Make sure you are in the right directory

```bash
cd <project-root>/cmd-chain/
```

Build the image with

```bash
docker build --force-rm -t ado/app -f Dockerfile.ubuntu-no-chain .
```

Check the new image size with

```bash
$ docker images | grep ado/app
ado/app     latest               ab2533223d80        About a minute ago   405MB
```

Notice how the image size went from 399MB to 405MB which is significant for a service as simple as our test app.
