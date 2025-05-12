import oci
import csv
from datetime import datetime


config = {
   " INSIRA AQUI O ARQUIVO DE CONFIGURAÇÃO"
}

identity_client = oci.identity.IdentityClient(config)
compute_client = oci.core.ComputeClient(config)
network_client = oci.core.VirtualNetworkClient(config)
object_storage_client = oci.object_storage.ObjectStorageClient(config)
blockstorage_client = oci.core.BlockstorageClient(config)


#Isso aqui foi um teste de dicionario que eu tentei fazer, ainda vou modificar ou colcoar em um codigo separado
#RUim de trabalhar com OCI é isso, tem que ter vários dicionarios pra nao ficar esses ids toscos no CSV

compartments_teste = {
    "ocid1.tenancy.oc1..a": "a",
    "ocid1.compartment.oc1..b": "b",
    "ocid1.compartment.oc1..c": "c",
    "ocid1.compartment.oc1..d": "d",
    "ocid1.compartment.oc1..e":"e",
    "ocid1.compartment.oc1..f":"f",
    "ocid1.compartment.oc1..g":"g",
    "ocid1.compartment.oc1..h":"h",
    "ocid1.compartment.oc1..i":"i",
    "ocid1.compartment.oc1..o":"o",
    "ocid1.compartment.oc1..u":"p" }

def list_instances(compartment_id):
    response = compute_client.list_instances(compartment_id)
    instance_data = []
    for instance in response.data:
        private_ips, public_ips, subnet_ids = [], [], []

        vnic_attachments = compute_client.list_vnic_attachments(compartment_id, instance_id=instance.id).data

        for vnic_attachment in vnic_attachments:
            vnic = network_client.get_vnic(vnic_attachment.vnic_id).data
            private_ips.append(vnic.private_ip)
            if vnic.public_ip:
                public_ips.append(vnic.public_ip)
            subnet_ids.append(vnic.subnet_id)
        instance_data.append({
            'CompartmentId': compartment_id,
            'CompartmentName': compartments_teste.get(compartment_id, "Unknown"),
            'Id': instance.id,
            'Name': instance.display_name,
            'State': instance.lifecycle_state,
            'Shape': instance.shape,
            'TimeCreated': instance.time_created.strftime('%Y-%m-%d %H:%M:%S'),
            'ImageId': instance.image_id,
            #'BootVolume': instance.attach_volume,
            #'AttachVolume': instance.attach_volume,
            'PrivateIPs': ", ".join(private_ips),
            'PublicIPs': ", ".join(public_ips),
            'Subnets': ", ".join(subnet_ids),
            'Region': config['region']

        })


    return instance_data

def list_vcn(compartment_id):

    #Observação: pro cod ficar melhor talvez eu tenha que inserir um dicionario aqui tbm ou separar ja o ID e o name ja criando um dicionario?

    response = network_client.list_vcns(compartment_id)
    vcn_data = [{
        'CompartmentId': compartment_id,
        'ComparmentName': compartments_teste.get(compartment_id, 'Unknowm'),
        'Id': vcn.id,
        'Name': vcn.display_name,
        'CIDR': vcn.cidr_block,
        'State': vcn.lifecycle_state,
        'TimeCreated': vcn.time_created.strftime('%Y-%m-%d %H:%M:%S')
    } for vcn in response.data]
    return vcn_data

def list_buckets(compartment_id, namespace):
    response = object_storage_client.list_buckets(namespace, compartment_id)
    bucket_data = [{
        'CompartmentId': compartment_id,
        'CompartmentName': compartments_teste.get(compartment_id, "Unknown"),
        'Name': bucket.name,
        'TimeCreated': bucket.time_created.strftime('%Y-%m-%d %H:%M:%S'),
        'Region': config['region']
    } for bucket in response.data]
    return bucket_data

def list_subnets(compartment_id):
    response = network_client.list_subnets(compartment_id)
    subnet_data = [{
        'CompartmentId': compartment_id,
        'CompartmentName': compartments_teste.get(compartment_id, "Unknown"),
        'Id': subnet.id,
        'Name': subnet.display_name,
        'CIDR': subnet.cidr_block,
        'VCN Id': subnet.vcn_id,
        'State': subnet.lifecycle_state,
        'TimeCreated': subnet.time_created.strftime('%Y-%m-%d %H:%M:%S')
    } for subnet in response.data]
    return subnet_data

