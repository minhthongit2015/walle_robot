#! /bin/sh


#################################
# Step #2: Install dependencies #
#################################

sudo apt-get update && sudo apt-get upgrade

# We then need to install some developer tools, including CMake, which helps us configure the OpenCV build process:
sudo apt-get install build-essential cmake pkg-config

# Next, we need to install some image I/O packages that allow us to load various image file formats from disk. Examples of such file formats include JPEG, PNG, TIFF, etc.:
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev

# Just as we need image I/O packages, we also need video I/O packages. These libraries allow us to read various video file formats from disk as well as work directly with video streams:
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev

# The OpenCV library comes with a sub-module named highgui which is used to display images to our screen and build basic GUIs. In order to compile the highgui module, we need to install the GTK development library:
sudo apt-get install libgtk2.0-dev libgtk-3-dev

# Many operations inside of OpenCV (namely matrix operations) can be optimized further by installing a few extra dependencies:
sudo apt-get install libatlas-base-dev gfortran

# These optimization libraries are especially important for resource constrained devices such as the Raspberry Pi.
# Lastly, let’s install both the Python 2.7 and Python 3 header files so we can compile OpenCV with Python bindings:
sudo apt-get install python2.7-dev python3-dev


############################################
# Step #3: Download the OpenCV source code #
############################################
# Now that we have our dependencies installed, let’s grab the 3.3.0 archive of OpenCV from the official OpenCV repository. This version includes the dnn  module which we discussed in a previous post where we did Deep Learning with OpenCV (Note: As future versions of openCV are released, you can replace 3.3.0 with the latest version number):
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.1.zip
unzip opencv.zip

# We’ll want the full install of OpenCV 3 (to have access to features such as SIFT and SURF, for instance), so we also need to grab the opencv_contrib repository as well:
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.1.zip
unzip opencv_contrib.zip


####################################
# Step #4: Python 2.7 or Python 3? #
####################################
# Before we can start compiling OpenCV on our Raspberry Pi 3, we first need to install pip , a Python package manager:
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

# It’s standard practice in the Python community to be using virtual environments of some sort, so I highly recommend that you do the same:
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

# Now that both virtualenv and virtualenvwrapper have been installed, we need to update our ~/.profile file to include the following lines at the bottom of the file:
echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

source ~/.profile

# Next, let’s create the Python virtual environment that we’ll use for computer vision development:
mkvirtualenv cv -p python2
mkvirtualenv cv -p python3

# After that, you can use workon and you’ll be dropped down into your virtual environment:
source ~/.profile
workon cv

# Assuming you’ve made it this far, you should now be in the cv virtual environment (which you should stay in for the rest of this tutorial). Our only Python dependency is NumPy, a Python package used for numerical processing:
pip install numpy


#######################################
# Step #5: Compile and Install OpenCV #
#######################################
# Once you have ensured you are in the cv virtual environment, we can setup our build using CMake:
cd ~/opencv-3.3.1/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.1/modules \
    -D BUILD_EXAMPLES=ON ..





