# JD Edwards EnterpriseOne Monitoring
Oracle Logging Analytics can help you identify JD Edwards EnterpriseOne issues to make your business operations smooth to delight your customers. This resource manager stack configures logging analytics to enable these functional sensors such as:

Work order records missing UOM in F3102 (JDE Manufacturing)
Voucher Post Code Mismatch Between F0411 and F0011 (JDE Financial)
Unique Key field blank in table F04572 (JDE Financial)
Number of AP Trade Accounts with blank Post Edit Code (JDE Financial)
Number of AP Trade accounts without AE documents (JDE Financial)
Number of AR Trade Accounts with blank Post Edit Code (JDE Financial)
Number of AR Trade accounts without AE documents (JDE Financial)
Corrupt or non-existent Unique Next Number in F03B22 (JDE Financial)
F4941 Flags Not Synched (JDE Distribution)
And 100s of more issues
This OCI Resource Manager stack creates a instance in the subnet from which JDE Database is accessible, configures Management Agent and Logging Analytics to run regular Business checks. It installs four new dashboards covering different tiers of JDE deployment. Note: This stack doesn't start standard Logs collection and Logging Analytics JDE Discovery from the UI should be used to discover and enable logs collection.

As part of this deployment, a compute instance is created and Oracle Cloud Agent is configured to collect log data. Users can select the JDE products that they are using and JDE sensor sources for those products are created. JDE Database entity and source-entity associations are also created.

## Prerequisites
- VCN and subnet from where database can be accessed.
- The subnet should have access to OCI Services (via a Service Gateway)
- Quota to create the following resources: 1 Compute instance,  1 dynamic group, 1 policy
- Store JDE DB password in OCI Vault in base encoded form.
- Store schedule file in OCI Object Storage bucket.
- Create database user with access to select from tables used in the sensors. Use USER_ACCESS_TABLES.md file.

If you don't have the required permissions and quota, contact your tenancy administrator. See [Policy Reference](https://docs.cloud.oracle.com/en-us/iaas/Content/Identity/Reference/policyreference.htm), [Service Limits](https://docs.cloud.oracle.com/en-us/iaas/Content/General/Concepts/servicelimits.htm), [Compartment Quotas](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcequotas.htm).

## Deploy Using OCI Resource Manager