def list_security_lists(compartment_id):
    response = network_client.list_security_lists(compartment_id)
    security_list_data = []
    ingress_rule_data = []
    egress_rule_data = []

    for sec_list in response.data:
        security_list_data.append({
            'CompartmentId': compartment_id,
            'CompartmentName': compartments_teste.get(compartment_id, "Unknown"),
            'Id': sec_list.id,
            'Name': sec_list.display_name,
            'VCN Id': sec_list.vcn_id,
            'TimeCreated': sec_list.time_created.strftime('%Y-%m-%d %H:%M:%S'),
            'Region': config['region']
        })

        #Adicionando regras de entrada (Ingress Rules) separadamente
        for rule in sec_list.ingress_security_rules:
            ingress_rule_data.append({
                'SecurityListId': sec_list.id,
                'Source': rule.source,
                'SourceType': rule.source_type,
                'Protocol': rule.protocol,
                'ICMP Options': rule.icmp_options,
                'TCP Options': rule.tcp_options,
                'UDP Options': rule.udp_options,
                'Description': rule.description
            })
        for rule in sec_list.egress_security_rules:
            egress_rule_data.append({
                'SecurityListId': sec_list.id,
                'Destination': rule.destination,
                'DestinationType': rule.destination_type,
                'Protocol': rule.protocol,
                'ICMP Options': rule.icmp_options,
                'TCP Options': rule.tcp_options,
                'UDP Options': rule.udp_options,
                'Description': rule.description
            })

    return security_list_data, ingress_rule_data, egress_rule_data

def list_boot_volumes(compartment_id):
    """Lista os volumes de boot em um compartimento."""

    availability_domains = [
    ad.name for ad in identity_client.list_availability_domains(compartment_id).data]
    
    boot_volumes_data = []

    for ad in availability_domains:
        response = blockstorage_client.list_boot_volumes(
            compartment_id=compartment_id,
            availability_domain=ad
        )
        for boot_volume in response.data:
            boot_volumes_data.append({
                'BootVolumeId': boot_volume.id,
                'DisplayName': boot_volume.display_name,
                'SizeInGBs': boot_volume.size_in_gbs,
                'LifecycleState': boot_volume.lifecycle_state,
                'AvailabilityDomain': boot_volume.availability_domain,
                'TimeCreated': boot_volume.time_created.strftime('%Y-%m-%d %H:%M:%S')
            })

    return boot_volumes_data

def list_attached_volumes(compartment_id):
    response = compute_client.list_volume_attachments(compartment_id)
    volume_data = [{
        'CompartmentId': compartment_id,
        'CompartmentName': compartments_teste.get(compartment_id, "Unknown"),
        'VolumeId': volume_attachment.volume_id,
        'InstanceId': volume_attachment.instance_id,
        'Type': volume_attachment.attachment_type,
        'State': volume_attachment.lifecycle_state,
        'Region': config['region']
    } for volume_attachment in response.data]
    return volume_data

def list_instances_with_availability_domain(compartment_id):
    response = compute_client.list_instances(compartment_id)
    instance_data = []
    for instance in response.data:
        private_ips, public_ips, subnet_ids = [], [], []

        #Pegando detalhes da VNIC
        vnic_attachments = compute_client.list_vnic_attachments(compartment_id, instance_id=instance.id).data
        for vnic_attachment in vnic_attachments:
            vnic = network_client.get_vnic(vnic_attachment.vnic_id).data
            private_ips.append(vnic.private_ip)
            if vnic.public_ip:
                public_ips.append(vnic.public_ip)
            subnet_ids.append(vnic.subnet_id)



def escrever_em_csv(data, filename):
    """Writes a list of dictionaries to a CSV file."""
    if not data:
        print(f"No data to write for {filename}")
        return
    if not isinstance(data[0],dict):
        print(f"Os {filename} nao ta no formato do dicionario")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    #Pega os compartimentos para consultar, fica tranquilo que só pega os IDs 
    compartments = list(compartments_teste.keys())

    #Pega o nome do Bucket
    namespace = object_storage_client.get_namespace().data

    #Armazena em uma lista antes de jogar para o CSV
    consolidated_data = {
        'oci_instancia.csv': [],
        'oci_vcn.csv': [],
        'oci_buckets.csv': [],
        'oci_subnets.csv': [],
        'oci_security_list.csv': [],
        'oci_boot_volumes.csv': [],
        'oci_attached_volumes.csv': [],
        'oci_ingress_rules.csv': [],
        'oci_egress_rules.csv': []
    }

    for compartment_id in compartments:
        print(f"Buscando em cada compartimento: {compartment_id}")
        consolidated_data['oci_instancia.csv'].extend(list_instances(compartment_id))
        consolidated_data['oci_vcn.csv'].extend(list_vcn(compartment_id))
        consolidated_data['oci_buckets.csv'].extend(list_buckets(compartment_id, namespace))
        consolidated_data['oci_subnets.csv'].extend(list_subnets(compartment_id))

        security_lists, ingress_rules, egress_rules = list_security_lists(compartment_id)
        consolidated_data['oci_security_list.csv'].extend(security_lists)
        consolidated_data['oci_ingress_rules.csv'].extend(ingress_rules)
        consolidated_data['oci_egress_rules.csv'].extend(egress_rules)


        consolidated_data['oci_boot_volumes.csv'].extend(list_boot_volumes(compartment_id))
        consolidated_data['oci_attached_volumes.csv'].extend(list_attached_volumes(compartment_id))



    for filename, data in consolidated_data.items():
        escrever_em_csv(data, filename)
        print(f"Dados escritos em: {filename}")
