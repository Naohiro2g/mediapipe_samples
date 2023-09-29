# Hello World for Minecraft Java Edition 1.16.5
# mcje, MCJE: Minecraft Java Edition
from mcje.minecraft import Minecraft
import param_MCJE as param

mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat('Hello Minecraft Java Edition 1.16.5')
#mc.setBlocks(-2, 86, -2,  2, 88, 2,  param.GOLD_BLOCK)
mc.setBlocks(-100, 20, 0,  100, 100, 0,  param.AIR)
