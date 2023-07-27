from dataclasses import dataclass, field
import warnings

import numpy as np
import torch
from torch.autograd import Variable

LEARNING_RATE = 0.001
EPOCHS = 100

class Queue_Model(torch.nn.Module):
    def __init__(self, half_lane_width, entry_width, effective_flare_length, entry_radius,
                 inscribed_circle_diameter, conflict_angle, entry_flow, circulatory_flow,
                 observed_queue, period_total_minutes, period_interval_minutes):
        self.half_lane_width: list = half_lane_width
        self.entry_width: list = entry_width
        self.effective_flare_length: list = effective_flare_length 
        self.entry_radius: list = entry_radius
        self.inscribed_circle_diameter: list = inscribed_circle_diameter
        self.conflict_angle: list = conflict_angle
        self.entry_flow: list = entry_flow
        self.circulatory_flow: list = circulatory_flow
        self.observed_queue: list = observed_queue 
        self.period_total_minutes: int = period_total_minutes
        self.period_interval_minutes: int = period_interval_minutes#
        
        self.x = Variable(torch.from_numpy(np.array([
            self.half_lane_width,
            self.entry_width,
            self.effective_flare_length,
            self.entry_radius,
            self.inscribed_circle_diameter,
            self.conflict_angle,
            self.entry_flow,
            self.circulatory_flow,
            self.observed_queue])).type(torch.float32))
        self.y = Variable(torch.from_numpy(np.array(self.observed_queue)))
        self.input_size = len(self.x)
        self.output_size = len(self.y)
        self.obs = len(self.half_lane_width)
        print(self.input_size)

        super().__init__()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(9, 200),
            torch.nn.ReLU(),
            torch.nn.Linear(200, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 1)
        )
    
    def __post_init__(self) -> None:
        if len(self.circulatory_flow) == len(self.observed_queue): return None
        elif len(self.observed_queue) % len(self.circulatory_flow) == 0: return self.align()
        else: raise ValueError(f'Dimension of Circulatory Flow and Obsevered Flows are not equal and cannot be resolved: OQ({len(self.observed_queue)}) / CF({len(self.circulatory_flow)}) != int')

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    def factor(self) -> float:
        return int(self.period_total_minutes / self.period_interval_minutes)
    
    def align(self) -> list:
        chunks = [self.observed_queue[x:x + (len(self.observed_queue / self.factor()))] for x in range(self.factor())]
        self.observed_queue = [round(sum(chunks[i]) / len(chunks[i]), 2) for i in range(len(chunks))]

geom = [
    np.random.randint(3, 6, size=200),
    np.random.randint(5, 9, size=200),
    np.random.randint(20, 30, size=200),
    np.random.randint(32, 70, size=200),
    np.random.randint(20, 30, size=200),
    np.random.randint(100, 500, size=200),
    np.random.randint(100, 400, size=200)
]

if __name__ == "__main__":
    q = Queue_Model(*geom, np.random.randint(0, 20, size=200), np.random.randint(0, 12, size=200), 60, 15)
    criterion = torch.nn.MSELoss()
    optimiser = torch.optim.SGD(q.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        x = Variable(torch.tensor(q.x))
        y = Variable(torch.tensor(q.y))

        optimiser.zero_grad()
        outputs = q(x)
        
        loss = criterion(outputs, y)
        loss.backward()
        optimiser.step()
        print(f'Epoch: {epoch} - Loss {loss.item()}')