#Autor: Felipe Mendes
 
import oci

config = {
   " INSIRA AQUI O ARQUIVO DE CONFIGURAÇÃO"
}

def stop_instance(instance_ids): #Função para desligar a instancia

    compute_client = oci.core.ComputeClient(config)
    for instance_id in instance_ids:

        try:
            response = compute_client.instance_action(instance_id, "STOP") #Comando que desliga a instancia
            print(f"Instância {instance_id} está sendo desligada. Status: {response.data.lifecycle_state}")
        except oci.exceptions.ServiceError as e:
            print(f"Erro ao desligar a instância: {e.message}")

def start_instance(instance_ids): #FUncao para ligar a instancia
    compute_client = oci.core.ComputeClient(config)

    for instance_id in instance_ids:
        try:
            response = compute_client.instance_action(instance_id, "START") #Comando que liga a instancia
            print(f"Instância {instance_id} está sendo ligada. Status: {response.data.lifecycle_state}")
        except oci.exceptions.ServiceError as e:
            print(f"Erro ao ligar a instância: {e.message}")

def restart_instance(instance_ids): #FUncao para ligar a instancia
    compute_client = oci.core.ComputeClient(config)

    for instance_id in instance_ids:
        try:
            response = compute_client.instance_action(instance_id, "RESET") #Comando que liga a instancia
            print(f"Instância {instance_id} está sendo reiniciada. Status: {response.data.lifecycle_state}")
        except oci.exceptions.ServiceError as e:
            print(f"Erro ao reiniciar a instância: {e.message}")

def list_running_instances():

    compute_client = oci.core.ComputeClient(config)

    compartment_ids = ["Insira aqui todos os ids dos compartimentos para o codigo te informar quais são as instancias que estão em cada compart"]
    
    for compartiment_id in compartment_ids:
        try:
            print(f"--- Listando instâncias no compartimento: {compartiment_id} ---")
            instances = compute_client.list_instances(compartiment_id).data
            if not instances:
                print("Nenhuma instância encontrada.\n")
                continue

            for instance in instances:
                print(f"- Nome: {instance.display_name}")
                print(f"  ID da Instancia: {instance.id}")
                print(f"  Estado: {instance.lifecycle_state}")    
                print()
        except oci.exceptions.ServiceError as e:
            print(f"Erro ao listar instâncias no compartimento {compartiment_id}: {e}")




def main(): #Menu para o usuário decidir se ele quer ligar ou desligar a instancia

    print("Bem-vindo ao gerenciador de instâncias OCI")
    print("Segue uma lista de todas as instancias da tenancy lumisinfra")

    list_running_instances()

    instance_ids = input("Digite o OCID da instância, se tiver +1 colocar separadas por vírgula: ").strip().split(',')

    instance_ids = [ocid.strip() for ocid in instance_ids]

    print("\nEscolha uma ação:")
    print("1. Ligar a instância")
    print("2. Desligar a instância")
    print("3. Restart a instância")
    choice = input("Digite o número da ação desejada (1, 2, 3): ").strip()

    if choice == "1":
        start_instance(instance_ids)
    elif choice == "2":
        stop_instance(instance_ids)
    elif choice == "3":
        restart_instance(instance_ids)
    else:
        print("Escolha inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
    
