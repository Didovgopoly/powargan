path_netG = f'trained/eda_ru_df_gan_lstm_cycle_loss_ingr_steps_128_netG_epoch_38.pth'
resnet_title_ingr_path = f'trained/best_resnet_title_ingr.pth'
resnet_steps_path = f'trained/best_resnet_steps.pth'

from collections import OrderedDict
import numpy as np
import torch
import torch.nn as nn
import torchvision.utils as vutils
import torch.nn.functional as F

EMB_SIZE = 512

class NetG(nn.Module):
    def __init__(self, ngf=64, nz=100):
        super(NetG, self).__init__()

        # self.fc_embedding = nn.Linear(768, 256)

        self.ngf = ngf

        
        self.fc = nn.Linear(nz, ngf*8*4*4)
        self.block0 = G_Block(ngf * 8, ngf * 8)#4x4
        self.block1 = G_Block(ngf * 8, ngf * 8)#4x4
        self.block2 = G_Block(ngf * 8, ngf * 8)#8x8
        self.block3 = G_Block(ngf * 8, ngf * 8)#16x16
        self.block4 = G_Block(ngf * 8, ngf * 4)#32x32
        # self.block5 = G_Block(ngf * 4, ngf * 2)#64x64
        # self.block6 = G_Block(ngf * 2, ngf * 1)#128x128
        self.block5 = G_Block(ngf * 4, ngf * 1)

        self.conv_img = nn.Sequential(
            nn.LeakyReLU(0.2,inplace=True),
            nn.Conv2d(ngf, 3, 3, 1, 1),
            nn.Tanh(),
        )

    def forward(self, x, c):

        # c = self.fc_embedding(c)

        out = self.fc(x)
        out = out.view(x.size(0), 8*self.ngf, 4, 4)
        out = self.block0(out,c)

        out = F.interpolate(out, scale_factor=2)
        out = self.block1(out,c)

        out = F.interpolate(out, scale_factor=2)
        out = self.block2(out,c)

        out = F.interpolate(out, scale_factor=2)
        out = self.block3(out,c)

        out = F.interpolate(out, scale_factor=2)
        out = self.block4(out,c)

        out = F.interpolate(out, scale_factor=2)
        out = self.block5(out,c)

        # out = F.interpolate(out, scale_factor=2)
        # out = self.block6(out,c)

        out = self.conv_img(out)

        return out


class G_Block(nn.Module):

    def __init__(self, in_ch, out_ch):
        super(G_Block, self).__init__()

        self.learnable_sc = in_ch != out_ch 
        self.c1 = nn.Conv2d(in_ch, out_ch, 3, 1, 1)
        self.c2 = nn.Conv2d(out_ch, out_ch, 3, 1, 1)
        self.affine0 = affine(in_ch)
        self.affine1 = affine(in_ch)
        self.affine2 = affine(out_ch)
        self.affine3 = affine(out_ch)
        self.gamma = nn.Parameter(torch.zeros(1))
        if self.learnable_sc:
            self.c_sc = nn.Conv2d(in_ch,out_ch, 1, stride=1, padding=0)

    def forward(self, x, y=None):
        return self.shortcut(x) + self.gamma * self.residual(x, y)

    def shortcut(self, x):
        if self.learnable_sc:
            x = self.c_sc(x)
        return x

    def residual(self, x, y=None):
        h = self.affine0(x, y)
        h = nn.LeakyReLU(0.2,inplace=True)(h)
        h = self.affine1(h, y)
        h = nn.LeakyReLU(0.2,inplace=True)(h)
        h = self.c1(h)
        
        h = self.affine2(h, y)
        h = nn.LeakyReLU(0.2,inplace=True)(h)
        h = self.affine3(h, y)
        h = nn.LeakyReLU(0.2,inplace=True)(h)
        return self.c2(h)



class affine(nn.Module):

    def __init__(self, num_features):
        super(affine, self).__init__()

        self.fc_gamma = nn.Sequential(OrderedDict([
            ('linear1',nn.Linear(EMB_SIZE, 256)),
            ('relu1',nn.ReLU(inplace=True)),
            ('linear2',nn.Linear(256, num_features)),
            ]))
        self.fc_beta = nn.Sequential(OrderedDict([
            ('linear1',nn.Linear(EMB_SIZE, 256)),
            ('relu1',nn.ReLU(inplace=True)),
            ('linear2',nn.Linear(256, num_features)),
            ]))
        self._initialize()

    def _initialize(self):
        nn.init.zeros_(self.fc_gamma.linear2.weight.data)
        nn.init.ones_(self.fc_gamma.linear2.bias.data)
        nn.init.zeros_(self.fc_beta.linear2.weight.data)
        nn.init.zeros_(self.fc_beta.linear2.bias.data)

    def forward(self, x, y=None):

        weight = self.fc_gamma(y)
        bias = self.fc_beta(y)        

        if weight.dim() == 1:
            weight = weight.unsqueeze(0)
        if bias.dim() == 1:
            bias = bias.unsqueeze(0)

        size = x.size()
        weight = weight.unsqueeze(-1).unsqueeze(-1).expand(size)
        bias = bias.unsqueeze(-1).unsqueeze(-1).expand(size)
        return weight * x + bias

netG = NetG(32, 100)

netG.load_state_dict(torch.load(path_netG,map_location=torch.device('cpu')))
netG.eval()

from torchvision import models
def load_resnet(resnet_path, food_space_dim=512):
    resnet_fe = models.resnet50(pretrained=False)
    num_ftrs = resnet_fe.fc.in_features
    resnet_fe.fc = nn.Linear(num_ftrs, food_space_dim) # Чтобы загрузить веса обученной ранее модели модели
    resnet_fe.load_state_dict(torch.load(resnet_path,map_location=torch.device('cpu')))
    return resnet_fe

resnet_title_ingr = load_resnet(resnet_title_ingr_path, 256)
resnet_steps = load_resnet(resnet_steps_path, 256)
resnet_title_ingr.eval()
resnet_steps.eval()

def dist(a,b):
  a = a.detach().numpy()[0]
  b = b.detach().numpy()[0]
  return a.dot(b)/np.linalg.norm(a)/np.linalg.norm(b)

def select_best(fake,title_emb,steps_emb,best_size):
  similarities = []
  for i in range(fake.shape[0]):
    resnet_emb_title_ingr = resnet_title_ingr(fake[i].unsqueeze(0))
    resnet_emb_steps = resnet_steps(fake[i].unsqueeze(0))
    d_ingr = dist(title_emb,resnet_emb_title_ingr)
    d_steps = dist(steps_emb,resnet_emb_steps)
    similarities.append(d_ingr/5.+d_steps)
  sorted_indexes = np.argsort(similarities)
  return fake[sorted_indexes[-best_size:]]

def generate_select(title_emb,steps_emb,sz=9):
    gen_sz = 2*sz
    emb = torch.cat([title_emb,steps_emb],axis=1)
    noise = torch.randn(gen_sz, 100)
    noise=noise.to('cpu')
    fake = netG(noise,emb)    
    return select_best(fake,title_emb,steps_emb,sz)