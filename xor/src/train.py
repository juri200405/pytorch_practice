import torch
import torch.optim as optim
import torch.nn as nn

from model import MyModel
from datas import get_data_loader

def run():
    use_cuda = torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')

    dataset = [
        {"in" : [0.0, 0.0], "out" : [0.0]},
        {"in" : [0.0, 1.0], "out" : [1.0]},
        {"in" : [1.0, 0.0], "out" : [1.0]},
        {"in" : [1.0, 1.0], "out" : [0.0]}]

    data_loader = get_data_loader(dataset=dataset, shuffle=True)

    model = MyModel()
    model.to(device)

    optimizer = optim.Adam(model.parameters())
    loss_func = nn.MSELoss()

    model.train()

    for _ in range(0, 2000):
        for output, input in data_loader:
            input = input.to(device)
            output = output.to(device)

            result = model(input)
            loss = loss_func(result, output)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    test_data_loader = get_data_loader(dataset=dataset, shuffle=False)
    model.eval()
    with torch.no_grad():
        for _, input in test_data_loader:
            print(input)
            input = input.to(device)
            result = model(input)
            print(result)

if __name__ == "__main__":
    run()