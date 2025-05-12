import oci

config = {
    INSIRA AQUI O ARQUIVO DE CONFIGURAÇÃO
}

def create_instance(compartment_id, availability_domain, display_name, shape, subnet_id):

    compute_client = oci.core.ComputeClient(config)
    network_client = oci.core.VirtualNetworkClient(config)



    # Configura os detalhes para criar a instância
    instance_details = oci.core.models.LaunchInstanceDetails(
        availability_domain=availability_domain,
        compartment_id=compartment_id,
        display_name=display_name,
        shape=shape,
        create_vnic_details=oci.core.models.CreateVnicDetails(
            subnet_id=subnet_id,
            assign_public_ip=True,
        ),
        source_details=oci.core.models.InstanceSourceViaImageDetails(
            source_type="image",
            image_id="ocid1.image.oc1.sa-saopaulo-1.aaaaaaaaup6otujgsh2oup46sv37h6ylwwn3q7defuy5a3lsnzfl3ascnt2a" #Imagem da instancia
        )
    )

    # Cria a instância
    response = compute_client.launch_instance(instance_details)
    instance = response.data
    print(f"Instância criada: {instance.display_name}, ID: {instance.id}")
    return instance


# Parâmetros necessários
COMPARTMENT_ID = "ID DO COMPARTIMENTO"
AVAILABILITY_DOMAIN = "ID DA REGIAO" 
SUBNET_ID = "ID DA SUBNET"
DISPLAY_NAME = "TesteInfraPy3" #NOME DA INSTANCIA
SHAPE = "VM.Standard.E2.1" #SHAPE DA VM

create_instance(COMPARTMENT_ID, AVAILABILITY_DOMAIN, DISPLAY_NAME, SHAPE, SUBNET_ID)
