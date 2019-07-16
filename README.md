
# YOCTO EC2  
  
A project with some tools that may help embedded linux developers build linux image with Yocto on EC2.  
  
The idea we may select a very cool computer with **16 cores** and **32 GB RAM**, this cost us ~$0.4 an hour for a build, it's a EC2 in AWS. We only run the EC2 once we start building the linux image and stop this once we are done. So, the EC2 does not cost us more than **$30-$40** a month, ~$400 a year. It's cheaper than you invest super desktop (**over $1100**) to build the code, plus utility bill and cooler as well.  

If you usually take **8 - 10 hours** to build your linux images with your work computer, you may want to enjoy a very fast build with Yocto EC2.

  
![](https://lh3.googleusercontent.com/C6a7PYTqcXImoVVdXW0JQMc00rTbUrP0LIe9P5nvZ_YQdF1Z1vMPX4k9mHvVL9SoqKrweRm0Ua5wYJMAYOoqjIrM0rlrSeyWufubRefiGIMrJBpZQiyzk0YKC9bWmeypSxCT3lSknWLhdClEGNwxEpL7FpZgfFTM5CnvpLNmVYLUZG6eBoAt7fNm73-BzOLOSKChQWh_b-QaJ-HDhPAiZh6iq4vDjk3IHPh5EmlLy_xpkLeAGlRq9tpwG-fiYx3nWXdro7Vp_6_RIHOj7LSqne5vLgqDCH3NFpMk9zbOKLF_8Nkhccm8LD5ImCuw_Ao91pyzCKTsRcuEAkajlhpR0NY1Q_UgBK_25UFe1i5YNsFhqM7YI8Oro1QsfA39c9lh3EMUZmfF1ChG3Kgil4Pr9OVJZu-8w10QaWa2yFwU_Zy04Y8BGjtAIfoOeJKbC_fgas7qCjEJMtDNt65TgBFP6hf9_v7tLN9Jxtb5LLffqTjx2qGULks6YfICgBpnQak9Nf4EGvFxgTioNrOdU5rGzrpBFeyMQVC3e_8Y30dzfPU5gTWOEAUXaM72hRRIugwVSiiKfMSGe6Z2P42aHNgbZg0P6_juH57iSK3F_TkbMYTB7docSrmUUTI7o8ClRb5GTZDdmksygfWnynMFxMxz-Wuxs5pykl-w45BDX9hptSabvkk-DzMDdsJeKMJq3J3__lqVu0QtcZSTyyqLRm0hOhfyrQ=w484-h766-no)  
  
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