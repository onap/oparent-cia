Casablanca Progress and Milestones
==================================

The CIA project has met a number of milestones:

| -Contributed code changes to the VNSDK and produced an arm container
  image. -Migrated OOF/HAS project to ONAP Normative image which reduced
  the image size by 70%. -Developed, reviewed and published 8 general
  guidelines for building container images -Developed, reviewed, and
  published 12 container build instructions -Developed, reviewed, and
  published 6 image minimization guidelines to reduce image footprint
  -Developed and coded three tutorials to educate ONAP projects and PTLs
  on how to apply image minimization guidelines. -Defined a generic
  build process for ONAP that will be container images-friendly.
  -Defined a set of platform-agnostic ONAP Normative Base Images that
  will contribute to the minimization of ONAP container images'
  footprint
| -Analyzed 150 Dockerfiles and developed a migration path from the 53
  large base images to 21 smaller, normative, platform-agnostic base
  images. -Performed an assessment of the SO project and identified
  opportunities for improvement.

Container Image Minimization Tutorials
======================================

Source files
------------

-  Tutorial documentation
   https://git.onap.org/oparent/cia/tree/demos/min/README.md
-  Base image guideline
   https://git.onap.org/oparent/cia/tree/demos/min/base-image
-  Command chaining guideline
   https://git.onap.org/oparent/cia/tree/demos/min/cmd-chain
-  Context guideline
   https://git.onap.org/oparent/cia/tree/demos/min/context

Description
-----------

The container build processes used by ONAP projects generates container
images that are larger than they should be. As a result, the
develop-build-test-deploy workflow takes a long time and consumes a lot
of resources.

The ONAP community has identified this delay as one of the main pain
points.

Furthermore, large image size has a detrimental effect on deployability.
In fact,operators consider image minimization as one of the main
priorities.

Usage
-----

The image minimization tutorials introduce a set of guidelines for the
minimization of container images.

Users may choose to simply read through the tutorial or run the
experiments; which is highly recommended.

Each tutorial guides the user through an experiment that demonstrates,
in a tangible manner, the benefits of following each guideline.

The expectation is that, with each experiment, userss will gain insight
into the value of the guideline and the positive impact on reducing
ONAP's footprint.
