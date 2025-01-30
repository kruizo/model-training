from . import RRDBNet_arch as arch
import torch


class ESRGAN:
    def __init__(self, model_path='./model/RRDB_PSNR_x4.pth', device='cpu'): 
        self.device = torch.device(device) 
        self.model = arch.RRDBNet(3, 3, 64, 23, gc=32)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device, weights_only=False))
        self.model.to(self.device)
        self.model.eval()
        
    def __call__(self, x):
        return self.model(x)