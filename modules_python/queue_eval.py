from dataclasses import dataclass, field
import warnings

import numpy as np
import torch
from torch.autograd import Variable

@dataclass
class Queue_Model(torch.nn.Module):
    half_lane_width: list
    entry_width: list
    effective_flare_length: list
    entry_radius: list
    inscribed_circle_diameter: list
    conflict_angle: list
    entry_flow: list
    circulatory_flow: list
    observed_queue: list
    period_total_minutes: int
    period_interval_minutes: int
    
    def __post_init__(self) -> None:
        try: self.x = np.array([getattr(self, vars(Queue_Model)['__match_args__'][:-2][i]) for i in range(len(vars(Queue_Model)['__match_args__'][:-2]))])
        except ValueError: print(f'Inputs do not have uniform length')
        self.y = np.array(self.observed_queue)
        self.input_size = len(self.x)
        self.output_size = len(self.y)
        super(Queue_Model, self).__init__()
        self.linear = torch.nn.Linear(self.input_size, self.output_size)    
        
        if len(self.circulatory_flow) == len(self.observed_queue): return None
        elif len(self.observed_queue) % len(self.circulatory_flow) == 0: return self.align()
        else: raise ValueError(f'Dimension of Circulatory Flow and Obsevered Flows are not equal and cannot be resolved: OQ({len(self.observed_queue)}) / CF({len(self.circulatory_flow)}) != int')

    def forward(self, x):
        out = self.linear(x)
        return out

    def factor(self) -> float:
        return int(self.period_total_minutes / self.period_interval_minutes)
    
    def align(self) -> list:
        chunks = [self.observed_queue[x:x + (len(self.observed_queue / self.factor()))] for x in range(self.factor())]
        self.observed_queue = [round(sum(chunks[i]) / len(chunks[i]), 2) for i in range(len(chunks))]

    def evaluate(self):
        learning_rate = 0.001
        epochs = 100
        
        model = Queue_Model
        criterion = torch.nn.MSELoss()
        optimiser = torch.optim.SGD(model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            x = Variable(torch.tensor(self.x))
            y = Variable(torch.tensor(self.y))

            optimiser.zero_grad()
            outputs = model(x)
            
            loss = criterion(outputs, y)
            loss.backward()
            optimiser.step()
            print(f'Epoch: {epoch} - Loss {loss.item()}')

geom = [
    np.random.randint(3, 5, size=200),
    np.random.randint(3, 5, size=200),
    np.random.randint(3, 5, size=200),
    np.random.randint(3, 5, size=200),
    np.random.randint(3, 5, size=200),
    np.random.randint(3, 5, size=200),
    np.random.randint(3, 5, size=200)
]




if __name__ == "__main__":
    q = Queue_Model(*geom, np.random.randint(0, 20, size=200), np.random.randint(0, 12, size=200), 60, 15)
    q.evaluate()