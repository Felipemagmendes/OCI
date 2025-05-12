#Listar Imagens!

import oci

config = {
   " INSIRA AQUI O ARQUIVO DE CONFIGURAÇÃO"
}

compute_client = oci.core.ComputeClient(config)

image_list = oci.pagination.list_call_get_all_results(
    compute_client.list_images,
    compartment_id="ID DO COMPARTIMENTO"
).data

for image in image_list:
    print(f"Name: {image.display_name}, OCID: {image.id}")
