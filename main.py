from netwolf import NetWolf


def main():
    udp_listener_port = int(input("Enter UDP port : "))
    files_directory = input("Enter address of files directory : ")
    cluster_list_address = input("Enter address of the list : ")
    discovery_period = int(input("Enter time period of discovery messages : "))
    max_clients = int(input("Enter the maximum number of clients : "))
    free_ride_delay = int(input("How much time should a free rider wait ? "))
    request_timeout = int(input("How much time does a file request last ? "))

    net_wolf = NetWolf(udp_listener_port, files_directory, cluster_list_address,
                       discovery_period, max_clients, free_ride_delay, request_timeout)

    net_wolf.start()

    print("\nCommands :")
    print("- get \"file_name\"")
    print("- list")
    print("- terminate")

    running = True
    while running:

        command = input()
        split_command = command.split()
        if split_command[0] == 'get':
            net_wolf.request_file(split_command[1])
        elif split_command[0] == 'list':
            net_wolf.print_list()
        elif split_command[0] == 'terminate':
            running = False
        else:
            print("The command is not supported!")

    net_wolf.stop()


if __name__ == '__main__':
    main()
