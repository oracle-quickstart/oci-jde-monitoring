# Copyright (c) 2022, Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.

variable "config_file_profile" {
  default = "DEFAULT"
}

variable "auth_type" {
    default = "instance"
}

variable "tenancy_ocid" {
  type        = string
  description = "The OCID of the tenancy."
}

variable "compartment_ocid" {
  type        = string
  description = "The compartment OCID where all new resources will be created"
}

variable "db_compartment" {
  type        = string
  description = "The compartment OCID where JDE DB resides"
}

variable "resource_compartment" {
  type        = string
  description = "The compartment OCID where log analytics resources will be created"
}

variable "db_cred_compartment" {
  type        = string
  description = "The compartment OCID where JDE DB password secret resides"
}

variable "region" {
  type        = string
  description = "OCI region"
}

variable "instance_name" {
  type        = string
  description = "Display name for compute instance"
  default     = "JDE-MgmtAgent"
}

variable "availability_domain" {
  type        = string
  description = "The availability domain of the instance"
}

variable "instance_shape" {
  type        = string
  description = "The shape of an instance. The shape determines the number of CPUs, amount of memory, and other resources allocated to the instance."
}

#variable "vcn_ocid" {
#  type        = string
#  description = "The OCID of the VCN to create the instance in."
#}

variable "subnet_ocid" {
  type        = string
  description = "The OCID of the subnet to create the VNIC in."
}

variable "user_ssh_secret" {
  description = "Public SSH keys to be included in the ~/.ssh/authorized_keys file for the default user on the instance. "
}

variable "db_host" {
  type        = string
  description = "JDE DB Host"
}

variable "db_port" {
  type        = number
  description = "JDE DB Port"
}

variable "db_service" {
  type        = string
  description = "JDE DB Service Name"
}


variable "db_credentials" {
  type        = string
  description = "OCID of secret in vault to use for connecting to JDE DB"
}

variable "db_username" {
  type        = string
  description = "Username for connecting to JDE DB"
}

variable "db_user_role" {
  type        = string
  default     = "NORMAL"
  description = "Role of user for Database."
}

variable "la_entity_name" {
  type        = string
  default     = "JDEEntity"
  description = "The JDE Entity Name."
}

variable "server_map_schema" {
  type        = string
  default     = "SVM920"
  description = "Server Map Schema Name."
}

variable "system_schema" {
  type        = string
  default     = "SY920"
  description = "System Schema Name."
}

variable "business_data_schema" {
  type        = string
  default     = "TESTDTA"
  description = "Business Data Schema Name."
}

variable "control_tables_schema" {
  type        = string
  default     = "TESTCTL"
  description = "Control Tables Schema Name."
}

variable "bucket_name" {
  type        = string
}

variable "file_name" {
  type        = string
}

variable "log_group_ocid" {
  type        = string
  default     = "dummy"
  description = "The unique identifier of the log group to use when auto-associting the log source to eligible entities."
}

variable "setup_policies" {
  type        = bool
  default     = true
  description = "Setup IAM policies or not"
}

variable "create_log_group" {
  type        = bool
  default     = false
  description = "Create Log Group or not"
}

variable "products" {
  type = string
}

variable "dashboard_files" {
  description = "Dashboard JSON files"
  type = set(string)
  default = ["JDE-Dashboard.json"]
  #default = ["eBS-sensors-dashboard.json"]
}
