from netmiko import  ConnectHandler
import yaml

def configure_router(device):
	try:
		connection = ConnectHandler(**device)
		print(f"Affichage de l'heure pour la routeur :")
		clock_output = connection.send_command('show clock')
		print(clock_output)

		filename = f"interfaces.txt"
		print(f"\nÉcriture des interfaces dans le fichier '{filename}'...")
		interfaces_output = connection.send_command('sh ip int br')
		with open(filename, 'w') as file:
			file.write(interfaces_output)

		print("\nConfiguration de l'interface Loopback...")
		config_commands = [
			'interface loopback0',
			'ip address 10.8.8.8 255.255.255.240', 
        	]
		connection.send_config_set(config_commands)
		print("Configuration terminée.")

	except Exception as e:
		print(f"Une erreur est survenue pour {device['host']}... : {e}")

if __name__ == "__main__":

    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for device in devices:
        print(f"Connexion à {device['host']}...")
        configure_router(device)
