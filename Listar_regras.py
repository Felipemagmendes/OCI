#LISTA REGRAS DE ENTRADA E SAIDA DE INSTANCIAS


import oci
import csv

# Cria o cliente para a Compute/Networking
config = {
    ""
}
virtual_network_client = oci.core.VirtualNetworkClient(config)
identity_client = oci.identity.IdentityClient(config)


# Lista de Compartimentos (Compartment OCIDs)
compartment_ids = [
    ""
]

# Arquivos CSV para armazenar as regras
nsg_ingress_csv = "nsg_ingress_rules.csv"
nsg_egress_csv = "nsg_egress_rules.csv"

# Função para listar Network Security Groups e salvar regras em CSV
def list_nsgs_to_csv(compartment_ids):
    try:
        # Inicializa os cabeçalhos dos CSVs
        with open(nsg_ingress_csv, mode="w", newline="") as ingress_file, \
             open(nsg_egress_csv, mode="w", newline="") as egress_file:
            
            ingress_writer = csv.writer(ingress_file)
            egress_writer = csv.writer(egress_file)
            
            # Escreve os cabeçalhos
            ingress_writer.writerow(["Compartment Name", "NSG Name", "Protocol", "Source", "Source Type", "TCP Options", "UDP Options", "ICMP Options","description"])
            egress_writer.writerow(["Compartment Name", "NSG Name", "Protocol", "Destination", "Destination Type", "TCP Options", "UDP Options", "ICMP Options", "description"])
            
            for compartment_id in compartment_ids:
                # Recupera o nome do compartimento
                compartment_name = oci.identity.IdentityClient(config).get_compartment(compartment_id).data.name
                
                # Lista todos os NSGs no compartimento
                nsgs = virtual_network_client.list_network_security_groups(compartment_id=compartment_id).data
                for nsg in nsgs:
                    nsg_name = nsg.display_name
                    
                    # Recupera as regras do NSG
                    nsg_rules = virtual_network_client.list_network_security_group_security_rules(
                        network_security_group_id=nsg.id
                    ).data
                    
                    # Regras de Entrada
                    for rule in nsg_rules:
                        if rule.direction == "INGRESS":
                            ingress_writer.writerow([
                                compartment_name,
                                nsg_name,
                                rule.protocol,
                                rule.source,
                                rule.source_type,
                                rule.tcp_options,
                                rule.udp_options,
                                rule.icmp_options,
                                rule.description
                            ])
                    
                    # Regras de Saída
                    for rule in nsg_rules:
                        if rule.direction == "EGRESS":
                            egress_writer.writerow([
                                compartment_name,
                                nsg_name,
                                rule.protocol,
                                rule.destination,
                                rule.destination_type,
                                rule.tcp_options,
                                rule.udp_options,
                                rule.icmp_options,
                                rule.description
                            ])
        print(f"Regras de NSGs salvas em '{nsg_ingress_csv}' e '{nsg_egress_csv}'.")

    except oci.exceptions.ServiceError as e:
        print(f"Erro ao listar NSGs: {e}")

# Executa a função
list_nsgs_to_csv(compartment_ids)