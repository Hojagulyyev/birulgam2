import sys
import os

ROOT_DIR = os.getcwd()
sys.path.append(ROOT_DIR)

from api.cli.controllers import controllers


def main():
    print("Started server process (Press CTRL+C to quit)")
    print("Waiting for user input.")
    
    for controller_name, controller in controllers.items():
        controllers[f"{controller_name}"] = controller

    def get_available_controllers():
        print("\nGetting available controllers")
        for controller in controllers:
            print(controller)
        print()

    def execute_controller(controller):
        response = controller()
        print(response)

    try:
        if controller := controllers.get(sys.argv[1:][0], False):
            execute_controller(controller)
    except IndexError:
        pass

    get_available_controllers()
    while True:
        controller = input("Enter your controller: ")
        if controller := controllers.get(controller, False):
            execute_controller(controller)
        else:
            print("Quit application")
            break


if __name__ == "__main__":
    main()
