# -*- mode: ruby -*-
# vi: set ft=ruby :

$conda_installation = <<SCRIPT
apt install -y bzip2 jq
curl https://repo.continuum.io/miniconda/Miniconda3-4.3.27-Linux-x86_64.sh -o miniconda.sh || exit 1;

# FIXME - gets installed in the root user account
# bash miniconda.sh -b || exit 1;
# grep -q miniconda ~/.bashrc;
# if [[ ${?} -ne 0 ]]; then
#     echo "export PATH=\"${HOME}/miniconda3/bin:\${PATH}\"" >> ~/.bashrc
# fi
# 
# source ~/.bashrc
# 
# conda info || exit 1;
# rm -f miniconda.sh || exit 1;
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"

  config.vm.box_check_update = false

  config.vm.provision "docker" do |d|
    d.pull_images "python:3"
  end

  config.vm.provision "shell", inline: $conda_installation
end