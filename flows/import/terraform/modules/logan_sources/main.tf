resource "null_resource" "create_sources" {

  triggers = {
    auth_type = var.auth_type
    profile_name = var.config_file_profile
    compartment_id = var.compartment_id
    schema_names = format("%q", jsonencode(var.schemas))
    path = format("%q", var.path)
    current_time = timestamp()
  }

  provisioner "local-exec" {
    command = "python3 ./scripts/import_contents.py -a ${self.triggers.auth_type} -p ${self.triggers.profile_name} -e ${self.triggers.schema_names} -f ${self.triggers.path}"
  }

  provisioner "local-exec" {
    when = destroy
    command = "python3 ./scripts/delete_sources.py -a ${self.triggers.auth_type} -p ${self.triggers.profile_name} -c ${self.triggers.compartment_id} -f ${self.triggers.path}"
  }
}