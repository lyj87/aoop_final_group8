from train import train_model
from test import test_model
from train_dqn import train_dqn_model
from test_dqn import test_dqn_model

def main():
    print("Bomberman AI")
    print("1. Train PPO Model")
    print("2. Test PPO Model")
    print("3. Train DQN Model")
    print("4. Test DQN Model")
    choice = input("Enter your choice: ")
    if choice == "1":
        train_model()
    elif choice == "2":
        test_model()
    elif choice == "3":
        train_dqn_model()
    elif choice == "4":
        test_dqn_model()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()