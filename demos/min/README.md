# Guidelines for minimizing the size of a container image

## The canonical test app

We will use a web service to demonstrate the effect of the minimization guidelines on the size of a container image.

At any step of the process, you can run the container to verify the service functionality by executing:

```bash
$ docker run -p 5000:5000 <image-id>
```

Point a browser to http://0.0.0.0:5000/. If everything is working fine, you should see a quote by Erwin Schrodinger.

# 1. Choose a small base image

Let's explore the effect the base image has on the size of a container image.

To demonstrate the effect of choosing the right base image, we will select three different base images to build container images that are functionaly equivalent.

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
$ docker images | grep 238
ado/app      latest               2383bad1d517        14 seconds ago      908MB
```

As you can see, the size of this container image is 908MB.

Let's continue the exploration by selecting a different base image.

## Using an ubuntu base image

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
$ docker images | grep dc99
ado/app     latest               dc99d28dec9d        40 seconds ago      399MB
```

The ubuntu base image has reduced the image size from 908MB to 399MB while retaining the exact same service function.

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
$ docker images | grep d11 
ado/app      latest               d11ab7ba27d2        39 seconds ago      85.7MB
```

By choosing the alpine base image we were able to produce a container image that's only 85.7MB. 

That's a reduction of 91% in size compared to using the python base image. In other word we have an image that's only a tenth of the size of the python image.

Determine if your application requires specific libraries or tools from a specific operating system and use small base images.

### Caveat emptor

We have used an alpine base image to demonstrate the dramatic effect the right base image can have on the size of the resulting container image. If your application can meet all of its requirements using a small base image, you will realize great space saving. 

Having said that, we are suggesting that ALL container images must use this same base image.


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
Notice the size of the build context, it is only 85.5kB. Recall that the image size was 85.7MB.

## Adding extra files to context

To modify the context, we created a new directory called "downstream" and copied tsimulus-ws-1.4.jar. We have done that for you. You are welcome to copy other files for your own tests.

## Build with extra files in the build context

Now that we have added an extra, and unnecessary, file to the build context, let's look at the effect on the image size.

Make sure you are in the right directory

```bash
cd <project-root>/context
```
And build the image 

```bash
docker build --force-rm -t ado/app -f Dockerfile.alpine .
```

The build backend should respond with

```bash
Sending build context to Docker daemon  32.27MB
```

Notice that the previous message indicated that the build context was only 85.5kB.

Let's check the size of the new image with (replace the image ID accordingly).

```bash
$ docker images | grep 4fd0
ado/app         latest               4fd041a960b7        21 seconds ago      118MB
```

Notice how the image went from 87.5MB to 118MB without any modifications to the code or the Dockerfile.

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
RUN pip install --upgrade setuptools # No command chaining
RUN pip install -r requirements.txt  # No command chaining
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

We get a successful build

```bash
Successfully built ab2533223d80
Successfully tagged ado/app:latest
```
And check the new image size with

```bash
$ docker images | grep ab25
ado/app     latest               ab2533223d80        About a minute ago   405MB
```

The image size went from 399MB to 405MB for a service as simple as our test app.