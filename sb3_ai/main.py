from train import train_model
from test import test_model

def main():
    print("Bomberman AI")
    print("1. Train Model")
    print("2. Test Model")
    choice = input("Enter your choice: ")
    if choice == "1":
        train_model()
    elif choice == "2":
        test_model()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()