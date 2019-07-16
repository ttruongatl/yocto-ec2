
# YOCTO EC2  
  
A project with some tools that may help embedded linux developers build linux image with Yocto on EC2.  
  
The idea we may select a very cool computer with **16 cores** and **32 GB RAM**, this cost us ~$0.4 an hour for a build, it's a EC2 in AWS. We only run the EC2 once we start building the linux image and stop this once we are done. So, the EC2 does not cost us more than **$30-$40** a month, ~$400 a year. It's cheaper than you invest super desktop (**over $1100**) to build the code, plus utility bill and cooler as well.  

If you usually take **8 - 10 hours** to build your linux images with your work computer, you may want to enjoy a very fast build with Yocto EC2.

  
![](https://lh3.googleusercontent.com/m-zRp4JaYeeZuNh1SOQhn8lvYHwt8VTb5TuDTUmC1A1dPxHnTBC9d7o_8gfsr0cv_VwhVdj3csTdpSXRe9ja8LTczSNzR_7P7sukSwHGPHOMmB1UWQUfd7g-RocsxsUWQTJRU_q7tKU=w482-h766-no)  
  
### THE CURRENT VERSION IS ONLY SUPPORT NXP iMX SOURCE CODE  
  
## Setup AWS  
  
1. [Create EC2 instance](https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html)
  
   - Type: c5.4xlarge and ESB 120GB  
   - OS: Ubuntu Server 18.04  
   
2. [Add your ssh public key to the EC2](https://hackernoon.com/add-new-users-to-ec2-and-give-ssh-key-access-d2abd084f30c) 
  
## Clone source code and initialize build environment  
  
You probaly follow your documentation to setup Yocto build enviroment and run Yocto setup environment variables as well. This is [NXP iMX Yocto documentation](https://drive.google.com/file/d/1XbPk4_y0rrc17M1MAjvSScyB2tVBnKYc/view?usp=sharing)
  
## Installation  
  
```bash  
pip install yoctoEC2
```  
 
## Yocto build  
  
You may want to modify build script `build.sh` with your project parameters.  
  
Start EC2, build, copy image and Stop EC2  
```
yocto-ec2 build

Usage: yocto-ec2 build [OPTIONS]

  Build Yocto project in EC2

Options:
  --instance-id TEXT   [required]
  --project-root TEXT  [required]
  --script-path TEXT   [required]
  --sdcard-image TEXT  [required]
  --local <string>     images file destination
  --help               Show this message and exit.
```

For instance:

```bash  
yocto-ec2 build --instance-id=i-12345678  --project-root=/home/ubuntu/Workspace/iMX6ULEVK/ --script-path=./build.sh --sdcard-image=/home/ubuntu/Workspace/iMX6ULEVK/build/tmp/deploy/images/imx6ulevk/core-image-base-imx6ulevk.sdcard.bz2
```