1. Click [![Deploy to Oracle Cloud](https://oci-resourcemanager-plugin.plugins.oci.oraclecloud.com/latest/deploy-to-oracle-cloud.svg)](https://cloud.oracle.com/resourcemanager/stacks/create?zipUrl=https://github.com/oracle-quickstart/oci-ebs-monitoring/releases/download/v0.9/ebs-v0.9.zip)

#    If you aren't already signed in, when prompted, enter the tenancy and user credentials.

2. Review and accept the terms and conditions.

3. Select the region where you want to deploy the stack.

4. Follow the on-screen prompts and instructions to create the stack.

5. After creating the stack, click **Terraform Actions**, and select **Plan**.

6. Wait for the job to be completed, and review the plan.

    To make any changes, return to the Stack Details page, click **Edit Stack**, and make the required changes. Then, run the **Plan** action again.

7. If no further changes are necessary, return to the Stack Details page, click **Terraform Actions**, and select **Apply**.

## Deploy Using the Terraform CLI

### Clone the Module
Now, you'll want a local copy of this repo. You can make that with the commands:

    git clonehttps://github.com/oracle-quickstart/oci-jde-monitoring.git
    cd oci-jde-monitoring
    ls

### Set Up and Configure Terraform

1. Complete the prerequisites described [here](https://github.com/cloud-partners/oci-prerequisites).

2. Create a `terraform.tfvars` file, and specify the following variables:

```
# Authentication
tenancy_ocid="<tenancy_ocid>"
auth_type="user"
# Config  file is ~/.oci/config
config_file_profile="DEFAULT"

# Region
region = "<oci_region>"

# Compartment
compartment_ocid = "<compartment_ocid>"

# JDE DB Info
subnet_ocid="<DB_NETWORK_SUBNET_OCID>"
db_compartment="<DB_COMPARTMENT_OCID>"
db_cred_compartment="<VAULT_COMPARTMENT_OCID>"

db_host="<DB_HOST>"
db_port=<DB_PORT>
db_service="<DB_SERVICE_NAME>"
db_username="<DB_USER_NAME>"
db_credentials="<VAULT_SECRET_OCID>"
db_user_role="NORMAL"

#Agent Compute Instance Info
instance_name="JDEAgentVM"
availability_domain="<AD>"
instance_shape="VM.Standard.E2.1"
user_ssh_secret="<SSH-KEY>"

# Set to false if you want to manually create dynamic group and policies
setup_policies=true

# Location of schedule file
bucket_name="<BUCKET_NAME>"
file_name="logan_schedule_database_sql_JDE.csv"

# Log Analytics Resources
resource_compartment="<RESOURCE_COMPARTMENT_OCID>"
create_log_group=false
log_group_ocid="<LOG_GROUP_OCID>"
la_entity_name = "<JDEDB entity name>"

# Selected products
#products="JD Edwards EnterpriseOne Accounts Payable, JD Edwards EnterpriseOne Accounts Receivable, JD Edwards EnterpriseOne Address Book, JD Edwards EnterpriseOne Advanced Pricing - Procurement, JD Edwards EnterpriseOne Advanced Pricing - Sales, JD Edwards EnterpriseOne Australia Payroll, JD Edwards EnterpriseOne Canadian Payroll, JD Edwards EnterpriseOne EDI, JD Edwards EnterpriseOne General Ledger, JD Edwards EnterpriseOne Inventory Foundation, JD Edwards EnterpriseOne Inventory Management, JD Edwards EnterpriseOne New Zealand Payroll, JD Edwards EnterpriseOne Procurement and Subcontract Management, JD Edwards EnterpriseOne Product Data Management, JD Edwards EnterpriseOne Sales Order Management, JD Edwards EnterpriseOne Shop Floor Control, JD Edwards EnterpriseOne Transportation Management, JD Edwards EnterpriseOne US Payroll"

products="JD Edwards EnterpriseOne Accounts Payable, JD Edwards EnterpriseOne Accounts Receivable, JD Edwards EnterpriseOne Address Book, JD Edwards EnterpriseOne Advanced Pricing - Procurement, JD Edwards EnterpriseOne Advanced Pricing - Sales, JD Edwards EnterpriseOne EDI, JD Edwards EnterpriseOne General Ledger, JD Edwards EnterpriseOne Inventory Foundation, JD Edwards EnterpriseOne Inventory Management, JD Edwards EnterpriseOne Procurement and Subcontract Management, JD Edwards EnterpriseOne Product Data Management, JD Edwards EnterpriseOne Sales Order Management, JD Edwards EnterpriseOne Shop Floor Control, JD Edwards EnterpriseOne Transportation Management"

### Create the Resources
Run the following commands:

    terraform init
    terraform plan
    terraform apply


```
Outputs:


### Destroy the Deployment
When you no longer need the deployment, you can run this command to destroy the resources:

    terraform destroy

### Dynamic Groups and Policies (if adding manually)

1. Create a dynamic group instance dynamic group with matching rule:
- ANY {instance.compartment.id = '<db_compartment_ocid>'}
2. Create dynamic group mgmtagent dynamic group with matching rule:
- ALL {resource.type='managementagent', resource.compartment.id='<db_compartment_ocid>'}
3. Create a policy at tenancy level with the following statements:
- Allow DYNAMIC-GROUP <mgmtagent_dynamic_group_name> to {LOG_ANALYTICS_LOG_GROUP_UPLOAD_LOGS} in tenancy
- ALLOW DYNAMIC-GROUP <mgmtagent_dynamic_group_name> TO MANAGE management-agents IN COMPARTMENT ID <db_compartment_ocid>
- ALLOW DYNAMIC-GROUP <mgmtagent_dynamic_group_name> TO USE METRICS IN COMPARTMENT ID <db_compartment_ocid>
- ALLOW DYNAMIC-GROUP <instance_dynamic_group_name> TO MANAGE management-agents IN COMPARTMENT ID <db_compartment_ocid>
- ALLOW DYNAMIC-GROUP <instance_dynamic_group_name> TO MANAGE management-agent-install-keys IN COMPARTMENT ID <db_compartment_ocid>
- ALLOW DYNAMIC-GROUP <instance_dynamic_group_name> TO MANAGE OBJECTS IN COMPARTMENT ID <db_compartment_ocid>
- ALLOW DYNAMIC-GROUP <instance_dynamic_group_name> TO READ BUCKETS IN COMPARTMENT ID <db_compartment_ocid>
- ALLOW DYNAMIC-GROUP <instance_dynamic_group_name> TO READ secret-family in COMPARTMENT ID <vault_compartment_ocid>} where target.secret.id = '<db_secret_ocid>'
