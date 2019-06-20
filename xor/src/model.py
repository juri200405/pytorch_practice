import torch
import torch.nn as nn
import torch.nn.functional as F

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(2, 4)
        self.fc2 = nn.Linear(4, 1)
    
    def forward(self, input):
        #result = F.relu(self.fc1(input))
        result = torch.tanh(self.fc1(input))
        result = self.fc2(result)
        return result