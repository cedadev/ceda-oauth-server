# ceda-oauth-server

This package provides the OAuth server for CEDA.

This server provides a SLCS service using the [Online CA service](https://github.com/cedadev/online_ca_service),
accessible using OAuth and Basic Auth credentials.


## Deploying the CEDA OAuth Server

The CEDA OAuth server is deployed using an [Ansible playbook](https://www.ansible.com/).
This playbook can be configured to deploy a development machine using [Vagrant](https://www.vagrantup.com/)
or a production machine using the regular Ansible inventory system.

This playbook is available to CEDA staff on request - contact Matt Pryor.
