import torch
import torch.utils.data as data
from torch.utils.data.sampler import RandomSampler

def get_collate_fn():
    def _f(batch):
        in_list = []
        out_list = []
        
        for ins in batch:
            in_list.append(ins["in"])
            out_list.append(ins["out"])
        
        return (torch.Tensor(out_list), torch.Tensor(in_list))
    return _f

def get_data_loader(dataset, shuffle):
    if shuffle:
        return data.DataLoader(dataset=dataset, sampler=RandomSampler(dataset), collate_fn=get_collate_fn())
    else:
        return data.DataLoader(dataset=dataset, shuffle=False, collate_fn=get_collate_fn())